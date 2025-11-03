# 3x3 Smart Hint: shortest path under "segment-slide = 1 move".
from collections import deque
from typing import Tuple, List, Optional

N = 3
GOAL = (1,2,3,4,5,6,7,8,0)

def neighbors_segment_3x3(s: Tuple[int, ...]) -> List[Tuple[int, ...]]:
    res = []
    s_list = list(s)
    b = s_list.index(0)
    br, bc = divmod(b, N)

    # same row
    for c in range(bc):  # left side -> shift right
        lst = s_list[:]
        for cc in range(bc, c, -1):
            lst[br*N + cc] = lst[br*N + (cc-1)]
        lst[br*N + c] = 0
        res.append(tuple(lst))
    for c in range(bc+1, N):  # right side -> shift left
        lst = s_list[:]
        for cc in range(bc, c):
            lst[br*N + cc] = lst[br*N + (cc+1)]
        lst[br*N + c] = 0
        res.append(tuple(lst))

    # same column
    for r in range(br):  # above -> shift down
        lst = s_list[:]
        for rr in range(br, r, -1):
            lst[rr*N + bc] = lst[(rr-1)*N + bc]
        lst[r*N + bc] = 0
        res.append(tuple(lst))
    for r in range(br+1, N):  # below -> shift up
        lst = s_list[:]
        for rr in range(br, r):
            lst[rr*N + bc] = lst[(rr+1)*N + bc]
        lst[r*N + bc] = 0
        res.append(tuple(lst))

    return res

def bfs_first_move_3x3(start: List[int] | Tuple[int, ...]) -> Tuple[Optional[Tuple[int, ...]], bool]:
    st = tuple(start)
    if st == GOAL:
        return None, True

    q = deque([st])
    parent = {st: None}

    while q:
        s = q.popleft()
        if s == GOAL:
            path = [s]
            while parent[path[-1]] is not None:
                path.append(parent[path[-1]])
            path.reverse()  # [start, step1, ..., goal]
            return (path[1], True)

        for nxt in neighbors_segment_3x3(s):
            if nxt not in parent:
                parent[nxt] = s
                q.append(nxt)

    return None, True  # unreachable in normal solvable cases
