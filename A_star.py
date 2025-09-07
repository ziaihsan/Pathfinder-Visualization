"""
A* Maze Visualizer (Tkinter)

Features:
- Generates a random maze (recursive backtracker) up to 200x200.
- Runs only the A* algorithm and animates how it explores:
  - Open set (frontier) cells in pale blue.
  - Closed (explored) cells in light gray.
  - Current node being expanded in orange.
  - Final shortest path in red.
- Canvas automatically scales to fit the whole maze; responsive on resize.

Run:
    python -m py_compile astar.py
    python astar.py
"""

from __future__ import annotations

import heapq
import random
import time
from array import array
from collections import deque
from typing import Dict, Iterable, List, Optional, Tuple

try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import font as tkfont
except Exception as e:  # pragma: no cover - for environments without Tk
    raise


# Direction bit flags for cell walls
N, S, E, W = 1, 2, 4, 8
DIRS: Dict[int, Tuple[int, int]] = {
    N: (-1, 0),
    S: (1, 0),
    E: (0, 1),
    W: (0, -1),
}
OPPOSITE = {N: S, S: N, E: W, W: E}


def generate_maze(rows: int, cols: int) -> Tuple[List[List[int]], Tuple[int, int], Tuple[int, int]]:
    """Generate a perfect maze with iterative recursive-backtracker (DFS).

    Cell stores bitflags of walls present (N|S|E|W). Removing a wall clears bit.
    """
    if rows <= 0 or cols <= 0:
        raise ValueError("rows and cols must be positive")

    grid = [[N | S | E | W for _ in range(cols)] for _ in range(rows)]
    visited = [[False] * cols for _ in range(rows)]

    stack: List[Tuple[int, int]] = [(0, 0)]
    visited[0][0] = True

    while stack:
        r, c = stack[-1]
        candidates: List[Tuple[int, int, int]] = []
        for d, (dr, dc) in DIRS.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                candidates.append((d, nr, nc))
        if candidates:
            d, nr, nc = random.choice(candidates)
            grid[r][c] &= ~d
            grid[nr][nc] &= ~OPPOSITE[d]
            visited[nr][nc] = True
            stack.append((nr, nc))
        else:
            stack.pop()

    return grid, (0, 0), (rows - 1, cols - 1)


def _neighbors(grid: List[List[int]], r: int, c: int) -> Iterable[Tuple[int, int]]:
    rows, cols = len(grid), len(grid[0])
    cell = grid[r][c]
    if c + 1 < cols and not (cell & E):
        yield r, c + 1
    if c - 1 >= 0 and not (cell & W):
        yield r, c - 1
    if r + 1 < rows and not (cell & S):
        yield r + 1, c
    if r - 1 >= 0 and not (cell & N):
        yield r - 1, c


