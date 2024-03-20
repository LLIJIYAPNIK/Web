from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from flask_msearch import Search
from flask_session import Session
from flask import render_template, request, redirect, url_for, session, flash, jsonify
from get_nearst_gym import get_gyms
from forms import LoginForm, RegistrationForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask
from models import User, Posts, db, PostReactions
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_key_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_DOMAIN'] = None  # Используйте домен по умолчанию
app.config['SESSION_COOKIE_PATH'] = '/'
app.config['SESSION_TYPE'] = 'filesystem'  # Можно выбрать другие типы хранения сессий
app.config["POSTS_PER_PAGE"] = 1

db.init_app(app)
Session(app)

search = Search(db=db)
search.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

latitude_user = 0
longitude_user = 0


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home_page():
    return render_template('index.html')


@app.route("/get_location", methods=["POST"])
def get_location():
    global latitude_user, longitude_user
    data = request.get_json()
    latitude = data["latitude"]
    longitude = data["longitude"]
    print(f"Latitude: {latitude}, Longitude: {longitude}")
    latitude_user = latitude
    longitude_user = longitude
    return redirect('/test_page')


@app.route("/test_page")
def test_page():
    data = get_gyms(latitude_user, longitude_user, db)

    places = []
    for item in data:
        place = {
            'name': item[0],
            'coords': [item[3], item[4]]
        }
        places.append(place)
    places.append({'name': 'Me', 'coords': [latitude_user, longitude_user]})

    return render_template('index_map.html', latitude_user=latitude_user, longitude_user=longitude_user, places=places)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))


@app.route("/log", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.mail.data
        password = form.password.data

        user = User.query.filter_by(mail=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            session['userID'] = user.id  # Save user ID in session
            name_last_name = f"{user.name} {user.last_name}"
            return redirect(url_for('index'))

        flash('Invalid email or password', 'error')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(mail=form.mail.data).first()
        if existing_user:
            flash('User with this email already exists', 'error')
        else:
            hash_and_salted_password = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )

            new_user = User(
                mail=form.mail.data,
                name=form.name.data,
                last_name=form.last_name.data,
                password=hash_and_salted_password
            )

            try:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                session['userID'] = new_user.id
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred. Please try again.', 'error')

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('userID', None)
    return redirect(url_for('index'))


@app.route('/index_login')
def index_login():
    data = request.args.get('data')
    user = str(data)
    return render_template('index_login.html', user=user)


@app.route('/editor')
@login_required
def editor():
    userID = session.get('userID')
    print(userID)
    return render_template('editor.html', userID=userID)


@app.route('/get_post', methods=['POST'])
def get_post():
    data = request.get_json()
    userID = int(session.get('userID'))
    title = str(data['title']).lower()
    content = data['content']

    print(userID, title, content)

    new_post = Posts(
        user_id=userID,
        title=title,
        content=content
    )

    db.session.add(new_post)
    db.session.commit()

    if new_post.id:
        return redirect(url_for('profile'))
    return 'Not good'


@app.route('/profile')
@login_required
def profile():
    userID = int(session.get('userID'))
    posts = Posts.query.filter_by(user_id=userID).all()
    user = User.query.filter_by(id=userID).first()
    # print(posts[0].content)
    post_len = len(posts)
    return render_template('profile.html', posts=posts, user=user, length=post_len)


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    post_reaction = PostReactions.query.filter(PostReactions.post_id == post_id).all()
    post_reaction_user = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                    PostReactions.user_id == current_user.id).first()
    if post:
        if not post_reaction:
            new_post_reaction = PostReactions(post_id=post_id, user_id=current_user.id, reaction_type='None')
            db.session.add(new_post_reaction)
            db.session.commit()
            likes_count = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                     PostReactions.reaction_type == 'like').count()
            dislikes_count = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                        PostReactions.reaction_type == 'dislike').count()
            user_position = 'None'
            return render_template('post.html', post=post, likes_count=likes_count, dislikes_count=dislikes_count,
                                   user_position=user_position)
        if post_reaction_user.reaction_type == 'like':
            likes_count = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                     PostReactions.reaction_type == 'like').count()
            dislikes_count = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                        PostReactions.reaction_type == 'dislike').count()
            user_position = 'like'
            print(likes_count, dislikes_count)
            return render_template('post.html', post=post, likes_count=likes_count, dislikes_count=dislikes_count,
                                   user_position=user_position)
        if post_reaction_user.reaction_type == 'dislike':
            likes_count = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                     PostReactions.reaction_type == 'like').count()
            dislikes_count = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                        PostReactions.reaction_type == 'dislike').count()
            user_position = 'dislike'
            print(likes_count, dislikes_count)
            return render_template('post.html', post=post, likes_count=likes_count, dislikes_count=dislikes_count,
                                   user_position=user_position)
        if post_reaction_user.reaction_type == 'None':
            likes_count = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                     PostReactions.reaction_type == 'like').count()
            dislikes_count = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                        PostReactions.reaction_type == 'dislike').count()
            user_position = 'None'
            print(likes_count, dislikes_count)
            return render_template('post.html', post=post, likes_count=likes_count, dislikes_count=dislikes_count,
                                   user_position=user_position)
    return "Post not found"


@app.route('/publish_post', methods=['POST'])
def publish_post():
    data = request.get_json()
    post_id = str(data['post_id']).split("_")[2]
    post = Posts.query.filter_by(id=post_id).first()
    post.is_published = True
    db.session.commit()

    if post.is_published:
        return jsonify({'redirect': url_for('all_posts')})
    return 'Bad'


