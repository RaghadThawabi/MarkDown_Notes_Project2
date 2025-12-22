from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine
from app.api import auth, notes, grammar_routes, render
from app.core.config import settings
from app.models.user import Base

app = FastAPI(title="Mark Down Notes API", description="Mark Down Notes API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    """Create database tables on startup"""
    try:
        engine = create_async_engine(settings.DATABASE_URL, echo=True)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await engine.dispose()
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        raise

app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(grammar_routes.router)
app.include_router(render.router)


@app.get("/")
async def root():
    """Root endpoint to check API status"""
    return {
        "message": "Mark Down Notes API is running",
        "status": "OK",
        "docs": "/docs"
    }
