from . import db
from . import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class Role():
    id = None
    name = 'role'
    users = {}


    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(UserMixin):
    def __init__(self, id, username, email, password_hash, role_id, confirmed):
        self.id = id
        self.username = username
        self.email = email
        self.role_id = role_id
        self.password_hash = password_hash
        self.confirmed = confirmed


    @staticmethod
    def getUserById(user_id):
        query = "select * from demo.users where user_id='{0}'".format(user_id)
        return User.getUserByQuery(query)


    @staticmethod
    def getUserByEmail(email):
        query = "select * from demo.users where email='{0}'".format(email)
        return User.getUserByQuery(query)


    @staticmethod
    def getUserByName(username):
        query = "select * from demo.users where username='{0}'".format(username)
        return User.getUserByQuery(query)


    @staticmethod
    def getUserByQuery(query):
        cursor = db.connect().cursor()
        cursor.execute(query)
        data = cursor.fetchone()
        if data is None:
            return None
        return User(id=data[0],
                    username=data[1],
                    email=data[2],
                    password_hash=data[3],
                    role_id=data[4],
                    confirmed=data[5])

    @staticmethod
    def createNewUser(username, password, email, role_id=0):
        cursor = db.connect().cursor()
        password_hash = generate_password_hash(password=password)
        query = "insert into demo.users(username, password, email, role_id) values('{0}', '{1}', '{2}', {3}); commit" \
            .format(username, password_hash, email, str(role_id))
        if cursor.execute(query=query):
            return User.getUserByEmail(email)


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


    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})


    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('confirm') != self.id:
            return False

        cursor = db.connect().cursor()
        query = "update demo.users set confirmed=1 where user_id={0}; commit".format(str(self.id))
        if cursor.execute(query=query):
            self.confirmed = True
            return True

        return False


    def __repr__(self):
        return '<User {}>'.format(self.username)


@login_manager.user_loader
def load_user(user_id):
    return User.getUserById(user_id)
