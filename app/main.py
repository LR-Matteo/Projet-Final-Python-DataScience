from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from app.routers import search, sports

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="WindSpot",
    description="Trouvez le meilleur spot nautique selon la météo",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "frontend" / "static"), name="static")

app.include_router(search.router, prefix="/api")
app.include_router(sports.router, prefix="/api")

from fastapi import Request
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory=BASE_DIR / "frontend" / "templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "ok", "service": "WindSpot"}
