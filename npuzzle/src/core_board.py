from typing import List, Tuple

class Board:
    """State + segment-slide moves (row/column slide toward blank)."""
    def __init__(self, N: int, initial: List[int]):
        self.N = N
        self.goal = list(range(1, N*N)) + [0]
        self.start = initial[:]
        self.state = initial[:]
        self.steps = 0

    def is_goal(self) -> bool:
        return self.state == self.goal

    def reset_to_start(self):
        self.state = self.start[:]
        self.steps = 0

    # --- segment-slide neighbors for a given click index ---
    def segment_move_if_valid(self, tile_idx: int) -> bool:
        """Click a tile; if blank in same row/col, slide the whole segment toward blank (one move)."""
        N = self.N
        s = self.state
        b = s.index(0)
        br, bc = divmod(b, N)
        r, c = divmod(tile_idx, N)

        if r == br:
            if c < bc:  # blank right: shift [c..bc-1] -> right
                for cc in range(bc, c, -1):
                    s[br*N + cc] = s[br*N + (cc-1)]
                s[br*N + c] = 0
            elif c > bc:  # blank left: shift [bc+1..c] -> left
                for cc in range(bc, c):
                    s[br*N + cc] = s[br*N + (cc+1)]
                s[br*N + c] = 0
            else:
                return False
            self.steps += 1
            return True

        if c == bc:
            if r < br:  # blank below: shift [r..br-1] -> down
                for rr in range(br, r, -1):
                    s[rr*N + bc] = s[(rr-1)*N + bc]
                s[r*N + bc] = 0
            elif r > br:  # blank above: shift [br+1..r] -> up
                for rr in range(br, r):
                    s[rr*N + bc] = s[(rr+1)*N + bc]
                s[r*N + bc] = 0
            else:
                return False
            self.steps += 1
            return True

        return False
