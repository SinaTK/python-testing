from more import take, chunked, first, last, nth_or_last, one, interleave, repeat_each, stricktly_n, only, TimeLimited, SequenceView
from more import always_reversible, split_after, split_into, map_if, difference, value_chain
import pytest
import traceback
from itertools import count, cycle, accumulate
from time import sleep
from operator import add
from sys import version_info


class TestTake:
    def test_simple_take(self):
        assert take(range(1, 10), 5) == [1, 2, 3, 4, 5]

    def test_null_take(self):
        assert take(range(1, 10), 0) == []

    def test_negative_take(self):
        with pytest.raises(ValueError):
            take(range(10), -2)

    def test_take_too_much(self):
        assert take(range(5), 10) == [0, 1, 2, 3, 4]


class TestChunk:
    def test_even(self):
        assert list(chunked('sina7462', 4)) == [['s', 'i', 'n', 'a'], ['7', '4', '6', '2']]
    
    def test_even(self):
        assert list(chunked('sina7462', 3)) == [['s', 'i', 'n'], ['a', '7', '4'], ['6', '2']]

    def test_none(self):
        assert list(chunked('sina7462', None)) == [['s', 'i', 'n', 'a', '7', '4', '6', '2']]

    def test_strict_false(self):
        assert list(chunked('sina7462', 3, strict=False)) == [['s', 'i', 'n'], ['a', '7', '4'], ['6', '2']]

    def test_strict_true(self):
        assert list(chunked('sina7462', 4, strict=True)) == [['s', 'i', 'n', 'a'], ['7', '4', '6', '2']]
        assert list(chunked(['a', 'b', 'c', 'd'], 2, strict=True)) == [['a', 'b'], ['c', 'd']]
        with pytest.raises(ValueError, match='Iterator is not divisible by n'):
            list(chunked('sina7462', 3, strict=True))    
        with pytest.raises(ValueError, match='Iterator is not divisible by n'):
            list(chunked(['a', 'b', 'c', 'd'], 3, strict=True))    

    def test_strict_true_none(self):
        # with pytest.raises(ValueError, match="n can't be None when strict is True"):
        #     list(chunked('sina7462', None, strict=True))    
        try:
            chunked('sina7462', None, strict=True) 
        except ValueError:
            formated_exc = traceback.format_exc()
            assert "n can't be None when strict is True" in formated_exc
        else: 
            self.fail()


class TestFirst:
    def test_more(self):
        assert first([1, 2, 3]) == 1
    
    def test_one(self):
        assert first([1]) == 1

    def test_default(self):
        assert first([], 'yes') == 'yes'

    def test_empty_stop_iteration(self): 
        try:
            first([])
        except ValueError:
            formated_exc = traceback.format_exc()
            assert 'StopIteration' in formated_exc
            assert 'The above exception was the direct cause' in formated_exc
        else:
            self.fail()


class TestLast:
    def test_basic(self):
        cases = [
            (range(4), 3),
            (iter(range(4)), 3),
            (range(1), 0),
            (iter(range(1)), 0),
            ({n: str(n) for n in range(5)}, 4)
        ]
    
        for iterable, expected in cases:
            assert last(iterable) == expected

    def test_default(self):
        cases = [
            (range(4), None, 3),
            ([], None, None),
            ({}, None, None),
            (iter([]), None, None),
        ]
        for iterable,default, expected in cases:
            assert last(iterable, default) == expected

    def test_empty(self):
        for iterable in ([], iter(range(0))):
            try:
                last(iterable)
            except ValueError:
                formated_exc = traceback.format_exc()
                assert 'The last() called on an empty iterable and no default provided.' in formated_exc
            else:
                self.fail()


class TestNthOrLast:
    def test_basic(self):
        assert nth_or_last(range(3), 2) == 2
        assert nth_or_last(range(3), 5) == 2

    def test_default_vlaue(self):
        default = 'beauty'
        assert nth_or_last([], 2, default) == default
        assert nth_or_last(range(0), 2, default) == default
        assert nth_or_last(iter(range(0)), 2, default) == default

    def test_empty_iterable_no_default(self):
        try:
            nth_or_last([], 2)
        except ValueError:
            formated_exc = traceback.format_exc()
            assert 'The last() called on an empty iterable and no default provided.' in formated_exc
        else:
            self.fail()


