

class Permutation(object):
    def __init__(self, _set, mapping):
        assert not (set(mapping) - _set)
        assert not (set(mapping.itervalues()) - _set)
        assert len(mapping) == len(set(mapping.itervalues()))

        self.set = _set
        self.mapping = dict((k, v) for k, v in mapping.iteritems() if k != v)
        self._sequences = None

    def __unicode__(self):
        if not self.sequences:
            return u'()'
        return u''.join(
            u'({0})'.format(u', '.join(map(unicode, seq)))
            for seq in self.sequences
        )

    def __repr__(self):
        return unicode(self)

    @property
    def sequences(self):
        if self._sequences is not None:
            return self._sequences
        affected = set(self.mapping)
        if not affected:
            self._sequences = ()
            return self._sequences

        fullseq = [[]]
        item = affected.pop()
        while affected:
            fullseq[-1].append(item)
            if self.mapping[item] not in affected:
                fullseq.append([])
                item = affected.pop()
            else:
                item = self.mapping[item]
                affected.remove(item)
        fullseq[-1].append(item)

        self._sequences = tuple(tuple(S) for S in fullseq)
        return self._sequences

    def __eq__(self, perm):
        return self.mapping == perm.mapping

    def __ne__(self, perm):
        return self.mapping != perm.mapping

    def __invert__(self):
        return Permutation(
            self.set.copy(), dict((v, k) for k, v in self.mapping.iteritems()))

    def __mul__(self, perm):
        if not self.sequences:
            return perm

        assert self.set == perm.set

        new_set = self.set.copy()
        new_mapping = dict(
            (x,
             perm.mapping.get(self.mapping[x], self.mapping[x])
             if x in self.mapping else
             perm.mapping.get(x, x))
            for x in self.set
        )

        return Permutation(new_set, new_mapping)
