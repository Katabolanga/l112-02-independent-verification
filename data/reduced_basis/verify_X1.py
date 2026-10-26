#!/usr/bin/env python3
# verify_X1.py -- exact checks of the catalogue entry X1_112.std (dimension 112).
# Written for this entry by Claude (Anthropic) for Ivan Gauvin's team, 26 October 2026. Python 3; the exact checks use the
# standard library only (integers and fractions.Fraction); the optional orbit check (--orbit) uses numpy.
#
#   python3 verify_X1.py X1_112.std                       sections, GRAM, generators, theta series
#   python3 verify_X1.py X1_112.std --passage X1_passage_from_roiban.txt genus_class_1.txt
#                                                         also: GRAM = P * G_roiban * P^T with P unimodular
#   python3 verify_X1.py X1_112.std --orbit               also: orbit of a random vector under the generators (numpy)
#
# Checks (each failure raises an explicit error; exit code 0 only if every check passes; no assert, so -O is harmless):
#   * sections in the order of the catalogue entries; DIMENSION 112, DET 1, MINIMAL_NORM 10, KISSING_NUMBER;
#   * GRAM ("112 0" + lower triangle): even diagonal, det = 1 (Bareiss, exact integers), positive definite (exact LDL^T in
#     rationals: all 112 pivots > 0);
#   * SUBGROUP_GENERATORS: integer matrices g with g * GRAM * g^T = GRAM (row convention), exact orders 29, 4, 2, 6 and the
#     order of T; relations listed in NOTES (c2, c6 commute with s29, s4; T^-1 s T and T^2 given as words) are checked;
#   * the kissing number equals the coefficient of q^5 of the extremal theta series of weight 56 (computed here exactly
#     from E4 and Delta); this checks the arithmetic of the KISSING_NUMBER line, NOT the minimum itself.
# The minimum 10 is NOT checked by this script (it is the computer-assisted theorem described in NOTES).
import sys
from fractions import Fraction

ORDER = ["NAME", "DIMENSION", "DET", "GRAM", "DIVISORS", "MINIMAL_NORM", "KISSING_NUMBER", "HERMITE_NUMBER",
         "SUBGROUP_ORDER", "SUBGROUP_NAME", "SUBGROUP_GENERATORS", "PROPERTIES", "REFERENCES", "NOTES", "LAST_LINE"]


class CheckError(Exception):
    pass


def check(label, cond):
    if not cond:
        raise CheckError("FAILED: " + label)
    print("[ok] " + label)


def sections(path):
    secs, order, cur = {}, [], None
    for line in open(path, encoding="ascii"):
        line = line.rstrip("\n")
        if line.startswith("%"):
            cur = line[1:].strip()
            order.append(cur)
            secs[cur] = []
        elif cur is not None:
            secs[cur].append(line)
    return order, secs


def read_gram(lines, n):
    head = lines[0].split()
    check("GRAM header '%d 0'" % n, head == [str(n), "0"])
    rows = [[int(t) for t in l.split()] for l in lines[1:] if l.strip()]
    check("GRAM: %d rows of the lower triangle" % n, len(rows) == n and all(len(r) == i + 1 for i, r in enumerate(rows)))
    G = [[0] * n for _ in range(n)]
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            G[i][j] = G[j][i] = v
    return G


def det_bareiss(M):
    A = [row[:] for row in M]
    n, sign, prev = len(A), 1, 1
    for k in range(n - 1):
        if A[k][k] == 0:
            p = next((i for i in range(k + 1, n) if A[i][k] != 0), None)
            if p is None:
                return 0
            A[k], A[p] = A[p], A[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sign * A[n - 1][n - 1]


def ldl_pivots(G):
    n = len(G)
    A = [[Fraction(x) for x in row] for row in G]
    piv = []
    for k in range(n):
        p = A[k][k]
        piv.append(p)
        if p <= 0:
            return piv
        for i in range(k + 1, n):
            if A[i][k]:
                f = A[i][k] / p
                for j in range(k + 1, n):
                    A[i][j] -= f * A[k][j]
    return piv


def mat_mul(A, B):
    Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(row, col) if a) for col in Bt] for row in A]


