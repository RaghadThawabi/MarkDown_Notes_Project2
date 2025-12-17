from fastapi import FastAPI
from app.api import auth

app = FastAPI()
app.include_router(auth.router)
if __name__ == '__main__':
    print("vfd")