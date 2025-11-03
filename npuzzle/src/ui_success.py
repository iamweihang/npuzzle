import tkinter as tk
from tkinter import ttk
from core_timer import GameTimer

class SuccessView(ttk.Frame):
    """
    整页成功界面：
    - 左上：Main Menu
    - 大标题：Congratulations!
    - This Run: mm:ss + steps
    - Best Time: mm:ss 或 N/A
    - 按钮：Generate New Level（同尺寸开新局，走预览流程）
    """
    def __init__(self, master, size: int, run_time_ms: int, steps: int,
                 best_time_ms: int | None,
                 on_home, on_new_level):
        super().__init__(master, padding=20)
        self.size = size
        self.on_home = on_home
        self.on_new_level = on_new_level

        # 顶部导航
        ttk.Button(self, text="← Main Menu", command=self.on_home).pack(anchor="w")

        # 内容
        body = ttk.Frame(self, padding=(0, 10, 0, 0))
        body.pack(fill="both", expand=True)
        ttk.Label(body, text="Congratulations!", font=("Arial", 20, "bold")).pack(pady=(10, 12))

        run_mmss = GameTimer.fmt(run_time_ms / 1000.0)
        # ttk.Label(body, text=f"This Run: {run_mmss}    Steps: {steps}",
        #           font=("Arial", 12)).pack(pady=(0, 6))
        ttk.Label(body, text=f"This Run: {run_mmss}",
            font=("Arial", 12)).pack(pady=(0, 6))

        best_mmss = GameTimer.fmt(best_time_ms / 1000.0) if best_time_ms is not None else "N/A"
        ttk.Label(body, text=f"Best Time: {best_mmss}",
                  font=("Arial", 12)).pack(pady=(0, 16))

        ttk.Button(body, text="New Game",
                   command=self.on_new_level, width=22).pack(pady=(8, 0))

        # 页脚（可选显示当前尺寸）
        ttk.Label(self, text=f"Board: {size}×{size}", foreground="#666").pack(pady=(16, 0))
