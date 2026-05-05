from fastapi import FastAPI
from app.models import ApplicationCreate, Application

app = FastAPI()

applications: list[Application] = []

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/applications")
def create_application(payload: ApplicationCreate) -> Application:
    new_id = len(applications) + 1
    new_app = Application(id=new_id, **payload.model_dump())
    applications.append(new_app)
    return new_app

