# Импорт необходимых модулей и классов
from app import app
from app.models.post import Posts
from flask import render_template


# Маршрут для редактирования поста
@app.route('/edit_post/<int:post_id>', methods=['GET'])
def edit_post(post_id):
    # Ищем пост по идентификатору в базе данных
    post = Posts.query.get(post_id)

    if post:
        # Если пост найден, отображаем шаблон для редактирования поста
        return render_template('post/edit_post.html', post=post)
    return "Post not found"
