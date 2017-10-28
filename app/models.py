from . import db
from . import login_manager
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from enum import IntEnum


def cursorFetchOne(query):
    cursor = db.connect().cursor()
    cursor.execute(query)
    return cursor.fetchone()


class Permissions(IntEnum):
    ADMINS = 0b10000000
    MODERATORS = 0b00001000
    CREATE_POSTS = 0b00000100
    CREATE_COMMENTS = 0b00000010
    FOLLOWING = 0b00000001
    EMPTY = 0b00000000


class Role:
    def __init__(self, role_id, name, permission):
        self.id = role_id
        self.name = name
        self.permission = permission


    @staticmethod
    def getRoleByName(role_name):
        data = cursorFetchOne("SELECT * FROM demo.user_roles where name='{0}';".format(role_name))
        if data is None:
            return None
        return Role(role_id=data[0], name=data[1], permission=data[3])


    @staticmethod
    def getDefaultRole():
        data = cursorFetchOne("SELECT * FROM demo.user_roles where default_role=1;")
        if data is None:
            return None
        return Role(role_id=data[0], name=data[1], permission=data[3])


    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(UserMixin):
    # base query for give a member from db. Just add condition after where
    base_query = "select users.*, user_roles.name, user_roles.permissions"\
                   " from users left join user_roles ON users.role_id=user_roles.role_id where {0};"


    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id', None)
        self.username = kwargs.get('username', None)
        self.email = kwargs.get('email', None)
        self.password_hash = kwargs.get('password_hash', None)
        self.confirmed = kwargs.get('confirmed', None)
        self.role = kwargs.get('role', None)
        self.location = kwargs.get('location', None)
        self.about = kwargs.get('about', None)
        self.member_since = kwargs.get('member_since', None)
        self.last_seen = kwargs.get('last_seen', None)
        if self.role is None:
            if self.email == current_app.config['ADMIN']:
                self.role = Role.getRoleByName('admin')
            if self.role is None:
                self.role = Role.getDefaultRole()


    @property
    def getRole(self):
        return self.role  #class Role

    def get_id(self):
        return self.user_id

    @staticmethod
    def getUserById(user_id):
        return User.getUserByQuery(User.base_query.format("user_id='{0}'".format(user_id)))


    @staticmethod
    def getUserByEmail(email):
        return User.getUserByQuery(User.base_query.format("email='{}'".format(email)))


    @staticmethod
    def getUserByName(username):
        return User.getUserByQuery(User.base_query.format("username='{}'".format(username)))


    @staticmethod
    def getAllUsersName():
        cursor = db.connect().cursor()
        cursor.execute('select username from demo.users')
        return cursor.fetchall()

    @staticmethod
    def getAllUsers():
        cursor = db.connect().cursor()
        cursor.execute('select * from demo.users')
        return cursor.fetchall()

    @staticmethod
    def getUserByQuery(query):
        print(query)
        cursor = db.connect().cursor()
        cursor.execute(query)
        data = cursor.fetchone()
        if data is None:
            return None
        return User(user_id=data[0],
                    username=data[1],
                    email=data[2],
                    password_hash=data[3],
                    role=Role(role_id=data[4], name=data[6], permission=data[7]),
                    confirmed=data[5],
                    location=data[8],
                    about=data[9],
                    member_since=data[10],
                    last_seen=data[11])


    @staticmethod
    def createNewUser(username, password, email, role_id=0):
        cursor = db.connect().cursor()
        password_hash = generate_password_hash(password=password)
        query = "insert into demo.users(username, password, email, role_id) values('{0}', '{1}', '{2}', {3}); commit" \
            .format(username, password_hash, email, str(role_id))
        if cursor.execute(query=query):
            last_row_id = cursor.lastrowid
            print("ID for newly created user: ", last_row_id)
            # maybe bad design:=)
            return User.getUserById(last_row_id)



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
        return check_password_hash(passwd_hash, password=password) if passwd_hash else False


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


    def can(self, permissions):
        return self.role is not None and \
            (self.role.permission & permissions) == permissions


    def is_administrator(self):
        return self.can(Permissions.ADMINS)


    def __repr__(self):
        return '<User {}>'.format(self.username)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False


    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.getUserById(user_id)
