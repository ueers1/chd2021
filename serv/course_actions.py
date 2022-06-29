from aiohttp import web
from urllib.parse import urlencode
from psycopg.errors import UniqueViolation, ForeignKeyViolation
from .config import web_routes
from .dblock import dblock
import traceback

@web_routes.post('/action/course/add')
async def action_course_add(request):
    params = await request.post()
    name = params.get("name")
    no = params.get("no")
    semester = params.get("semester")
    credits = params.get("credits")
    hours = params.get("hours")

    if (name is None or no is None or semester is None or
        credits is None or hours is None):
        return web.HTTPBadRequest(text="name, no, semester, credits, hours must be required")

    try:
        with dblock() as db:
            db.execute("""
            INSERT INTO course(no, name, semester, credits, hours) 
            VALUES ( %(no)s, %(name)s, %(semester)s, %(credits)s, %(hours)s)
            """, dict(no=no, name=name, semester=semester, credits=credits, hours=hours))
    except UniqueViolation:
        query = urlencode({
            "message": "已经添加该课程",
            "return": "/course"
        })
        return web.HTTPFound(location=f"/error?{query}")
    return web.HTTPFound(location="/course")


@web_routes.post('/action/student/edit/{stu_sn}/{cou_sn}')
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


@web_routes.post('/action/student/delete/{stu_sn}/{cou_sn}')
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
