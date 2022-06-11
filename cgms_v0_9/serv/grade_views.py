from aiohttp import web
from .config import web_routes
from .jinjapage import jinjapage, get_location
from .dblock import dblock


@web_routes.get("/grade")
async def view_list_grades(request):
    with dblock() as db:
        db.execute("""
        SELECT sn AS stu_sn, name as stu_name FROM student ORDER BY name
        """)
        students = list(db)

        db.execute("""
        SELECT sn AS cou_sn, name as cou_name FROM course ORDER BY name
        """)
        courses = list(db)

        db.execute("""
        SELECT g.stu_sn, g.cou_sn, 
            s.name as stu_name, 
            c.name as cou_name, 
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.stu_sn = s.sn
            INNER JOIN course as c  ON g.cou_sn = c.sn
        ORDER BY stu_sn, cou_sn;
        """)

        items = list(db)

    return jinjapage('grade_list.html',
                     location=get_location(request),
                     students=students,
                     courses=courses,
                     items=items)


@web_routes.get('/grade/edit/{stu_sn}/{cou_sn}')
def view_grade_editor(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")
    if stu_sn is None or cou_sn is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn, must be required")

    with dblock() as db:
        db.execute("""
        SELECT grade FROM course_grade
            WHERE stu_sn = %(stu_sn)s AND cou_sn = %(cou_sn)s;
        """, dict(stu_sn=stu_sn, cou_sn=cou_sn))

        record = db.fetchone()

    if record is None:
        return web.HTTPNotFound(text=f"no such grade: stu_sn={stu_sn}, cou_sn={cou_sn}")

    return jinjapage("grade_edit.html",
                     location=get_location(request),
                     stu_sn=stu_sn,
                     cou_sn=cou_sn,
                     grade=record.grade)


@web_routes.get("/grade/delete/{stu_sn}/{cou_sn}")
def grade_deletion_dialog(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")
    if stu_sn is None or cou_sn is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn, must be required")

    with dblock() as db:
        db.execute("""
        SELECT g.stu_sn, g.cou_sn,
            s.name as stu_name, 
            c.name as cou_name, 
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.stu_sn = s.sn
            INNER JOIN course as c  ON g.cou_sn = c.sn
        WHERE stu_sn = %(stu_sn)s AND cou_sn = %(cou_sn)s;
        """, dict(stu_sn=stu_sn, cou_sn=cou_sn))

        record = db.fetchone()

    if record is None:
        return web.HTTPNotFound(text=f"no such grade: stu_sn={stu_sn}, cou_sn={cou_sn}")

    return jinjapage('grade_dialog_deletion.html',
                     location=get_location(request), record=record)
