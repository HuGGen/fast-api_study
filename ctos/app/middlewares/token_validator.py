
import time
import re

import sqlalchemy.exc

from starlette.requests import Request
from starlette.responses import JSONResponse

from app.errors.exceptions import APIException, SqlFailureEx

from app.utils.date_utils import D
from starlette.middleware.base import RequestResponseEndpoint

async def access_control(request: Request, call_next:RequestResponseEndpoint):
    request.state.req_time = D.datetime()
    request.state.start    = time.time()
    request.state.inspect  = None
    request.state.service  = None
    request.state.user     = None

    ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
    request.state.ip = ip.split(",")[0] if "," in ip else ip

    try:
        response = await call_next(request)
        return response
    except Exception as e:
        error = await exception_handler(e)
        error_dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)
        response = JSONResponse(status_code=error.status_code, content=error_dict)
    return response


async def exception_handler(error: Exception):
    if isinstance(error, sqlalchemy.exc.OperationalError):
        error = SqlFailureEx(ex=error)
    if not isinstance(error, APIException):
        error = APIException(ex=error, detail=str(error))
    return error
