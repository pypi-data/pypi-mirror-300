from fastapi import FastAPI
app = FastAPI()

from .main import Server  # noqa: F401, E402
