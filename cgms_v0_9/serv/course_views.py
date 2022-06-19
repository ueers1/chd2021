from aiohttp import web
from .config import web_routes
from .jinjapage import get_location, jinjapage
from .dblock import dblock


@web_routes.get("/course")
async def view_list_courses(request):
    with dblock() as db:
        db.execute("""
        SELECT no AS no, name as cou_name,
        semester,credits, hours as cou_hours
        FROM course ORDER BY name
        """)
        courses = list(db)

    return jinjapage('course_list.html',
                     location=get_location(request),
                     courses=courses)