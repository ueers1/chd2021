from aiohttp import web
from .config import web_routes
from .jinjapage import get_location, jinjapage


@web_routes.get("/student")
async def view_student_list(request):
    return jinjapage('student_list.html', location=get_location(request))
