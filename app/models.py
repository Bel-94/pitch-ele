from datetime import datetime
from sqlalchemy import text
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
# from email.policy import default
from flask_login import UserMixin, current_user
from . import login_manager






@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    bio = db.Column(db.String(255))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    profile_pic_path = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True, index=True)
    password_secure = db.Column(db.String(255)) 
    
    pitches = db.relationship('Pitch',backref = 'user',lazy = 'dynamic')
    comments = db.relationship('Comment',backref = 'user',lazy = "dynamic")
    upvotes = db.relationship('UpVote',backref = 'user',lazy = "dynamic")
    downvote = db.relationship('DownVote',backref = 'user',lazy = "dynamic")
   
    @property
    def password(self):
        raise AttributeError('You cannot Read Attribute Error')

    @password.setter
    def password(self,password):
        self.password_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_secure,password)

    def __repr__(self):
        return f'User: {self.username} {self.email}'

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'

class Pitch(db.Model):
    __tablename__ = 'pitches'



    id = db.Column(db.Integer,primary_key = True)
    title  = db.Column(db.String(255))
    category = db.Column(db.String(255))
    content = db.Column(db.String(255))
    posted = db.Column(db.DateTime,default=datetime.utcnow)

    author = db.Column(db.Integer, db.ForeignKey('users.id'))

    comments  = db.relationship('Comment',backref = 'pitch',lazy = 'dynamic')
    upvotes = db.relationship('UpVote',backref = 'pitch',lazy = 'dynamic')
    downvotes = db.relationship('DownVote',backref = 'pitch',lazy = 'dynamic')
      


    def save_pitch(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_pitch(cls,id):
        pitches = Pitch.query.filter_by(id=id).all()
        return pitches

    @classmethod
    def get_all_pitches(cls):
        pitches = Pitch.query.order_by('-id').all()
        return pitches

    def __repr__(self):
        return f'Pitch: {self.title}'

class Comment(db.Model):

    __tablename__ = 'comments'

    id  = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    comment = db.Column(db.String(255))


    def save_comment(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(pitch_id=id).all()
        return comments
    @classmethod
    def get_all_comments(cls,id):
        comments = Comment.query.order_by('-id').all()
        return comments


    

class UpVote(db.Model):

    __tablename__ = 'upvotes'

    id = db.Column(db.Integer,primary_key =True)
    upvote = db.Column(db.Integer,default = 0)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_upvote(self):
        db.session.add(self)
        db.session.commit()

    def add_upvotes(cls,id):
        upvote = UpVote(user = current_user, pitch_id=id)
        upvote.save_upvote()

    @classmethod
    def get_upvotes(cls,id):
        upvote = UpVote.query.filter_by(pitch_id=id).all()
        return upvote


    @classmethod
    def get_all_upvotes(cls,pitch_id):
        upvote = UpVote.query.order_by(text('-id')).all()
        return upvote

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'
        

class DownVote(db.Model):
    __tablename__ = 'downvotes'

    id = db.Column(db.Integer,primary_key = True)
    downvote = db.Column(db.Integer,default = 0)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_downvote(self):
        db.session.add(self)
        db.session.commit()

    def add_downvote(cls,id):
        downvote = DownVote(user = current_user, pitch_id = id)
        return downvote.save_downvote()

    @classmethod
    def get_downvotes(cls,id):
        downvote = DownVote.query.filter_by(pitch_id=id).all()
        return downvote

    @classmethod
    def get_all_downvotes(cls,pitch_id):
        downvote = DownVote.query.order_by(text('-id')).all()
        return downvote
        
    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'

class Quote:
    """
    Class for quotes consumed from API
    """
    def __init__(self, author, quote):
        self.author = author
        self.quote = quote

    