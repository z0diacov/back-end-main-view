#fastapi
from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect, Form, Cookie, Response, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
#typing
from typing import Annotated
from contextlib import asynccontextmanager
from database import mysql_client, redis_client
from rabbitmq import rabbitmq_client
#routers
from routers.authorization import router as auth_router
from routers.sessions import router as sessions_router
from routers.development import router as development_router
from routers.profile_and_settings import router as profile_and_settings_router
#logging
from loguru import logger
from security.config import LOGGER_CONFIG
#other
import httpx
from utils.ondelete_events.ondelete_event import expired_token_callback

logger.remove()

logger.add(sink=LOGGER_CONFIG['sink'], 
           rotation=LOGGER_CONFIG['rotation'], 
           retention=LOGGER_CONFIG['retention'], 
           level=LOGGER_CONFIG['level']
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await mysql_client.connect()
    await redis_client.connect()
    await rabbitmq_client.connect()

    redis_client.add_expire_listener("whitelist:", expired_token_callback)
    yield 
    await rabbitmq_client.disconnect()
    await mysql_client.disconnect()
    await redis_client.disconnect()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    client_ip = request.client.host
    url = request.url.path

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(f"Status: {response.status_code} | URL: {url} | IP: {client_ip} | Processing Time: {process_time:.4f}s")
    
    return response

@app.get("/")
async def root(request: Request):
    return RedirectResponse(url="/docs")

app.include_router(auth_router, tags=["Authorization"])
app.include_router(sessions_router, tags=["Sessions"])
app.include_router(profile_and_settings_router, tags=["Profile and settings"])
app.include_router(development_router, tags=["Development"])
