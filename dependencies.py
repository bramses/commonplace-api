from typing import Annotated
import httpx
from fastapi import Header, HTTPException
from datetime import datetime
from fastapi.templating import Jinja2Templates



def get_host():
    return "http://127.0.0.1:8000"

async def get_token_header(x_token: Annotated[str, Header(...)]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")

client = httpx.AsyncClient()

def get_client():
    return client


def get_now():
    return datetime.now()

def humanize_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_templates():
    return Jinja2Templates(directory="templates")
