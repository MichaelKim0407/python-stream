from stream.functions.filter import Filter, remove_empty


def test_filter():
    f = Filter(lambda x: x % 2 == 0)
    assert tuple(f(range(10))) == tuple(range(0, 10, 2))


def test_filter_logical():
    f1 = Filter(lambda x: x % 2 == 0)
    f2 = Filter(lambda x: x % 3 == 0)
    assert tuple((f1 | f2)(range(10))) == (0, 2, 3, 4, 6, 8, 9)
    assert tuple((f1 & f2)(range(10))) == (0, 6)


def test_remove_empty():
    assert tuple(remove_empty(('123', '', 'abc'))) == ('123', 'abc')
