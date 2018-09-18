# import os, jwt
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from time import time

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(48), unique = True, index=True)
    email = db.Column(db.String(48),unique=True, index = True)
    phone = db.Column(db.String(12),unique = True, index = True)
    language_category = db.Column(db.String(200),unique = True, index = True)
    hash_pass = db.Column(db.String(255)) 
    error = db.relationship('Error',backref='user',lazy='dynamic')
    solution = db.relationship('Solution',backref='user',lazy='dynamic')
    photo = db.relationship('Photo',backref='user',lazy='dynamic')
    

    @property
    def password(self):
        raise AttributeError("You cannot read password attribute")

    @password.setter
    def password(self,password):
        self.hash_pass = generate_password_hash(password)
    
    def set_password(self,password):
        self.hash_pass = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.hash_pass,password)  
    
    def get_reset_password_token(self, expires_in=1800):
        return jwt.encode({'reset_password':self.id, 'exp':time()+expires_in}, os.environ.get('SECRET_KEY'), algorithm='HS256').decode('utf-8')
    
    @staticmethod
    def verify_reset_password(token):
        try:
            id = jwt.decode(token, os.environ.get('SECRET_KEY'),algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)  

class Error(db.Model):
    __tablename__='errors'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String())
    error_content = db.Column(db.String())
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    error_pic = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    comment = db.relationship('Comment',backref='blog',lazy='dynamic')
    photo = db.relationship('Photo', backref='blog',lazy='dynamic')

    def save_error(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_all_errors(cls):
        errors = Error.query.order_by('-id').all()
        return errors

    @classmethod
    def get_single_error(cls,id):
        error = Error.query.filter_by(id=id).first()
        return error

class Solution(db.Model):
    __tablename__='solutions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    solution_post = db.Column(db.String())
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    solution_post = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def save_solution(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_blog_solutions(cls,id):
        solutions = Solution.query.order_by('-id').all()
        return solutions
    
    @classmethod
    def get_single_solution(cls,id):
        solution = Solution.query.filter_by(id=id).first()
        return solution


class Photo(db.Model):
    __tablename__='photos'
    id = db.Column(db.Integer,primary_key=True)
    photo_data = db.Column(db.String(255))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))