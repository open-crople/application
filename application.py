from flask import Flask, render_template, request
import sys

application = Flask(__name__)


@application.route("/")
def hello():
    return render_template("buy_items_list.html")


@application.route("/rent_items_list")
def rent_list():
    return render_template("rent_items_list.html")


@application.route("/mypage")
def view_mypage():
    return render_template("mypage.html")

@application.route("/reg_reviews")
def reg_reviews():
    return render_template("reg_reviews.html")

@application.route("/reg_items")
def reg_items():
    return render_template("/reg_items.html")


@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    image_file = request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form
    print(request.form["name"], request.form["price"], request.form["addr"], request.form["keyword"], request.form["explain"])
    return render_template("result.html", data=data, img_path="static/images/{}".format(image_file.filename))


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
