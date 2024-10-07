import threading
import time
import weakref
import atexit
from abc import ABC, abstractmethod


class SelfCleaningBackgroundService(ABC):
    _instances = weakref.WeakSet()
    _cleanup_registered = False
    _is_debug = False

    def __init__(self, is_debug=False):
        self._is_debug = is_debug
        self._stop_event = threading.Event()
        self._update_thread = threading.Thread(target=self._background_task)
        self._update_thread.daemon = True
        self._update_thread.start()
        self._instances.add(self)

        self._finalizer = weakref.finalize(self, self._cleanup)

        if not self.__class__._cleanup_registered:
            atexit.register(self.__class__._cleanup_all)
            self.__class__._cleanup_registered = True

    @abstractmethod
    def _background_task(self):
        pass

    def _cleanup(self):
        if self._is_debug:
            print(f"正在清理 {self.__class__.__name__} 实例...")
        self._stop_event.set()
        if self._update_thread.is_alive():
            self._update_thread.join(timeout=0.1)
        if self._is_debug:
            print(f"{self.__class__.__name__} 实例已清理")

    @classmethod
    def _cleanup_all(cls):
        if cls._is_debug:
            print(f"正在清理所有 {cls.__name__} 实例...")
        for instance in list(cls._instances):
            if instance._finalizer.alive:
                instance._finalizer()
        if cls._is_debug:
            print(f"所有 {cls.__name__} 实例已清理")
