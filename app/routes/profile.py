# Импорт необходимых модулей и классов
from flask import render_template, session
from app.models.user import User
from app.models.post import Posts
from app.models.post_reaction import PostReactions
from flask_login import login_required, current_user
from app import app


# Обработчик GET-запроса для отображения профиля пользователя
@app.route('/profile')
@login_required
def profile():
    # Получаем идентификатор пользователя из сессии
    userID = int(session.get('userID'))

    # Получаем все посты пользователя и информацию о пользователе
    posts = Posts.query.filter_by(user_id=userID).all()
    user = User.query.filter_by(id=userID).first()

    # Получаем реакции пользователя на посты (лайки и дизлайки)
    posts_reactoins_like = PostReactions.query.filter(PostReactions.user_id == current_user.id,
                                                      PostReactions.reaction_type == 'like').all()
    posts_reactoins_dislike = PostReactions.query.filter(PostReactions.user_id == current_user.id,
                                                         PostReactions.reaction_type == 'dislike').all()

    # Вычисляем количество постов, лайков и дизлайков
    post_len = len(posts)
    like_len = len(posts_reactoins_like)
    dislike_len = len(posts_reactoins_dislike)

    # Отображаем шаблон профиля пользователя с информацией о постах, пользователе, лайках и дизлайках
    return render_template('profile.html', posts=posts, user=user, length=post_len, lemgth_l=like_len,
                           dislike_len=dislike_len, likes=posts_reactoins_like, dislikes=posts_reactoins_dislike)
