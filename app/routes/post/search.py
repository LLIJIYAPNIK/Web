from sqlalchemy import func
from flask import render_template, request, url_for
from app.models.post import Posts
from app import app
from app.config import Config


@app.route("/search", methods=["GET"])
def w_search():
    page = request.args.get('page', 1, type=int)

    keyword = str(request.args.get('keyword')).lower()
    results = Posts.query.filter(Posts.is_published == True, (
            func.lower(Posts.title).ilike(f"%{keyword}%") | func.lower(Posts.content).ilike(
        f"%{keyword}%"))).msearch(keyword, fields=['title', 'content'])
    print(list(results))
    posts = results.paginate(page=page, per_page=Config.POSTS_PER_PAGE, error_out=False)

    next_url = url_for('w_search', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('w_search', page=posts.prev_num) if posts.has_prev else None
    this_url = url_for('w_search', page=page)

    total_pages = (results.count()) // Config.POSTS_PER_PAGE + 1

    return render_template('post/search.html', posts=posts, next_url=next_url, prev_url=prev_url, this_url=this_url,
                           page=page, threshold=3, total_pages=total_pages)