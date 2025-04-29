import uuid
from pathlib import Path
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import openai
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
    text=data.get('text')
    filename = f"{uuid.uuid4()}.mp3"
    speech_file_path = Path(__file__).parent / AUDIO_DIR / filename
    with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
        instructions="당신은 정보를 전달하는 뉴스의 아나운서입니다. 공식적인 말투를 쓰길 바래요.",
        ) as response:
        response.stream_to_file(speech_file_path)

    return {"audio_url": speech_file_path}

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
    
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join('temp_audio', filename)

    try:    
        speech_file_path = Path(__file__).parent / TEMP_DIR / filename
        with openai.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text,
            instructions="당신은 정보를 전달하는 뉴스의 아나운서입니다. 공식적인 말투를 쓰길 바래요.",
            ) as response:
            response.stream_to_file(speech_file_path)

            playbackManager = PlaybackManager()
            playbackManager.play_new_sound(filepath)

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    return { "message": "재생 성공" }


@app.get("/emergency/")
async def get_emergency():
    try:
        playbackManager = PlaybackManager()
        playbackManager.play_new_sound('preset/fire_alert.mp3')
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