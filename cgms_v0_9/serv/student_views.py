from aiohttp import web
from .config import web_routes
from .jinjapage import get_location, jinjapage
from .dblock import dblock


@web_routes.get("/student")
async def view_list_students(request):
    with dblock() as db:
        db.execute("""
        SELECT sn, no, name, gender, enrolled, 
        college, grade, class as classname
        FROM student ORDER BY name
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

    return jinjapage('student_list.html',
                     location=get_location(request),
                     students=students,
                     courses=courses,
                     items=items)