import threading
from just_playback import Playback
import time
import os
import logging


class VoicePlaybackManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        with self.__class__._lock:
            if self._initialized:
                return
            logging.info("Initializing PlaybackManager...")
            self.current_playback = None
            self._playback_lock = threading.Lock()
            self._initialized = True

    def play_new_sound(self, file_path):
        """
        새로운 사운드 재생을 요청합니다.
        기존에 재생 중인 사운드가 있다면 중지하고 새로 재생합니다.
        """
        logging.info(f"\nRequest received to play: {file_path}")

        if not os.path.exists(file_path):
            logging.info(f"Error: File not found - {file_path}")
            return False

        with self._playback_lock:
            if self.current_playback and self.current_playback.active:
                logging.info("Stopping existing playback...")
                try:
                    self.current_playback.stop()
                    time.sleep(0.1)
                except Exception as e:
                    logging.info(f"Error stopping previous playback: {e}")
                self.current_playback = None  # 이전 인스턴스 참조 제거

            logging.info(f"Starting new playback for: {file_path}")
            try:
                new_playback = Playback()
                new_playback.load_file(file_path)
                new_playback.play()

                self.current_playback = new_playback
                logging.info("Playback started successfully.")
                return True

            except Exception as e:
                logging.info(f"Error starting new playback: {e}")
                self.current_playback = None
                return False

    def stop_current_sound(self):
        """현재 재생 중인 사운드를 명시적으로 중지합니다."""
        with self._playback_lock:
            if self.current_playback and self.current_playback.active:
                logging.info("Stopping current playback...")
                try:
                    self.current_playback.stop()
                    self.current_playback = None  # 중지 후 참조 제거
                    logging.info("Playback stopped.")
                    return True
                except Exception as e:
                    logging.info(f"Error stopping playback: {e}")
                    return False
            else:
                logging.info("No active playback to stop.")
                return False

    def playback_health_check(self):
        if self.current_playback and self.current_playback.active:
            return True
        return False

