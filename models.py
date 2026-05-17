from datetime import datetime
from database.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Client(db.Model):
    __tablename__ = "client"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(70), nullable=False)
    bouquet = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_count = db.Column(db.Integer, default=1)


class Flower(db.Model):
    __tablename__ = "Flowers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer)
    tags = db.Column(db.String(100))
    description = db.Column(db.Text)  # додаємо опис
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    images = db.relationship("Image", backref="flower", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Flower {self.name}>"



class Image(db.Model):
    __tablename__ = "Images"
    id = db.Column(db.Integer, primary_key=True)  # простіше назвати id
    imgPath = db.Column(db.String(255))
    flower_id = db.Column(db.Integer, db.ForeignKey("Flowers.id"), nullable=False)



