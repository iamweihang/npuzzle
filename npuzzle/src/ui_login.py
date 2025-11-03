# ui_login.py
import tkinter as tk
from tkinter import ttk

class LoginView(ttk.Frame):
    def __init__(self, master, on_confirm):
        super().__init__(master)
        self.on_confirm = on_confirm

        self.columnconfigure(0, weight=1)
        wrapper = ttk.Frame(self, padding=24)
        wrapper.grid(row=0, column=0, sticky="nsew")
        for i in range(3):
            wrapper.rowconfigure(i, weight=1)
        wrapper.columnconfigure(0, weight=1)

        title = ttk.Label(wrapper, text="n-Puzzle", font=("Segoe UI", 24, "bold"))
        title.grid(row=0, column=0, pady=(40, 10))

        prompt = ttk.Label(wrapper, text="Enter your ID:")
        prompt.grid(row=1, column=0, pady=(10, 6))

        self.entry = ttk.Entry(wrapper, width=30)
        self.entry.grid(row=2, column=0, pady=(0, 12))
        self.entry.focus_set()

        btn = ttk.Button(wrapper, text="Confirm", command=self._confirm)
        btn.grid(row=3, column=0, pady=(6, 40))

        # 允许回车直接确认
        self.entry.bind("<Return>", lambda _e: self._confirm())

    def _confirm(self):
        user = self.entry.get().strip()
        if not user:
            user = "player"
        self.on_confirm(user)
