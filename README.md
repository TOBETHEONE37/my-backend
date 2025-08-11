# TTS-Back

TTS (Text-to-Speech) Backend Service - FastAPI 기반 음성 변환 서비스

## 프로젝트 소개

TTS-Back은 한국어 텍스트를 음성으로 변환하는 백엔드 서비스입니다. Google Text-to-Speech API를 활용하여 고품질의 음성 변환 기능을 제공합니다.

## 주요 기능

- 📝 **텍스트 음성 변환**: 한국어 텍스트를 자연스러운 음성으로 변환
- 🎙️ **음성 방송**: 실시간 음성 방송 기능
- 💾 **프리셋 관리**: 자주 사용하는 음성 메시지 저장 및 관리
- 🚨 **비상 방송**: 긴급 상황용 비상 방송 기능
- 🎵 **음성 재생 제어**: 음성 재생 시작, 정지, 상태 확인

## 기술 스택

- **Backend Framework**: FastAPI
- **TTS Engine**: Google Text-to-Speech (gTTS)
- **Audio Processing**: just-playback
- **HTTP Client**: HTTPx
- **Environment**: Python 3.8+

## API 엔드포인트

### 📝 텍스트 음성 변환

- `POST /tts/` - 텍스트를 음성으로 변환하고 프리셋으로 저장

### 🎵 음성 파일 제공

- `GET /audio/{filename}` - 생성된 음성 파일 제공

### 💾 프리셋 관리

- `GET /preset/` - 저장된 프리셋 목록 조회
- `DELETE /preset/?id={preset_id}` - 프리셋 삭제

### 🎙️ 방송 기능

- `POST /broadcasts/` - 음성 방송 시작
- `POST /broadcasts/stop/` - 음성 방송 정지
- `GET /broadcasts/health-check` - 방송 시스템 상태 확인

### 🚨 비상 방송

- `GET /emergency/` - 비상 방송 실행

## 설치 및 실행

### 1. 프로젝트 클론

\`\`\`bash
git clone https://github.com/your-username/tts-back.git
cd tts-back
\`\`\`

### 2. 가상환경 생성 및 활성화

\`\`\`bash
python -m venv venv

# Windows

venv\\Scripts\\activate

# Linux/Mac

source venv/bin/activate
\`\`\`

### 3. 의존성 설치

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. 서버 실행

\`\`\`bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
\`\`\`

서버가 시작되면 \`http://localhost:8000\`에서 API에 접근할 수 있습니다.

## 개발 환경 설정

### API 문서

- Swagger UI: \`http://localhost:8000/docs\`
- ReDoc: \`http://localhost:8000/redoc\`

### CORS 설정

프론트엔드 연동을 위해 \`main.py\`에서 CORS 설정을 확인하고 필요에 따라 수정하세요.

\`\`\`python
allow_origins=["https://your-frontend-domain.com"]
\`\`\`

## 프로젝트 구조

\`\`\`
tts-back/
├── main.py # FastAPI 메인 애플리케이션
├── manager/ # 매니저 클래스들
│ ├── PresetManager.py # 프리셋 관리
│ └── VoicePlaybackManager.py # 음성 재생 관리
├── audios/ # 생성된 음성 파일 저장소
├── requirements.txt # Python 의존성
├── pyproject.toml # 프로젝트 설정
└── README.md # 프로젝트 문서
\`\`\`

## 배포

이 프로젝트는 Railway, Heroku, AWS 등 다양한 플랫폼에 배포할 수 있습니다.

### Railway 배포 예시

1. Railway 계정 생성 및 프로젝트 연결
2. 환경 변수 설정 (필요시)
3. 자동 배포 완료

## 기여하기

1. 이 저장소를 Fork 합니다
2. 새로운 기능 브랜치를 생성합니다 (\`git checkout -b feature/amazing-feature\`)
3. 변경사항을 커밋합니다 (\`git commit -m 'Add some amazing feature'\`)
4. 브랜치에 Push 합니다 (\`git push origin feature/amazing-feature\`)
5. Pull Request를 생성합니다

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 \`LICENSE\` 파일을 참조하세요.

## 연락처

프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 등록해주세요.

---

**TTS-Back** - 더 나은 음성 서비스를 위해 🎵
