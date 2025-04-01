import logging
from app import db
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from geopy.distance import geodesic
from app.models.pairs import Pairs
from app.models.groups import Groups
from app.models.schedule import Schedule
from app.models.students import Students
from app.models.attendance import Attendance
from app.models.shcedulegropuds import ScheduleGroups


logger = logging.getLogger("para_check")

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s — %(levelname)s — %(message)s',
        datefmt='%H:%M:%S'
)

class Attendance_serv():

    TARGET_LOCATION = (55.845356, 37.506611)
    RADIUS_KM = 20000

    @classmethod
    def check_location(cls, student_location, student_id, student_group, student_ip, user_agent):

        current_time = datetime.now().time() 
        current_date = datetime.now().date()

        if not cls.is_browser(user_agent):
            return 'Неверное устройство!'

        # Сначала ищем занятие по группе и времени
        pair = Pairs.query.filter(
            Pairs.start_time <= current_time,
            Pairs.end_time > current_time
        ).first()

        if not pair:
            info = "Сейчас нет пар."
            logger.info(info)
            return info
        
        logger.info(f'Сейчас - {pair.pair_number}-ая пара')
        
        group = Groups.query.filter_by(group_id=student_group).first()
        
        class_id =  db.session.query(Schedule.class_id).\
            join(ScheduleGroups, Schedule.class_id == ScheduleGroups.class_id)\
                .filter(Schedule.pair_number == pair.pair_number, \
                        func.date(Schedule.class_date) == current_date, \
                        ScheduleGroups.group_id == group.group_id).limit(1).scalar()
        
        if not class_id:
            info = f"Нет занятий для группы {group.group_name} на текущую пару."
            logger.info(info)
            return info
        
        # Проверяем, что IP еще не отмечался
        logger.info(f'IP студента - {student_ip}')
        ip = Attendance.query.filter_by(
            ip_address = student_ip,
            class_id = class_id
            ).first()
        
        if ip:
            info = f'Студент с таким IP адресом уже отмечен на паре!'
            logger.info(info)
            return f'{info} ❌'

        # Проверяем дистанцию
        distance = geodesic(cls.TARGET_LOCATION, student_location).km
        logger.info(f'Геолокация студента - {student_location}')
        logger.info(f'Расстояние студента от таргетной точки - {round(distance, 2)} км')
        
        if distance <= cls.RADIUS_KM:
            logger.info(f'Студент {student_id} на паре!')
            # Отмечаем студента
            new_attendance = Attendance(student_id=student_id,
                                        class_id=class_id,
                                        ip_address=student_ip,
                                        status=True)
            db.session.add(new_attendance)
            db.session.commit()
            return "Вы успешно отмечены на занятии ✅"
        else:
            logger.info(f'Студент {student_id} не на паре!')
            return "Вы находитесь за пределами вуза ❌"
    
    @staticmethod
    def get_groups():

        return [{"id": g.group_id, "name": g.group_name} for g in Groups.query.all()]
    
    @staticmethod
    def get_students(group_id):
        
        students = Students.query.filter_by(group_id=group_id).all()
        return [{"id": s.student_id, "last_name": s.student_second_name, "first_name": s.student_first_name} for s in students]
    
    @staticmethod
    def is_browser(user_agent):
        if any(browser in user_agent.lower() for browser in ['chrome', 'firefox', 'safari', 'edge', 'opera']):
            return True
        return False
