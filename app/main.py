from fastapi import FastAPI, HTTPException
from app.models import ApplicationCreate, Application, ApplicationUpdate

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

@app.get("/applications")
def list_applications()->list[Application]:
    return applications

@app.get("/applications/{app_id}")
def get_application(app_id: int)-> Application:
    for app in applications:
        if app.id == app_id:
            return app
    raise HTTPException(status_code=404, detail=f"Application {app_id} not found")

@app.patch("/applications/{app_id}")
def update_application(app_id:int, payload: ApplicationUpdate) -> Application:
    for i, app in enumerate(applications):
        if app.id == app_id:
            update_data = payload.model_dump(exclude_unset=True)
            updated = app.model_copy(update=update_data)
            applications[i] = updated
            return updated
    raise HTTPException(status_code=404, detail=f"Application {app_id} not found")

@app.delete("/applications/{app_id}", status_code=204)
def delete_application(app_id: int) -> None:
    for i, app in enumerate(applications):
        if app.id == app_id:
            applications.pop(i)
            return
    raise HTTPException(status_code=404, detail=f"application {app_id} not found")