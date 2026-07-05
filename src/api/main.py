from fastapi import FastAPI
from src.api.routes import recommend, feedback, health

app = FastAPI(
    title="Smart Mental Health Recommendation API",
    version="1.0"
)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Stress Monitoring Recommendation API Running",
        "docs": "http://127.0.0.1:8000/docs"
    }

# Include route modules
app.include_router(recommend.router)
app.include_router(feedback.router)
app.include_router(health.router)