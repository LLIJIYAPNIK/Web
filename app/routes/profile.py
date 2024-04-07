from flask import render_template, session
from app.models.user import User
from app.models.post import Posts
from app.models.post_reaction import PostReactions
from flask_login import login_required, current_user
from app import app


@app.route('/profile')
@login_required
def profile():
    userID = int(session.get('userID'))
    posts = Posts.query.filter_by(user_id=userID).all()
    user = User.query.filter_by(id=userID).first()

    posts_reactoins_like = PostReactions.query.filter(PostReactions.user_id == current_user.id,
                                                      PostReactions.reaction_type == 'like').all()
    posts_reactoins_dislike = PostReactions.query.filter(PostReactions.user_id == current_user.id,
                                                         PostReactions.reaction_type == 'dislike').all()

    # print(posts[0].content)
    post_len = len(posts)
    like_len = len(posts_reactoins_like)
    dislike_len = len(posts_reactoins_dislike)
    return render_template('profile.html', posts=posts, user=user, length=post_len, lemgth_l=like_len,
                           dislike_len=dislike_len, likes=posts_reactoins_like, dislikes=posts_reactoins_dislike)