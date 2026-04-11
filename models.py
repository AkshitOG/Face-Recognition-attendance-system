from db_config import db
from datetime import datetime

class Person(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(30), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"{self.name} at {self.date_time}"