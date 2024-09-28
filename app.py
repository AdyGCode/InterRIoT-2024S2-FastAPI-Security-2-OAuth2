import os
from pathlib import Path
from datetime import timedelta, date, datetime
import dateutil

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import requests
from jose import jwt

app = FastAPI(title="FastAPI Templating")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
load_dotenv(".env")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/css", StaticFiles(directory="static/css"), name="css")
app.mount("/js", StaticFiles(directory="static/js"), name="js")

app.secret_key = os.environ.get("APP_SECRET")

# Constants
BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory="templates")
LOGGED_IN = "Logged in"

print(BASE_PATH)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return TEMPLATES.TemplateResponse(
        request=request, name="pages/home.html"
    )


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return TEMPLATES.TemplateResponse(
        request=request, name="pages/about.html"
    )


@app.route('/providers')
def providers(request: Request):
    # profile = session.get('profile')
    profile = {'name': 'ady'}

    providers = [
        {'name': 'Google', 'colour': 'red', 'bg': 'black',
         'logo': 'google', 'url': '/google/',
         'text': "connect", },
        {'name': 'Facebook', 'colour': 'sky', 'bg': 'black',
         'logo': 'facebook', 'url': '/facebook/',
         'text': "connect", },
        {'name': 'Twitter', 'colour': 'cyan', 'bg': 'black',
         'logo': 'twitter', 'url': '/twitter/',
         'text': "connect", },
        {'name': 'Github', 'colour': 'teal', 'bg': 'black',
         'logo': 'github', 'url': '/github/',
         'text': "connect", },
        {'name': 'Gitlab', 'colour': 'amber', 'bg': 'black',
         'logo': 'gitlab', 'url': '/gitlab/',
         'text': "connect", },
        {'name': 'Bitbucket', 'colour': 'indigo', 'bg': 'black',
         'logo': 'bitbucket', 'url': '/bitbucket/',
         'text': "connect", },
        {'name': 'Instagram', 'colour': 'pink', 'bg': 'black',
         'logo': 'instagram', 'url': '/instagram/',
         'text': "connect", },
        {'name': 'Wordpress', 'colour': 'green', 'bg': 'black',
         'logo': 'wordpress', 'url': '/wordpress/',
         'text': "connect", },
        {'name': 'Microsoft', 'colour': 'blue', 'bg': 'black',
         'logo': 'microsoft', 'url': '/microsoft/',
         'text': "connect", },
        {'name': 'Other', 'colour': 'zinc', 'bg': 'black',
         'logo': 'question', 'url': '/other/',
         'text': "connect", },
    ]

    return TEMPLATES.TemplateResponse(
        request=request,
        name="pages/providers.html",
        context={
            'user': profile,
            'providers': providers
        }
    )


@app.route('/colours')
def colours(request: Request):
    return TEMPLATES.TemplateResponse(request=request, name="pages/colours.html")

@app.route('/privacy')
def privacy(request: Request):
    return TEMPLATES.TemplateResponse(request=request, name="pages/privacy.html")

@app.route('/terms')
def terms(request: Request):
    return TEMPLATES.TemplateResponse(request=request, name="pages/terms.html")
