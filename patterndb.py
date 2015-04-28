import math
import array
import cPickle
import os.path
import datetime
import itertools
from operator import mul

import rubiks
import group


_corner_positions = (
    ('u', 'r', 'f'), ('u', 'r', 'b'),
    ('u', 'l', 'f'), ('u', 'l', 'b'),
    ('d', 'r', 'f'), ('d', 'r', 'b'),
    ('d', 'l', 'f'), ('d', 'l', 'b'),
)

_upper_edge_positions = (
    ('u', 'f'), ('u', 'r'), ('u', 'b'), ('u', 'l'), ('f', 'l'), ('f', 'r')
)

_lower_edge_positions = (
    ('b', 'r'), ('b', 'l'), ('d', 'f'), ('d', 'r'), ('d', 'b'), ('d', 'l')
)

_edge_positions = _upper_edge_positions + _lower_edge_positions


def corner_hash(P):
    corners = [set(c) for c in _corner_positions]
    position_vector, rotation_vector = [], []

    # Ignore the final cubie, its position and rotation are fully
    # determined by the other 7.  Unless someone screws with the Cube.
    for corner in _corner_positions[:7]:
        face = '{0}_{1}{2}'.format(corner[0], *sorted(corner[1:]))
        location = tuple(P[face].replace('_', ''))
        loc_set = set(location)

        index = corners.index(loc_set)
        rotation = location.index('u') if 'u' in location else location.index('d')
        del corners[index]

        position_vector.append(index)
        rotation_vector.append(rotation)

    vector = position_vector + rotation_vector
    return reduce(
        lambda acc, new: (acc[0]*new[1] + new[0], 0),
        zip(vector, (8, 7, 6, 5, 4, 3, 2, 3, 3, 3, 3, 3, 3, 3)),
        (0, 0)
    )[0]


def upper_hash(P):
    edges = [set(edge) for edge in _edge_positions]
    position_vector, rotation_vector = [], []

    for edge in _upper_edge_positions:
        face = '{0}_{1}'.format(*edge)
        location = tuple(P[face].split('_'))
        loc_set = set(location)

        index = edges.index(loc_set)
        rotation = 0 if location in _edge_positions else 1
        del edges[index]

        position_vector.append(index)
        rotation_vector.append(rotation)

    vector = position_vector + rotation_vector
    return reduce(
        lambda acc, new: (acc[0]*new[1] + new[0], 0),
        zip(vector, (12, 11, 10, 9, 8, 7, 2, 2, 2, 2, 2, 2)),
        (0, 0)
    )[0]


def lower_hash(P):
    edges = [set(edge) for edge in _edge_positions]
    position_vector, rotation_vector = [], []

    for edge in _lower_edge_positions:
        face = '{0}_{1}'.format(*edge)
        location = tuple(P[face].split('_'))
        loc_set = set(location)

        index = edges.index(loc_set)
        rotation = 0 if location in _edge_positions else 1
        del edges[index]

        position_vector.append(index)
        rotation_vector.append(rotation)

    vector = position_vector + rotation_vector
    return reduce(
        lambda acc, new: (acc[0]*new[1] + new[0], 0),
        zip(vector, (12, 11, 10, 9, 8, 7, 2, 2, 2, 2, 2, 2)),
        (0, 0)
    )[0]


def move_permutations(M, depth, db):
    if depth == 1:
        for name, move in M.iteritems():
            yield (move, name)
    else:
        for P, last in move_permutations(M, depth-1, db):
            if db[P] < depth-1:
                continue
            for name, move in M.iteritems():
                if move[0] == last[0]:
                    continue
                yield (P * move, name)


class DB(object):
    def __init__(self, size, hashf):
        self._size = size
        self._db = array.array('B', [0]) * size
        self.hashf = hashf

    def __getitem__(self, key):
        return self._db[self.hashf(key)] or None

    def __setitem__(self, key, value):
        self._db[self.hashf(key)] = value


e = group.Permutation({})


if not os.path.isfile('patterns.db'):
    corner_db = DB(math.factorial(8) * (3 ** 7), corner_hash)
    upper_db = DB(math.factorial(12) / math.factorial(6) * (2 ** 6), upper_hash)
    lower_db = DB(math.factorial(12) / math.factorial(6) * (2 ** 6), lower_hash)

    dbs = (("corners", corner_db),
           ("upper edges", upper_db),
           ("lower edges", lower_db))

    corner_moves = dict(
        (name,
         group.Permutation(
             dict((k, v) for k, v in P._mapping.iteritems()
                  if len(k) == 4)
         ))
        for name, P in rubiks.moves.iteritems()
    )

    edge_moves = dict(
        (name,
         group.Permutation(
             dict((k, v) for k, v in P._mapping.iteritems()
                  if len(k) == 3)
         ))
        for name, P in rubiks.moves.iteritems()
    )

    moves = {"corners": corner_moves,
             "upper edges": edge_moves,
             "lower edges": edge_moves}

    start = datetime.datetime.utcnow()
    for name, db in dbs:
        depth = 1
        current, new = [e], []
        while current:
            print "Calculating {0} depth {1}.".format(name, depth),
            for P in current:
                for F in moves[name].itervalues():
                    N = P * F
                    if db[N] is None:
                        db[N] = depth
                        new.append(N)

            depth += 1
            current, new = new, []
            print datetime.datetime.utcnow() - start, len(current)

    del current
    del new
    with open('patterns.db', 'wb') as f:
        cPickle.dump((corner_db, upper_db, lower_db), f)
else:
    with open('patterns.db', 'rb') as f:
        corner_db, upper_db, lower_db = cPickle.load(f)
