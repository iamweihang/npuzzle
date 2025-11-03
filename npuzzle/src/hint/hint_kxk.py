from __future__ import annotations
from typing import List, Tuple, Iterable, Optional

# ----------------- 基础工具 -----------------

def _goal_of(n: int) -> Tuple[int,...]:
    return tuple(list(range(1, n*n)) + [0])

def _index_of(state: Tuple[int,...], value: int) -> int:
    return state.index(value)

def _rc(i: int, n: int) -> Tuple[int,int]:
    return divmod(i, n)

def _manhattan_sum(state: Tuple[int,...], n: int, ignore_idx: Optional[set[int]] = None) -> int:
    """所有非 0 的曼哈顿距离之和；ignore_idx 中的格子不计入"""
    if ignore_idx is None:
        ignore_idx = set()
    dist = 0
    for i, v in enumerate(state):
        if v == 0 or i in ignore_idx:
            continue
        gr, gc = divmod(v-1, n)
        r, c = divmod(i, n)
        dist += abs(gr - r) + abs(gc - c)
    return dist

def _locked_mask(state: Tuple[int,...], n: int) -> set[int]:
    """
    简单锁定策略：
    - 从上到下，凡是「整行均已到位」的行，全部锁定；
    - 在已锁行之外，从左到右，凡是「整列均已到位」的列，全部锁定。
    （尽量不破坏这些“墙”）
    """
    goal = _goal_of(n)
    locked: set[int] = set()

    # 锁定整行（从上往下）
    for r in range(n):
        ok = True
        for c in range(n):
            idx = r*n + c
            if state[idx] != goal[idx]:
                ok = False
                break
        if ok:
            for c in range(n):
                locked.add(r*n + c)
        else:
            break  # 仅锁定前缀的整行

    # 锁定整列（从左往右），但不覆盖已锁定行之外
    # 注意：最后一列在 15-puzzle 的目标里也必须匹配才算锁
    for c in range(n):
        ok = True
        for r in range(n):
            idx = r*n + c
            if state[idx] != goal[idx]:
                ok = False
                break
        if ok:
            for r in range(n):
                locked.add(r*n + c)
        else:
            break  # 仅锁定前缀的整列

    return locked

# ----------------- 段滑动邻居 -----------------

def _neighbors_segment(state: Tuple[int,...], n: int) -> Iterable[Tuple[Tuple[int,...], int]]:
    """
    生成所有一次「段滑动」邻居。
    返回 (next_state, moved_index)：
    - moved_index 表示用户若点击该 index 的格子，就会产生这个 next_state（仅用于调试/打分）。
    规则：
    - 空格与同一行/列的任一格均可选择，选中后空格会与路径上所有格按方向整体交换（整段平移）。
    """
    s_list = list(state)
    z = s_list.index(0)
    br, bc = divmod(z, n)

    # 同一行
    # 左侧 -> 往右推
    for c in range(bc-1, -1, -1):
        lst = s_list[:]
        # c..bc-1 右移一格，空格到 c
        for cc in range(bc, c, -1):
            lst[br*n + cc] = lst[br*n + (cc-1)]
        lst[br*n + c] = 0
        yield (tuple(lst), br*n + c)

    # 右侧 -> 往左推
    for c in range(bc+1, n):
        lst = s_list[:]
        for cc in range(bc, c):
            lst[br*n + cc] = lst[br*n + (cc+1)]
        lst[br*n + c] = 0
        yield (tuple(lst), br*n + c)

    # 同一列
    # 上侧 -> 往下推
    for r in range(br-1, -1, -1):
        lst = s_list[:]
        for rr in range(br, r, -1):
            lst[rr*n + bc] = lst[(rr-1)*n + bc]
        lst[r*n + bc] = 0
        yield (tuple(lst), r*n + bc)

    # 下侧 -> 往上推
    for r in range(br+1, n):
        lst = s_list[:]
        for rr in range(br, r):
            lst[rr*n + bc] = lst[(rr+1)*n + bc]
        lst[r*n + bc] = 0
        yield (tuple(lst), r*n + bc)

# ----------------- 评估函数 -----------------

def _eval_state(state: Tuple[int,...], n: int, locked: set[int]) -> int:
    """
    启发式评分：越小越好
    - 基础：未锁格子的曼哈顿距离和
    - 惩罚：若把 locked 中的块移离其目标位置，加大惩罚（这里简化为 +K）
    """
    goal = _goal_of(n)
    base = _manhattan_sum(state, n, ignore_idx=locked)

    # 惩罚破坏锁定区：如果锁定格子里有任何 != 目标的，惩罚
    penalty = 0
    for idx in locked:
        if state[idx] != goal[idx]:
            penalty += 10  # 一个固定的权重，经验上已经足够抑制破坏
    return base + penalty

# ----------------- 主入口：返回下一状态 -----------------

def next_state_after_one_segment(state_list: List[int], n: int) -> Optional[Tuple[int,...]]:
    """
    给定当前盘面（扁平列表）和尺寸 n，返回「执行一次段滑动」后的下一状态（作为 Hint）。
    若已经是目标或找不到更优动作，返回 None。
    """
    cur = tuple(state_list)
    goal = _goal_of(n)
    if cur == goal:
        return None

    locked = _locked_mask(cur, n)
    cur_score = _eval_state(cur, n, locked)

    # 先尝试一步贪心
    best_next = None
    best_score = 10**9
    best_len = 10**9  # 鼓励短距离移动（更可控）
    for nxt, moved_idx in _neighbors_segment(cur, n):
        # 移动长度 = 曼哈顿距离中空格沿行/列走的长度
        zr, zc = _rc(cur.index(0), n)
        r, c = _rc(moved_idx, n)
        move_len = abs(zr - r) + abs(zc - c)

        score = _eval_state(nxt, n, locked)
        if (score < best_score) or (score == best_score and move_len < best_len):
            best_score = score
            best_len = move_len
            best_next = nxt

    if best_next is not None and best_score <= cur_score:
        return best_next

    # 若一步无改进，做深度2束搜索：min_{a,b} score(b) ，返回对应的第一步 a
    # 简化：扩 8 ~ (2n-2) 个第一层，再各自扩一层，取末端最优
    best_first = None
    best_two_score = 10**9
    best_two_len = 10**9

    first_layer = list(_neighbors_segment(cur, n))
    for s1, idx1 in first_layer:
        locked1 = _locked_mask(s1, n)
        s1_score = _eval_state(s1, n, locked1)
        # 直接允许第一步让分数更差，但只要第二步能显著下降即可
        for s2, idx2 in _neighbors_segment(s1, n):
            score2 = _eval_state(s2, n, locked1)
            # 估计“总代价”：末端评分 + 第一移动长度（微弱正则）
            zr, zc = _rc(cur.index(0), n)
            r1, c1 = _rc(idx1, n)
            len1 = abs(zr - r1) + abs(zc - c1)

            if (score2 < best_two_score) or (score2 == best_two_score and len1 < best_two_len):
                best_two_score = score2
                best_two_len = len1
                best_first = s1

    if best_first is not None and best_two_score < 10**9:
        return best_first

    # 实在找不到改进（极少数局面），返回贪心一步作为 fallback
    return best_next