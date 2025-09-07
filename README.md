# Pathfinder-Visualization
# Maze Solver Visualizer — A*, BFS, DFS (Tkinter)
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
   - A*: `python A_star.py`
   - BFS: `python BFS.py`
   - DFS: `python DFS.py`

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

------------------------------------------------------------

## Bahasa Indonesia

### Apa ini?
Proyek kecil ini adalah visualizer algoritma pencarian jalur di labirin (maze) menggunakan Python + Tkinter. Anda dapat melihat bagaimana A*, BFS, dan DFS menjelajah sel dari waktu ke waktu, dan membandingkan jalur yang ditemukan serta performanya.

Fokusnya untuk pembelajaran: tampilannya sederhana, kontrolnya minim, dan cocok untuk pemula yang ingin “melihat” cara kerja algoritma graf.

### Tujuan
- Memperkenalkan A*, BFS, dan DFS dengan visual yang jelas.
- Menyediakan alat latihan interaktif bagi siswa/guru/siapa saja yang penasaran dengan algoritma pencarian.
- Memberi gambaran dampak pilihan algoritma terhadap kecepatan dan kualitas jalur.

### Fitur Utama
- Pembuatan labirin acak (maksimal 200×200) dengan algoritma recursive-backtracker.
- Visualisasi eksplorasi langkah‑demi‑langkah:
  - Open/frontier (biru muda), Closed/visited (abu‑abu agak gelap), Current (oranye), Intersection/branch (ungu), Final path (merah).
- Kontrol animasi: Solve, Pause/Resume, Stop/Reset.
- Pengaturan ukuran labirin dan kecepatan animasi.
- Metrik: Steps (panjang jalur) dan Time (ms), plus banyaknya expansions (simpul diekspansi).

### Berkas dalam repo
- `A_star.py` — Visualizer A*.
- `BFS.py` — Visualizer BFS (First-In-First-Out queue).
- `DFS.py` — Visualizer DFS (stack).

> Catatan: File `maze_solver.py` tidak digunakan di README ini sesuai permintaan Anda.

### Cara Menjalankan
Persyaratan:
- Python 3.8+ (Windows/macOS/Linux).
- Tkinter tersedia (di Windows/macOS biasanya sudah termasuk; di Linux: `sudo apt install python3-tk`).
- (Opsional) Font “EB Garamond” agar tampilan sesuai; jika tidak ada, sistem akan memakai font bawaan.

Langkah cepat:
1. Buka terminal di folder proyek.
2. Jalankan salah satu visualizer di bawah:
   - A*: `python A_star.py`
   - BFS: `python BFS.py`
   - DFS: `python DFS_.py`

Jika perintah `python` tidak ditemukan, coba `python3`.

### Ringkasan Algoritma (Mendalam)
Labirin direpresentasikan sebagai graf kisi (grid) tak berbobot. Tiap sel terhubung ke tetangga jika tidak ada dinding di antaranya. Titik awal di kiri‑atas, titik akhir di kanan‑bawah.

1) BFS (Breadth‑First Search)
- Strategi: jelajah berlapis (level by level) menggunakan antrian FIFO.
- Properti: selalu menemukan jalur terpendek pada graf tak berbobot (optimal), lengkap (complete).
- Kompleksitas: waktu O(V+E), ruang O(V). Pada grid padat, keduanya bisa besar.
- Ciri visual: gelombang ekspansi yang “membulat”, jalur yang dihasilkan memang terpendek.

2) DFS (Depth‑First Search)
- Strategi: menyelam sedalam mungkin menggunakan tumpukan (LIFO).
- Properti: tidak menjamin jalur terpendek, tetapi sering cepat menemukan “sebuah” jalur.
- Kompleksitas: waktu O(V+E), ruang bisa sedalam panjang jalur (O(V) terburuk) namun sering lebih hemat dibanding BFS pada graf lebar.
- Ciri visual: satu cabang panjang, sering mundur (backtrack) ketika buntu.

3) A* (A‑Star)
- Strategi: perluasan simpul berdasar biaya `f(n) = g(n) + h(n)`.
  - `g(n)`: biaya dari start ke n (jumlah langkah).
  - `h(n)`: heuristik ke goal. Di sini digunakan Manhattan distance (|dx| + |dy|) yang admissible pada grid 4‑arah.
- Properti: dengan heuristik admissible & konsisten, A* optimal dan biasanya jauh lebih sedikit ekspansi dibanding BFS.
- Kompleksitas: bergantung pada kualitas heuristik; bisa mendekati BFS bila `h` lemah, atau sangat efisien bila `h` informatif.
- Ciri visual: frontier “mengarah” ke goal, ekspansi cenderung selektif.

Tentang Implementasi
- Struktur data: `prev` (parent) untuk rekonstruksi jalur, serta penanda `open/closed` sesuai algoritma.
- BFS memakai queue; DFS memakai stack; A* memakai priority queue (min‑heap) dengan prioritas f.
- Visualisasi menyorot: open (biru), closed (abu‑abu), current (oranye), persimpangan (ungu), dan final path (merah).
