from aiohttp import web
from urllib.parse import urlencode
from psycopg.errors import UniqueViolation, ForeignKeyViolation
from .config import web_routes
from .dblock import dblock
import traceback

@web_routes.post('/action/student/add')
async def action_student_add(request):
    params = await request.post()
    name = params.get("name")
    no = params.get("no")
    gender = params.get("gender")
    enrolled = params.get("enrolled")
    college = params.get("college")
    grade = params.get("grade")
    classname = params.get("class")

    if (name is None or no is None or gender is None or
        enrolled is None or college is None or classname is None):
        return web.HTTPBadRequest(text="name, no, gender, enrolled, college, grade, class must be required")

    try:
        with dblock() as db:
            db.execute("""
            INSERT INTO student (no, name, gender, enrolled, college, grade, class) 
            VALUES ( %(no)s, %(name)s, %(gender)s, %(enrolled)s, %(college)s, %(grade)s, %(classname)s)
            """, dict(no=no, name=name, gender=gender, enrolled=enrolled, college=college, grade=grade, classname=classname))
    except UniqueViolation:
        query = urlencode({
            "message": "已经添加该学生",
            "return": "/student"
        })
        return web.HTTPFound(location=f"/error?{query}")
    return web.HTTPFound(location="/student")


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
