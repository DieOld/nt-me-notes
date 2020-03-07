from routes import routes
from aiohttp.web import run_app, Application
import middlewares


def create_app():
    app = Application(middlewares=middlewares.middleware_list)
    app.add_routes(routes)
    return app


if __name__ == '__main__':
    run_app(create_app())
