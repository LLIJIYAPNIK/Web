from flask import render_template, session
from flask_login import login_required
from app import app


@app.route('/editor')
@login_required
def editor():
    userID = session.get('userID')
    print(userID)
    return render_template('post/editor.html', userID=userID)
