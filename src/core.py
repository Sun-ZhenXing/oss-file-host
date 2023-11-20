from sanic import Blueprint, Request, Sanic
from sanic.handlers import ErrorHandler

from src.services.oss import sanic_send_oss_file
from src.utils.oss import OSS
from src.utils.result import Result

bp = Blueprint("core", url_prefix="/")
oss = OSS.from_env()


@bp.route("/<path:path>")
async def index(request: Request, path: str):
    if not path:
        return Result.not_found()
    elif path.endswith("/"):
        return Result.fail("Invalid path", 400)
    return await sanic_send_oss_file(oss, path)


class CustomErrorHandler(ErrorHandler):
    def default(self, request: Request, exception: Exception):
        """handles errors that have no error handlers assigned"""
        status_code = getattr(exception, "status_code", 500)
        return Result.fail(
            msg="Internal Server Error",
            code=-1,
            http_code=status_code,
        )


def init_app(app: Sanic):
    app.blueprint(bp)
