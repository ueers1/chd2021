from aiohttp import web
from .config import web_routes


@web_routes.get("/")
async def home_page(request):
    return web.HTTPFound(location="/grade")

