from app import db

class Pairs(db.Model):
    __tablename__ = 'pairs'

    pair_number = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    
    schedules = db.relationship('Schedule', back_populates='pair')