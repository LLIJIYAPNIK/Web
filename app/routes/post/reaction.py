# Импорт необходимых модулей и классов
from app import app
from flask_login import current_user, login_required
from app.models.post_reaction import PostReactions
from app import db
from flask import request, redirect, abort


# Функция для обновления реакции пользователя на пост
def update_post_reaction(post_id, reaction_type):
    # Проверяем, оставлял ли пользователь уже реакцию на пост
    post_reaction = PostReactions.query.filter_by(post_id=post_id, user_id=current_user.id).first()

    # Если пользователь еще не оставлял реакцию на пост, создаем новую запись
    if not post_reaction:
        new_post_reaction = PostReactions(post_id=post_id, user_id=current_user.id, reaction_type=reaction_type)
        db.session.add(new_post_reaction)
    else:
        # Если пользователь уже оставлял реакцию, переключаем тип реакции
        if post_reaction.reaction_type == reaction_type:
            post_reaction.reaction_type = 'None'
        else:
            post_reaction.reaction_type = reaction_type

    # Применяем изменения к базе данных
    db.session.commit()


# Маршрут для постановки лайка на пост
@app.route('/like_post/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    # Проверяем, аутентифицирован ли пользователь
    if not current_user.is_authenticated:
        return abort(401)

    # Обновляем реакцию пользователя на пост на 'лайк'
    update_post_reaction(post_id, 'like')
    return redirect(request.referrer)


# Маршрут для постановки дизлайка на пост
@app.route('/dislike_post/<int:post_id>', methods=['POST'])
@login_required
def dislike_post(post_id):
    # Проверяем, аутентифицирован ли пользователь
    if not current_user.is_authenticated:
        return abort(401)

    # Обновляем реакцию пользователя на пост на 'дизлайк'
    update_post_reaction(post_id, 'dislike')
    return redirect(request.referrer)
