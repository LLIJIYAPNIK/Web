from flask import render_template
from app import app


@app.route('/independent_training')
def independent_training():
    return render_template("articles/independent_training.html")


@app.route("/group_classes")
def group_classes():
    return render_template("articles/group_classes.html")


@app.route('/personal_training')
def personal_training():
    return render_template("articles/personal_training.html")