@app.route('/all_posts', methods=['GET'])
def all_posts():
    page = request.args.get('page', 1, type=int)

    query = Posts.query.filter(Posts.is_published == True)

    # Используем объект запроса для пагинации
    posts = query.paginate(page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('all_posts', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('all_posts', page=posts.prev_num) \
        if posts.has_prev else None
    this_url = url_for('all_posts', page=posts.page)

    return render_template('all_posts.html', posts=posts, next_url=next_url, prev_url=prev_url, this_url=this_url,
                           page=page, threshold=3, total_pages=(query.count() - 1) // app.config['POSTS_PER_PAGE'] + 1)


@app.route('/get_edit_post', methods=["POST"])  # Изменяем метод на GET
def get_edit_post():
    data = request.get_json()
    post_id = str(data['post_id']).split("_")[2]
    post = Posts.query.filter_by(id=post_id).first()
    print(post)
    if post:
        return jsonify({'redirect': url_for('edit_post', post_id=post_id)})
    return jsonify({'error': 'Post not found'})


@app.route('/edit_post/<int:post_id>', methods=['GET'])
def edit_post(post_id):
    post = Posts.query.filter_by(id=post_id).first()

    if post:
        return render_template('edit_post.html', post=post)
    return "Post not found"


@app.route("/update_post", methods=["POST"])
def update_post():
    data = request.get_json()
    post_id = data['post_id']
    user_id = data['user_id']
    title = str(data['title']).lower()
    content = data['content']

    post = Posts.query.filter_by(id=post_id).first()

    post.title = title
    post.content = content
    db.session.commit()
    return redirect(url_for('profile'))


@app.route("/delete_post", methods=["POST"])
def delete_post():
    data = request.get_json()
    post_id = str(data['post_id']).split("_")[2]
    post = Posts.query.filter_by(id=post_id).first()

    db.session.delete(post)
    db.session.commit()
    if True:
        return jsonify({'redirect': url_for('profile')})
    return "Post not found"


@app.route("/search", methods=["GET"])
def w_search():
    page = request.args.get('page', 1, type=int)

    keyword = str(request.args.get('keyword')).lower()
    results = Posts.query.filter(Posts.is_published == True, (
            func.lower(Posts.title).ilike(f"%{keyword}%") | func.lower(Posts.content).ilike(
        f"%{keyword}%"))).msearch(keyword, fields=['title', 'content'])

    posts = results.paginate(page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)

    next_url = url_for('w_search', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('w_search', page=posts.prev_num) if posts.has_prev else None
    this_url = url_for('w_search', page=page)

    total_pages = (results.count()) // app.config['POSTS_PER_PAGE']

    return render_template('search.html', posts=posts, next_url=next_url, prev_url=prev_url, this_url=this_url,
                           page=page, threshold=3, total_pages=total_pages)


@app.route('/independent_training')
def independent_training():
    return render_template("independent_training.html")


@app.route("/group_classes")
def group_classes():
    return render_template("group_classes.html")


@app.route('/personal_training')
def personal_training():
    return render_template("personal_training.html")


@app.route('/like_post/<int:post_id>', methods=['POST'])
def like_post(post_id):
    if current_user.is_authenticated:
        post_reaction = PostReactions.query.filter(PostReactions.post_id == post_id).first()
        # print(current_user.id, post_reaction, post_id)
        if not post_reaction:
            new_post_reaction = PostReactions(post_id=post_id, user_id=current_user.id, reaction_type='like')
            db.session.add(new_post_reaction)
            db.session.commit()
            return redirect(request.referrer)
        if post_reaction.reaction_type == 'like':
            post_reaction.reaction_type = 'None'
            db.session.commit()
            return redirect(request.referrer)
        if post_reaction.reaction_type == 'dislike':
            post_reaction.reaction_type = 'like'
            db.session.commit()
            return redirect(request.referrer)
        if post_reaction.reaction_type == 'None':
            post_reaction.reaction_type = 'like'
            db.session.commit()
            return redirect(request.referrer)
        return redirect(request.referrer)
    else:
        return redirect(url_for('login'))


@app.route('/dislike_post/<int:post_id>', methods=['POST'])
def dislike_post(post_id):
    if current_user.is_authenticated:
        post_reaction = PostReactions.query.filter(PostReactions.post_id == post_id).first()
        # print(current_user.id, post_reaction, post_id)
        if not post_reaction:
            new_post_reaction = PostReactions(post_id=post_id, user_id=current_user.id, reaction_type='dislike')
            db.session.add(new_post_reaction)
            db.session.commit()
            return redirect(request.referrer)
        if post_reaction.reaction_type == 'dislike':
            post_reaction.reaction_type = 'None'
            db.session.commit()
            return redirect(request.referrer)
        if post_reaction.reaction_type == 'like':
            post_reaction.reaction_type = 'dislike'
            db.session.commit()
            return redirect(request.referrer)
        if post_reaction.reaction_type == 'None':
            post_reaction.reaction_type = 'dislike'
            db.session.commit()
            return redirect(request.referrer)
        return redirect(request.referrer)
    else:
        return redirect(url_for('login'))


if __name__ == "__main__":
    with app.app_context():
        # Создание всех таблиц
        db.create_all()
    app.run(debug=True)
