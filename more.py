from itertools import islice, chain, repeat, starmap, tee
from functools import partial
from collections.abc import Sequence
from collections import deque
from time import monotonic
from operator import sub

_marker = object()

class TimeLimited:
    def __init__(self, limit_seconds, iterable):
        if limit_seconds < 0:
            raise ValueError('limit_seconds must be positive.')
        self.limit_seconds = limit_seconds
        self._iterable = iter(iterable)
        self._start_time = monotonic()
        self.time_out = False

    def __iter__(self):
        return self
    
    def __next__(self):
        item = next(self._iterable)
        if monotonic() - self._start_time > self.limit_seconds:
            self.time_out = True
            raise StopIteration
        return item


class SequenceView(Sequence):
    def __init__(self, target):
        if not isinstance(target, Sequence):
            raise TypeError
        self._target = target

    def __getitem__(self, index):
        return self._target[index]
    
    def __len__(self):
        return len(self._target)
    
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self._target)


def take(iterable, n):
    return list(islice(iterable, n))

def chunked(iterable, n, strict=False):
    iterator = iter(partial(take, iter(iterable), n), [])
    if strict:
        if n is None:
            raise ValueError("n can't be None when strict is True")
        
        # def rat():
        #     for chunk in iterator:
        #         if len(chunk) != n:
        #             raise ValueError('Iterator is not divisible by n')
        #         yield chunk
        # return iter(rat())
        
        if (len(iterable) % n) != 0:
            raise ValueError('Iterator is not divisible by n')

    return iterator

def first(iterable, default=_marker):
    try:
        return next(iter(iterable))
    except StopIteration as e:
        if default == _marker:
            raise ValueError('first() call with empty variable and no default provided.') from e
        else:
            return default

def last(iterable, default=_marker):
    try:
        if isinstance(iterable, Sequence):
            print('isinstance')
            return iterable[-1]
        elif hasattr(iterable, '__reversed__'):
            print('hasattr')
            return next(reversed(iterable))
        else:
            print('deque')
            return deque(iterable, maxlen=1)[-1]
    except (IndexError, StopIteration, TypeError):
        if default == _marker:
            raise ValueError('The last() called on an empty iterable and no default provided.')            
        return default

def nth_or_last(iterable, n, default=_marker):
    # return last(islice(iterable, n+1), default=default)
    return last(take(iterable, n+1), default=default)

def one(iterable, too_short=None, too_long=None):
    it = iter(iterable)
    try:
        first_value = next(it)
    except StopIteration as e:
        raise (
            too_short or ValueError('Too few item im the iterable (expected 1)')
        ) from e

    try:
        second_value = next(it)
    except StopIteration:
        pass
    else:
        raise(too_long or ValueError('Too much items in the iterable, {}, {} and perhaps more'.format(first_value, second_value)))
    
    return first_value

def interleave(*iterable):
    return chain.from_iterable(zip(*iterable))

def repeat_each(iterable, n=2):
    return chain.from_iterable(map(repeat, iterable, repeat(n)))

def raise_(exception, *args):
    raise exception(*args)

def stricktly_n(iterable, n, too_short=None, too_long=None):
    if too_short is None:
        too_short = lambda item_count: raise_(
            ValueError,
            'Too few items in iterable, got {}'.format(item_count)
        )

    if too_long is None:
        too_long = lambda item_count: raise_(
            ValueError,
            'Too much items in iterable, got at least {}'.format(item_count)
        )

    it = iter(iterable)

    for i in range(n):
        try:
            item = next(it)
        except StopIteration:
            too_short(i)
            return
        else:
            yield item
        
    try:
        next(it)
    except StopIteration:
        pass
    else:
        too_long(n+1)

def only(iterable, default=None, too_long=None):
    it = iter(iterable)

    first_item = next(it, default)
    
    try:
        second_item = next(it)
    except StopIteration:
        pass
    else:
        msg = 'Expected exactly one item in the iterable but got {}, {} and perhaps more'.format(first_item, second_item)
        raise too_long or ValueError(msg)

    return first_item
    
def always_reversible(iterable):
    try:
        return reversed(iterable)
    except TypeError:
        return reversed(list(iterable))

def split_after(iterable, pred, max_split=-1):
    if max_split == 0:
        yield list(iterable)
        return
        
    
    it = iter(iterable)
    buf = []
    for item in it:
        buf.append(item)
        # print(max_split, buf)
        if pred(item):
            yield buf
            if max_split == 1:
                yield list(it)
                return
            
            buf = []
            max_split -= 1
        
    if buf:
        yield buf

def split_into(iterable, sizes):
    it = iter(iterable)
    for size in sizes:
        if size is None:
            yield list(it)
            return 
        yield list(islice(it, size))

def map_if(iterable, pred, func, func_else= lambda x:x):
    for item in iterable:
        yield func(item) if pred(item) else func_else(item)

def difference(iterable, func=sub, *, initial=None):
    a, b = tee(iterable)
    try:
        first = [next(b)]
    except StopIteration:
        return iter([])

    if initial is not None:
        first = []

    return chain(first, starmap(func, zip(b, a)))

def value_chain(*args):
    for value in args:
        if isinstance(value, (str, bytes)):
            yield value
            continue
        try:
            yield from value
        except TypeError:
            yield value
