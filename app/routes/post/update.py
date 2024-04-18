# Импорт необходимых модулей и классов
from app import app, db
from flask import request, redirect, url_for
from app.models.post import Posts


# Маршрут для обновления поста
@app.route("/update_post", methods=["POST"])
def update_post():
    # Получаем данные из запроса в формате JSON
    data = request.get_json()
    post_id = data['post_id']
    user_id = data['user_id']
    title = str(data['title']).lower()  # Приводим заголовок к нижнему регистру
    content = data['content']

    # Находим пост по его идентификатору
    post = Posts.query.filter_by(id=post_id).first()

    # Обновляем заголовок и содержимое поста
    post.title = title
    post.content = content

    # Применяем изменения к базе данных
    db.session.commit()

    # Перенаправляем пользователя на страницу профиля
    return redirect(url_for('profile'))
