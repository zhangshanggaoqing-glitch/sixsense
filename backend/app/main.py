from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database import init_db
from backend.app.routers import exams, audio, vocab, progress, dict as dict_router, auth, admin

app = FastAPI(
    title="SixSense API",
    description="Minimalist CET-6 Intensive Listening Workstation Backend",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(exams.router)
app.include_router(audio.router)
app.include_router(vocab.router)
app.include_router(progress.router)
app.include_router(dict_router.router)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "SixSense Backend"}
