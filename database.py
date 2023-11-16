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
            "seller": sessionid
        }
        self.db.child("item").child(name).set(item_info)
        print(data, img_path)
        return True

    def insert_rent_item(self, name, data, img_path, sessionid):
        item_info = {
            "price": data["price"],
            "addr": data['addr'],
            "send": data['send'],
            "period": data['period'],
            "keyword": data["keyword"],
            "explain": data["explain"],
            "img_path": img_path,
            "seller": sessionid
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

    def get_rent_item_byname(self, name):
        items = self.db.child("rent_item").get()
        target_value = ""
        print("###########", name)
        for res in items.each():
            key_value = res.key()
            if key_value == name:
                target_value = res.val()
        return target_value

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
