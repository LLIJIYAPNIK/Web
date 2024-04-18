from flask import render_template
from app.models.post import Posts
from app import db
from app.models.post_reaction import PostReactions
from flask_login import current_user
from app import app
from flask_login import current_user


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    post_reaction = PostReactions.query.filter(PostReactions.post_id == post_id).all()

    if current_user.is_authenticated:
        post_reaction_user = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                        PostReactions.user_id == current_user.id).first()
        if post_reaction_user == None:
            post_reaction_user = PostReactions(user_id=current_user.id, post_id=post_id, reaction_type='None')
            db.session.add(post_reaction_user)
            db.session.commit()
        if post:
            if not post_reaction:
                new_post_reaction = PostReactions(post_id=post_id, user_id=current_user.id, reaction_type='None')
                db.session.add(new_post_reaction)
                db.session.commit()
                likes_count = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                         PostReactions.reaction_type == 'like').count()
                dislikes_count = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                            PostReactions.reaction_type == 'dislike').count()
                user_position = 'None'
                return render_template('post/post.html', post=post, likes_count=likes_count,
                                       dislikes_count=dislikes_count,
                                       user_position=user_position)
            if post_reaction_user.reaction_type == 'like':
                likes_count = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                         PostReactions.reaction_type == 'like').count()
                dislikes_count = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                            PostReactions.reaction_type == 'dislike').count()
                user_position = 'like'
                print(likes_count, dislikes_count)
                return render_template('post/post.html', post=post, likes_count=likes_count,
                                       dislikes_count=dislikes_count,
                                       user_position=user_position)
            if post_reaction_user.reaction_type == 'dislike':
                likes_count = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                         PostReactions.reaction_type == 'like').count()
                dislikes_count = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                            PostReactions.reaction_type == 'dislike').count()
                user_position = 'dislike'
                print(likes_count, dislikes_count)
                return render_template('post/post.html', post=post, likes_count=likes_count,
                                       dislikes_count=dislikes_count,
                                       user_position=user_position)
            if post_reaction_user.reaction_type == 'None':
                likes_count = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                         PostReactions.reaction_type == 'like').count()
                dislikes_count = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                            PostReactions.reaction_type == 'dislike').count()
                user_position = 'None'
                print(likes_count, dislikes_count)
                return render_template('post/post.html', post=post, likes_count=likes_count,
                                       dislikes_count=dislikes_count,
                                       user_position=user_position)
    else:
        likes_count = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                 PostReactions.reaction_type == 'like').count()
        dislikes_count = PostReactions.query.filter(PostReactions.post_id == post_id,
                                                    PostReactions.reaction_type == 'dislike').count()
        return render_template('post/post.html', post=post, likes_count=likes_count, dislikes_count=dislikes_count,
                               user_position="None")
    return "Post not found"