def transpose(A):
    return [list(r) for r in zip(*A)]


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def read_generators(lines, n):
    vals = [l for l in lines if l.strip()]
    k = int(vals[0])
    gens, pos = [], 1
    for _ in range(k):
        check("generator header '%d<TAB>%d'" % (n, n), vals[pos].split() == [str(n), str(n)])
        M = [[int(t) for t in vals[pos + 1 + i].split()] for i in range(n)]
        check("generator: %d x %d integer matrix" % (n, n), all(len(r) == n for r in M))
        gens.append(M)
        pos += n + 1
    check("no trailing data in SUBGROUP_GENERATORS", pos == len(vals))
    return gens


def order_of(M, bound=200):
    n = len(M)
    I, P = identity(n), M
    for k in range(1, bound + 1):
        if P == I:
            return k
        P = mat_mul(P, M)
    return None


def theta_extremal_112(N=6):
    # E4 = 1 + 240 sum sigma_3(n) q^n ; Delta = q prod (1 - q^n)^24 ; basis E4^(14-3b) Delta^b of M_56 ; extremal = 1 + O(q^5)
    def sigma3(n):
        return sum(d ** 3 for d in range(1, n + 1) if n % d == 0)
    E4 = [1] + [240 * sigma3(n) for n in range(1, N + 1)]
    P = [1] + [0] * N
    for m in range(1, N + 1):
        for _ in range(24):
            P = [P[i] - (P[i - m] if i >= m else 0) for i in range(N + 1)]
    D = [0] + P[:N]

    def mul(a, b):
        return [sum(a[i] * b[k - i] for i in range(k + 1)) for k in range(N + 1)]

    def pw(a, e):
        r = [1] + [0] * N
        for _ in range(e):
            r = mul(r, a)
        return r
    B = [mul(pw(E4, 14 - 3 * b), pw(D, b)) for b in range(5)]
    c = [Fraction(0)] * 5
    target = [1, 0, 0, 0, 0]
    for m in range(5):                      # triangular: B[b] = q^b + ...
        c[m] = Fraction(target[m] - sum(c[b] * B[b][m] for b in range(m)), B[m][m])
    th = [sum(c[b] * B[b][k] for b in range(5)) for k in range(N + 1)]
    return th


