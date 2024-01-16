from fastapi import FastAPI
from app.routes.user import create_user_routers
from app.exceptionhandler import add_exception_handlers


def create_application() -> FastAPI:
    user_contents, profile_infos = create_user_contents_profile_info()
    user_routers = create_user_routers(user_contents, profile_infos)
    app = FastAPI()
    app.include_router(user_routers)

    add_exception_handlers(app)

    return app


def create_user_contents_profile_info():
    user_contents = {
        0: {
            "name": "default user",  # used to be "username": "tests user"
            "liked_post": [1, 2, 3]
        },
    }

    profile_infos = {
        0: {
            "description": "default description",
            "long_bio": "default long bio"
        },
    }

    return user_contents, profile_infos


app = create_application()