class TestOne:
    def test_basic(self):
        assert one([2]) == 2
        assert one(['item']) == 'item'

    def test_too_short(self):
        for too_short, exp_type in [
            (None, ValueError),
            (IndexError, IndexError)
        ]:
            try:
                one([], too_short=too_short)
            except exp_type:             
                formated_exc = traceback.format_exc()
                assert 'StopIteration' in formated_exc
                assert 'The above exception was the direct cause' in formated_exc

    def test_too_long(self):
        try:
            one([1, 2])
        except ValueError:
            formated_exc = traceback.format_exc()
            assert 'Too much items in the iterable, 1, 2 and perhaps more' in formated_exc

    def test_too_long_too_long(self):
        with pytest.raises(IndexError):
            one([1, 2], too_long=IndexError)


class TestInterLeave:
    def test_same_size(self):
        actual = list(interleave([1, 4, 7], [2, 5, 8], [3, 6, 9]))
        expected = list(range(1, 10))
        assert actual == expected

    def test_short(self):
        actual = list(interleave([1, 4, 7], [2, 5], [3, 6, 9]))
        expected = list(range(1, 7))
        assert actual == expected

    def test_mixed_type(self):
        l1 = ['s', 'i', 'n', 'a', 't', 'k']
        l2 = '12345678'
        l3 = count()
        actual = list(interleave(l1, l2, l3))
        excpected = ['s', '1', 0, 'i', '2', 1, 'n', '3', 2, 'a', '4', 3, 't', '5', 4, 'k', '6', 5]


class TestRepeatEach:
    def test_default(self):
        assert list(repeat_each('ABC')) == ['A', 'A', 'B', 'B', 'C', 'C']
    
    def test_basic(self):
        assert list(repeat_each('ABC', n=3)) == ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C']

    def test_zero_repeat(self):
        assert list(repeat_each('ABC', n=0)) == []

    def test_negative_repeat(self):
        assert list(repeat_each('ABC', n=-1)) == []

    def test_infinite_repeate(self):
        repeater = repeat_each(cycle('AB'))
        actual = take(repeater, 8)
        expected = ['A', 'A', 'B', 'B', 'A', 'A', 'B', 'B' ]
        assert actual == expected


class TestStricktlyN:
    def test_basic(self):
        assert list(stricktly_n(['1', '2', '3', '4'], 4)) == ['1', '2', '3', '4']

    def tset_too_short_default(self):
        with pytest.raises(ValueError, match='Too few items in iterable, got 4'):
            stricktly_n(['1', '2', '3', '4'], 5)
        
    def test_too_long_default(self):
        with pytest.raises(ValueError, match='Too much items in iterable, got at least 3'):
            list(stricktly_n(['1', '2', '3', '4'], 2))


    def test_too_long_custome(self):
        call_count = 0

        def too_short(item_count):
            nonlocal call_count
            call_count += 1

        iterable = expected = ['1', '2', '3', '4']
        actual = []
        
        for item in stricktly_n(iterable, 5, too_short=too_short):
            actual.append(item)

        assert actual == expected
        assert call_count == 1

    def test_too_long_custom(self):
        call_count = 0

        def too_long(item_count):
            nonlocal call_count
            call_count += 1

        iterable = ['1', '2', '3', '4']
        actual = []

        for item in stricktly_n(iterable, 3, too_long=too_long):
            actual.append(item)
        
        expected =  ['1', '2', '3']

        assert actual == expected
        assert call_count == 1


class TestOnly:
    def test_basic(self):
        assert only([1]) == 1
        assert only([]) == None
        with pytest.raises(ValueError, match='Expected exactly one item in the iterable but got beauty, nice and perhaps more'):
            only(['beauty', 'nice'])
    
    def test_costume_value(self):
        assert only([], 'beauty') == 'beauty'
        assert only([1], 'beauty') == 1
        with pytest.raises(ValueError, match='Expected exactly one item in the iterable but got beauty, nice and perhaps more'):
            only(['beauty', 'nice'], 'funny')

    def test_custome_too_long(self):
        assert only([1], too_long=RuntimeError) == 1
        with pytest.raises(RuntimeError):
            only(['beauty', 'nice'], too_long=RuntimeError)


