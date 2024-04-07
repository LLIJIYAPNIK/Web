from app import app
from flask_login import current_user
from app.models.post_reaction import PostReactions
from app import db
from flask import request, redirect, url_for


@app.route('/like_post/<int:post_id>', methods=['POST'])
def like_post(post_id):
    if current_user.is_authenticated:
        post_reaction = PostReactions.query.filter(PostReactions.post_id == post_id).first()
        # print(current_user.id, post_reaction, post_id)
        if not post_reaction:
            new_post_reaction = PostReactions(post_id=post_id, user_id=current_user.id, reaction_type='like')
            db.session.add(new_post_reaction)
            db.session.commit()
            return redirect(request.referrer)
        if post_reaction.reaction_type == 'like':
            post_reaction.reaction_type = 'None'
            db.session.commit()
            return redirect(request.referrer)
        if post_reaction.reaction_type == 'dislike':
            post_reaction.reaction_type = 'like'
            db.session.commit()
            return redirect(request.referrer)
        if post_reaction.reaction_type == 'None':
            post_reaction.reaction_type = 'like'
            db.session.commit()
            return redirect(request.referrer)
        return redirect(request.referrer)
    else:
        return redirect(url_for('login'))


@app.route('/dislike_post/<int:post_id>', methods=['POST'])
def dislike_post(post_id):
    if current_user.is_authenticated:
        post_reaction = PostReactions.query.filter(PostReactions.post_id == post_id).first()
        # print(current_user.id, post_reaction, post_id)
        if not post_reaction:
            new_post_reaction = PostReactions(post_id=post_id, user_id=current_user.id, reaction_type='dislike')
            db.session.add(new_post_reaction)
            db.session.commit()
            return redirect(request.referrer)
        if post_reaction.reaction_type == 'dislike':
            post_reaction.reaction_type = 'None'
            db.session.commit()
            return redirect(request.referrer)
        if post_reaction.reaction_type == 'like':
            post_reaction.reaction_type = 'dislike'
            db.session.commit()
            return redirect(request.referrer)
        if post_reaction.reaction_type == 'None':
            post_reaction.reaction_type = 'dislike'
            db.session.commit()
            return redirect(request.referrer)
        return redirect(request.referrer)
    else:
        return redirect(url_for('login'))