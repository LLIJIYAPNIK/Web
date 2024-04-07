from app import app
from flask import request, url_for, jsonify
from app import db
from app.models.post import Posts


@app.route("/delete_post", methods=["POST"])
def delete_post():
    data = request.get_json()
    post_id = str(data['post_id']).split("_")[2]
    post = Posts.query.filter_by(id=post_id).first()

    db.session.delete(post)
    db.session.commit()
    if True:
        return jsonify({'redirect': url_for('profile')})
    return "Post not found"
