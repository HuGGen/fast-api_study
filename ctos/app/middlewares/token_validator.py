
import time
import re

import sqlalchemy.exc

from starlette.requests import Request
from starlette.responses import JSONResponse

from app.errors.exceptions import APIException, SqlFailureEx, APIQueryStringEx

from app.utils.date_utils import D
from starlette.middleware.base import RequestResponseEndpoint

from fastapi.responses import RedirectResponse

from app.utils.logger import api_logger

async def access_control(request: Request, call_next:RequestResponseEndpoint):
    request.state.req_time = D.datetime()
    request.state.start    = time.time()
    request.state.inspect  = None
    request.state.service  = None
    request.state.user     = None

    ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
    request.state.ip = ip.split(",")[0] if "," in ip else ip

    url = request.url.path
    try:
        """
        if url.startswith("/api"):
            if url.startswith("/api/services"):
            qs = str(request.query_params)
            qs_list = qs.split("&")
            try:
                qs_dict = {qs_split.split("=")[0]: qs_split.split("=")[1] for qs_split in qs_list}
            except Exception:
                raise APIQueryStringEx()
            qs_keys = qs_dict.keys()
            print(qs_keys)
        """
        response = await call_next(request)
        await api_logger(request=request, response=response)
        if response.status_code == 404:
            response = RedirectResponse(url='/docs')
        return response
    except Exception as e:
        error = await exception_handler(e)
        error_dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)
        response = JSONResponse(status_code=error.status_code, content=error_dict)
        await api_logger(request=request, response=response)
    return response


async def exception_handler(error: Exception):
    if isinstance(error, sqlalchemy.exc.OperationalError):
        error = SqlFailureEx(ex=error)
    if not isinstance(error, APIException):
        error = APIException(ex=error, detail=str(error))
    return error
