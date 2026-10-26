# parite_x1_rep_v1.py -- paquet de replication X1 pour MACHINE_B (agent Claude n° 121, 26 oct. 2026). Code ecrit ici.
# PARITE DU RECOLLEMENT (hypothese Glue.parity de ChainX1.lean) : N x + N'(phi x) = 0 mod 4 pour tout x, c'est-a-dire
#   D = G_L - f G f^t a ses 56 coefficients diagonaux = 0 mod 4 et ses 1 540 coefficients hors diagonale = 0 mod 2.
# MEME CALCUL que le bloc « parite » de verdict_x1_v3.py (agent 119, 9 h 33 : 56 + 1 540 congruences vraies sur 1 596), mais en
# BIBLIOTHEQUE STANDARD SEULE (lecture du .npz par zipfile + en-tete .npy, entiers Python exacts) et chemins en argument.
# Controles annexes (entiers exacts) : G et G_L symetriques et paires, f de taille 56 x 56.
# Usage : python3 -I parite_x1_rep_v1.py STRUCTURE_X1_NPZ L56_GRAM_TXT    (0 = BILAN : OK ; 1 = ECHEC ; 2 = donnee manquante)
import ast, hashlib, os, struct, sys, zipfile

if len(sys.argv) != 3:
    print("usage : parite_x1_rep_v1.py STRUCTURE_X1_NPZ L56_GRAM_TXT", flush=True); sys.exit(2)
FST, FG = sys.argv[1:3]
manq = [p for p in (FST, FG) if not os.path.isfile(p)]
if manq:
    print("DONNEES MANQUANTES (arret avant tout calcul) :", manq, flush=True); sys.exit(2)
_DT = {"<i8": ("q", 8), "<i4": ("i", 4), "<i2": ("h", 2), "|i1": ("b", 1)}


def npz_tableau(p, cle):
    with zipfile.ZipFile(p) as z:
        raw = z.read(cle + ".npy")
    if raw[:6] != b"\x93NUMPY":
        raise ValueError("pas un .npy")
    if raw[6] == 1:
        hl = struct.unpack("<H", raw[8:10])[0]; deb = 10
    else:
        hl = struct.unpack("<I", raw[8:12])[0]; deb = 12
    h = ast.literal_eval(raw[deb:deb + hl].decode("latin1"))
    code, taille = _DT[h["descr"]]
    a, b = h["shape"]
    data = raw[deb + hl:]
    if len(data) != a * b * taille:
        raise ValueError("taille incoherente")
    v = list(struct.unpack("<%d%s" % (a * b, code), data))
    if h["fortran_order"]:
        return [[v[j * a + i] for j in range(b)] for i in range(a)]
    return [v[i * b:(i + 1) * b] for i in range(a)]


ok = True
GL = npz_tableau(FST, "G_L"); F = npz_tableau(FST, "f")
G = [[int(t) for t in l.split()] for l in open(FG, encoding="utf-8") if l.strip() and not l.startswith("#")]
taille = len(GL) == 56 and all(len(r) == 56 for r in GL) and len(F) == 56 and all(len(r) == 56 for r in F) and len(G) == 56 and all(len(r) == 56 for r in G)
print("tailles 56 x 56 (G_L, f, G) :", taille, flush=True); ok &= taille
symG = all(G[i][j] == G[j][i] for i in range(56) for j in range(56)); pairG = all(G[i][i] % 2 == 0 for i in range(56))
symL = all(GL[i][j] == GL[j][i] for i in range(56) for j in range(56)); pairL = all(GL[i][i] % 2 == 0 for i in range(56))
print("G (L56) symetrique : %s ; paire : %s ; G_L symetrique : %s ; paire : %s" % (symG, pairG, symL, pairL), flush=True)
ok &= symG and pairG and symL and pairL
FGm = [[sum(F[i][k] * G[k][j] for k in range(56)) for j in range(56)] for i in range(56)]
Dm = [[GL[i][j] - sum(FGm[i][k] * F[j][k] for k in range(56)) for j in range(56)] for i in range(56)]
nd = sum(1 for i in range(56) if Dm[i][i] % 4 == 0)
no = sum(1 for i in range(56) for j in range(i + 1, 56) if Dm[i][j] % 2 == 0)
print("PARITE : %d + %d congruences vraies sur 1596 (56 diagonales = 0 mod 4, 1540 hors diagonale = 0 mod 2)" % (nd, no), flush=True)
ok &= (nd == 56 and no == 1540)
print("structure sha %s ; G sha %s" % (hashlib.sha256(open(FST, "rb").read()).hexdigest()[:16], hashlib.sha256(open(FG, "rb").read()).hexdigest()[:16]), flush=True)
print("BILAN : OK" if ok else "BILAN : ECHEC", flush=True)
sys.exit(0 if ok else 1)
