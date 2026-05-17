"""Point d'entrée de l'application FastAPI."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.session import init_db
from app.api import routes_blocks, routes_projects, routes_export, websocket_graph


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialisation au démarrage / nettoyage à l'arrêt."""
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="API d'OrgaLego - simulateur de structures organisationnelles",
    lifespan=lifespan,
)

# CORS pour permettre au frontend de communiquer
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["health"])
def root() -> dict:
    """Health check basique."""
    return {
        "app": settings.app_name,
        "version": settings.version,
        "status": "ok",
    }


# Routes HTTP
app.include_router(routes_blocks.router)
app.include_router(routes_projects.router)
app.include_router(routes_export.router)

# WebSocket
app.include_router(websocket_graph.router)
