from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
import os
import uuid

app = FastAPI()

# CORS 설정 (필수)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://my-react-app-virid-pi.vercel.app"],  # 본인의 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 음성 파일 저장 위치
AUDIO_DIR = "audios"
os.makedirs(AUDIO_DIR, exist_ok=True)

@app.post("/tts/")
async def text_to_speech(data: dict):
    text = data.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="텍스트를 입력해주세요.")
    
    # 파일명 생성
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)

    # TTS 음성 생성
    tts = gTTS(text=text, lang='ko')
    tts.save(filepath)

    # 음성 파일 URL 반환 (Railway가 정적 파일 지원을 하지 않으므로 실제 서비스는 클라우드 저장소를 사용해야 함)
    audio_url = f"/audio/{filename}"

    return {"audio_url": audio_url}

# 생성된 오디오 파일 제공 엔드포인트
from fastapi.responses import FileResponse

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    filepath = os.path.join(AUDIO_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")
    return FileResponse(filepath, media_type="audio/mpeg")

@app.get("/emergency")
async def get_emergency():
    return 0
