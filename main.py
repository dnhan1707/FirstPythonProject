from fastapi import FastAPI
from app.routes.user import create_user_routers
from app.exceptionhandler import add_exception_handlers


def create_application() -> FastAPI:
    user_routers = create_user_routers()
    app = FastAPI()
    app.include_router(user_routers)

    add_exception_handlers(app)

    return app


app = create_application()
