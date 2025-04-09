from app import db

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('schedule.class_id'), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.Boolean, nullable=False, default=True)

    # Связь с основными таблицами
    student = db.relationship('Students', back_populates='attendances')
    schedule = db.relationship('Schedule', back_populates='attendances')

