# Импорт необходимых модулей и классов
from app import app
from flask import request, url_for, jsonify
from app.models.post import Posts
from app import db

# Маршрут для публикации поста
@app.route('/publish_post', methods=['POST'])
def publish_post():
    # Получение данных из запроса в формате JSON
    data = request.get_json()

    # Извлечение идентификатора поста из данных
    post_id = str(data['post_id']).split("_")[2]

    # Поиск поста в базе данных по идентификатору
    post = Posts.query.filter_by(id=post_id).first()

    # Установка флага is_published в True и сохранение изменений в базе данных
    post.is_published = True
    db.session.commit()

    # Проверка успешности публикации поста и возврат редиректа на страницу всех постов
    if post.is_published:
        return jsonify({'redirect': url_for('all_posts')})

    return 'Bad'
