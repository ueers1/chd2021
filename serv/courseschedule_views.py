from aiohttp import web
from .config import web_routes
from .jinjapage import get_location, jinjapage
from .dblock import dblock


@web_routes.get("/courseschedule")
async def view_list_coursesschedule(request):
    with dblock() as db:
        db.execute("""
        SELECT 
        t1.id,
        t2.no, 
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

@web_routes.get("/courseschedule/studentlist/{coursescheduleid}")
async def view_student_list_grades(request):
    coursescheduleid = request.match_info.get("coursescheduleid")
    with dblock() as db:
        db.execute(f"""
        -- 选一门课的所有学生
        select 
        t2.name as student_name,
        t2.no as student_no,
        t2.college,
        t2.grade as college_grade,
        t3.class_teacher,
        t3.class_date,
        t3.class_location,
        t4.no as course_no,
        t4.name,
        t4.credits,
        t5.grade
        from student_course t1
        join student t2 
        on t1.student_sn = t2.sn
        and t1.class_schedule_id = {coursescheduleid}
        join class_schedule t3
        on t1.class_schedule_id = t3.id
        join course t4
        on t3.course_sn = t4.sn
        join course_grade t5
        on t3.course_sn = t5.cou_sn
        and t2.sn = t5.stu_sn
        """)
        items = list(db)

        # 获取选这门课但是没有成绩的学生
        db.execute(f"""
        select 
        t2.name as stu_name,
        t2.no as stu_no,
        t2.sn as stu_sn
        from student_course t1
        join student t2 
        on t1.student_sn = t2.sn
        and t1.class_schedule_id = {coursescheduleid}
        join class_schedule t3
        on t1.class_schedule_id = t3.id
        join course t4
        on t3.course_sn = t4.sn
        left join course_grade t5
        on t3.course_sn = t5.cou_sn
        and t2.sn = t5.stu_sn
        where t5.cou_sn is null
        """)
        students = list(db)

        db.execute(f"""
        SELECT sn AS cou_sn, name as cou_name,
        t2.class_teacher,
        t2.id
        FROM course t1
        join class_schedule t2
        on t1.sn = t2.course_sn
        and t2.id = {coursescheduleid}
        ORDER BY name
        """)
        courses = list(db)
        
        # 获取课程信息
        db.execute(f"""
        select 
        t2.name as stu_name,
        t2.no as stu_no,
        t2.sn as stu_sn
        from student_course t1
        join student t2 
        on t1.student_sn = t2.sn
        and t1.class_schedule_id = {coursescheduleid}
        join class_schedule t3
        on t1.class_schedule_id = t3.id
        join course t4
        on t3.course_sn = t4.sn
        left join course_grade t5
        on t3.course_sn = t5.cou_sn
        and t2.sn = t5.stu_sn
        where t5.cou_sn is null
        """)
        students = list(db)


    return jinjapage('student_grade_list.html',
                     location=get_location(request),
                     items=items,
                     students=students,
                     courses=courses)