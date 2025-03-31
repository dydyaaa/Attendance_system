from app import db

class Groups(db.Model):
    __tablename__ = 'groups'

    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(120), nullable=False)