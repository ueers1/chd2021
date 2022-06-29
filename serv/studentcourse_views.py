from aiohttp import web
from .config import web_routes
from .jinjapage import get_location, jinjapage
from .dblock import dblock


@web_routes.get("/studentcourse/{student_sn}")
async def view_list_students(request):
    student_sn = request.match_info.get("student_sn")
    with dblock() as db:
        db.execute(f"""
        select t1.id,t2.name,t1.student_sn,t4.name as course_name,t4.semester, t4.credits,t4.hours, 
        t3.clas_shift, t3.class_location,t3.class_date,t3.class_teacher
        from student_course t1
        join student t2
        on t1.student_sn = t2.sn
        join class_schedule t3
        on t1.class_schedule_id = t3.id
        and t1.student_sn = {student_sn}
        join course t4 
        on t3.course_sn = t4.sn
        """)
        studentcourses = list(db)

        db.execute(f"""
        SELECT {student_sn} || '_' || t1.id as id, 
		t2.name as course_name,
		t1.clas_shift::varchar as clas_shift,
		t1.class_location,
		t1.class_date || '第' || t1.clas_shift::varchar || '节课' as class_date,
		t1.class_teacher
        FROM class_schedule t1
        join course t2
        on t1.course_sn = t2.sn
		order by t1.id;
        """)
        courseschedule = list(db)

    return jinjapage('studentcourse_list.html',
                     location=get_location(request),
                     studentcourses=studentcourses,
                     courseschedule=courseschedule,
                     student_sn=student_sn)