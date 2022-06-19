from aiohttp import web
from .config import web_routes
from .jinjapage import get_location, jinjapage
from .dblock import dblock


@web_routes.get("/courseschedule")
async def view_list_coursesschedule(request):
    with dblock() as db:
        db.execute("""
        SELECT t2.no, 
		t2.name as course_name,
		t1.clas_shift,
		t1.class_location,
		t1.class_date,
		t1.class_teacher
        FROM class_schedule t1
        join course t2
        on t1.course_sn = t2.sn
		order by t1.id;
        """)
        courseschedule = list(db)

        db.execute("""
        SELECT sn, no, name FROM course ORDER BY name
        """)
        courses = list(db)
        print(courses)

    return jinjapage('courseschedule_list.html',
                     location=get_location(request),
                     courseschedule=courseschedule,
                     courses = courses)