from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import auth,notes,grammar_routes,render


app = FastAPI(title="Mark Down Notes API", description="Mark Down Notes API")
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(grammar_routes.router)
app.include_router(render.router)
