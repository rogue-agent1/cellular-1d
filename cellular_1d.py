#!/usr/bin/env python3
"""cellular_1d - 1D elementary cellular automata (Wolfram rules)."""
import sys

def make_rule(rule_number):
    return {tuple(int(b) for b in f"{i:03b}"): (rule_number >> i) & 1 for i in range(8)}

def step(cells, rule):
    n = len(cells)
    new = [0] * n
    for i in range(n):
        left = cells[(i - 1) % n]
        center = cells[i]
        right = cells[(i + 1) % n]
        new[i] = rule[(left, center, right)]
    return new

def simulate(rule_number, width, steps, init=None):
    rule = make_rule(rule_number)
    if init is None:
        cells = [0] * width
        cells[width // 2] = 1
    else:
        cells = list(init)
    history = [cells[:]]
    for _ in range(steps):
        cells = step(cells, rule)
        history.append(cells[:])
    return history

def render(history):
    lines = []
    for row in history:
        lines.append("".join("#" if c else "." for c in row))
    return "\n".join(lines)

def test():
    # Rule 30
    h = simulate(30, 11, 5)
    assert len(h) == 6
    assert h[0][5] == 1  # center cell
    assert sum(h[0]) == 1
    assert sum(h[1]) > 1  # cells spread
    # Rule 110 (Turing complete)
    h2 = simulate(110, 21, 10)
    assert len(h2) == 11
    # Rule 0 should kill everything
    h3 = simulate(0, 11, 3)
    assert sum(h3[-1]) == 0
    # Rule 255 should fill everything
    h4 = simulate(255, 11, 1)
    assert all(c == 1 for c in h4[1])
    print("OK: cellular_1d")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: cellular_1d.py test")
