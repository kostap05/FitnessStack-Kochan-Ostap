from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.database import Base, engine
from backend.auth import router as auth_router
from backend.routes.user import router as user_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
def home():
    return {"msg": "Welcome to FitnessTracker"}
