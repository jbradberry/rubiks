

class Permutation(object):
    def __init__(self, val):
        if isinstance(val, dict):
            keys = set(val)
            values = set(val.itervalues())
            if keys != values:
                raise ValueError("Mapping must be one-to-one and onto.")
            self._mapping = dict((k, v) for k, v in val.iteritems() if k != v)
        elif isinstance(val, (list, tuple)):
            self._mapping = {}
            for seq in val:
                if len(set(seq)) != len(seq):
                    raise ValueError("Sequences must be one-to-one and onto.")
                if any(k in self._mapping for k in seq):
                    raise ValueError("Sequences must be one-to-one and onto.")
                self._mapping.update(
                    (k, v) for k, v in zip(*[seq, seq[1:] + seq[:1]]))
        else:
            raise ValueError("Value must be either a sequence of sequences"
                             " or a mapping.")

    def __unicode__(self):
        if not self._mapping:
            return u'()'
        return u''.join(unicode(S) for S in self.sequences)

    def __repr__(self):
        return unicode(self)

    def __hash__(self):
        return hash(tuple(sorted(self._mapping.items())))

    @property
    def sequences(self):
        keys = set(self._mapping)
        sequences = []
        while keys:
            k = keys.pop()
            seq = [k]
            while self._mapping[k] in keys:
                k = self._mapping[k]
                seq.append(k)
                keys.remove(k)
            if len(seq) > 1:
                sequences.append(tuple(seq))
        return tuple(sequences)

    def __getitem__(self, key):
        return self._mapping.get(key, key)

    def __eq__(self, perm):
        return self._mapping == perm._mapping

    def __ne__(self, perm):
        return self._mapping != perm._mapping

    def __invert__(self):
        return Permutation(
            dict((v, k) for k, v in self._mapping.iteritems())
        )

    def __mul__(self, perm):
        return Permutation(
            dict((k, perm[self[k]])
                 for k in set(self._mapping) | set(perm._mapping))
        )
