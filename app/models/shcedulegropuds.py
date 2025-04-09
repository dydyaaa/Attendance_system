from app import db

class ScheduleGroups(db.Model):
    __tablename__ = 'schedule_groups'

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('schedule.class_id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)
    
    schedule = db.relationship('Schedule', back_populates='group_links')
    group = db.relationship('Groups', back_populates='schedule_links')