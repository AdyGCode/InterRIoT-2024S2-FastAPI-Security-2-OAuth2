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
app.mount("/img", StaticFiles(directory="static/img"), name="img")

app.secret_key = os.environ.get("APP_SECRET")

# Constants
BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory="templates")
LOGGED_IN = "Logged in"

print(BASE_PATH)


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return TEMPLATES.TemplateResponse(
        request=request, name="pages/about.html"
    )


@app.get('/colours')
def colours(request: Request):
    return TEMPLATES.TemplateResponse(request=request, name="pages/colours.html")


@app.get('/privacy')
def privacy(request: Request):
    return TEMPLATES.TemplateResponse(request=request, name="pages/privacy.html")


@app.get('/terms')
def terms(request: Request):
    return TEMPLATES.TemplateResponse(request=request, name="pages/terms.html")


@app.get('/providers')
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


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    statuses = []

    return TEMPLATES.TemplateResponse(
        request=request,
        name="pages/home.html",
        context={
            'user': [],
            'statuses': statuses
        }
    )

@app.get("/alerts", response_class=HTMLResponse)
async def alerts(request: Request):
    statuses = [
        {
            'name': 'DANGER', 'colour': 'zinc', 'bg': 'red',
            'logo': 'skull-crossbones', 'url': 'home',
            'heading': "Alert Type: Danger",
            'details': "It's dead Jim! Yep, we've had a major error!",
        },
        {
            'name': 'WARNING', 'colour': 'zinc', 'bg': 'amber',
            'logo': 'exclamation', 'url': 'home',
            'heading': "Alert Type: Warning",
            'details': "When something isn't quite broken, it's a warning.",
        },
        {
            'name': 'SUCCESS', 'colour': 'zinc', 'bg': 'green',
            'logo': 'check', 'url': 'home',
            'heading': "Alert Type: Success",
            'details': "The task completed successfully.",
        },
        {
            'name': 'QUESTION', 'colour': 'zinc', 'bg': 'teal',
            'logo': 'question', 'url': 'home',
            'heading': "Alert Type: Question",
            'details': "Want the user to answer a question, you may use this alert.",
        },
        {
            'name': 'INFO', 'colour': 'zinc', 'bg': 'sky',
            'logo': 'info', 'url': 'home',
            'heading': "Alert Type: Information",
            'details': "When you just want to tell the user something that is not an alert.",
        },
        {
            'name': 'PRIMARY', 'colour': 'zinc', 'bg': 'blue',
            'logo': 'thumbs-up', 'url': 'home',
            'heading': "Alert Type: Primary",
            'details': "A general primary alert message with details.",
        },
        {
            'name': 'DIRECTIVE', 'colour': 'zinc', 'bg': 'indigo',
            'logo': 'traffic-light', 'url': 'home',
            'heading': "Alert Type: Directive",
            'details': "When you need the user to do something, you could use this alert.",
        },
        {
            'name': 'SECONDARY', 'colour': 'zinc', 'bg': 'zinc',
            'logo': 'pencil', 'url': 'home',
            'heading': "Alert Type: Secondary",
            'details': "This is a general secondary alert and details.",
        },
    ]

    return TEMPLATES.TemplateResponse(
        request=request,
        name="pages/alerts.html",
        context={
            'user': [],
            'statuses': statuses
        }
    )


@app.get("/login/google")
async def login_google(request: Request):
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_CONF_URL = os.environ.get("GOOGLE_CONFIG_URL")
    GOOGLE_REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI')
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?"
               f"response_type=code&client_id={GOOGLE_CLIENT_ID}&"
               f"redirect_uri={GOOGLE_REDIRECT_URI}&"
               f"scope=openid%20profile%20email&access_type=offline"
    }

@app.get("/auth/google")
async def auth_google(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_CONF_URL = os.environ.get("GOOGLE_CONFIG_URL")
    GOOGLE_REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI')

    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                             headers={"Authorization": f"Bearer {access_token}"})
    return user_info.json()

@app.get("/token")
async def get_token(token: str = Depends(oauth2_scheme)):
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    return jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["HS256"])
