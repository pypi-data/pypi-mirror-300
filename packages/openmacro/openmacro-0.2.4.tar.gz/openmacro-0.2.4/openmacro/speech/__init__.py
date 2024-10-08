from ..utils import lazy_import

class Speech:
    def __init__(self, 
                 tts: dict = None, 
                 stt: dict = None) -> None:
        config = stt or {}
        if config.get("enabled"):
            try: from .stt import STT
            except: print("An error occured: Disabling STT.")
            self.stt = STT(config, config.get("engine", "SystemEngine"))
            
        config = tts or {}
        if config.get("enabled"):
            try: from .tts import TTS
            except: print("An error occured: Disabling TTS.")
            self.tts = TTS(config, config.get("engine", "SystemEngine"))
