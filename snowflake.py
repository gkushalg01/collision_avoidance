import random
import time

# inspiration: https://mathematica.stackexchange.com/questions/39361/how-to-generate-a-random-snowflake

# see https://www.redblobgames.com/grids/hexagons/ for information
# about hexagon grids and coordinate systems

# neighbors in axial coordinates
DIRS = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]

# this cellular automata doesn't just count the number of neighbors
# but rather considers their layout
# but the layout is invariant to reflection and rotation
# each hexagon has 6 neighbors, so the presence or absence of
# neighbors can be indicated with a 6-bit mask
# we make a lookup table to map this 6-bit number to a normalized
# value after considering reflection and rotation
def make_lookup(n):
    def normalize(x):
        s = bin(x | (1 << n))[-n:]
        values = []
        for i in range(n):
            values.append(int(s, 2))
            values.append(int(''.join(reversed(s)), 2))
            s = s[1:] + s[0]
        return min(values)
    lookup = [normalize(x) for x in range(1 << n)]
    distinct = list(sorted(set(lookup)))
    lookup = [distinct.index(x) for x in lookup]
    return lookup

LOOKUP = make_lookup(len(DIRS))

# neighborhood returns the set of currently-on cells plus all
# of their neighboring (off) cells
# this "neighborhood" are all of the cells we need to consider
# when computing one iteration
def neighborhood(cells):
    return {(q + dq, r + dr)
        for q, r in cells for dq, dr in DIRS} | cells

# mask generates the 6-bit mask based on presence or absence
# of the six neighboring cells
def mask(cells, q, r):
    return sum(1 << i for i, (dq, dr) in enumerate(DIRS)
        if (q + dq, r + dr) in cells)

# step executes one iteration, returning a new set of on cells
# `on` and `off` indicate probabilities of an off cell coming on
# and an on cell becoming off based on # and layout of neighbors
def step(cells, on, off):
    result = set()
    # within a single time step, all cells should behave the same
    # (the probabilities are across steps, not within steps)
    on = [random.random() < x for x in on]
    off = [random.random() < x for x in off]
    for p in neighborhood(cells):
        i = LOOKUP[mask(cells, *p)]
        if p in cells:
            if not off[i]:
                result.add(p)
        else:
            if on[i]:
                result.add(p)
    return result

# generate creates one random snowflake based on random rules and
# a single seed cell
# the result is a set of on-cells in axial (q, r) coordinates
def generate(iterations, animate=False):
    # random rules are often duds, so loop until we get something
    while True:
        on = [random.random() for _ in range(len(LOOKUP))]
        off = [random.random() for _ in range(len(LOOKUP))]
        cells = set([(0, 0)])
        for i in range(iterations):
            cells = step(cells, on, off)
            if len(cells) < 2:
                break
            if animate:
                print(render_ascii(cells))
                time.sleep(0.1)
        if len(cells) > 1:
            return cells

# render_ascii produces an ASCII string representing the specified
# snowflake
def render_ascii(cells):
    points = set()
    for q, r in cells:
        x = (q + (r - (r & 1)) // 2) * 2
        y = r
        if y % 2:
            x += 1
        points.add((x, y))
    x0 = min(x for x, y in points)
    y0 = min(y for x, y in points)
    x1 = max(x for x, y in points)
    y1 = max(y for x, y in points)
    ox = (80 - (x1 - x0)) // 2
    oy = (40 - (y1 - y0)) // 2
    x0, x1 = x0 - ox, x1 + ox
    y0, y1 = y0 - oy, y1 + oy
    lines = []
    for y in range(y0, y1+1):
        line = []
        for x in range(x0, x1+1):
            if (x, y) in points:
                line.append('*')
            else:
                line.append(' ')
        lines.append(''.join(line))
    return '\n'.join(lines)

# main just generates and prints random snowflakes forever
def main():
    while True:
        cells = generate(20, animate=True)
        print(render_ascii(cells))
        time.sleep(1)

if __name__ == '__main__':
    main()