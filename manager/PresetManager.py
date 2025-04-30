class Preset:
    def __init__(self, id, text, audioUrl, filePath):
        self.id = id                           # List Index
        self.text = text                       # TTS Text
        self.audioUrl = audioUrl               # TTS URL(TTS 파일 경로)
        self.filePath = filePath

    def __repr__(self):
        return f"Preset(id={self.id}, text={self.text}, audio_url={self.audioUrl}, file_path={self.filePath})"


class PresetManager:
    _instance = None
    sequence = 0
    presetList = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PresetManager, cls).__new__(cls)
        return cls._instance

    def addPreset(self, text, audio_url, file_path):
        id = self.sequence
        self.sequence += 1
        preset = Preset(id, text, audio_url, file_path)
        self.solution(self.add, preset)
        return preset

    def removePreset(self, id):
        target = self.search(id)
        if target is None:
            return None
        self.solution(self.remove, target)
        return target

    def search(self, id):
        return next((preset for preset in self.presetList if preset.id == id), None)

    def add(self, preset):
        self.presetList.append(preset)

    def remove(self, preset):
        self.presetList.remove(preset)

    def solution(self, func, preset):
        # 동시성 이슈 발생시 작업
        func(preset)