def _reconstruct_path_idx(prev: array, end_idx: int, cols: int) -> List[Tuple[int, int]]:
    path_idx: List[int] = []
    cur = end_idx
    while cur != -1:
        path_idx.append(cur)
        cur = prev[cur]
    path_idx.reverse()
    return [(i // cols, i % cols) for i in path_idx]


class AStarVisualizer:
    MAX_WINDOW = 800
    PANEL_WIDTH = 260
    CANVAS_MARGIN = 8

    # Colors for visualization
    COLOR_OPEN = "#A7C7FF"     # pale blue
    COLOR_CLOSED = "#C2C2C2"   # darker light gray (better contrast)
    COLOR_CURRENT = "#FF8C00"  # dark orange
    COLOR_PATH = "#FF4500"     # red
    COLOR_BRANCH = "#B39DDB"   # muted purple for intersections

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("A* Maze Visualizer")

        self.root.geometry(f"{self.MAX_WINDOW}x{self.MAX_WINDOW}")
        self.root.minsize(self.MAX_WINDOW, self.MAX_WINDOW)
        self.root.maxsize(self.MAX_WINDOW, self.MAX_WINDOW)

        # Apply EB Garamond font across the UI (slightly larger for readability)
        family = "EB Garamond"
        try:
            base_size = 14
            heading_size = 16
            tkfont.nametofont("TkDefaultFont").configure(family=family, size=base_size)
            tkfont.nametofont("TkTextFont").configure(family=family, size=base_size)
            tkfont.nametofont("TkMenuFont").configure(family=family, size=base_size)
            tkfont.nametofont("TkHeadingFont").configure(family=family, size=heading_size, weight="bold")
            # Also affect ttk widgets
            style = ttk.Style(self.root)
            style.configure('.', font=(family, base_size))
            style.configure('TButton', font=(family, base_size))
            style.configure('TLabel', font=(family, base_size))
        except Exception:
            pass

        container = tk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True)

        self.canvas_size = min(self.MAX_WINDOW - self.PANEL_WIDTH - 10, self.MAX_WINDOW - 10)
        self.canvas = tk.Canvas(container, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

        panel = tk.Frame(container, width=self.PANEL_WIDTH)
        panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        panel.pack_propagate(False)

        # Controls
        tk.Label(panel, text="Settings", font=tkfont.nametofont("TkHeadingFont")).pack(anchor="w", pady=(0, 8))

        size_frame = tk.Frame(panel)
        size_frame.pack(fill=tk.X, pady=(0, 6))
        tk.Label(size_frame, text="Maze Size (N × N)").pack(anchor="w")
        self.size_var = tk.IntVar(value=40)
        self.size_scale = tk.Scale(
            size_frame,
            from_=2,
            to=200,      # limit to 200
            resolution=2,
            orient=tk.HORIZONTAL,
            variable=self.size_var,
            length=self.PANEL_WIDTH - 20,
        )
        self.size_scale.pack(anchor="w")

        speed_frame = tk.Frame(panel)
        speed_frame.pack(fill=tk.X, pady=(0, 6))
        tk.Label(speed_frame, text="Animation Speed").pack(anchor="w")
        # Slider 1..100; <=50 linear 0.1..5 steps/tick, >50 exponential up to ~400
        self.speed_var = tk.IntVar(value=60)
        self.speed_scale = tk.Scale(
            speed_frame,
            from_=1,
            to=100,
            resolution=1,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            length=self.PANEL_WIDTH - 20,
        )
        self.speed_scale.pack(anchor="w")

        self.solve_btn = tk.Button(panel, text="Solve (A*)", command=self.on_solve)
        self.solve_btn.pack(fill=tk.X, pady=(0, 4))
        self.pause_btn = tk.Button(panel, text="Pause", state=tk.DISABLED, command=self.on_pause_resume)
        self.pause_btn.pack(fill=tk.X, pady=(0, 8))
        self.stop_btn = tk.Button(panel, text="Stop/Reset", command=self.on_stop_reset)
        self.stop_btn.pack(fill=tk.X, pady=(0, 8))

        # Info area
        self.info_steps = tk.StringVar(value="Steps: -")
        self.info_time = tk.StringVar(value="Time: - ms")
        self.info_status = tk.StringVar(value="Status: ready")
        ttk.Label(panel, textvariable=self.info_steps).pack(anchor="w")
        ttk.Label(panel, textvariable=self.info_time).pack(anchor="w")
        ttk.Label(panel, textvariable=self.info_status).pack(anchor="w", pady=(4, 0))

        # State
        self.grid: Optional[List[List[int]]] = None
        self.start: Optional[Tuple[int, int]] = None
        self.end: Optional[Tuple[int, int]] = None
        self.cell_px: float = 0.0
        self.offset_x: float = 0.0
        self.offset_y: float = 0.0

        # Animation control
        self._running = False
        self._paused = False
        self._gen = None  # type: ignore[var-annotated]
        self._current_item: Optional[int] = None
        self._tick_ms = 16  # ~60 FPS
        self._speed_accum = 0.0

        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.root.update_idletasks()

    # ----------------------- UI Actions -----------------------
    def on_solve(self) -> None:
        if self._running:
            # Ignore if an animation is in progress
            return
        n = int(self.size_var.get())
        if n % 2:
            n -= 1
            self.size_var.set(max(2, n))
        self.grid, self.start, self.end = generate_maze(n, n)
        self._prepare_draw_params(n, n)
        self._draw_maze()
        self.info_status.set("Status: running A*")
        self.info_steps.set("Steps: 0")
        self.info_time.set("Time: - ms")

        # Start generator for animation
        assert self.grid and self.start and self.end
        self._gen = self._astar_steps(self.grid, self.start, self.end)
        self._running = True
        self._paused = False
        self._t0 = time.perf_counter()
        self.pause_btn.config(state=tk.NORMAL, text="Pause")
        self._speed_accum = 0.0
        self._animate_step()

    def on_pause_resume(self) -> None:
        if not self._running:
            return
        if not self._paused:
            self._paused = True
            self.pause_btn.config(text="Resume")
            self.info_status.set("Status: paused")
        else:
            self._paused = False
            self.pause_btn.config(text="Pause")
            self.info_status.set("Status: running A*")
            # Kick animation loop again
            self._animate_step()

    def on_stop_reset(self) -> None:
        # Stop animation if running; otherwise just reset overlays/info
        if self._running or self._paused:
            self._running = False
            self._paused = False
            self._gen = None
            self.pause_btn.config(state=tk.DISABLED, text="Pause")
            self.info_status.set("Status: stopped")
        # Redraw maze to clear overlays
        if self.grid is not None:
            self._draw_maze()
        self.info_steps.set("Steps: -")
        self.info_time.set("Time: - ms")

    def _animate_step(self) -> None:
        if not self._running or self._gen is None:
            return
        if self._paused:
            return
        # Convert slider to fractional steps per tick
        v = int(self.speed_var.get())
        if v <= 50:
            steps_per_tick = 0.1 + (v / 50.0) * (5.0 - 0.1)
        else:
            x = (v - 50) / 50.0
            base = 5.0
            steps_per_tick = base * ((400.0 / base) ** x)
        self._speed_accum += steps_per_tick
        steps_this_frame = int(self._speed_accum)
        self._speed_accum -= steps_this_frame
        if steps_this_frame <= 0:
            # ensure some progress over time even at very low settings
            self.root.after(self._tick_ms, self._animate_step)
            return
        finished = False
        for _ in range(max(1, steps_this_frame)):
            try:
                action = next(self._gen)
            except StopIteration as e:  # e.value may contain (prev, cols, end_idx)
                finished = True
                break
            self._apply_action(action)
        if finished:
            # Draw final path and update metrics
            prev, cols, end_idx, expansions = self._final_state  # type: ignore[attr-defined]
            path = _reconstruct_path_idx(prev, end_idx, cols)
            self._draw_final_path(path)
            t_ms = (time.perf_counter() - self._t0) * 1000.0
            self.info_time.set(f"Time: {t_ms:.2f} ms")
            self.info_steps.set(f"Steps: {max(0, len(path)-1)} (expansions: {expansions})")
            self.info_status.set("Status: completed")
            self._running = False
            self._paused = False
            self.pause_btn.config(state=tk.DISABLED, text="Pause")
            return
        # Schedule next animation frame
        self.root.after(self._tick_ms, self._animate_step)

    # ----------------------- Drawing -----------------------
    def _prepare_draw_params(self, rows: int, cols: int) -> None:
        w = max(1, self.canvas.winfo_width())
        h = max(1, self.canvas.winfo_height())
        if w <= 1 or h <= 1:
            w = h = self.canvas_size
        m = self.CANVAS_MARGIN
        usable_w = max(1, w - 2 * m)
        usable_h = max(1, h - 2 * m)
        size = min(usable_w / max(1, cols), usable_h / max(1, rows))
        maze_w = cols * size
        maze_h = rows * size
        self.offset_x = (w - maze_w) / 2
        self.offset_y = (h - maze_h) / 2
        self.cell_px = size

    def _clear_canvas(self) -> None:
        self.canvas.delete("all")

    def _cell_rect(self, r: int, c: int, shrink: float = 0.12) -> Tuple[float, float, float, float]:
        size = self.cell_px
        x0 = self.offset_x + c * size
        y0 = self.offset_y + r * size
        x1 = x0 + size
        y1 = y0 + size
        dx = dy = size * shrink
        return x0 + dx, y0 + dy, x1 - dx, y1 - dy

    def _draw_maze(self) -> None:
        if self.grid is None:
            return
        self._clear_canvas()
        rows, cols = len(self.grid), len(self.grid[0])
        self._prepare_draw_params(rows, cols)
        size = self.cell_px
        x0, y0 = self.offset_x, self.offset_y
        x1, y1 = x0 + cols * size, y0 + rows * size
        self.canvas.create_rectangle(x0, y0, x1, y1)

        # Draw internal walls
        for r in range(rows):
            for c in range(cols):
                cell = self.grid[r][c]
                cx0, cy0 = x0 + c * size, y0 + r * size
                cx1, cy1 = cx0 + size, cy0 + size
                if cell & E:
                    self.canvas.create_line(cx1, cy0, cx1, cy1)
                if cell & S:
                    self.canvas.create_line(cx0, cy1, cx1, cy1)

        # Start and end markers
        if self.start and self.end:
            sx0, sy0, sx1, sy1 = self._cell_rect(*self.start, shrink=0.25)
            ex0, ey0, ex1, ey1 = self._cell_rect(*self.end, shrink=0.25)
            self.canvas.create_oval(sx0, sy0, sx1, sy1, fill="#FFD700", outline="")
            self.canvas.create_oval(ex0, ey0, ex1, ey1, fill="#DC143C", outline="")

        # Clear overlays
        self.canvas.delete("open")
        self.canvas.delete("closed")
        self.canvas.delete("current")
        self.canvas.delete("path")

    def _fill_cell(self, r: int, c: int, color: str, tag: str) -> int:
        x0, y0, x1, y1 = self._cell_rect(r, c)
        return self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="", tags=(tag,))

    def _draw_current(self, r: int, c: int) -> None:
        if self._current_item is not None:
            # Turn previous current to closed color (it should already be closed though)
            self.canvas.delete(self._current_item)
        self._current_item = self._fill_cell(r, c, self.COLOR_CURRENT, "current")

    def _draw_final_path(self, path: List[Tuple[int, int]]) -> None:
        if not path:
            return
        points: List[float] = []
        size = self.cell_px
        x0, y0 = self.offset_x, self.offset_y
        for r, c in path:
            x = x0 + c * size + size / 2
            y = y0 + r * size + size / 2
            points.extend([x, y])
        self.canvas.create_line(*points, fill=self.COLOR_PATH, width=max(2, int(size / 3)),
                                capstyle=tk.ROUND, joinstyle=tk.ROUND, tags=("path",))

    def _on_canvas_resize(self, event: tk.Event) -> None:  # type: ignore[name-defined]
        if self.grid is None:
            return
        self._draw_maze()

    # ----------------------- A* Animation -----------------------
    def _apply_action(self, action: Tuple[str, object]) -> None:
        kind, payload = action
        if kind == "open_add":
            for i in payload:  # type: ignore[assignment]
                r, c = divmod(i, self._cols)
                self._fill_cell(r, c, self.COLOR_OPEN, "open")
        elif kind == "closed_add":
            for i in payload:
                r, c = divmod(i, self._cols)
                self._fill_cell(r, c, self.COLOR_CLOSED, "closed")
        elif kind == "branch":
            for i in payload:
                r, c = divmod(i, self._cols)
                self._fill_cell(r, c, self.COLOR_BRANCH, "branch")
        elif kind == "current":
            i = payload  # type: ignore[assignment]
            r, c = divmod(i, self._cols)
            self._draw_current(r, c)
        elif kind == "finish":
            # store final state for the outer loop to render path
            self._final_state = payload  # type: ignore[attr-defined]

    def _astar_steps(self, grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]):
        rows, cols = len(grid), len(grid[0])
        self._cols = cols
        total = rows * cols
        def idx(r: int, c: int) -> int:
            return r * cols + c
        start_i = idx(*start)
        end_i = idx(*end)

        def h_idx(a: int, b: int) -> int:
            ar, ac = divmod(a, cols)
            br, bc = divmod(b, cols)
            return abs(ar - br) + abs(ac - bc)

        g = array('i', [10**9] * total)
        g[start_i] = 0
        prev = array('i', [-1] * total)
        open_heap: List[Tuple[int, int, int]] = []
        counter = 0
        heapq.heappush(open_heap, (h_idx(start_i, end_i), counter, start_i))
        in_open = bytearray(total)
        in_open[start_i] = 1
        closed = bytearray(total)

        expansions = 0

        # Initial visuals
        yield ("open_add", [start_i])

        while open_heap:
            _, _, i = heapq.heappop(open_heap)
            if closed[i]:
                continue  # skip entries that are outdated
            yield ("current", i)

            if i == end_i:
                # Signal finish and pass data for path reconstruction
                yield ("finish", (prev, cols, end_i, expansions))
                return

            closed[i] = 1

            r, c = divmod(i, cols)
            cell = grid[r][c]

            # Explore 4-neighbors
            def relax(ni: int) -> None:
                nonlocal counter
                tentative = g[i] + 1
                if tentative < g[ni]:
                    g[ni] = tentative
                    prev[ni] = i
                    if not in_open[ni]:
                        counter += 1
                        heapq.heappush(open_heap, (tentative + h_idx(ni, end_i), counter, ni))
                        in_open[ni] = 1
                        _open_add.append(ni)
                # If already in open and better, we still push a new tuple;
                # outdated tuple will be ignored when popped due to 'closed' check above.

            _open_add: List[int] = []
            if c + 1 < cols and not (cell & E):
                relax(i + 1)
            if c - 1 >= 0 and not (cell & W):
                relax(i - 1)
            if r + 1 < rows and not (cell & S):
                relax(i + cols)
            if r - 1 >= 0 and not (cell & N):
                relax(i - cols)

            if _open_add:
                yield ("open_add", _open_add)

            expansions += 1

            # Determine if this cell is an intersection (>=3 exits)
            exits = 0
            if c + 1 < cols and not (cell & E):
                exits += 1
            if c - 1 >= 0 and not (cell & W):
                exits += 1
            if r + 1 < rows and not (cell & S):
                exits += 1
            if r - 1 >= 0 and not (cell & N):
                exits += 1
            if exits >= 3:
                yield ("branch", [i])
            else:
                yield ("closed_add", [i])

        # If we exit loop without reaching end, still finish
        yield ("finish", (prev, cols, end_i, expansions))


def main() -> None:
    root = tk.Tk()
    app = AStarVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
