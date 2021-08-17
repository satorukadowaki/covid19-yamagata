#!/usr/bin/env python

import uvicorn
import logging
import ujson
import time
import traceback
import sys
import asyncio

from typing import Set, List, Optional
from typing import Callable
from fastapi import FastAPI, Header, Query, Depends, HTTPException
from fastapi import Security
from fastapi.exceptions import RequestValidationError
from fastapi.security.api_key import APIKeyHeader, APIKey
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles

from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.datastructures import CommaSeparatedStrings
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import Response
from starlette.responses import JSONResponse

# from fastapi.encoders import jsonable_encoder

from enum import Enum
from pydantic import BaseModel, Field

from settings import LOG_FORMAT
from settings import SERVER_PORT
from settings import ENV_NAME
from settings import RELEASE_VERSION

from model import modelResponsePing
from model import modelResponseProperties

# from settings import STATIC_FILE_DIRECTORY


log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = LOG_FORMAT
log_config["formatters"]["default"]["fmt"] = LOG_FORMAT
logging.basicConfig(format=LOG_FORMAT, datefmt="%Y-%m-%dT%H:%M:%S%z", level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    docs_url=f"/toybox/covid19-yamagata/api/docs",
    openapi_url=f"/toybox/covid19-yamagata/api/docs/openapi.json",
    redoc_url="/toybox/covid19-yamagata/api/docs/redoc",
    title="[Fastapi Example] API",
    version=RELEASE_VERSION,
)

# -- CORS initialize  {{{
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware)
# }}}


# -- Access Log用のカスタムルータ
# class LoggingContextRoute(APIRoute):
#     def get_route_handler(self) -> Callable:
#         original_route_handler = super().get_route_handler()
#
#         async def custom_route_handler(request: Request) -> Response:
#             """
#             時間計測
#             """
#             before = time.time()
#             response: Response = await original_route_handler(request)
#             duration = round(time.time() - before, 4)
#
#             record = {}
#
#             if await request.body():
#                 request_body = (await request.body()).decode("utf-8")
#                 logger.info("Request Body: " + request_body)
#
#             # logger.info('Remote Address: ' + request.client.host)
#             # logger.info('X-Forwarded-For: ' + request.headers.get('X-Forwarded-For'))
#             # logger.info('X-Real-IP: ' + request.headers.get('X-Real-IP'))
#             logger.info("Duration: " + str(duration))
#             return response
#
#         return custom_route_handler
#
#
# app.router.route_class = LoggingContextRoute


# -- Custom Exception  {{{
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    res = {"isSuccess": False, "message": str(exc.detail)}
    try:
        if type(exc.headers) == dict:
            res.update(exc.headers)
    except:
        pass

    return JSONResponse(content=res, status_code=exc.status_code)


# -- リクエストパラメータのバリデーションエラー(カスタム)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    res = {"isSuccess": False, "message": str(exc).replace("\n", " ")}
    return JSONResponse(content=res, status_code=400)


# @app.on_event("startup")
# async def startup_check():
#     try:
#         logger.info("Initial Data Check Completed")
#     except:
#         logger.error(traceback.format_exc())
#         logger.error("Unable to Create Schedule Object")
#

# -- Count
@app.get(
    f"/toybox/covid19-yamagata/",
    tags=["dashborad"],
    summary="",
    response_description="",
)
async def getCount(  # {{{
    response: Response,
    # islocalonly: bool = Query(False, description="地方局のみを取得したい場合に true を指定 [Default] false"),
    limit: int = Query(15, description="レスポンスに含める件数を指定する [Default] 15"),
    # is4k8k: bool = Query(False, description="4K8K番組のみを取得したい場合に指定する [Default] False")
):

    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"


# -- properties 用
@app.get(
    "/api/v1/properties.json",
    tags=["Properties"],
    summary="プロパティ出力用",
    response_model=modelResponseProperties,
    response_description="",
)
async def getProperties(request: Request):
    # remote_pdb.set_trace(host='0.0.0.0', port=8010)
    logger.info(f"GET: {request.url.path}")
    try:
        res = {"isSuccess": True, "environment": ENV_NAME.lower(), "version": RELEASE_VERSION}
    except:
        err_args = {
            "isSuccess": False,
        }
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500, detail="[Error] Internal Server Error", headers=err_args
        )

    return res


# -- healthcheck 用
@app.get(
    "/api/v1/ping",
    tags=["healthcheck"],
    summary="ヘルスチェック用",
    response_model=modelResponsePing,
    response_description="",
)
async def pingPong(request: Request):
    # remote_pdb.set_trace(host='0.0.0.0', port=8010)
    logger.info(f"GET: {request.url.path}")
    res = {"isSuccess": True, "message": "Pong"}

    return res


# -- リクエスト毎に呼ばれるミドルウェアにdbセッションとヘッダーを入れておく
@app.middleware("http")
async def req_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response


# -- Static File Serving （パス設計を同じにするときは最後に書く)
# app.mount(
#     "/toybox/covid19-yamagata",
#     StaticFiles(directory=STATIC_FILE_DIRECTORY, html=True),
#     name="static",
# )


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(SERVER_PORT),
        log_config=log_config,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
