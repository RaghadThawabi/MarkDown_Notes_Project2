from fastapi import FastAPI
from app.api import auth,notes

app = FastAPI(title="Mark Down Notes API", description="Mark Down Notes API")
app.include_router(auth.router)
app.include_router(notes.router)
