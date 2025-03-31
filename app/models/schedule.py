from app import db

class Schedule(db.Model):
    __tablename__ = 'schedule'

    class_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, nullable=False)
    class_type = db.Column(db.String(120), nullable=False)
    audience = db.Column(db.String(120), nullable=False)
    class_name = db.Column(db.String(120), nullable=False)
    teacher_name = db.Column(db.String(120), nullable=False)
    started_at = db.Column(db.DateTime, nullable=False)
    ends_at = db.Column(db.DateTime, nullable=False)