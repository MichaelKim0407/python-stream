from stream.functions.bytes import decode


def test_decode():
    assert tuple(decode((b'abc', b'123'))) == ('abc', '123')
