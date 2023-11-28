import pyrebase
import json


class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

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
            "openkakao": data['openkakao']
        }
        self.db.child("item").child(name).set(item_info)
        print(data, img_path)
        return True

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

    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        target_value = []
        for res in users.each():
            value = res.val()

            if value['id'] == id_ and value['pw'] == pw_:

                user_info = {
                'id': id_,
                'email': value['email'],  # Replace with actual email retrieval
                'openkakao': value['openkakao'],  # Replace with actual openkakao retrieval
                'department': value['department']  # Replace with actual department retrieval
            }
                return user_info
                # return True

        # return False
        return None

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

    def get_items(self):
        items = self.db.child("item").get().val()
        return items

    def get_rent_items(self):
        items = self.db.child("rent_item").get().val()
        return items

    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value = ""
        print("###########", name)
        for res in items.each():
            key_value = res.key()
            if key_value == name:
                target_value = res.val()
        return target_value

    def get_rent_item_byname(self, name):
        items = self.db.child("rent_item").get()
        target_value = ""
        print("###########", name)
        for res in items.each():
            key_value = res.key()
            if key_value == name:
                target_value = res.val()
        return target_value
    
    def get_rent_list_byid(self, user_id):
        items = self.db.child("rent_list").get()
        target_value = ""
        print("###########", user_id)
        for res in items.each():
            key_value = res.key()
            if key_value == user_id:
                target_value = res.val()
        return target_value

    def reg_review(self, data, img_path):
        review_info = {
            "title": data['reviewTitle'],
            "text": data['reviewText'],
            "img_path": img_path,
            "writer": data['writer'],
            "rate": data['reviewStar'],
            "seller":data['seller']
        }
        self.db.child("review").child(data['name']).set(review_info)
        print(data, img_path)
        return True

    def get_reviews(self):
        reviews = self.db.child("review").get().val()
        return reviews

    def get_review_byname(self, name):
        reviews = self.db.child("review").get()
        target_value = ""

        for res in reviews.each():
            key_value = res.key()
            if key_value == name:
                target_value = res.val()

        return target_value

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


    def update_rent_list(self, data, user_id, isRent, item):
        rent_info = {
            "borrow": isRent,
            "price": data['price'],
            "seller": data['seller'],
            "img_path": data['img_path']
            #"address" : data['address'],
            #"deliveryMethod" : data['deliveryMethod']
        }
        self.db.child("rent_list").child(user_id).child(item).set(rent_info)
        print(rent_info)
        return True
    
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

    def reg_review(self, data, img_path):
        review_info = {
            "title": data['reviewTitle'],
            "text": data['reviewText'],
            "img_path": img_path,
            "writer": data['writer'],
            "rate": data['reviewStar'],
            "seller":data['seller']
        }
        self.db.child("review").child(data['name']).set(review_info)
        print(data, img_path)
        return True

    def update_heart(self, user_id, isHeart, item):
        heart_info = {
            "interested": isHeart
        }
        self.db.child("heart").child(user_id).child(item).set(heart_info)
        return True
    
