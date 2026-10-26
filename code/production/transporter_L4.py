# transporter_L4.py -- lot R112_X1_EFFORT_MAX_20261025 (agent 116). Temoin positif X4 : transporte les donnees de L1 (facteur de
# type b de X1) vers L4 (facteur de type b de X4) par l'isometrie S-equivariante T (x4 T = x1) : representants x4 = x1 T^-1,
# unites u4 = T u1 T^-1 ; le groupe S sur L4 est re-enumere a partir des generateurs de structure_X4.npz (lib/group.py, LU).
# Controles : normes conservees, unites isometries de L4 commutant aux generateurs.
# Usage : python -I transporter_L4.py RACINE STRUCT_X4 ISO_NPZ DONNEES_L1 MINREPS_L1 [NORM8_L1] DOSSIER
import os, sys
import numpy as np
racine, fs4, fiso, fdon, fmin = sys.argv[1:6]
f8 = sys.argv[6] if len(sys.argv) > 7 else None
sortie = sys.argv[-1]
sys.path.insert(0, os.path.join(racine, "code"))
from lib import exact, group
os.makedirs(sortie, exist_ok=True)
s4 = np.load(fs4, allow_pickle=False); G4 = s4["G_L"].astype(np.int64)
iso = np.load(fiso, allow_pickle=False); T = iso["T"].astype(np.int64); Ti = iso["Tinv"].astype(np.int64)
U1 = np.load(fdon, allow_pickle=False)["units"].astype(np.int64)
U4 = np.stack([exact.i64_matmul(exact.i64_matmul(T, u), Ti) for u in U1])
assert all((exact.i64_matmul(exact.i64_matmul(u, G4), u.T) == G4).all() for u in U4)
for h in (s4["h1"].astype(np.int64), s4["h2"].astype(np.int64)):
    assert all((exact.i64_matmul(u, h) == exact.i64_matmul(h, u)).all() for u in U4)
S4 = group.sl2_29_mod_sign([s4["h1"].astype(np.int64), s4["h2"].astype(np.int64)])
np.savez_compressed(os.path.join(sortie, "donnees_L4.npz"), S=S4, units=U4)
R1 = np.load(fmin, allow_pickle=False)["reps"].astype(np.int64)
R4 = exact.i64_matmul(R1, Ti)
assert (exact.norms(R4, G4) == 6).all()
np.savez_compressed(os.path.join(sortie, "min_reps_L4.npz"), reps=R4.astype(np.int16))
if f8:
    z = np.load(f8, allow_pickle=False)
    X4 = exact.i64_matmul(z["reps"].astype(np.int64), Ti)
    assert (exact.norms(X4, G4) == 8).all()
    np.savez_compressed(os.path.join(sortie, "norm8_reps_L4.npz"), reps=X4.astype(np.int16), sizes=z["sizes"])
print("transport OK : %d unites, %d representants minimaux%s" % (len(U4), len(R4), (", %d de norme 8" % len(X4)) if f8 else ""))
