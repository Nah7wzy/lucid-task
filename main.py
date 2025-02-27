from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import auth_controller, post_controller
from models.database import engine, Base

app = FastAPI(title="MyApp API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_controller.router, prefix="/auth", tags=["auth"])
app.include_router(post_controller.router, prefix="/posts", tags=["posts"])

@app.get("/")
async def root():
    """Root endpoint for health check"""
    return {"message": "Welcome to MyApp API"}