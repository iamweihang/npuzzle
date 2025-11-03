import tkinter as tk
from tkinter import ttk, messagebox
from core_board import Board
from core_scramble import scramble_from_goal
from core_timer import GameTimer
from io_leaderboard import load_lb, save_lb, submit_record, best_time_ms, best_time_ms_user

class GameView(ttk.Frame):
    CELL, PAD = 80, 20

    def __init__(self, master, user: str, size: int, on_back_home, on_success):
        super().__init__(master)
        self.user = user
        self.size = size
        self.on_back_home = on_back_home
        self.on_success = on_success  # 跳转成功页

        # ---------- 预览态 ----------
        self.prestart = True
        self.used_hint = False   # ★ 本局是否用过 Hint
        goal = list(range(1, size*size)) + [0]
        self.board = Board(size, goal)
        self.board.start = self.board.state[:]  # 仅为 reset 安全
        self.timer = GameTimer()                # 未 start，计时显示 00:00

        self._build_ui()
        self._draw_board()
        self._tick()

    # ---------------- UI layout ----------------
    def _build_ui(self):
        # —— 第1行：返回按钮（独占一行）——
        row1 = ttk.Frame(self, padding=(10, 10, 10, 0))
        row1.pack(fill="x")
        ttk.Button(row1, text="← Main Menu", command=self._back_home).pack(anchor="w")

        # —— 第2行：时间 / 标题 / 步数 —— 用grid三列布局
        row2 = ttk.Frame(self, padding=(10, 4, 10, 0))
        row2.pack(fill="x")

        self.lbl_time = ttk.Label(row2, text="00:00")
        self.lbl_time.grid(row=0, column=0, sticky="w")

        ttk.Label(
            row2,
            text=f"Level: {self.size}×{self.size}",
            font=("Arial", 14, "bold")
        ).grid(row=0, column=1, sticky="n")

        self.lbl_steps = ttk.Label(row2, text="Steps: 0")
        self.lbl_steps.grid(row=0, column=2, sticky="e")

        # 让中间列撑开，从而实现左中右对齐
        row2.grid_columnconfigure(0, weight=0)
        row2.grid_columnconfigure(1, weight=1)
        row2.grid_columnconfigure(2, weight=0)

        # —— 画布保持不变 ——
        w = self.size * self.CELL + 2 * self.PAD
        h = self.size * self.CELL + 2 * self.PAD
        self.canvas = tk.Canvas(self, width=w, height=h, bg="#f7f7f7", highlightthickness=0)
        self.canvas.pack(padx=10, pady=(10, 4))
        self.canvas.bind("<Button-1>", self._on_click)

        # —— 预览提示 —— 
        self.lbl_preview_hint = ttk.Label(self, text="Target pattern")
        if self.prestart:
            self.lbl_preview_hint.pack(pady=(0, 8))

        # —— 底部区域保持不变 —— 
        self.bottom = ttk.Frame(self, padding=10)
        self.bottom.pack(fill="x")
        self._render_bottom()


    def _render_bottom(self):
        for w in self.bottom.winfo_children():
            w.destroy()
        if self.prestart:
            ttk.Button(self.bottom, text="Confirm", command=self._confirm_and_start).pack(side="right")
        else:
            ttk.Button(self.bottom, text="Reset", command=self._reset).pack(side="left")
            if self.size == 3:
                ttk.Button(self.bottom, text="Hint", command=self._hint_3x3).pack(side="right")
            # ★ 管理员专属按钮
            if self.user == "admin":
                ttk.Button(self.bottom, text="Restore", command=self._admin_restore).pack(side="right", padx=6)

    # ---------------- drawing ----------------
    def _draw_board(self):
        N, CELL, PAD = self.size, self.CELL, self.PAD
        s = self.board.state
        self.canvas.delete("all")
        for r in range(N + 1):
            y = PAD + r * CELL
            self.canvas.create_line(PAD, y, PAD + N * CELL, y, fill="#ddd")
        for c in range(N + 1):
            x = PAD + c * CELL
            self.canvas.create_line(x, PAD, x, PAD + N * CELL, fill="#ddd")
        for i, v in enumerate(s):
            if v == 0: continue
            r, c = divmod(i, N)
            x0, y0 = PAD + c * CELL, PAD + r * CELL
            x1, y1 = x0 + CELL, y0 + CELL
            self.canvas.create_rectangle(x0 + 2, y0 + 2, x1 - 2, y1 - 2,
                                         fill="#ffffff", outline="#333", width=2)
            self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2,
                                    text=str(v), font=("Arial", 16, "bold"))

    # ---------------- input ----------------
    def _on_click(self, e):
        if self.prestart or getattr(self, "_ui_locked", False):
            return
        N, CELL, PAD = self.size, self.CELL, self.PAD
        r = (e.y - PAD) // CELL
        c = (e.x - PAD) // CELL
        if not (0 <= r < N and 0 <= c < N):
            return
        idx = r * N + c
        moved = self.board.segment_move_if_valid(idx)
        if moved:
            self.lbl_steps.config(text=f"Steps: {self.board.steps}")
            self._draw_board()
            if self.board.is_goal():
                self._handle_win()

    # ---------------- actions ----------------
    def _confirm_and_start(self):
        steps = 60 if self.size == 3 else (200 if self.size == 4 else 400)
        self.board = Board(self.size, scramble_from_goal(self.size, steps))
        self.board.start = self.board.state[:]
        self.board.steps = 0

        self.timer = GameTimer()
        self.timer.start()

        self.prestart = False
        self.used_hint = False      # ★ 新局清零
        self.lbl_steps.config(text="Steps: 0")

        if self.lbl_preview_hint and self.lbl_preview_hint.winfo_ismapped():
            self.lbl_preview_hint.pack_forget()

        self._render_bottom()
        self._draw_board()

    def _reset(self):
        if getattr(self, "_ui_locked", False):
            return
        self.board.reset_to_start()
        self.timer = GameTimer()
        self.timer.start()
        self.used_hint = False      # ★ 重置也清零
        self.lbl_steps.config(text="Steps: 0")
        self._draw_board()

    def _back_home(self):
        if getattr(self, "_ui_locked", False):
            return
        self.on_back_home()

    def _hint_3x3(self):
        if self.size != 3 or self.board.is_goal() or self.prestart or getattr(self, "_ui_locked", False):
            return
        try:
            from hint.hint_3x3 import bfs_first_move_3x3
        except Exception:
            messagebox.showerror("Hint", "Hint module not found.")
            return
        next_state, _ = bfs_first_move_3x3(self.board.state)
        if next_state is None: return
        self.board.state = list(next_state)
        self.used_hint = True          # ★ 标记
        self.board.steps += 1
        self.lbl_steps.config(text=f"Steps: {self.board.steps}")
        self._draw_board()
        if self.board.is_goal():
            self._handle_win()

    # ---------------- admin restore ----------------
    def _admin_restore(self):
        """管理员一键还原"""
        if self.prestart:  # 预览态不用
            return
        # 设置到目标状态
        self.board.state = list(range(1, self.size*self.size)) + [0]
        self.board.steps += 1
        self.lbl_steps.config(text=f"Steps: {self.board.steps}")
        self._draw_board()
        # 直接进入胜利流程
        self._handle_win()

    # ---------------- UI lock/unlock ----------------
    def _lock_ui(self):
        if getattr(self, "_ui_locked", False):
            return
        self._ui_locked = True
        self._lock_layer = tk.Frame(self, bg="", cursor="watch")
        self._lock_layer.place(relx=0, rely=0, relwidth=1, relheight=1)
        def _eat(_e=None): return "break"
        for seq in (
            "<Button-1>", "<Button-2>", "<Button-3>",
            "<ButtonRelease-1>", "<ButtonRelease-2>", "<ButtonRelease-3>",
            "<B1-Motion>", "<B2-Motion>", "<B3-Motion>",
            "<MouseWheel>", "<Key>", "<KeyRelease>"
        ):
            self._lock_layer.bind(seq, _eat)

    def _unlock_ui(self):
        if getattr(self, "_ui_locked", False):
            if hasattr(self, "_lock_layer") and self._lock_layer.winfo_exists():
                self._lock_layer.destroy()
            self._ui_locked = False

    # ---------------- victory ----------------
    def _handle_win(self):
        if getattr(self, "_win_pending", False):
            return
        self._win_pending = True

        self.timer.stop()
        t_ms = int(self.timer.elapsed() * 1000)

        lb = load_lb()

        if not self.used_hint and self.user != 'admin':
            submit_record(lb, self.size, self.user, t_ms, self.board.steps)
            save_lb(lb)
        
        # best_ms = best_time_ms(lb, self.size)
        best_ms = best_time_ms_user(lb, self.size, self.user)

        self._lock_ui()
        self.after(500, lambda: self.on_success(self.size, t_ms, self.board.steps, best_ms))

    def _new_game_same_size(self):
        pass

    def _tick(self):
        self.lbl_time.config(text=GameTimer.fmt(self.timer.elapsed()))
        self.after(200, self._tick)

    # # ---------------- hint ----------------
    # def _hint_any(self):
    #     if self.board.is_goal() or self.prestart or getattr(self, "_ui_locked", False):
    #         return
    #     try:
    #         if self.size == 3:
    #             from hint.hint_3x3 import bfs_first_move_3x3
    #             next_state, _ = bfs_first_move_3x3(self.board.state)
    #             if next_state is None:
    #                 return
    #             self.board.state = list(next_state)
    #         else:
    #             from hint.hint_kxk import compute_hint
    #             moves = compute_hint(self.board.get_matrix(), max_steps=5)
    #             # 逐步执行提示
    #             for mv in moves:
    #                 self.board.move(mv)
    #         self.board.steps += 1
    #         self.lbl_steps.config(text=f"Steps: {self.board.steps}")
    #         self._draw_board()
    #         if self.board.is_goal():
    #             self._handle_win()
    #     except Exception as e:
    #         messagebox.showerror("Hint", f"Hint error: {e}")
