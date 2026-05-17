#!/usr/bin/env python3
"""
Tower of Hanoi & Conway's Game of Life — Terminal Demo
Coding challenge for the RISC-V High Precision Code Base and Reach project.

Usage:
    python3 demo.py hanoi [--disks N] [--speed S]
    python3 demo.py life  [--gens N]  [--speed S]
"""

import sys
import os
import time
import argparse


def clear():
    os.system("cls" if os.name == "nt" else "clear")


# ---------------------------------------------------------------------------
# Tower of Hanoi
#
# Classic puzzle: move N disks from peg A to peg C one at a time, never
# placing a larger disk on a smaller one. The self-similar structure makes
# it a natural fit for recursion — to free the bottom disk you first solve
# the same problem on N-1 disks. Optimal move count: 2^N - 1.
# ---------------------------------------------------------------------------

_moves = 0
_speed = 0.4


def draw_hanoi(pegs, n_disks, total_moves):
    clear()
    col_w  = n_disks * 2 + 3
    height = n_disks

    print(f"\n  Tower of Hanoi  —  {n_disks} disks")
    print(f"  Move {_moves:>3} / {total_moves}\n")

    columns = []
    for peg in pegs:
        col = []
        for _ in range(height - len(peg)):
            col.append("|".center(col_w))
        for disk in reversed(peg):
            col.append(f"[{'=' * (disk * 2 - 1)}]".center(col_w))
        columns.append(col)

    for row_idx in range(height):
        print("  " + "  ".join(col[row_idx] for col in columns))

    print("  " + "  ".join(("=" * col_w) for _ in pegs))
    print("  " + "  ".join(name.center(col_w) for name in ("A", "B", "C")))
    print()


def hanoi(n, src, tgt, aux, pegs, n_disks, total_moves):
    # RECURSION: each call solves a smaller version of the same problem
    global _moves

    if n == 1:
        # base case — one disk left, just move it
        disk = pegs[src].pop()
        pegs[tgt].append(disk)
        _moves += 1
        draw_hanoi(pegs, n_disks, total_moves)
        time.sleep(_speed)
    else:
        hanoi(n - 1, src, aux, tgt, pegs, n_disks, total_moves)  # clear the way
        disk = pegs[src].pop()
        pegs[tgt].append(disk)
        _moves += 1
        draw_hanoi(pegs, n_disks, total_moves)
        time.sleep(_speed)
        hanoi(n - 1, aux, tgt, src, pegs, n_disks, total_moves)  # reassemble


def run_hanoi(n_disks, speed):
    global _moves, _speed
    _moves = 0
    _speed = speed

    # pegs are lists; pop/append act as a stack (top of stack = last element)
    pegs = [list(range(n_disks, 0, -1)), [], []]
    total_moves = 2 ** n_disks - 1

    draw_hanoi(pegs, n_disks, total_moves)
    time.sleep(_speed * 2)

    hanoi(n_disks, 0, 2, 1, pegs, n_disks, total_moves)

    print(f"  Solved in {_moves} moves  (optimal for {n_disks} disks).\n")


# ---------------------------------------------------------------------------
# Conway's Game of Life
#
# Grid of cells, each alive or dead. Every generation all cells update at
# once by four rules: die if < 2 or > 3 neighbours, survive at 2-3,
# born at exactly 3. Pure iteration — no recursion anywhere.
# ---------------------------------------------------------------------------

GRID_COLS = 40
GRID_ROWS = 20

GLIDER  = [(0,1),(1,2),(2,0),(2,1),(2,2)]   # travels diagonally
BLINKER = [(0,0),(0,1),(0,2)]               # oscillates period 2
BLOCK   = [(0,0),(0,1),(1,0),(1,1)]         # still life, never changes


def make_grid(rows, cols):
    return [[0] * cols for _ in range(rows)]


def stamp(grid, pattern, row_off, col_off):
    for (r, c) in pattern:
        grid[row_off + r][col_off + c] = 1


def live_neighbours(grid, r, c, rows, cols):
    count = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            # modulo wraps edges so the grid behaves like a torus
            count += grid[(r + dr) % rows][(c + dc) % cols]
    return count


def step_life(grid, rows, cols):
    # ITERATION: visit every cell, write next state into a fresh grid so
    # updates don't corrupt neighbour counts for cells not yet processed
    next_grid = make_grid(rows, cols)
    for r in range(rows):
        for c in range(cols):
            n = live_neighbours(grid, r, c, rows, cols)
            if grid[r][c]:
                next_grid[r][c] = 1 if n in (2, 3) else 0
            else:
                next_grid[r][c] = 1 if n == 3 else 0
    return next_grid


def draw_life(grid, rows, cols, gen):
    clear()
    live = sum(grid[r][c] for r in range(rows) for c in range(cols))
    print(f"\n  Conway's Game of Life  —  Generation {gen:>4}   Live cells: {live}\n")
    for r in range(rows):
        print("  " + " ".join("█" if grid[r][c] else "·" for c in range(cols)))
    print()


def run_life(generations, speed):
    rows, cols = GRID_ROWS, GRID_COLS
    grid = make_grid(rows, cols)

    stamp(grid, GLIDER,  2,         2)
    stamp(grid, BLINKER, rows // 2, cols // 2 - 1)
    stamp(grid, BLOCK,   rows - 5,  cols - 6)

    draw_life(grid, rows, cols, 0)
    for gen in range(1, generations + 1):
        time.sleep(speed)
        grid = step_life(grid, rows, cols)
        draw_life(grid, rows, cols, gen)

    print("  Simulation complete.\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Tower of Hanoi (recursion) and Conway's Game of Life (iteration)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    hp = sub.add_parser("hanoi", help="Animated Tower of Hanoi solver")
    hp.add_argument("--disks", type=int,   default=4,   help="Number of disks (1-10, default: 4)")
    hp.add_argument("--speed", type=float, default=0.4, help="Seconds per move (default: 0.4)")

    lp = sub.add_parser("life", help="Conway's Game of Life simulation")
    lp.add_argument("--gens",  type=int,   default=60,  help="Generations (default: 60)")
    lp.add_argument("--speed", type=float, default=0.1, help="Seconds per generation (default: 0.1)")

    args = parser.parse_args()

    if args.cmd == "hanoi":
        if not (1 <= args.disks <= 10):
            sys.exit("--disks must be between 1 and 10.")
        run_hanoi(args.disks, args.speed)

    elif args.cmd == "life":
        run_life(args.gens, args.speed)


if __name__ == "__main__":
    main()
