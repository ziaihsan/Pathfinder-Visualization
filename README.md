# Pathfinder-Visualization
A small learning‑oriented maze pathfinding visualizer written in Python + Tkinter. It shows how A*, BFS, and DFS explore the maze over time so you can compare their routes and performance.

<img width="912" height="940" alt="Screenshot 2025-09-07 at 21 43 13" src="https://github.com/user-attachments/assets/3fdc6352-4e60-4142-a760-752c9d122ca7" />


### Goals
- Introduce A*, BFS, and DFS with clear visuals.
- Provide an interactive tool for students/teachers/curious learners.
- Show how algorithm choice affects speed and path quality.

### Key Features
- Random maze generation (up to 200×200) via recursive backtracker.
- Step‑by‑step exploration visuals:
  - Open/frontier (light blue), Closed/visited (darker gray), Current (orange), Intersection/branch (purple), Final path (red).
- Animation controls: Solve, Pause/Resume, Stop/Reset.
- Maze size and animation speed sliders.
- Metrics: Steps (path length) and Time (ms), plus expansions count.

### Files in the repo
- `astar.py` — A* visualizer.
- `BFS.py` — BFS visualizer (FIFO queue).
- `DFS_.py` — DFS visualizer (stack). The file name intentionally has an underscore.

### How to Run
Requirements:
- Python 3.8+ (Windows/macOS/Linux).
- Tkinter available (Windows/macOS ship it; on Linux: `sudo apt install python3-tk`).
- (Optional) “EB Garamond” font for the intended look. Without it, system defaults will be used.

Quick start:
1. Open a terminal in the project folder.
2. Run any visualizer:
   - A*: `python astar.py`
   - BFS: `python BFS.py`
   - DFS: `python DFS_.py`

If `python` isn’t found, try `python3`.

### App Controls
- `Maze Size (N × N)`: maze dimension. Even values only, 2–200.
- `Animation Speed`: speed of steps. Left side is slow and smooth; right side increases exponentially to very fast.
- `Solve (…​)`: start the animation for the selected algorithm.
- `Pause` / `Resume`: pause and resume the animation.
- `Stop/Reset`: stop the animation and clear overlays.

### Tips
- Sizes 40–80 are a sweet spot: patterns are visible and still fast.
- For the speed slider >50, growth is exponential; nudge slowly if you still want to watch the process.
- The “branch” (purple) highlight marks cells with ≥3 exits; helpful to reason about intersections.

### Algorithm Notes (Deeper Context)
The maze is modeled as an unweighted grid graph. Two cells are neighbors if there is no wall between them. Start is top‑left, goal is bottom‑right.

1) BFS (Breadth‑First Search)
- Strategy: layer‑by‑layer expansion using a FIFO queue.
- Properties: finds shortest paths in unweighted graphs (optimal), complete.
- Complexity: time O(V+E), space O(V). On dense grids both can be large.
- Visual signature: expanding “wavefront”; the returned path is shortest by hop count.

2) DFS (Depth‑First Search)
- Strategy: dive as deep as possible using a LIFO stack.
- Properties: does not guarantee shortest paths, but often finds a path quickly.
- Complexity: time O(V+E); space up to path depth (O(V) worst‑case) but can be lighter than BFS on wide graphs.
- Visual signature: long branches with backtracking when hitting dead‑ends.

3) A* (A‑Star)
- Strategy: expand nodes by `f(n) = g(n) + h(n)`.
  - `g(n)`: cost from start (step count in this maze).
  - `h(n)`: heuristic to the goal. We use Manhattan distance (|dx| + |dy|), admissible and consistent for 4‑connected grids.
- Properties: with admissible & consistent `h`, A* is optimal and typically explores far fewer nodes than BFS.
- Complexity: depends on heuristic quality; can degrade toward BFS when `h` is weak, or be much faster when `h` is informative.
- Visual signature: the frontier “leans” toward the goal; expansions are selective.

Implementation Highlights
- Data structures: `prev` parent array for path reconstruction, and `open/closed` bookkeeping per algorithm.
- BFS uses a queue; DFS a stack; A* a min‑heap prioritized by `f`.
- Visualization colors: open (blue), closed (gray), current (orange), branch (purple), final path (red).

