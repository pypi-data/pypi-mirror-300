import asyncio
import weakref
import atexit
from abc import ABC, abstractmethod


class SelfCleaningBackgroundService(ABC):
    _instances = weakref.WeakSet()
    _cleanup_registered = False
    _is_debug = False
    _loop = None

    def __init__(self, auto_start=True, is_debug=False):
        self._is_debug = is_debug
        self._stop_event = asyncio.Event()
        self._update_task = None
        self._instances.add(self)
        self._auto_start = auto_start

        if self.__class__._loop is None:
            self.__class__._loop = asyncio.get_event_loop()

        self._finalizer = weakref.finalize(self, self._sync_cleanup)

        if not self.__class__._cleanup_registered:
            atexit.register(self.__class__._sync_cleanup_all)
            self.__class__._cleanup_registered = True

        if self._auto_start:
            self.start()

    @abstractmethod
    async def _background_task(self):
        pass

    def start(self):
        """启动后台任务"""
        if self._update_task is None or self._update_task.done():
            self._stop_event.clear()
            self._update_task = asyncio.run_coroutine_threadsafe(self._background_task(), self.__class__._loop)
            if self._is_debug:
                print(f"{self.__class__.__name__} 后台任务已启动")

    def stop(self):
        """停止后台任务"""
        if self._update_task and not self._update_task.done():
            self._stop_event.set()
            self._update_task.cancel()
            if self._is_debug:
                print(f"{self.__class__.__name__} 后台任务已停止")

    def _sync_cleanup(self):
        if self._is_debug:
            print(f"正在清理 {self.__class__.__name__} 实例...")
        self.stop()
        if self._is_debug:
            print(f"{self.__class__.__name__} 实例已清理")

    @classmethod
    def _sync_cleanup_all(cls):
        if cls._is_debug:
            print(f"正在清理所有 {cls.__name__} 实例...")
        for instance in list(cls._instances):
            if instance._finalizer.alive:
                instance._finalizer()
        if cls._is_debug:
            print(f"所有 {cls.__name__} 实例已清理")
