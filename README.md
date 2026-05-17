# Coding Challenge — Tower of Hanoi & Conway's Game of Life

Terminal demos written in Python 3 for the RISC-V High Precision Code Base and Reach project.
Demonstrates **recursion** (Tower of Hanoi) and **iteration** (Conway's Game of Life) with ASCII graphics.

---

## Requirements

- Python 3.6+
- No external dependencies

---

## Usage

### Tower of Hanoi

```bash
python3 demo.py hanoi [--disks N] [--speed S]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--disks N` | `4` | Number of disks to solve (1–10) |
| `--speed S` | `0.4` | Seconds to pause between moves |

**Examples:**
```bash
python3 demo.py hanoi
python3 demo.py hanoi --disks 5
python3 demo.py hanoi --disks 3 --speed 0.2
```

---

### Conway's Game of Life

```bash
python3 demo.py life [--gens N] [--speed S]
```

Grid is fixed at 40×20 cells.

| Flag | Default | Description |
|------|---------|-------------|
| `--gens N` | `60` | Number of generations to simulate |
| `--speed S` | `0.1` | Seconds per generation |

**Examples:**
```bash
python3 demo.py life
python3 demo.py life --gens 100 --speed 0.05
```

---

## What to look for

- **Hanoi** — watch the move counter tick toward 2^N - 1 as the recursive solution plays out.
- **Life** — the simulation seeds three classic patterns: a **glider** (travels diagonally), a **blinker** (oscillates every 2 generations), and a **block** (still life that never changes). All driven by four simple rules and a nested iteration over every cell.
