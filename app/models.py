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
    def __init__(self, id, username, email, password_hash, role_id):
        self.id = id
        self.username = username
        self.email = email
        self.role_id = role_id
        self.password_hash = password_hash


    def get_auth_token(self):
        pass
        # return make_secure_token(self.username, key='secret_key')


    @staticmethod
    def getUserById(user_id):
        query = "select * from demo.users where user_id='{0}'".format(user_id)
        return User.getUserByQuery(query)


    @staticmethod
    def getUserByEmail(email):
        query = "select * from demo.users where email='{0}'".format(email)
        return User.getUserByQuery(query)


    @staticmethod
    def getUserByQuery(query):
        cursor = db.connect().cursor()
        cursor.execute(query)
        data = cursor.fetchone()
        if data is None:
            return None
        return User(id=data[0], username=data[1], email=data[2], password_hash=data[3], role_id=data[4])


    def verify_password(self, password):
        passwd_hash = None
        if self.password_hash:
            passwd_hash = self.password_hash
        else:
            cursor = db.connect().cursor()
            query = "select password from demo.users where username='{0}'".format(self.username)
            cursor.execute(query)
            data = cursor.fetchone()
            if data:
                passwd_hash = data[0]
        return (check_password_hash(passwd_hash, password=password)) if (passwd_hash) else (False)


    def create_user(self, password):
        cursor = db.connect().cursor()
        self.password_hash = generate_password_hash(password=password)
        query = "insert into demo.users(username, password) values('{0}', '{1}'); commit" \
            .format(self.username, self.password_hash)
        cursor.execute(query=query)


    def __repr__(self):
        return '<User {}>'.format(self.username)


@login_manager.user_loader
def load_user(user_id):
    return User.getUserById(user_id)
