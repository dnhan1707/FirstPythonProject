from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from app.exceptions import UserNotFound
import logging


logger = logging.getLogger(__name__)


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserNotFound)
    async def handler_user_not_found_exception(request: Request, exc: UserNotFound):
        # logger.warning("Logging: User not found")
        return JSONResponse(status_code=404, content=f"User {exc.user_id} does not exist")

    return None
