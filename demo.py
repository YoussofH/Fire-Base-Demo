import pyrebase
import os

config = {
    "apiKey": "AIzaSyD5YMBHFyKCkn_KH9wSfdEOO8U2puvItN4",
    "authDomain": "a-new-project-fe23a.firebaseapp.com",
    "databaseURL": "https://a-new-project-fe23a-default-rtdb.firebaseio.com/",
    "projectId": "a-new-project-fe23a",
    "storageBucket": "a-new-project-fe23a.appspot.com",
    "messagingSenderId": "719984821207",
    "appId": "1:719984821207:web:72240dad4cb6d045c68192"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()


def sign_in():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    try:
        auth.sign_in_with_email_and_password(email, password)
        print("Signed in successfully!")
    except:
        print("Wrong Email or Password. Try again!")


def sign_up():
    email = input("Enter your email: ")
    password = 0
    confirm_password = 1
    while password != confirm_password:
        password = input("Enter your password: ")
        confirm_password = input("Confirm your password: ")
        if password != confirm_password:
            print("Passwords don't match!")
    try:
        auth.create_user_with_email_and_password(email, password)
        print("Signed up successfully!")
    except Exception as e:
        print(e)


def upload_file():
    local_file_path = input("Enter file path: ")
    #cloud_storage_folder_path = input("Enter cloud storage folder path: ")
    cloud_storage_folder_path = ""
    try:
        cloud_final_path = cloud_storage_folder_path + "/" + local_file_path
        storage.child(cloud_final_path).put(local_file_path)
        print(storage.child(cloud_final_path).get_url(None))  # URL to Uploaded document/file
    except:
        print("Something went wrong.")


def download_file():
    try:
        cloud_storage_file_path = input("Enter cloud storage file path(hint:text.txt): ")
        storage.child(cloud_storage_file_path).download("", filename="downloaded_file.txt")
        os.replace("./downloaded_file.txt", "downloads_folder/downloaded_file.txt")
    except:
        print("Something went wrong.")


class students:
    std_dir = "/University/Students"  # Students Directory

    def __init__(self, id=None, name=None, age=None, gender=None, employed=None):
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender
        self.employed = employed

    def select(self):
        if type(self.id) is not int and self.id is not None:
            raise TypeError("Integer should be passed instead of " + str(type(self.id)).split("'")[1].__str__())

        id_res = []
        std_res_keys = []
        found_in = {
            "name": 0,
            "age": 0,
            "gender": 0,
            "employed": 0
        }
        stds = db.child(students.std_dir).get()
        for std in stds.each():
            user = db.child(students.std_dir).child(std.key()).get().val()
            index = user["id"]

            if self.id and user["id"] == self.id:
                id_res.append(index)
                std_res_keys.append(std.key())
                return std_res_keys
            else:
                if self.name and user["name"] == self.name:
                    id_res.append(index)
                    std_res_keys.append(std.key())
                    found_in["name"] = 1
                if self.age and user["age"] == self.age:
                    std_res_keys.append(std.key())
                    id_res.append(index)
                    found_in["age"] = 1
                if self.gender and user["gender"] == self.gender:
                    std_res_keys.append(std.key())
                    id_res.append(index)
                    found_in["gender"] = 1
                if self.employed and user["employed"] == self.employed:
                    std_res_keys.append(std.key())
                    id_res.append(index)
                    found_in["employed"] = 1
                id_res = list(set([id for id in id_res if id_res.count(id) == sum(found_in.values())]))
                std_res_keys = list(
                    set([user for user in std_res_keys if std_res_keys.count(user) == sum(found_in.values())]))
        return std_res_keys

    def create(self):
        data = {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "employed": self.employed
        }
        stds = db.child(students.std_dir).get()
        max_id = 0
        for std in stds.each():
            max_id = std.val()["id"] if std.val()["id"] > max_id else max_id

        data["id"] = max_id + 1
        db.child(students.std_dir).push(data)  # for random Key

    def update(self, new_name=None, new_age=None, new_gender=None, new_employed=None):
        stds = students.select(self)
        for std in stds:
            user = db.child(students.std_dir).child(std).get()
            db.child(students.std_dir).child(std).update({
                "name": new_name if new_name is not None else user.val()["name"],
                "age": new_age if new_age is not None else user.val()["age"],
                "gender": new_gender if new_gender is not None else user.val()["gender"],
                "employed": new_employed if new_employed is not None else user.val()["employed"]
            })

    def delete(self):
        parent = students.select(self)
        db.child(students.std_dir).remove(parent)

    @staticmethod
    def users_data():
        data = []
        try:
            data = list(filter(None, list(db.child(students.std_dir).get().val())))
        except:
            data = []
        return data

    @staticmethod
    def users_capacity():
        return len(students.users_data())  # Serves as an ID referrer


if __name__ == '__main__':
    # sign_up()
    # sign_in()  # foobar@mail.com/foobar
    # upload_file()
    # download_file()

    # students(name="Ahmad", age=4, gender="male", employed=False).create()
    # students(employed=True).update(new_gender="gen")
    # students(id=1).delete()
    pass
