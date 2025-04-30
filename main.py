from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
import os
import uuid
import logging

from manager.PresetManager import PresetManager
from manager.VoicePlaybackManager import VoicePlaybackManager

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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
    preset_manager = PresetManager()
    preset = preset_manager.addPreset(text, audio_url, filepath)
    return preset

# 생성된 오디오 파일 제공 엔드포인트
from fastapi.responses import FileResponse

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    filepath = os.path.join(AUDIO_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")
    return FileResponse(filepath, media_type="audio/mpeg")

@app.get("/emergency/")
async def get_emergency():
    voice_playback_manager = VoicePlaybackManager()
    voice_playback_manager.stop_current_sound()
    voice_playback_manager.play_new_sound("./audios/emergency.mp3")
    return {"message": "Success"}


@app.get("/preset/")
async def get_preset_list():
    preset_manager = PresetManager()
    return preset_manager.presetList

@app.delete("/preset/")
async def delete_preset(id: int = Query(...)):
    preset_manager = PresetManager()
    preset = preset_manager.removePreset(id)

    res = {"message": "Preset Delete Success"}

    if preset is None:
        raise HTTPException(status_code=404, detail=f"Preset Not Found")

    # audio_url에서 파일명만 추출
    filename = os.path.basename(preset.audioUrl)
    filepath = os.path.join(AUDIO_DIR, filename)

    # 파일 존재 여부 확인 및 삭제
    if not os.path.exists(filepath):
        return res

    try:
        os.remove(filepath)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 삭제 중 오류 발생: {str(e)}")

    return res

# 방송
@app.post("/broadcasts/")
async def broadcasts(data: dict):
    # 방송할 특정 지역 및 구역들 Id
    zone_ids = data.get("zoneIds")
    # 방송에 담을 preset
    preset = data.get("preset")
    logging.info(preset)
    # 조건 1: zone_ids가 없다면 전체 방송
    # 조건 2: preset이 없다면 마이크 방송
    voice_playback_manager = VoicePlaybackManager()
    voice_playback_manager.play_new_sound(preset.get("filePath"))
    logging.info(zone_ids)
    logging.info(preset)

    return {"message": "Broadcasts start"}

# 방송 취소
@app.post("/broadcasts/stop/")
async def broadcasts(data: dict):
    # 방송할 특정 지역 및 구역들 Id
    zone_ids = data.get("zoneIds")

    voice_playback_manager = VoicePlaybackManager()
    voice_playback_manager.stop_current_sound()
    # 조건 1: zone_ids가 없다면 전체 방송 종료?
    logging.info(zone_ids)

    return {"message": "Broadcasts stop"}
