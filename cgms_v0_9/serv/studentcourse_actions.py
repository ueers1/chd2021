from aiohttp import web
from urllib.parse import urlencode
from psycopg.errors import UniqueViolation, ForeignKeyViolation
from .config import web_routes
from .dblock import dblock

@web_routes.post('/action/studentcourse/add')
async def action_grade_add(request):
    params = await request.post()
    courseschedule = params.get("courseschedule")


    if courseschedule is None:
        return web.HTTPBadRequest(text="course schedule must be required")

    try:
        with dblock() as db:
            (student_sn, class_schedule_id) = courseschedule.split('_')
            db.execute("""
            INSERT INTO student_course (student_sn, class_schedule_id) 
            VALUES ( %(student_sn)s, %(class_schedule_id)s)
            """, dict(student_sn=student_sn, class_schedule_id=class_schedule_id))
    except UniqueViolation:
        query = urlencode({
            "message": "已经添加该选课",
            "return": f"/studentcourse/{student_sn}"
        })
        return web.HTTPFound(location=f"/error?{query}")
    except ForeignKeyViolation as ex:
        return web.HTTPBadRequest(text=f"无此课程安排: {ex}")

    return web.HTTPFound(location=f"/studentcourse/{student_sn}")


@web_routes.post('/action/grade/edit/{stu_sn}/{cou_sn}')
async def edit_grade_action(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")
    if stu_sn is None or cou_sn is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn, must be required")

    params = await request.post()
    grade = params.get("grade")

    try:
        stu_sn = int(stu_sn)
        cou_sn = int(cou_sn)
        grade = float(grade)
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")

    with dblock() as db:
        db.execute("""
        UPDATE course_grade SET grade=%(grade)s
        WHERE stu_sn = %(stu_sn)s AND cou_sn = %(cou_sn)s
        """, dict(stu_sn=stu_sn, cou_sn=cou_sn, grade=grade))

    return web.HTTPFound(location="/grade")


@web_routes.post('/action/grade/delete/{stu_sn}/{cou_sn}')
def delete_grade_action(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")
    if stu_sn is None or cou_sn is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn, must be required")

    with dblock() as db:
        db.execute("""
        DELETE FROM course_grade
            WHERE stu_sn = %(stu_sn)s AND cou_sn = %(cou_sn)s
        """, dict(stu_sn=stu_sn, cou_sn=cou_sn))

    return web.HTTPFound(location="/grade")
