from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import models
from app.seed import seed_database
from app.routes import destinations, trips, ai, auth, wishlist, expenses

# Ensure database tables are created & seeded
models.Base.metadata.create_all(bind=engine)
try:
    seed_database()
except Exception as e:
    print("Seed error:", e)

app = FastAPI(title="TravelVerse API", version="2.0.0")

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(destinations.router, prefix="/api/destinations", tags=["destinations"])
app.include_router(trips.router, prefix="/api/trips", tags=["trips"])
app.include_router(wishlist.router, prefix="/api/wishlist", tags=["wishlist"])
app.include_router(expenses.router, prefix="/api/expenses", tags=["expenses"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])

@app.get("/")
def read_root():
    return {
        "message": "Welcome to TravelVerse High-Level API",
        "status": "online",
        "version": "2.0.0",
        "docs": "/docs"
    }

@app.get("/health")
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "TravelVerse Backend API"}

@app.get("/v1/models")
def list_models():
    return {"data": [{"id": "travelverse-ai-v2", "object": "model"}]}

@app.get("/api/categories")
def get_categories():
    return {"categories": ["Beaches", "Cities", "Culture", "Mountains", "Luxury", "Nature", "Romantic", "Adventure"]}

@app.get("/api/metrics")
def get_metrics():
    return {"status": "ok", "uptime": "100%", "active_destinations": 160}