def main(argv):
    if len(argv) < 2:
        print(__doc__ if __doc__ else "usage: verify_X1.py X1_112.std [--passage P.txt G.txt] [--orbit]")
        return 2
    std = argv[1]
    order, secs = sections(std)
    check("sections in the order of the catalogue entries", order == ORDER)
    n = int(secs["DIMENSION"][0])
    check("DIMENSION 112", n == 112)
    check("DET 1", secs["DET"][0].strip() == "1")
    G = read_gram(secs["GRAM"], n)
    check("GRAM: even diagonal", all(G[i][i] % 2 == 0 for i in range(n)))
    check("GRAM: det = 1 (Bareiss, exact)", det_bareiss(G) == 1)
    piv = ldl_pivots(G)
    check("GRAM: positive definite (exact LDL^T, 112 positive pivots), rank 112", len(piv) == n and all(p > 0 for p in piv))
    print("     diagonal of GRAM: min %d, max %d" % (min(G[i][i] for i in range(n)), max(G[i][i] for i in range(n))))
    check("MINIMAL_NORM 10, HERMITE_NUMBER 10, DIVISORS 1", secs["MINIMAL_NORM"][0].strip() == "10" and
          secs["HERMITE_NUMBER"][0].strip() == "10" and secs["DIVISORS"][0].strip() == "1")
    th = theta_extremal_112()
    check("extremal theta series of weight 56 (exact): 1 + 0 q + ... + 0 q^4", th[:5] == [1, 0, 0, 0, 0])
    check("KISSING_NUMBER = coefficient of q^5 = %d" % th[5], int(secs["KISSING_NUMBER"][0]) == th[5])
    gens = read_generators(secs["SUBGROUP_GENERATORS"], n)
    Gt = G
    for idx, g in enumerate(gens):
        check("generator %d: g * GRAM * g^T = GRAM" % (idx + 1), mat_mul(mat_mul(g, Gt), transpose(g)) == Gt)
    names = ["s29", "s4", "c2", "c6", "T"]
    expected = {"s29": 29, "s4": 4, "c2": 2, "c6": 6}
    gd = dict(zip(names, gens))
    for nm in ("s29", "s4", "c2", "c6"):
        check("order of %s = %d" % (nm, expected[nm]), order_of(gd[nm], 60) == expected[nm])
    oT = order_of(gd["T"], 200)
    print("     order of T: %s" % oT)
    I = identity(n)
    minusI = [[-x for x in r] for r in I]
    check("s4^2 = -1", mat_mul(gd["s4"], gd["s4"]) == minusI)
    for c in ("c2", "c6"):
        for s in ("s29", "s4"):
            check("%s commutes with %s" % (c, s), mat_mul(gd[c], gd[s]) == mat_mul(gd[s], gd[c]))
    check("c2 commutes with c6", mat_mul(gd["c2"], gd["c6"]) == mat_mul(gd["c6"], gd["c2"]))
    # relations given in NOTES as words "RELATION: lhs = word" in the letters a = s29, b = s4, A = s29^-1, B = s4^-1
    rel = [l.split(":", 1)[1].strip() for l in secs["NOTES"] if l.startswith("RELATION:")]
    if rel:
        ai = order_of(gd["s29"], 60)
        inv = {"a": gd["s29"], "b": gd["s4"]}
        inv["A"] = gd["s29"]
        for _ in range(ai - 2):
            inv["A"] = mat_mul(inv["A"], gd["s29"])
        inv["B"] = mat_mul(mat_mul(gd["s4"], gd["s4"]), gd["s4"])
        Tinv = gd["T"]
        for _ in range(oT - 2):
            Tinv = mat_mul(Tinv, gd["T"])

        def word(w):
            M = I
            for ch in w:
                M = mat_mul(M, inv[ch])
            return M
        lhs_map = {"T^-1*s29*T": mat_mul(mat_mul(Tinv, gd["s29"]), gd["T"]),
                   "T^-1*s4*T": mat_mul(mat_mul(Tinv, gd["s4"]), gd["T"])}
        for r in rel:
            lhs, w = [t.strip() for t in r.split("=")]
            check("relation %s = word of length %d in s29, s4" % (lhs, len(w)), lhs_map[lhs] == word(w))
    if "--passage" in argv:
        i = argv.index("--passage")
        P = [[int(t) for t in l.split()] for l in open(argv[i + 1], encoding="utf-8") if l.strip() and not l.startswith("#")]
        G0 = [[int(t) for t in l.split()] for l in open(argv[i + 2], encoding="utf-8") if l.strip() and not l.startswith("#")]
        check("passage matrix: 112 x 112, det = +-1 (Bareiss)", len(P) == n and abs(det_bareiss(P)) == 1)
        check("GRAM = P * G_roiban * P^T", mat_mul(mat_mul(P, G0), transpose(P)) == G)
    if "--orbit" in argv:
        import numpy as np
        rng = np.random.default_rng(2026)
        v = rng.integers(-3, 4, size=n).astype(np.int64)
        gm = [np.array(g, dtype=np.int64) for g in gens]
        seen = {v.tobytes()}
        todo = [v]
        while todo:
            w = todo.pop()
            for g in gm:
                u = w @ g
                key = u.tobytes()
                if key not in seen:
                    seen.add(key)
                    todo.append(u)
        print("     orbit of a random vector under the generators: %d vectors" % len(seen))
        check("orbit length 292320 (so the group has order >= 292320)", len(seen) == 292320)
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except CheckError as e:
        print(e)
        sys.exit(1)
