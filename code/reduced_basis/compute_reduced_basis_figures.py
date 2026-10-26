# compute_reduced_basis_figures.py -- recounts, in exact integer arithmetic, the figures quoted in README.md (Section 5) and in
# data/reduced_basis/README.md. Python 3, standard library only. MIT licence (see LICENSE).
# usage: python3 compute_reduced_basis_figures.py X1_gram.txt X1_generators.txt X1_passage_from_roiban.txt \
#            lattices/L112.02/gram.txt [certificates/genus_class_1.txt]
import sys
from fractions import Fraction


def mat(p):
    return [[int(t) for t in l.split()] for l in open(p, encoding="utf-8") if l.strip() and not l.startswith("#")]


def mul(A, B):
    Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(r, c)) for c in Bt] for r in A]


def tr(A):
    return [list(r) for r in zip(*A)]


n = 112
G, P, G0 = mat(sys.argv[1]), mat(sys.argv[3]), mat(sys.argv[4])
gens, cur, names = [], [], []
for l in open(sys.argv[2], encoding="utf-8"):
    if l.startswith("#"):
        if cur:
            gens.append(cur)
        cur = []
        names.append(l[1:].strip())
        continue
    if l.strip():
        cur.append([int(t) for t in l.split()])
if cur:
    gens.append(cur)
names = names[1:]
if len(gens) != 5 or any(len(g) != n or any(len(r) != n for r in g) for g in gens):
    sys.exit("unexpected generator file")
d = [G[i][i] for i in range(n)]
print("reduced basis: diagonal entries from %d to %d; %d basis vectors of norm 10; trace %d" % (min(d), max(d), d.count(10), sum(d)))
print("reduced basis: largest |off-diagonal entry| = %d" % max(abs(G[i][j]) for i in range(n) for j in range(n) if i != j))
print("reduced basis: largest |entry| of the generators %s = %d" % (", ".join(names), max(abs(x) for g in gens for r in g for x in r)))
d0 = [G0[i][i] for i in range(n)]
print("published Gram matrix: diagonal entries from %d to %d" % (min(d0), max(d0)))
if len(sys.argv) > 5:
    print("published Gram matrix equal, entry by entry, to %s: %s" % (sys.argv[5].replace("\\", "/").split("/")[-1], G0 == mat(sys.argv[5])))
if mul(mul(P, G0), tr(P)) != G:
    sys.exit("GRAM != P G P^T")
print("GRAM = P * G_published * P^T: True")
A = [[Fraction(x) for x in r] + [Fraction(int(i == j)) for j in range(n)] for i, r in enumerate(P)]
for k in range(n):
    p = next(i for i in range(k, n) if A[i][k] != 0)
    A[k], A[p] = A[p], A[k]
    pv = A[k][k]
    A[k] = [x / pv for x in A[k]]
    for i in range(n):
        if i != k and A[i][k] != 0:
            f = A[i][k]
            A[i] = [x - f * y for x, y in zip(A[i], A[k])]
if any(x.denominator != 1 for r in A for x in r[n:]):
    sys.exit("P is not unimodular")
Pi = [[int(x) for x in r[n:]] for r in A]
mx = 0
for g in gens:
    h = mul(mul(Pi, g), P)
    if mul(mul(h, G0), tr(h)) != G0:
        sys.exit("a transported generator is not an isometry")
    mx = max(mx, max(abs(x) for r in h for x in r))
print("generators written in the published basis (P^-1 g P, isometries checked): largest |entry| = %d" % mx)
