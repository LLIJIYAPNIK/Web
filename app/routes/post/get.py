# Импорт необходимых модулей и классов
from app import app
from flask import request, redirect, url_for, session, jsonify
from app.models.post import Posts
from app import db


# Маршрут для создания нового поста
@app.route('/get_post', methods=['POST'])
def get_post():
    # Получаем данные из запроса
    data = request.get_json()
    userID = int(session.get('userID'))
    title = str(data['title']).lower()
    content = data['content']

    # Создаем новый пост и сохраняем его в базе данных
    new_post = Posts(
        user_id=userID,
        title=title,
        content=content
    )

    db.session.add(new_post)
    db.session.commit()

    # Перенаправляем пользователя на страницу профиля после создания поста
    if new_post.id:
        return redirect(url_for('profile'))
    return 'Not good'


@app.route('/get_edit_post', methods=["POST"])  # Изменяем метод на GET
def get_edit_post():
    # Получаем данные из запроса
    data = request.get_json()

    # Ищем пост по идентификатору в базе данных
    post_id = str(data['post_id']).split("_")[2]
    post = Posts.query.filter_by(id=post_id).first()

    if post:
        # Если пост найден, возвращаем URL для редактирования этого поста
        return jsonify({'redirect': url_for('edit_post', post_id=post_id)})
    return jsonify({'error': 'Post not found'})
