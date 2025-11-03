import tkinter as tk
from ui_login import LoginView
from ui_home import HomeView
from ui_leaderboard import LeaderboardView
from ui_game import GameView
from ui_success import SuccessView

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("n-Puzzle")
        self.geometry("640x640")
        self.resizable(False, False)

        self.user: str | None = None
        self._frame = None

        # 启动先显示登录页（不再弹窗）
        self.show_login()

    def _switch(self, widget):
        if self._frame:
            self._frame.destroy()
        self._frame = widget
        self._frame.pack(fill="both", expand=True)

    # -------- routes --------
    def show_login(self):
        self._switch(LoginView(self, on_confirm=self._on_login_confirmed))

    def _on_login_confirmed(self, username: str):
        self.user = username or "player"
        self.show_home()

    def show_home(self):
        self._switch(HomeView(
            self,
            on_pick_size=self.start_game,
            on_open_leaderboard=self.show_leaderboard,
            on_quit=self.destroy,
            current_user=self.user or "player"
        ))

    def start_game(self, size: int):
        self._switch(GameView(
            self, self.user or "player", size,
            on_back_home=self.show_home,
            on_success=self.show_success
        ))

    def show_leaderboard(self):
        # 传递当前用户名，便于排行榜判断是否显示 Admin 功能
        self._switch(LeaderboardView(self, on_back=self.show_home, current_user=self.user or "player"))

    def show_success(self, size: int, run_time_ms: int, steps: int, best_time_ms: int | None):
        """整页切到 SuccessView。"""
        self._switch(SuccessView(
            self, size, run_time_ms, steps, best_time_ms,
            on_home=self.show_home,
            on_new_level=lambda: self.start_game(size)
        ))

if __name__ == "__main__":
    App().mainloop()