class TestAlwaysReversible:
    def test_regular_reversed(self):
        assert list(reversed([1,2,3])) == list(always_reversible([1, 2, 3]))
        assert list(reversed(range(10))) == list(always_reversible(range(10)))
        assert list(reversed([1,2,3])).__class__ == list(always_reversible([1, 2, 3])).__class__

    def test_nonsequence_reversed(self):
        assert list(reversed([1,2,3])) == list(always_reversible(iter([1, 2, 3])))
        assert list(reversed(range(10))) == list(always_reversible(iter(range(10))))
        assert list(reversed([1,2,3])).__class__ == list(always_reversible(iter([1, 2, 3]))).__class__


class TestSplitAfter:
    def test_start_with_sep(self):
        actual = list(split_after('xooxoo', pred=lambda c: c=='x'))
        expected = [['x'], ['o', 'o', 'x'], ['o', 'o']]
        assert actual == expected

    def test_end_with_sep(self):
        actual = list(split_after('ooxoox', pred=lambda c: c=='x'))
        expected = [['o', 'o', 'x'], ['o', 'o', 'x']]
        assert actual == expected

    def test_no_sep(self):
        actual = list(split_after('ooxoox', pred= lambda c:c=='a'))
        expected = [['o', 'o', 'x', 'o', 'o', 'x']]
        assert actual == expected

    def test_max_split(self):
        for actual, expexted in [
            (
                split_after('ooxoox', pred= lambda c:c=='x', max_split=0),
                ([['o', 'o', 'x', 'o', 'o', 'x']])
            ),
            (
                split_after('xooxoo', pred= lambda c:c=='x', max_split=1),
                ([['x'],['o', 'o', 'x', 'o', 'o']])
            ),
            (   
                split_after('xooxoo', pred= lambda c:c=='x', max_split=2),
                ([['x'],['o', 'o', 'x'], ['o', 'o']])
            ),
            (
                split_after('xooxoo', pred= lambda c:c=='x', max_split=10),
                ([['x'],['o', 'o', 'x'], ['o', 'o']])
            ),
            (
                split_after('xooxoo', pred= lambda c:c=='a', max_split=1),
                ([['x','o', 'o', 'x', 'o', 'o']])
            )
        ]:
            assert list(actual) == expexted


class TestSplitInto:
    def test_iterable(self):
        iterable = 'sina7462'
        for size, expected in [
            (
                [2, 3, 3],
                [['s', 'i'], ['n', 'a', '7'], ['4', '6', '2']]
            ),
            (
                [1, 2, 3],
                [['s'], ['i','n'], ['a', '7', '4']]
            ),
            (
                [2, 3, 4],
                [['s', 'i'], ['n', 'a', '7'], ['4', '6', '2']]
            ),
            (
                [2, 3, 4, 5],
                [['s', 'i'], ['n', 'a', '7'], ['4', '6', '2'], []]
            ),
            (
                [None, 2, 3],
                [['s', 'i', 'n', 'a', '7', '4', '6', '2']]
            ),
            (
                [1, None, 2],
                [['s'], ['i', 'n', 'a', '7', '4', '6', '2']]
            ),
            (
                [1, 2, None],
                [['s'], ['i', 'n'], ['a', '7', '4', '6', '2']]
            ),
            (
                [2, 3, 3, None],
                [['s', 'i'], ['n', 'a', '7'], ['4', '6', '2'], []]
            ),
            (
                [True, 2, 5, False],
                [['s'], ['i', 'n'], ['a', '7', '4', '6', '2'], []]
            ),
            
            
        ]:
            assert list(split_into(iterable, size)) == expected

    def test_generator_iterable(self):
        iterable = iter(range(1, 10))
        sizes = [1, 2, 3]
        expected = [[1], [2, 3], [4, 5, 6]] 
        expected_ = [7, 8, 9]
        assert list(split_into(iterable, sizes)) == expected
        assert list(iterable) == expected_
        
    def test_generator_sizes(self):
        iterable = [1, 2, 3, 4, 5, 6]
        sizes = (i for i in [0, 1, None, 2, 3])
        expected = [[], [1], [2, 3, 4, 5, 6]]
        expected_ = [2, 3]
        assert list(split_into(iterable, sizes)) == expected
        assert list(sizes) == expected_
        
    def test_invalid_in_size(self):
        with pytest.raises(ValueError):
            list(split_into('sina7462', [1, [], 3]))
        assert list(split_into('sina7462', [1, None, []])) == [['s'], ['i', 'n', 'a', '7', '4', '6', '2']]
                
    def test_empty(self)    :
        assert list(split_into([], [1, 2, 3])) == [[], [], []]
        assert list(split_into([1, 2, 3], [])) == []
        assert list(split_into([], [])) == []
                

