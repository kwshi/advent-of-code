import collections.abc as cabc

def bezout(a: int, b: int) -> tuple[int, int, int]:
    """
    Extended Euclidean algorithm, for evaluating/"certifying" Bézout's lemma. Given `a`, `b`, returns `(d,m,n)` such that `gcd(a,b)==d==m*a+n*b`. `d` is guaranteed to be positive, unless `a==b==0` (in which case `d==m==n==0`).

    https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    """
    m, n, x, y = 1, 0, 0, 1
    while b:
        # a = m a₀ + n b₀, b = x a₀ + y b₀
        q = a // b
        a, m, n, b, x, y = b, x, y, a % b, m-q*x, n-q*y
    s = (0 < a) - (a < 0)
    return (s*a,s*m,s*n)

def crt(system: cabc.Mapping[int, int]) -> int:
    """
    Chinese remainder theorem. Given a mapping from (pairwise coprime) moduli `mᵢ` to remainders `rᵢ`, returns `x` such that `x≡r(mod m)`.

    https://en.wikipedia.org/wiki/Chinese_remainder_theorem
    """
    congruences = [*system.items()]
    if not congruences: return 0
    while len(congruences) >1:
        (m, r), (n, s) = congruences.pop(), congruences.pop()
        d, a, b = bezout(m, n)
        if d != 1:
            raise ValueError(f'CRT moduli not coprime')
        congruences.append((m*n, (s*a*m+r*b*n) % (m*n)))
    [(_, r)] = congruences
    return r
