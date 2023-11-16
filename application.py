from flask import Flask, render_template, request, flash
from flask import redirect, url_for, session
from database import DBhandler
import hashlib
import sys


application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"


DB = DBhandler()


@application.route("/")
def hello():
    return redirect(url_for('view_list'))


@application.route("/list")
def view_list():
    page = request.args.get("page", 0, type=int)
    per_page = 8
    start_idx = per_page*page
    end_idx = per_page*(page+1)
    data = DB.get_items()
    item_count = len(data)
    total = item_count
    data = dict(list(data.items())[start_idx:end_idx])

    return render_template(
        "buy_items_list.html", datas=data.items(),
        limit=per_page, page=page,
        page_count=int((item_count/per_page)+1), total=item_count)


@application.route("/rent")
def view_rent_list():
    #page = request.args.get("page", 0, type=int)
    #per_page = 8
    #start_idx = per_page*page
    #end_idx = per_page*(page+1)
    data = DB.get_rent_items()
    #item_count = len(data)
    #total = item_count
    #data = dict(list(data.items())[start_idx:end_idx])

    return render_template(
        "rent_items_list.html"
        ) #, datas=data.items(),limit=per_page, page=page,
        #page_count=int((item_count/per_page)+1), total=item_count


@application.route("/rent_items_list")
def rent_list():
    return redirect(url_for('view_rent_list'))


@application.route("/list")
def half_list():
    return render_template("list.html")


"""
@application.route("/list")
def view_list():
    data = DB.get_items()
    tot_count = len(data)
    return render_template("list.html",datas=data.items(),total=tot_count)

"""


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


@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_ = request.form['id']
    pw = request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    if DB.find_user(id_, pw_hash):
        user = DB.find_user(id_, pw_hash)
        session['id'] = id_
        session['email'] = user['email']
        session['openkakao'] = user['openkakao']
        session['department'] = user['department']
        return redirect(url_for('view_list'))
    else:
        flash("Wrong ID of PW!")
        return render_template("login.html")


@application.route("/logout")
def logout_user():
    session.clear()
    # return redirect(url_for('half_list'))
    return render_template("buy_items_list.html")


@application.route("/signup")
def signup():
    return render_template("/signup.html")


@application.route("/signup_post", methods=['POST'])
def register_user():
    data = request.form
    pw = request.form['pw']
    # password_check = data['password_check']
    # if pw != password_check:
    # flash("Password and password confirmation do not match")
    # return render_template("signup.html")
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


@application.route("/buy_detail/<name>")
def view_item_detail(name):
    print("###name:", name)
    data = DB.get_item_byname(str(name))
    print("####data:", data)
    return render_template("/buy_detail_testing.html", name=name, data=data)


@application.route("/rent_detail")
def view_rent_detail():
    return render_template("/rent_detail.html")


@application.route("/reg_rent_items")
def reg_rent_items():
    return render_template("/reg_rent_items.html")


@application.route("/rent_detail/<name>")
def view_rent_item_detail(name):
    print("###name:", name)
    data = DB.get_rent_item_byname(str(name))
    print("####data:", data)
    return render_template("/rent_detail.html", name=name, data=data)


@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    image_file = request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form
    sessionid = session.get('id')
    DB.insert_item(data['name'], data, image_file.filename, sessionid)

    return render_template("submit_item_result.html", data=data,
                           img_path="static/images/{}".format(image_file.filename))


@application.route("/submit_rent_item_post", methods=['POST'])
def reg_rent_item_submit_post():
    image_file = request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form
    sessionid = session.get('id')
    DB.insert_rent_item(data['name'], data, image_file.filename, sessionid)

    return render_template("submit_rent_item_result.html", data=data,
                           img_path="static/images/{}".format(image_file.filename))



if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8000, debug=True)