class TestMapIf:
    def test_without_func_else(self):
        actual = map_if(range(-3, 4), lambda x: x>2, lambda x: 'too big')
        expected = [-3, -2, -1, 0, 1, 2, 'too big']
        assert list(actual) == expected

    def test_with_func_else(self):
        actual = map_if(range(-3, 3), lambda x: x>0, lambda x: 'pos', lambda x: 'neg')
        expected = ['neg', 'neg', 'neg', 'neg', 'pos', 'pos']
        assert list(actual) == expected
    
    def test_empty(self):
        actual = map_if([], lambda x: x>0, lambda x: 'pos', lambda x: 'neg')
        expected = []
        assert list(actual) == expected

        
class TestTimeLimited:
    def test_basic(self):
        def generator():
            yield 1
            yield 2
            sleep(0.5)
            yield 3
        
        result = TimeLimited(0.1, generator())
        assert list(result) == [1, 2]
        assert result.time_out == True
               
    def test_complete(self):
        result = TimeLimited(1, range(10))
        assert list(result) == list(range(10))
        assert result.time_out == False

    def test_zero_seconds(self):
        result = TimeLimited(0, count())
        assert list(result) == []
        assert result.time_out == True

    def test_invalid_time(self):
        with pytest.raises(ValueError, match='limit_seconds must be positive.'):
            result = TimeLimited(-1, count())


class TestDiffernce:
    def test_normal(self):
        original = [10, 20 ,30 ,40 , 50]
        actual = difference(original)
        expected = [10, 10, 10, 10, 10]
        assert list(actual) == expected

    def test_costum(self):
        original = [10, 20 ,30 ,40 , 50]
        actual = difference(original, add)
        expected = [10, 30, 50, 70, 90]
        assert list(actual) == expected
    
    def test_roundtrip(self):
        original = list(range(100))
        accumulated = list(accumulate(original))
        actual = difference(accumulated)
        assert list(actual) == original
    
    @pytest.mark.skipif(version_info[:2] < (3, 8), reason='The accumulate with initial needs 3.8 or above')
    def test_roundtrip_initial(self):
        original = list(range(100))
        accumulated = list(accumulate(original, initial=100))
        actual = difference(accumulated, initial=100)
        assert list(actual) == original

    def test_one(self):
        assert list(difference([0])) == [0]

    def test_empty(self):
        assert list(difference([])) == []


class TestValueChain:
    def test_empty(self):
        assert tuple(value_chain()) == ()

    def test_basic(self):
        actual = value_chain(1, 2, 'beauty', b'sina', 3, 4)
        assert list((actual)) == [1, 2, 'beauty', b'sina', 3, 4]

    def test_simple_iterables(self):
        actual = value_chain(0, 1, 2, [3, 4], 5, (6, 7), 8, {9:'nine'})
        assert list(actual) == list(range(10))
    
    def test_complex_iterables(self):
        actual = value_chain(
            (1, (2, (3,))),
            [4, [5, 6], 'beaty'],
            {b'nice': {1: 2}}
        )
        expexted = (1, (2, (3,)), 4 , [5, 6], 'beaty', b'nice')
        assert tuple(actual) == expexted


class TestSequenceView:
    def test_init(self):
        view = SequenceView((1, 2, 3))
        assert repr(view) == 'SequenceView((1, 2, 3))'
        with pytest.raises(TypeError):
            SequenceView({})

    def test_update(self):
        seq = [1, 2, 3]
        assert len(SequenceView(seq)) == 3
        assert repr(SequenceView(seq)) == 'SequenceView([1, 2, 3])'

        seq.pop()

        assert len(SequenceView(seq)) == 2
        assert repr(SequenceView(seq)) == 'SequenceView([1, 2])'

    def test_indexing(self):
        seq = 'sinatk'
        view = SequenceView(seq)
        for i in range(-len(seq), len(seq)):
            assert view[i] == seq[i]

    def test_abc_methods(self):
        seq = 'sinatkk'
        view = SequenceView(seq)
        
        assert 's' in view
        assert 'b' not in view
        assert list(reversed(view)) == list(reversed(seq))
        assert view.index('i') == 1
        assert view.count('k') == 2
















