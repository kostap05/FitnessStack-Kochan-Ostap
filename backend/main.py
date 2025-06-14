from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.auth import router as auth_router
from backend.routes.user import router as user_router
from backend.routes import workout, own_programs
from backend.routes.external_api import create_external_api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000 "],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")



app.include_router(auth_router)
app.include_router(user_router)
app.include_router(workout.router)
app.include_router(own_programs.router)

create_external_api_router(app)

@app.get("/")
def home():
    return {"msg": "Welcome to FitnessTracker"}
