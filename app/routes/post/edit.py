from app import app
from app.models.post import Posts
from flask import render_template


@app.route('/edit_post/<int:post_id>', methods=['GET'])
def edit_post(post_id):
    post = Posts.query.filter_by(id=post_id).first()

    if post:
        return render_template('edit_post.html', post=post)
    return "Post not found"
