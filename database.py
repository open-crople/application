import pyrebase
import json


class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    # 판매할 물건 item 아래에 등록
    def insert_item(self, name, data, img_path, sessionid):
        item_info = {
            "price": data["price"],
            "addr": data['addr'],
            "status": data['status'],
            "send": data['send'],
            "keyword": data["keyword"],
            "explain": data["explain"],
            "img_path": img_path,
            "seller": sessionid,
            "openkakao": data['openkakao'],
            "confirm":0
        }
        self.db.child("item").child(name).set(item_info)
        print(data, img_path)
        return True

    # 구매 완료시 item confirm 값 처리
    def confirm_buying(self,name):
        self.db.child("item").child(name).update({"confirm":1})
        return True
    
    def get_confirm_value(name):
        confirm = self.db.child("item").child(name).child("confirm").get()
        return confirm

    # 대여해줄 물건 rent_item 아래에 등록
    def insert_rent_item(self, name, data, img_path, sessionid):
        item_info = {
            "price": data["price"],
            "addr": data['addr'],
            "send": data['send'],
            "period-start": data['period-start'],
            "period-end": data['period-end'],
            "keyword": data["keyword"],
            "explain": data["explain"],
            "img_path": img_path,
            "seller": sessionid,
            "openkakao": data['openkakao']
        }
        self.db.child("rent_item").child(name).set(item_info)
        print(data, img_path)
        return True

    # 회원가입정보 user 아래에 등록
    def insert_user(self, data, pw):
        user_info = {
            "id": data['id'],
            "pw": pw,
            # "password_check": data['password_check'],
            "email": data['email'],
            "openkakao": data['openkakao'],
            "department": data['department']
        }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            print(data)
            return True
        else:
            return False

    # id와 pw에 해당하는 사용자 정보를 user_info로 반환
    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        target_value = []
        for res in users.each():
            value = res.val()
            if value['id'] == id_ and value['pw'] == pw_:
                user_info = {
                    "id_": id_,
                    "email": value['email'],
                    "openkakao": value['openkakao'],
                    "department": value['department']
                }
                return user_info
        return None

    # 아이디 중복 확인
    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        print("users###", users.val())
        if str(users.val()) == "None":
            return True
        else:
            for res in users.each():
                value = res.val()

                if value['id'] == id_string:
                    return False
            return True

    # 판매상품 가져오기
    def get_items(self):
        items = self.db.child("item").get().val()
        return items

    # 대여상품 가져오기
    def get_rent_items(self):
        items = self.db.child("rent_item").get().val()
        return items

    # 판매상품 이름으로 찾기
    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value = ""
        print("###########", name)
        for res in items.each():
            key_value = res.key()
            if key_value == name:
                target_value = res.val()
        return target_value

    # 대여상품 이름으로 찾기
    def get_rent_item_byname(self, name):
        items = self.db.child("rent_item").get()
        target_value = ""
        print("###########", name)
        for res in items.each():
            key_value = res.key()
            if key_value == name:
                target_value = res.val()
        return target_value

    # 대여상품 사용자 아이디로 찾기
    def get_rent_list_byid(self, user_id):
        items = self.db.child("rent_list").get()
        target_value = ""
        print("###########", user_id)
        for res in items.each():
            key_value = res.key()
            if key_value == user_id:
                target_value = res.val()
        return target_value

    # 리뷰내용 review 아래에 상품이름별로 등록
    def reg_review(self, data, img_path, current_time):
        review_info = {
            "item": data['name'],
            "title": data['reviewTitle'],
            "text": data['reviewText'],
            "img_path": img_path,
            "writer": data['writer'],
            "rate": data['reviewStar'],
            "seller": data['seller'],
            "date": current_time
        }
        self.db.child("review").child(data['name']+data['writer']).set(review_info)
        self.db.child("rent_list").child(data['writer']).child(data['name']).update({"review": "Y"})
        print(data, img_path)
        return True

    # 리뷰내용 가져오기
    def get_reviews(self):
        reviews = self.db.child("review").get().val()
        return reviews

    # 리뷰내용 상품명으로 찾기
    def get_review_byname(self, name):
        reviews = self.db.child("review").get()
        target_value = ""
        for res in reviews.each():
            key_value = res.key()
            if key_value == name:
                target_value = res.val()
        return target_value

    # 하트 클릭한 적 있는지 사용자 이름으로 확인
    def get_heart_byname(self, uid, name):
        hearts = self.db.child("heart").child(uid).get()
        target_value = ""
        if hearts.val() == None:
            return target_value

        for res in hearts.each():
            key_value = res.key()

            if key_value == name:
                target_value = res.val()
        return target_value

    # 대여한 물건을 rent_list 아래에 사용자 아이디별로 등록
    def update_rent_list(self, data, user_id, isRent, item):
        rent_info = {
            "borrow": isRent,
            "price": data['price'],
            "seller": data['seller'],
            "img_path": data['img_path'],
            "review": "N"
        }
        self.db.child("rent_list").child(user_id).child(item).set(rent_info)
        print(rent_info)
        return True

    # 구매한 물건을 buy_list 아래에 사용자 아이디별로 등록
    def update_buy_list(self, data, user_id, isBuy, item):
        buy_info = {
            "buy": isBuy,
            "price": data['price'],
            "seller": data['seller'],
            "img_path": data['img_path']
        }
        self.db.child("buy_list").child(user_id).child(item).set(buy_info)
        print(buy_info)
        return True

    # 하트 클릭한 경우 heart 아래에 사용자 아이디별로 등록
    def update_heart(self, user_id, isHeart, item):
        heart_info = {
            "interested": isHeart
        }
        self.db.child("heart").child(user_id).child(item).set(heart_info)
        return True
