from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class Role():
    pass


class User():

    def verify_pass(self, password, username):
        cursor = db.connect().cursor()
        cursor.execute("select password from demo.users where username='" + username + "'")
        data = cursor.fetchone()
        return check_password_hash(data[0], password=password)

    def set_pass(self, password, username):
        cursor = db.connect().cursor()
        password_hash = generate_password_hash(password=password)
        print(password_hash)
        query = "insert into demo.users(`password`) values('" + password_hash + "'); commit"
        print(query)
        cursor.execute(query=query)
