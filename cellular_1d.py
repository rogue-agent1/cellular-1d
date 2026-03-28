#!/usr/bin/env python3
"""1D cellular automaton explorer — all 256 Wolfram rules."""
import sys

def evolve(cells, rule):
    n = len(cells); new = [0]*n
    for i in range(n):
        pattern = (cells[(i-1)%n] << 2) | (cells[i] << 1) | cells[(i+1)%n]
        new[i] = (rule >> pattern) & 1
    return new

def classify(rule, steps=200, width=201):
    cells = [0]*width; cells[width//2] = 1
    seen = set(); populations = []
    for _ in range(steps):
        key = tuple(cells)
        if key in seen: return 'Class 1: Fixed point' if len(populations) < 3 else 'Class 2: Periodic'
        seen.add(key)
        populations.append(sum(cells))
        cells = evolve(cells, rule)
    pop_var = max(populations[-50:]) - min(populations[-50:])
    return 'Class 3: Chaotic' if pop_var > width*0.1 else 'Class 4: Complex'

def render(rule, width=79, steps=40, init='center'):
    cells = [0]*width
    if init == 'center': cells[width//2] = 1
    elif init == 'random': import random; cells = [random.randint(0,1) for _ in range(width)]
    for _ in range(steps):
        print(''.join('█' if c else ' ' for c in cells))
        cells = evolve(cells, rule)

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('rule', type=int, nargs='?', default=110)
    p.add_argument('-w', '--width', type=int, default=79)
    p.add_argument('-s', '--steps', type=int, default=40)
    p.add_argument('--classify', action='store_true')
    p.add_argument('--all-classes', action='store_true')
    p.add_argument('--random', action='store_true')
    args = p.parse_args()
    if args.all_classes:
        classes = {}
        for r in range(256):
            c = classify(r); classes.setdefault(c, []).append(r)
        for c, rules in sorted(classes.items()): print(f"{c}: {rules[:10]}{'...' if len(rules)>10 else ''} ({len(rules)} rules)")
    elif args.classify:
        print(f"Rule {args.rule}: {classify(args.rule)}")
    else:
        print(f"Rule {args.rule}")
        render(args.rule, args.width, args.steps, 'random' if args.random else 'center')
