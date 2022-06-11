from .config import web_routes
from .jinjapage import jinjapage


@web_routes.get('/error')
async def dialog_error(request):
    message = request.query.get("message")
    return_path = request.query.get("return")

    return jinjapage(request, 'dialog_error.html',
                     message=message,
                     return_path=return_path)
