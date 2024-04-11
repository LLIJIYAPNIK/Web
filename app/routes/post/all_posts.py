from app import app
from flask import render_template, request, url_for
from app.models.post import Posts


@app.route('/all_posts', methods=['GET'])
def all_posts():
    page = request.args.get('page', 1, type=int)

    query = Posts.query.filter(Posts.is_published == True)

    # Используем объект запроса для пагинации
    posts = query.paginate(page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('all_posts', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('all_posts', page=posts.prev_num) \
        if posts.has_prev else None
    this_url = url_for('all_posts', page=posts.page)

    return render_template('post/all_posts.html', posts=posts, next_url=next_url, prev_url=prev_url, this_url=this_url,
                           page=page, threshold=3, total_pages=(query.count() - 1) // app.config['POSTS_PER_PAGE'] + 1)
