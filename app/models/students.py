from app import db

class Groups(db.Model):
    __tablename__ = 'groups'

    student_id = db.Column(db.Integer, primary_key=True)
    student_group = db.Column(db.String(120), nullable=False)
    student_first_name = db.Column(db.String(120), nullable=False)
    student_second_name = db.Column(db.String(120), nullable=False)
    student_surname = db.Column(db.String(120), nullable=False)