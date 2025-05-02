import threading
from time import sleep
import pygame

def singleton(cls):
  class Singleton(cls):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
      if Singleton._instance is None:
        with cls._lock:
          if Singleton._instance is None:
            Singleton._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
            Singleton._instance._initialized = False
      return Singleton._instance
    
    def __init__(self, *args, **kwargs):
      if self._initialized:
        return
      super(Singleton, self).__init__(*args, **kwargs)
      self._initialized = True

  Singleton.__name__ = cls.__name__
  return Singleton


@singleton
class BgmPlayer:
  def __init__(self):
    self._thread = None
    self._stop_sign = False
    pygame.mixer.init()

  def _play(self, url):
    with BgmPlayer._lock:
      pygame.mixer.music.load(url)
      pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
      if self._stop_sign:
        pygame.mixer.music.stop()
      pygame.time.wait(100)

  def _stop(self):
    with BgmPlayer._lock:
      self._stop_sign = True

  def play_new_sound(self, url):
    if self._thread is not None:
      if self._thread.is_alive():
        self._stop()
        self._thread.join()
      self._thread = None

    self._stop_sign = False
    t = threading.Thread(target=self._play, args=(url,))
    self._thread = t
    t.start()

  def stop(self):
    self._stop()

  def health_check(self):
    return (BgmPlayer._instance == self) and (BgmPlayer._instance._initialized) and (pygame.mixer.get_init() is not None)
