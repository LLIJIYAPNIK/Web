from flask import render_template
from app import app


@app.route('/about-us')
def about_us():
    return render_template("about-us.html")
