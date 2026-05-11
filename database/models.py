from datetime import datetime
from database.db import db


class Client(db.Model):
    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(70), nullable=False)
    bouquet = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_count = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f"<Client {self.name}>"