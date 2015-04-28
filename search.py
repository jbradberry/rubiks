import group, rubiks
from operator import mul


e = group.Permutation({})


def estimate(start, moves):
    return 1 # FIXME


def search(start, moves, bound):
    f = len(moves) + estimate(start, moves)
    if f > bound:
        return f
    if start * reduce(mul, (rubiks.moves[m] for m in moves), e) == e:
        return moves

    minimum = 100
    for m in rubiks.moves:
        t = search(start, moves + (m,), bound)
        if isinstance(t, tuple):
            return t
        if t < minimum:
            minimum = t

    return minimum


def solve(start):
    bound = estimate(start, ())
    while True:
        t = search(start, (), bound)
        if isinstance(t, tuple):
            return t
        if t == 100:
            return None
        bound = t
