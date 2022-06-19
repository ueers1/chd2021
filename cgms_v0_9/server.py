from aiohttp import web


from serv.config import web_routes, home_path
import serv.dblock
import serv.error_views
import serv.main_views
import serv.grade_views
import serv.student_views
import serv.student_actions
import serv.grade_actions
import serv.course_views
import serv.course_actions
import serv.courseschedule_views
import serv.courseschedule_actions
import serv.studentcourse_views
import serv.studentcourse_actions


app = web.Application()
app.add_routes(web_routes)
app.add_routes([web.static("/", home_path / "static")])
serv.dblock.setup(app, dsn="host=localhost dbname=examdb user=examdb password=123456")

if __name__ == "__main__":
    web.run_app(app, port=8080)
