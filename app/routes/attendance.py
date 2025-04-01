from flask import Blueprint, request, jsonify, render_template
from app.services.attendance_service import Attendance_serv
from flask_wtf import FlaskForm
from wtforms import HiddenField


class CSRFForm(FlaskForm):
        csrf_token = HiddenField()

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/')
def index():
    form = CSRFForm()
    return render_template('index.html', form=form)


@attendance_bp.route('/check_location', methods=['POST'])
def check_location():
    data = request.json
        
    student_location = (data['latitude'], data['longitude'])
    student_id = data.get('student_id')
    student_group = data.get('group_id')
    student_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    result = Attendance_serv.check_location(student_location, 
                                            student_id,
                                            student_group,
                                            student_ip,
                                            user_agent)
    
    return jsonify({'result': f'{result}'})

@attendance_bp.route('/get_groups', methods=['GET'])
def get_groups():
    groups = Attendance_serv.get_groups()
    
    return jsonify({"groups": groups})


@attendance_bp.route('/get_students', methods=['GET'])
def get_students():
    group_id = request.args.get("group_id")
    if not group_id:
        return jsonify({"students": []})

    students = Attendance_serv.get_students(group_id)
    return jsonify({"students": students})



