# Импорт необходимых модулей и классов
from app import app
from flask import request, url_for, jsonify
from app import db
from app.models.post import Posts


# Маршрут для удаления поста
@app.route("/delete_post", methods=["POST"])
def delete_post():
    # Получаем данные из запроса
    data = request.get_json()

    # Извлекаем идентификатор поста из данных
    post_id = str(data['post_id']).split("_")[2]

    # Поиск поста в базе данных по идентификатору
    post = Posts.query.get(post_id)

    if post:
        # Удаляем пост из базы данных
        db.session.delete(post)
        db.session.commit()

        # Возвращаем JSON с URL для перенаправления на профиль
        return jsonify({'redirect': url_for('profile')})

    # Если пост не найден, возвращаем сообщение об ошибке
    return "Post not found"
