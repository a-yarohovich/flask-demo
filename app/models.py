from . import db
from . import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Role():
    id = None
    name = 'role'
    users = {}

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(UserMixin):
    def __init__(self, id, username, email, role_id):
        self.id = id
        self.username = username
        self.email = email
        self.role_id = role_id


    def get_auth_token(self):
        pass
        #return make_secure_token(self.username, key='secret_key')

    @staticmethod
    def getUserById(user_id):
        query = "select user_id, username, email, role_id " \
                "from demo.users where user_id='{0}'".format(user_id)
        cursor = db.connect().cursor()
        cursor.execute(query)
        data = cursor.fetchone()
        if data is None:
            return None
        return User(id=data[0],username=data[1],email=data[2], role_id=data[3])


    def verify_pass(self, password):
        cursor = db.connect().cursor()
        query = "select password from demo.users where username='{0}'".format(self.username)
        cursor.execute(query)
        data = cursor.fetchone()
        return check_password_hash(data[0], password=password) if data else False


    def create_user(self, password):
        cursor = db.connect().cursor()
        password_hash = generate_password_hash(password=password)
        query = "insert into demo.users(username, password) values('{0}', '{1}'); commit"\
            .format(self.username, password_hash)
        cursor.execute(query=query)


    def __repr__(self):
        return '<User {}>'.format(self.username)


@login_manager.user_loader
def load_user(user_id):
    return User.getUserById(user_id)