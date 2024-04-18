# Импорт необходимых модулей и классов
from flask import render_template
from app.models.post import Posts
from app import db
from app.models.post_reaction import PostReactions
from flask_login import current_user
from app import app


# Маршрут для нахождения и отображения поста
@app.route('/post/<int:post_id>')
def post(post_id):
    # Получаем пост по его id
    post = Posts.query.get(post_id)

    # Если пост не найден, возвращаем сообщение об ошибке
    if not post:
        return "Post not found"

    # Если пользователь аутентифицирован, получаем его реакцию на пост
    if current_user.is_authenticated:
        post_reaction_user = PostReactions.query.filter_by(post_id=post_id, user_id=current_user.id).first()

        # Если пользователь еще не ставил реакцию, добавляем ее
        if not post_reaction_user:
            post_reaction_user = PostReactions(user_id=current_user.id, post_id=post_id, reaction_type='None')
            db.session.add(post_reaction_user)
            db.session.commit()

        # Получаем количество лайков и дизлайков
        likes_count = PostReactions.query.filter_by(post_id=post_id, reaction_type='like').count()
        dislikes_count = PostReactions.query.filter_by(post_id=post_id, reaction_type='dislike').count()

        # Определяем, какая реакция пользователя на пост
        user_position = post_reaction_user.reaction_type

    else:
        # Если пользователь не аутентифицирован, получаем количество лайков и дизлайков
        likes_count = PostReactions.query.filter_by(post_id=post_id, reaction_type='like').count()
        dislikes_count = PostReactions.query.filter_by(post_id=post_id, reaction_type='dislike').count()
        user_position = "None"

    # Возвращаем шаблон с данными о посте, количестве лайков и дизлайков, а также реакции пользователя
    return render_template('post/post.html', post=post, likes_count=likes_count,
                           dislikes_count=dislikes_count, user_position=user_position)
