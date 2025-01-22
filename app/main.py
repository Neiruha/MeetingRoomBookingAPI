from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import bookings
from app import availability


app = FastAPI(title="Meeting Room Booking API", debug=True)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(bookings.router, prefix="/api/v1", tags=["bookings"])
app.include_router(availability.router, prefix="/api/v1", tags=["availability"])

@app.get("/")
async def root():
    return {"message": "Meeting Room Booking API"} 