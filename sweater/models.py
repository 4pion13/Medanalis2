from flask_sqlalchemy import SQLAlchemy
from flask_login import (UserMixin)
from sweater import db

class UserInfo(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    status = db.Column(db.String(10))
    age = db.Column(db.String(10))
    def __repr__(self):
        return f"<id={self.id}, email={self.email}, name={self.name}>"


class Symptoms(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Symptom = db.Column(db.String(100))
    Weight = db.Column(db.String(100))
    def __repr__(self):
        return f"{self.Symptom}, {self.Weight}"

class Weight(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Wei = db.Column(db.String(100))
    def __repr__(self):
        return str(self.Wei)
    
    
class Doctor_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(100))
    name = db.Column(db.String(100))
    photo = db.Column(db.String(100))
    def __repr__(self):
        return f"{self.id}, {self.post}, {self.name}, {self.photo}"


class Doctor_schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_info.id'))
    reception_time = db.Column(db.DateTime)

    def __repr__(self):
        return f"{self.id}, {self.doctor_id}, {self.reception_time}"
    

db.create_all()





