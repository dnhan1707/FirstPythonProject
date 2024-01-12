from fastapi import FastAPI
from app.routes.user import create_user_routers


def create_application() -> FastAPI:
    user_routers = create_user_routers()
    app = FastAPI()
    app.include_router(user_routers)
    return app


app = create_application()
