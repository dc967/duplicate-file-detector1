from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import auth, scan, files, settings as settings_router
from app.core.database import connect_db, close_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    await connect_db()
    yield

    await close_db()

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
    description="Duplicate File Detector API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(auth.router)
app.include_router(scan.router)
app.include_router(files.router)
app.include_router(settings_router.router)



@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )