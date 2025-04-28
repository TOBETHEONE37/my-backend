from typing import Union
import uuid

from fastapi import FastAPI, HTTPException
from gtts import gTTS
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import os

from player import PlaybackManager

app = FastAPI()

# CORS 설정 (필수)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 본인의 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# 음성 파일 저장 위치
AUDIO_DIR = "audios"
os.makedirs(AUDIO_DIR, exist_ok=True)

# 음성 파일 직접 출력시 저장 위치
TEMP_DIR = "temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)


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


# 추가
class InputText(BaseModel):
    text: str

@app.post("/tts_direct")
def read_item(input: InputText):
    print(os.listdir(TEMP_DIR))
    # 임시 폴더 청소
    for file in os.listdir(TEMP_DIR):
        try:
            print(f"deleted successfully: {file}")
            os.remove(os.path.join('temp_audio', file))
        except:
            print(f"cannot delete: {file}")

    text = input.text

    if not text:
        raise HTTPException(status_code=400, detail="텍스트를 입력해주세요.")
    
    language = 'ko'
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join('temp_audio', filename)

    try:
        speech = gTTS(text=text, lang=language)
        speech.save(filepath)

        playbackManager = PlaybackManager()
        playbackManager.play_new_sound(filepath)

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    return { "message": "재생 성공" }


@app.get("/emergency/")
async def get_emergency():
    try:
        playbackManager = PlaybackManager()
        playbackManager.play_new_sound('audios/fire_alert.mp3')
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    return { "message": "재생 성공" }


@app.get("/stop/")
async def get_emergency():
    try:
        playbackManager = PlaybackManager()
        playbackManager.stop_current_sound()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    return { "message": "정지" }