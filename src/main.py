from routes import routes
from aiohttp.web import run_app, Application
from aiohttp_swagger import setup_swagger
import middlewares
import aiohttp_cors


def create_app():
    app = Application(middlewares=middlewares.middleware_list)
    app.add_routes(routes)
    setup_swagger(
        app,
        title='NOTES API',
        ui_version=3
    )
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    for route in list(app.router.routes()):
        cors.add(route)
    return app


if __name__ == '__main__':
    run_app(create_app())
