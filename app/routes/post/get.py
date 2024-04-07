from app import app
from flask import request, redirect, url_for, session, jsonify
from app.models.post import Posts
from app import db


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


@app.route('/get_edit_post', methods=["POST"])  # Изменяем метод на GET
def get_edit_post():
    data = request.get_json()
    post_id = str(data['post_id']).split("_")[2]
    post = Posts.query.filter_by(id=post_id).first()
    print(post)
    if post:
        return jsonify({'redirect': url_for('edit_post', post_id=post_id)})
    return jsonify({'error': 'Post not found'})
