# src/core_timer.py
import time

class GameTimer:
    """
    简单准确的计时器：
    - start(): 开始/重新开始计时（清零并启动）
    - stop(): 停止计时（保留累计时间）
    - elapsed(): 返回累计秒数（运行中 = now - t0；停止后 = 固定累计值）
    - fmt(): 将秒数转 MM:SS
    说明：默认构造后不启动（用于预览态显示 00:00）。
    """
    def __init__(self):
        self._running = False
        self._t0 = 0.0          # 最近一次 start 的起点
        self._elapsed = 0.0     # 累计时长（秒）

    def start(self):
        """清零并开始计时。"""
        self._elapsed = 0.0
        self._t0 = time.perf_counter()
        self._running = True

    def stop(self):
        """停止计时并固定累计值。"""
        if self._running:
            self._elapsed = time.perf_counter() - self._t0
            self._running = False

    def reset(self):
        """等价于重新开始计时（清零并启动）。"""
        self.start()

    def elapsed(self) -> float:
        """返回累计秒数（运行中或停止后都正确）。"""
        if self._running:
            return time.perf_counter() - self._t0
        return self._elapsed

    @staticmethod
    def fmt(seconds: float) -> str:
        s = int(seconds + 0.5)  # 四舍五入到最近整秒，显示更自然
        m, s = divmod(s, 60)
        return f"{m:02d}:{s:02d}"
