import json
import logging
from datetime import timedelta, datetime
from time import time
from fastapi.requests import Request
from fastapi import Body
from fastapi.logger import logger
from dataclasses import dataclass

from typing import Dict
logger.setLevel(logging.INFO)

TIME_FORMATTER = "%Y/%m/%d %H:%M:%S"

async def api_logger(request: Request, response=None, error=None):

    t = time() - request.state.start
    status_code = error.status_code if error else response.status_code
    error_log = None
    if error:
        if request.state.inspect:
            frame = request.state.inspect
            error_file = frame.f_code.co_filename
            error_func = frame.f_code.co_name
            error_line = frame.f_lineno
        else:
            error_func = error_file = error_line = "UNKNOWN"
        error_log = dict(
            errorFunc=error_func,
            location="{} line in {}".format(str(error_line), error_file),
            raised=str(error.__class__.__name__),
            msg=str(error.ex),
        )
    log_dict = dict(
        url=request.url.hostname + request.url.path,
        method=str(request.method),
        statusCode=status_code,
        errorDetail=error_log,
        client=request.state.ip,
        processedTime=str(round(t * 1000, 5)) + "ms",
        datetimeKST=(datetime.utcnow() + timedelta(hours=9)).strftime(TIME_FORMATTER),
    )
    if error and error.status_code >= 500:
        logger.error(json.dumps(log_dict))
    else:
        logger.info(json.dumps(log_dict))

async def common_logger(msg:str, error=None):
    log_dict = dict(
        msg=msg,
        datetimeKST=(datetime.utcnow() + timedelta(hours=9)).strftime(TIME_FORMATTER),
    )

    if error and error.status_code >= 500:
        logger.error(json.dumps(log_dict))
    else:
        logger.info(json.dumps(log_dict))
