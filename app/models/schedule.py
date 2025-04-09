from app import db

class Schedule(db.Model):
    __tablename__ = 'schedule'

    class_id = db.Column(db.Integer, primary_key=True)
    class_type = db.Column(db.String(120), nullable=False)
    audience = db.Column(db.String(120), nullable=False)
    class_name = db.Column(db.String(120), nullable=False)
    teacher_name = db.Column(db.String(120), nullable=False)
    pair_number = db.Column(db.Integer, db.ForeignKey('pairs.pair_number'), nullable=False)
    class_date = db.Column(db.Date)
    
    group_links = db.relationship('ScheduleGroups', back_populates='schedule')
    attendances = db.relationship('Attendance', back_populates='schedule')
    pair = db.relationship('Pairs', back_populates='schedules')