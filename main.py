# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "안녕하세요! Railway에 배포된 FastAPI 서버입니다."}
