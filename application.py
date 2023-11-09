from flask import Flask, render_template, request, flash
#from flask import redirect, url_for, session
from database import DBhandler
import hashlib
import sys


application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"


DB = DBhandler()


@application.route("/")
def hello():
    return render_template("buy_items_list.html")


@application.route("/rent_items_list")
def rent_list():
    return render_template("rent_items_list.html")


@application.route("/list")
def half_list():
    return render_template("list.html")


@application.route("/mypage")
def view_mypage():
    return render_template("mypage.html")


@application.route("/reg_reviews")
def reg_reviews():
    return render_template("reg_reviews.html")


@application.route("/reg_items")
def reg_items():
    return render_template("/reg_items.html")


@application.route("/login")
def login():
    return render_template("/login.html")


@application.route("/signup")
def signup():
    return render_template("/signup.html")


@application.route("/signup_post", methods=['POST'])
def register_user():
    data = request.form
    pw = request.form['pw']
    #password_check = data['password_check']
    #if pw != password_check:
     #   flash("Password and password confirmation do not match")
      #  return render_template("signup.html")
   # else:
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data, pw_hash):
        return render_template("login.html")
    else:
        flash("user id already exist!")
        return render_template("signup.html")


@application.route("/review")
def view_review():
    return render_template("/review.html")


@application.route("/buy_detail")
def view_buy_detail():
    return render_template("/buy_detail.html")


@application.route("/rent_detail")
def view_rent_detail():
    return render_template("/rent_detail.html")


@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    image_file = request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form
    DB.insert_item(data['name'], data, image_file.filename)

    return render_template("submit_item_result.html", data=data, img_path="static/images/{}".format(image_file.filename))


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8000, debug=True)
