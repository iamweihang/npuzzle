import random
from typing import List, Tuple

def neighbors_adjacent(state: Tuple[int, ...], N: int, last_blank: int | None):
    res = []
    b = state.index(0)
    r, c = divmod(b, N)
    for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
        nr, nc = r+dr, c+dc
        if 0 <= nr < N and 0 <= nc < N:
            nb = nr*N + nc
            if last_blank is not None and nb == last_blank:  # avoid immediate backtrack
                continue
            lst = list(state)
            lst[b], lst[nb] = lst[nb], lst[b]
            res.append((nb, tuple(lst)))
    return res

def scramble_from_goal(N: int, steps: int = 200, seed: int | None = None) -> List[int]:
    goal = tuple(list(range(1, N*N)) + [0])
    rnd = random.Random(seed)
    s = goal
    last_blank = None
    for _ in range(steps):
        opts = neighbors_adjacent(s, N, last_blank)
        nb, nxt = rnd.choice(opts)
        last_blank = s.index(0)
        s = nxt
    return list(s)
