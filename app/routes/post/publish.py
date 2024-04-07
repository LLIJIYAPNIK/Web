from app import app
from flask import request, url_for, jsonify
from app.models.post import Posts
from app import db


@app.route('/publish_post', methods=['POST'])
def publish_post():
    data = request.get_json()
    post_id = str(data['post_id']).split("_")[2]
    post = Posts.query.filter_by(id=post_id).first()
    post.is_published = True
    db.session.commit()

    if post.is_published:
        return jsonify({'redirect': url_for('all_posts')})
    return 'Bad'
