from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🚩 CORS 허용 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://my-react-app-virid-pi.vercel.app"],  # 🚩 프론트엔드 URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "안녕하세요, Railway 백엔드입니다!"}
