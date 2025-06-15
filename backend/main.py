from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from backend.database import Base, engine
from backend.auth import router as auth_router
from backend.routes.user import router as user_router
from backend.routes import workout, own_programs
from backend.routes.external_api import create_external_api_router

# Инициализация приложения
app = FastAPI()

# Подключение CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

templates = Jinja2Templates(directory="frontend/templates")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(workout.router)
app.include_router(own_programs.router)

create_external_api_router(app)


@app.get("/index")
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/profile-page")
async def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/workouts")
async def workouts_page(request: Request):
    return templates.TemplateResponse("workouts.html", {"request": request})
