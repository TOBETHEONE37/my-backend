class Preset:
    def __init__(self, id, text, audioUrl):
        self.id = id                           # List Index
        self.text = text                       # TTS Text
        self.audioUrl = audioUrl               # TTS URL(TTS 파일 경로)


class PresetHandler:
    _instance = None
    presetList = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PresetHandler, cls).__new__(cls)
        return cls._instance

    def addPreset(self, text, audioUrl):
        id = len(self.presetList)
        preset = Preset(id, text, audioUrl)
        self.presetList.append(preset)
        return preset