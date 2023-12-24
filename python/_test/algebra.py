from ..ks.algebra import matrix

import hypothesis as hy
import hypothesis.strategies as hs


def hs_matrix(shape: tuple[int, int]):
    m, n = shape
    size = m * n
    return hs.iterables(
        hs.fractions(max_denominator=13), min_size=size, max_size=size
    ).map(lambda data: matrix.FracMatrix(data, m))


hs_frac_matrices = hs.tuples(hs.integers(1, 5), hs.integers(1, 5)).flatmap(hs_matrix)


@hy.given(hs_frac_matrices)
def test_matrix_lup_hy(m: matrix.FracMatrix):
    l, u, p = m.factor_lup()
    assert l @ u == m.clone().permute_rows(p)


def test_matrix_lup():
    m = matrix.FracMatrix([0, 2, 3, 0, 7, 3, 0, 2, 5, 2, 3, 5], 4)
    l, u, p = m.factor_lup()

    m.permute_rows(p)

    m.display()
    l.display()
    u.display()
    assert l @ u == m


@hy.given(hs_matrix((3, 5)))
def test_matrix_solve_lup_3(out: matrix.FracMatrix):
    m = matrix.FracMatrix([1, -3, 7, -1, 4, 2, 5, 2, 3], 3)
    x = m.solve_lup(out)

    out.display()
    m.display()

    assert m @ x == out


@hy.given(hs_matrix((3, 3)))
def test_matrix_solve_lup(m: matrix.FracMatrix):
    m.solve_lup(m)
