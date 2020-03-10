from flask import render_template, request, Blueprint, redirect, url_for

main = Blueprint("main", __name__)

#####  Splash  #####
@main.route("/")
def splash():
    return render_template("splash.html", title="ATC Blog")

