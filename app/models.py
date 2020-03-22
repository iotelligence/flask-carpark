from datetime import datetime
from app import db


class Carpark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    floor_slot = db.Column(db.Text)
    available = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Floor_Slot {}, Available {}, timestamp {}>".format(
            self.floor_slot, self.available, self.timestamp
        )
