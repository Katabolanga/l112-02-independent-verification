# ordre_par_orbite.py -- lot R112_X1_FICHE_CATALOGUE_20261026 (agent Claude n° 119, 26 oct. 2026). Code ecrit ici (numpy).
# Ordre de N = <S, C(S), T> SANS GAP : orbite d'un vecteur aleatoire (graine fixe) de X1 sous les generateurs, par
# parcours exhaustif (entiers exacts : les images sont des vecteurs entiers, bornes verifiees). |orbite| divise |N| et
# |orbite| = |N| / |Stab(v)| ; une orbite de 292 320 = 12 x 24 360 vecteurs donne |N| >= 292 320. Comme N normalise S et
# |C_Aut(X1)(S)| = 12 (enumeration exacte), N/C(S) se plonge dans Aut(SL_2(29)) = PGL_2(29) d'ordre 24 360, donc
# |N| <= 12 x 24 360 = 292 320 : d'ou |N| = 292 320 exactement (et Stab(v) = 1).
# Usage : python -I ordre_par_orbite.py GROUPE_NPZ SORTIE_TXT
import sys, time
import numpy as np

fgr, fout = sys.argv[1:3]
t0 = time.time()
z = np.load(fgr, allow_pickle=False)
GX = z["GX"].astype(np.int64)
gens = [m.astype(np.int64) for m in z["S_g1g2"]] + [m.astype(np.int64) for m in z["C"]] + [z["T_tous"][0].astype(np.int64)]
for g in gens:
    if not (g @ GX @ g.T == GX).all():
        raise SystemExit("generateur non isometrique")
rng = np.random.default_rng(119)
v = rng.integers(-2, 3, size=112).astype(np.int64)
nv = int(v @ GX @ v)
seen = {v.tobytes()}
todo = [v]
borne = max(int(np.abs(g).max()) for g in gens)
mx = int(np.abs(v).max())
while todo:
    w = todo.pop()
    if int(np.abs(w).max()) * borne * 112 >= 2 ** 62:
        raise SystemExit("borne int64")
    for g in gens:
        u = w @ g
        key = u.tobytes()
        if key not in seen:
            seen.add(key)
            todo.append(u)
            mx = max(mx, int(np.abs(u).max()))
    if len(seen) > 2_000_000:
        raise SystemExit("orbite trop grande")
n = len(seen)
txt = ("vecteur aleatoire (graine 119) de norme %d ; generateurs : 2 de S, 12 de C(S), 1 T ; orbite : %d vecteurs ; "
       "max |coordonnee| %d ; %.1f s\n" % (nv, n, mx, time.time() - t0))
txt += "orbite = 292320 = 12 x 24360 : %s\n" % (n == 292320)
open(fout, "w").write(txt)
print(txt)
