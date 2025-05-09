
from fastapi import FastAPI
from routes import energy
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(energy.router, prefix="/energy", tags=["Energy"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
