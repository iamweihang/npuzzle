import tkinter as tk
from tkinter import ttk, messagebox
from io_leaderboard import load_lb, save_lb, top10, clear_level, delete_record
from core_timer import GameTimer

class LeaderboardView(ttk.Frame):
    def __init__(self, master, on_back, current_user: str):
        super().__init__(master, padding=20)
        self.on_back = on_back
        self.current_user = current_user
        self.current_size = 3  # 默认显示 3x3

        # 顶部返回
        ttk.Button(self, text="← Back", command=self.on_back).pack(anchor="w")

        ttk.Label(self, text="Leaderboard", font=("Arial",16,"bold")).pack(pady=(6,12))

        # 尺寸切换
        pick = ttk.Frame(self); pick.pack(pady=6)
        ttk.Label(pick, text="Choose Level:").pack(side="left", padx=(0,8))
        for n in (3,4,5):
            ttk.Button(pick, text=f"{n}×{n}",
                       command=lambda s=n: self._show_size(s)).pack(side="left", padx=4)

        # 表格
        self.table = ttk.Treeview(self, columns=("rank","user","time","steps","date"),
                                  show="headings", height=12)
        for c, w in (("rank",60),("user",120),("time",80),("steps",80),("date",180)):
            self.table.heading(c, text=c.capitalize())
            self.table.column(c, width=w, anchor="center")
        self.table.pack(pady=8, fill="x")

        # 底部 admin 操作区（仅 admin 可见）
        if self.current_user == "admin":
            bar = ttk.Frame(self)
            bar.pack(fill="x", pady=(8,0))

            # 左下角：Clear All（仅清空当前尺寸）
            ttk.Button(bar, text="Clear All", command=self._on_clear_all)\
               .pack(side="left")

            # 右下角：Delete（删除选中记录）
            ttk.Button(bar, text="Delete", command=self._on_delete_selected)\
               .pack(side="right")

        # 默认展示 3x3
        self._show_size(3)

    def _show_size(self, size: int):
        self.current_size = size
        lb = load_lb()
        rows = top10(lb, size)

        # 清空表格
        for i in self.table.get_children():
            self.table.delete(i)

        # 填充表格（Time 显示 mm:ss）
        for i, r in enumerate(rows, start=1):
            mmss = GameTimer.fmt(r["time_ms"]/1000.0)
            self.table.insert("", "end",
                              values=(i, r["user"], mmss, r["steps"], r["date"]))

    def _on_clear_all(self):
        """清空当前尺寸排行榜"""
        if messagebox.askyesno("Confirm", f"Clear leaderboard for {self.current_size}×{self.current_size}?"):
            lb = load_lb()
            clear_level(lb, self.current_size)
            save_lb(lb)
            self._show_size(self.current_size)
            messagebox.showinfo("Cleared", f"Leaderboard for {self.current_size}×{self.current_size} cleared.")

    def _on_delete_selected(self):
        """删除表格中选中的一条记录"""
        sel = self.table.selection()
        if not sel:
            messagebox.showwarning("No selection", "Please select a record to delete.")
            return

        # 取第一条选中（如果支持多选，可遍历删除；这里按需求删除单条）
        row_id = sel[0]
        idx_in_view = self.table.index(row_id)  # 0-based
        if not messagebox.askyesno("Confirm", "Delete selected record?"):
            return

        lb = load_lb()
        ok = delete_record(lb, self.current_size, idx_in_view)
        if ok:
            save_lb(lb)
            self._show_size(self.current_size)
            messagebox.showinfo("Deleted", "Record deleted.")
        else:
            messagebox.showerror("Error", "Failed to delete the record.")
