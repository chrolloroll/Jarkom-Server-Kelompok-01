"""
Fungsi determinan & invers matriks 3x3, dipakai bersama oleh Server
dan Client.
"""


def determinant_3x3(m):
    """Determinan matriks 3x3 dengan ekspansi kofaktor baris pertama."""
    a, b, c = m[0]
    d, e, f = m[1]s
    g, h, i = m[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def inverse_3x3(m, tol=1e-9):
    """
    Invers matriks 3x3 menggunakan matriks adjoin (adjugate) dibagi
    determinan. Mengembalikan None jika matriks singular (det ~ 0).
    """
    det = determinant_3x3(m)
    if abs(det) < tol:
        return None

    a, b, c = m[0]
    d, e, f = m[1]
    g, h, i = m[2]

    cofactor = [
        [(e * i - f * h), -(d * i - f * g), (d * h - e * g)],
        [-(b * i - c * h), (a * i - c * g), -(a * h - b * g)],
        [(b * f - c * e), -(a * f - c * d), (a * e - b * d)],
    ]

    adjoint = [[cofactor[col][row] for col in range(3)] for row in range(3)]

    inverse = [[round(adjoint[r][c] / det, 6) for c in range(3)] for r in range(3)]
    return inverse


def matrices_almost_equal(m1, m2, tol=1e-4):
    """Membandingkan dua matriks (atau dua None) dengan toleransi floating point."""
    if m1 is None or m2 is None:
        return m1 == m2
    for r in range(len(m1)):
        for c in range(len(m1[0])):
            if abs(m1[r][c] - m2[r][c]) > tol:
                return False
    return True
