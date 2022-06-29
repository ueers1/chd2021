from aiohttp import web
from urllib.parse import urlencode
from psycopg.errors import UniqueViolation, ForeignKeyViolation
from .config import web_routes
from .dblock import dblock

@web_routes.post('/action/courseschedule/add')
async def action_grade_add(request):
    params = await request.post()
    course_no = params.get("course_no")
    clas_shift= params.get("clas_shift")
    class_location = params.get("class_location")
    class_date = params.get("class_date")
    class_teacher = params.get("class_teacher")

    if (course_no is None or clas_shift is None or 
        class_location is None or class_date is None or
        class_teacher is None):
        return web.HTTPBadRequest(text="courses_no, clas_shift, class_location, class_date, class_teacher must be required")

    try:
        with dblock() as db:
            db.execute("""
            INSERT INTO class_schedule (course_sn, clas_shift, class_location, class_date, class_teacher) 
            VALUES ( %(course_sn)s, %(clas_shift)s, %(class_location)s, %(class_date)s, %(class_teacher)s)
            """, dict(course_sn=course_no, clas_shift=clas_shift, class_location=class_location, class_date=class_date, class_teacher=class_teacher))
    except UniqueViolation:
        query = urlencode({
            "message": "已经添加该课程安排",
            "return": "/grade"
        })
        return web.HTTPFound(location=f"/error?{query}")
    except ForeignKeyViolation as ex:
        return web.HTTPBadRequest(text=f"无此课程安排: {ex}")

    return web.HTTPFound(location="/courseschedule")

@web_routes.post('/action/courseschedule/addgrade')
async def action_grade_add(request):
    params = await request.post()
    stu_sn = params.get("stu_sn")
    cou_sn = params.get("cou_sn")
    grade = params.get("grade")
    class_schedule_id = params.get('course_schedule_id')

    if stu_sn is None or cou_sn is None or grade is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn, grade must be required")

    try:
        stu_sn = int(stu_sn)
        cou_sn = int(cou_sn)
        grade = float(grade)
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")

    try:
        with dblock() as db:
            db.execute("""
            INSERT INTO course_grade (stu_sn, cou_sn, grade) 
            VALUES ( %(stu_sn)s, %(cou_sn)s, %(grade)s)
            """, dict(stu_sn=stu_sn, cou_sn=cou_sn, grade=grade))
    except UniqueViolation:
        query = urlencode({
            "message": "已经添加该学生的课程成绩",
            "return": f"/courseschedule/studentlist/{class_schedule_id}"
        })
        return web.HTTPFound(location=f"/error?{query}")
    except ForeignKeyViolation as ex:
        return web.HTTPBadRequest(text=f"无此学生或课程: {ex}")

    return web.HTTPFound(location=f"/courseschedule/studentlist/{class_schedule_id}")
