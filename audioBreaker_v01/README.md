### Audio Breaking Test

|endpoint|method|input type|note|
|---|---|---|---|
|/tts|POST|{"text": string}|gTTS 를 이용해 텍스트를 입력받아 uuid로 저장합니다.|
|/audio/{filename}|GET||filename 에 해당하는 오디오 파일을 다운받습니다.|
|/tts_direct|POST|{"text": string}|gTTS 를 이용해 텍스트를 입력받아 재생합니다. temp_audio폴더에 저장합니다. 시작시 temp_audio폴더를 비웁니다.|
|/emergency|GET||미리 지정해 둔 화재경보 메시지를 출력합니다. 이미 재생중이더라도 끊고 메시지를 출력합니다.|
|/stop|GET||메시지를 정지합니다.|

### 설명
1. 메시지 재생을 테스트 합니다.   
라이브러리 just_playback을 사용하였습니다.
window 환경에서 테스트 하였으므로, RaspberyPi에서 돌아가는지 테스트 하여야 합니다.

2. 메시지 재생 중에 정지가 되는지 테스트 합니다.   
just_playback 라이브러리는 재생중 정지 메서드 기능이 있습니다.
따라서 playback인스턴스를 싱글턴으로 구현하여 정지 메서드를 실행시키고
재생하도록 하면 재생 중 정지가 가능합니다.
