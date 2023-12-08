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

def crt():
    pass
