from ..ks import num
import math
import hypothesis
import hypothesis.strategies as st

@hypothesis.given(st.integers(), st.integers())
def test_bezout(a: int, b: int):
    d, m, n = num.bezout(a, b)
    assert d == m*a + n*b == math.gcd(a, b)

def test_bezout_zero():
    d, m, n = num.bezout(0, 0)
    assert d == m == n == 0

def test_crt():
    assert num.crt({3: 0, 4: 3, 5: 4}) == 39
