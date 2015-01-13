import group


faces = ('u', 'd', 'r', 'l', 'f', 'b')

movements = {
    'u': ('f', 'l', 'b', 'r'),
    'd': ('f', 'r', 'b', 'l'),
    'r': ('u', 'b', 'd', 'f'),
    'l': ('u', 'f', 'd', 'b'),
    'f': ('u', 'r', 'd', 'l'),
    'b': ('u', 'l', 'd', 'r'),
}

moves = {}
for move, S in movements.iteritems():
    seqs = [
        ['{0}_{1}'.format(move, f) for f in S],
        ['{1}_{0}'.format(move, f) for f in S],
        ['{0}_{1}{2}'.format(move, *sorted((a, b))) for a, b in zip(S, S[1:] + S[:1])],
        ['{0}_{1}{2}'.format(a, *sorted((b, move))) for a, b in zip(S, S[1:] + S[:1])],
        ['{0}_{1}{2}'.format(b, *sorted((a, move))) for a, b in zip(S, S[1:] + S[:1])],
    ]
    P = group.Permutation(seqs)
    name = move.upper()
    moves.update({name: P, '{0}2'.format(name): P * P, '{0}i'.format(name): ~P})

locals().update(moves)
