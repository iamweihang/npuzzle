import tkinter as tk
from tkinter import ttk

class HomeView(ttk.Frame):
    def __init__(self, master, on_pick_size, on_open_leaderboard, on_quit, current_user: str = "player"):
        super().__init__(master, padding=20)

        # 顶部：标题（左）+ 当前ID（右）
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 12))
        ttk.Label(header, text="n-Puzzle", font=("Arial", 20, "bold")).pack(side="left")
        self.user_label = ttk.Label(header, text=f"ID: {current_user}")
        self.user_label.pack(side="right")

        sizes = ttk.Frame(self); sizes.pack(pady=8)
        ttk.Label(sizes, text="Choose Level").pack(pady=(0,6))
        for n in (3,4,5):
            ttk.Button(sizes, text=f"{n}×{n}", width=16,
                       command=lambda s=n: on_pick_size(s)).pack(pady=4)

        ttk.Button(self, text="Leaderboard", command=on_open_leaderboard).pack(pady=10)
        ttk.Button(self, text="Exit", command=on_quit).pack(pady=(16,0))

    # # 可选：若后续支持切换账号，可动态更新
    # def set_user(self, user: str):
    #     self.user_label.config(text=f"ID: {user or 'player'}")
