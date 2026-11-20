from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import router as legacy_endpoints_router
from app.api.clients import router as clients_router
from app.api.projects import router as projects_router
from app.api.documents import router as documents_router
from app.api.clauses import router as clauses_router
from app.api.studio import router as studio_router
from app.db.session import engine
from app.models.base import Base

# Buat tabel SQLite jika belum ada
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Arsi-TeX API: Otomasi Dokumen Arsitektur & Interior dengan Mesin PDF Typst"
)

# CORS middleware untuk koneksi lancar ke frontend Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(legacy_endpoints_router, prefix=settings.API_V1_STR)
app.include_router(clients_router, prefix=settings.API_V1_STR)
app.include_router(projects_router, prefix=settings.API_V1_STR)
app.include_router(documents_router, prefix=settings.API_V1_STR)
app.include_router(clauses_router, prefix=settings.API_V1_STR)
app.include_router(studio_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "app": "Arsi-TeX API",
        "status": "online",
        "engine": "Typst PDF Compiler",
        "docs": "/docs"
    }
