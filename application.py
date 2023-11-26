from flask import Flask, render_template, request, flash
from flask import redirect, url_for, session, jsonify
from database import DBhandler
import hashlib
import sys
from datetime import datetime

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

"""
@application.route("/rent")
def view_rent_list():
    page = request.args.get("page", 0, type=int)
    per_page = 8
    start_idx = per_page*page
    end_idx = per_page*(page+1)
    data = DB.get_rent_items()
    item_count = len(data)
    total = item_count
    data = dict(list(data.items())[start_idx:end_idx])

    return render_template(
        "rent_items_list.html", datas=data.items(),
        limit=per_page, page=page,
        page_count=int((item_count/per_page)+1), total=item_count)

"""


@application.route("/rent")
def view_rent_list():
    page = request.args.get("page", 0, type=int)
    per_page = 8
    start_idx = per_page * page
    end_idx = per_page * (page + 1)

    startdate = request.args.get("period_start")
    enddate = request.args.get("period_end")

    data = DB.get_rent_items()

    # Filter items based on the rental period if dates are provided
    if startdate and enddate:
        start_date = datetime.strptime(startdate, "%Y-%m-%d").date()
        end_date = datetime.strptime(enddate, "%Y-%m-%d").date()
        
        
        data = {key: value for key, value in data.items() if start_date >= datetime.strptime(value['period-start'], "%Y-%m-%d").date() and end_date <= datetime.strptime(value['period-end'], "%Y-%m-%d").date()}
        print(data)
    item_count = len(data)
    total = item_count
    data = dict(list(data.items())[start_idx:end_idx])

    return render_template(
        "rent_items_list.html", datas=data.items(),
        limit=per_page, page=page,
        page_count=int((item_count / per_page) + 1), total=item_count)


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

"""
@application.route("/mypage")
def view_mypage():
    #판매물품
    data = DB.get_items()
    data = dict(list(data.items())[:])
    #대여물품
    rent_data = DB.get_rent_items()
    rent_data = dict(list(rent_data.items())[:])
    #대여내역
    rent_list_data = DB.get_rent_list_byid(session['id'])
    rent_list_data = dict(list(rent_list_data.items())[:])
    return render_template(
        "mypage.html", datas=data.items(), rent_datas=rent_data.items(), rent_list_datas=rent_list_data.items()
    )
"""
@application.route("/mypage")
def view_mypage():
    # 판매물품
    data = DB.get_items()
    data = dict(list(data.items())[:])

    # 대여물품
    rent_data = DB.get_rent_items()
    rent_data = dict(list(rent_data.items())[:])

    # 대여내역
    user_id = session.get('id', None)
    rent_list_data = DB.get_rent_list_byid(user_id)

    if not isinstance(rent_list_data, dict):
        rent_list_data = {}

    return render_template(
        "mypage.html", datas=data.items(), rent_datas=rent_data.items(), rent_list_datas=rent_list_data.items()
    )





@application.route("/reg_review_init/<name>/")
def reg_review_init(name):
    data = DB.get_rent_item_byname(name)
    return render_template("reg_reviews.html", name=name, data=data)


@application.route("/reg_items")
def reg_items():
    return render_template("/reg_items.html")


@application.route("/reg_reviews", methods=['POST'])
def reg_review():
    image_file = request.files["reviewImage"]
    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form
    DB.reg_review(data, image_file.filename)
    return redirect(url_for('view_review'))


@application.route("/review")
def view_review():
    page = request.args.get("page", 0, type=int)
    per_page = 3  # item count to display per page
    per_row = 1  # item count to display per row
    row_count = int(per_page/per_row)
    start_idx = per_page*page
    end_idx = per_page*(page+1)
    data = DB.get_reviews()  #read the table
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    for i in range(row_count):  #last row
        if (i == row_count-1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
    return render_template(
        "review.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        row3=locals()['data_2'].items(),
        limit=per_page, page=page,
        page_count=int((item_counts/per_page)+1),
        total=item_counts)



"""return render_template("/review.html")"""


@application.route("/review_testing")
def view_review_testing():
    page = request.args.get("page", 0, type=int)
    per_page = 6  # item count to display per page
    per_row = 2  # item count to display per row
    row_count = int(per_page/per_row)
    start_idx = per_page*page
    end_idx = per_page*(page+1)
    data = DB.get_reviews()  #read the table
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    for i in range(row_count):  #last row
        if (i == row_count-1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
    return render_template(
        "review_testing.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        row3=locals()['data_2'].items(),
        limit=per_page, page=page,
        page_count=int((item_counts/per_page)+1),
        total=item_counts)

"""
return render_template(
        "review_testing.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        row3=locals()['data_2'].items(),
        limit=per_page, page=page,
        page_count=int((item_counts/per_page)+1),
        total=item_counts)
"""


@application.route("/view_review_detail/<name>/")
def view_review_detail(name):
    data = DB.get_review_byname(str(name))

    return render_template("review_detail.html", name=name, data=data)


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
    return redirect(url_for('view_list'))
    # return render_template("buy_items_list.html")


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

@application.route("/check_duplicate_id", methods=['POST'])
def check_duplicate_id():
    data = request.form
    user_id = data['id']
    if DB.check_duplicate_id(user_id):
        return jsonify({'status': 'duplicate'})
    else:
        return jsonify({'status': 'ok'})
    
    

@application.route("/buy_detail")
def view_buy_detail():
    return render_template("/buy_detail.html")


@application.route("/buy_detail/<name>/")
def view_item_detail(name):
    print("###name:", name)
    data = DB.get_item_byname(str(name))
    print("####data:", data)
    return render_template("/buy_detail_testing.html", name=name, data=data)


@application.route("/rent_detail")
def view_rent_detail():
    return render_template("/rent_detail.html")


@application.route("/rent_detail/<name>")
def view_rent_item_detail(name):
    print("###name:", name)
    data = DB.get_rent_item_byname(str(name))
    print("####data:", data)
    return render_template("/rent_detail.html", name=name, data=data)


@application.route("/reg_rent_items")
def reg_rent_items():
    return render_template("/reg_rent_items.html")


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


@application.route('/show_heart/<name>/', methods=['GET'])
def show_heart(name):
    my_heart = DB.get_heart_byname(session['id'], name)
    return jsonify({'my_heart': my_heart})


@application.route('/like/<name>/', methods=['POST'])
def like(name):
    my_heart = DB.update_heart(session['id'], 'Y', name)   
    return jsonify({'msg': '좋아요 완료!'})


@application.route('/unlike/<name>/', methods=['POST'])
def unlike(name):
    my_heart = DB.update_heart(session['id'], 'N', name)
    return jsonify({'msg': '안좋아요 완료!'})


@application.route('/update_rent/<name>/', methods=['POST'])
def update_rent(name):
    #price = request.form.get('price')
    #seller = request.form.get('seller')
    #address = request.form.get('address')
    #period = request.form.get('period')
    #delivery_method = request.form.get('deliveryMethod')
    data = request.form
    sessionid = session.get('id')
    isRent = 'Y'
    success = DB.update_rent_list(data, sessionid, isRent, name)
    print(data)
    if success:
        return jsonify({'msg': "대여 완료!"})
    else:
        #return "Failed to update rent list"
        return jsonify({'msg': "대여 실패..."})

@application.route('/update_buy/<name>/', methods=['POST'])
def update_buy(name):
    data = request.form
    sessionid = session.get('id')
    isBuy = 'Y'
    success = DB.update_buy_list(data, sessionid, isBuy, name)
    print(data)
    if success:
        return jsonify({'msg': "구매 완료!"})
    else:
        return jsonify({'msg': "구매 실패..."})


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8000, debug=True)
