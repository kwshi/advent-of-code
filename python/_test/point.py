from ..ks import point


def test_hash():
    p = point.P2(1, 3)
    s = {p}
    assert p in s
    assert point.P2(1, 3) in s
    assert (1, 3) in s
