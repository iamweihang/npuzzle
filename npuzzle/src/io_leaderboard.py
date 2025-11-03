import json, os, datetime
from typing import Dict, List

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
PATH = os.path.join(DATA_DIR, "leaderboard.json")

def _empty_lb() -> Dict:
    return {"3":{"records_time":[]}, "4":{"records_time":[]}, "5":{"records_time":[]}}

def _ensure():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(PATH):
        with open(PATH, "w", encoding="utf-8") as f:
            json.dump(_empty_lb(), f)

def load_lb() -> Dict:
    _ensure()
    with open(PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_lb(lb: Dict):
    _ensure()
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(lb, f, ensure_ascii=False, indent=2)

def _now_str() -> str:
    # 24h 制，仅到秒：YYYY-MM-DD HH:MM:SS
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def submit_record(lb: Dict, size: int, user: str, time_ms: int, steps: int):
    """写入一条记录并保持 Top10（按 time_ms 升序；时间相同按日期先后）"""
    key = str(size)
    lb.setdefault(key, {"records_time":[]})
    lb[key]["records_time"].append({
        "user": user,
        "time_ms": time_ms,
        "steps": steps,
        "date": _now_str()
    })
    lb[key]["records_time"].sort(key=lambda r:(r["time_ms"], r["date"]))
    lb[key]["records_time"] = lb[key]["records_time"][:10]

def top10(lb: Dict, size: int) -> List[dict]:
    return lb.get(str(size), {}).get("records_time", [])

def best_time_ms(lb: Dict, size: int):
    arr = top10(lb, size)
    return arr[0]["time_ms"] if arr else None

def best_time_ms_user(lb: dict, size: int, user: str) -> int | None:
    """返回该用户在指定尺寸下的最佳时间（毫秒）。若无记录返回 None。"""
    recs = lb.get(str(size), {}).get("records_time", [])
    # 如果你的 user 是大小写不敏感的，可以统一 lower：
    u = (user or "").strip()
    if not u:
        return None
    times = [r.get("time_ms") for r in recs if (r.get("user") == u and isinstance(r.get("time_ms"), int))]
    return min(times) if times else None

def clear_all(lb: Dict):
    """清空所有尺寸排行榜（admin 使用）"""
    lb.clear()
    lb.update(_empty_lb())

# === 新增：按当前关卡清空 ===
def clear_level(lb: Dict, size: int):
    """仅清空某个尺寸的排行榜"""
    lb[str(size)] = {"records_time":[]}

# === 新增：按索引删除一条记录 ===
def delete_record(lb: Dict, size: int, idx: int) -> bool:
    """
    删除 size 维度下第 idx 条记录（基于 top10 的排序）。
    返回 True 表示删除成功，False 表示索引无效。
    """
    key = str(size)
    if key not in lb:
        lb[key] = {"records_time":[]}
        return False
    arr = lb[key]["records_time"]
    if 0 <= idx < len(arr):
        arr.pop(idx)
        return True
    return False
