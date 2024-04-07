from app import app
from flask import request, redirect, url_for
from app import db
from app.models.post import Posts


@app.route("/update_post", methods=["POST"])
def update_post():
    data = request.get_json()
    post_id = data['post_id']
    user_id = data['user_id']
    title = str(data['title']).lower()
    content = data['content']

    post = Posts.query.filter_by(id=post_id).first()

    post.title = title
    post.content = content
    db.session.commit()
    return redirect(url_for('profile'))
