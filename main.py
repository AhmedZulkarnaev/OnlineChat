from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.router_page import router as router_page
from api.router_socket import router as router_socket
import os

app = FastAPI()

static_dir = os.path.join(os.path.dirname(__file__), 'static')
app.mount('/static', StaticFiles(directory=static_dir), 'static')

app.include_router(router_socket)
app.include_router(router_page)
