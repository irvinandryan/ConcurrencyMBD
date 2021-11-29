import random
from collections import *

class Transaction:

    def __init__(self, name, f):
        self.name = name
        self._f = f

    def init(self):
        self._x = self._f()
        self._v = next(self._x)
        self._d = False

    def process(self, cont):
        if self._d:
            return True
        try:
            self._v = self._x.send(cont(self._v))
            return False
        except StopIteration:
            self._d = True
            return True

class Rollback(RuntimeError):
    pass

class Timestamp:
    __slots__ = ('v', 'rt', 'wt')

    def __init__(self, *param):
        if len(param) == 1:
            o = param[0]
            self.v = o.v
            self.rt = o.rt
            self.wt = o.wt
        elif len(param) == 3:
            self.v, self.rt, self.wt = param
        else:
            raise TypeError('error syntax, harus 3 argument')

    def __str__(self):
        return f'({self.v!s}, {self.rt!s}, {self.wt!s})'

    def __repr__(self):
        return f'Timestamp({self.v!r}, {self.rt!r}, {self.wt!r})'

def process_transaction(*t):

    data = {
        'A': deque([Timestamp(0, -1, -1)]),
        'B': deque([Timestamp(0, -1, -1)]),
        'C': deque([Timestamp(0, -1, -1)]),
        'D': deque([Timestamp(0, -1, -1)]),
    }

    ts = 0
    m = {i: x for i, x in enumerate(t)}
    TS = {i: None for i in range(len(t))}

    def cont(i):
        def f(v):
            op, args = v
            if op == Read:
                print(f'R{m[i].name} pada {args[0]}')
                t = TS[i]
                for x in data[args[0]]:
                    if x.wt > t:
                        break
                    r = x
                r.rt = max(r.rt, t)
                return r.v
            elif op == Write:
                print(f'W{m[i].name} pada {args[0]}')
                t = TS[i]
                l = data[args[0]]
                for x in l:
                    if x.wt > t:
                        break
                    r = x
                if t < r.rt:
                    raise Rollback()
                if t == r.wt:
                    r.v = args[1]
                else:
                    r = Timestamp(r)
                    r.rt = r.wt = t
                    r.v = args[1]
                    for i_, x in enumerate(l):
                        if x.wt > t:
                            l.insert(i_, r)
                            break
                    else:
                        l.append(r)
            elif op == Commit:
                print(f'C{m[i].name} pada {TS[i]}')
                pass
        return f

    while m:
        i = random.sample(m.keys(), 1)[0]
        x = m[i]
        try:
            if TS[i] is None:
                print(f'T{x.name} mulai pada timestamp {ts}')
                TS[i] = ts
                ts += 1
                x.init()
            if x.process(cont(i)):
                del m[i]
        except Rollback:
            print(f'T{x.name} rollback')
            t = TS[i]
            for l in data.values():
                for i_ in range(len(l)):
                    if l[i_].wt == t:
                        del l[i_]
                        break
            TS[i] = None

if __name__ == '__main__':
    random.seed(0xc12af7ed)

    Read = 1
    Write = 2
    Commit = 3

    def T1():
        a = (yield (Read, ('A',)))
        b = (yield (Read, ('B',)))
        a -= 1
        b += 1
        yield (Write, ('A', a))
        yield (Write, ('B', b))
        yield (Commit, ())

    def T2():
        a = (yield (Read, ('A',)))
        b = (yield (Read, ('B',)))
        a -= 5
        b *= 2
        yield (Write, ('A', a))
        yield (Write, ('B', b))
        yield (Commit, ())

    def T3():
        d = (yield (Read, ('D',)))
        d += 1
        yield (Write, ('C', 5))
        yield (Write, ('D', d))
        yield (Commit, ())

    process_transaction(
        Transaction('1', T1),
        Transaction('2', T2),
        Transaction('3', T3),
    )

