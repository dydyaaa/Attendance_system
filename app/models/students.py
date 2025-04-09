from app import db

class Students(db.Model):
    __tablename__ = 'students'

    student_id = db.Column(db.Integer, primary_key=True)
    student_first_name = db.Column(db.String(120), nullable=False)
    student_second_name = db.Column(db.String(120), nullable=False)
    student_surname = db.Column(db.String(120), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)
    
    group = db.relationship('Groups', back_populates='students')
    attendances = db.relationship('Attendance', back_populates='student')