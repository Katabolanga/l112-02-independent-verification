# verdict_x1_v3.py -- lot R112_X1_FICHE_CATALOGUE_20261026 (agent Claude n° 119, 26 oct. 2026). Code ecrit ici.
# REGLE DE VERDICT PROPRE A X1 (demande d'<REVIEWER> du 25 oct. 23 h 14 UTC, § 5 b, rappelee le 26 oct. 08:12 UTC) :
#   X1 est CONFORME seulement si TOUTES les conditions suivantes sont lues dans les sorties existantes :
#     (8,8)  nb_touches88 = 0, sur 1 528 956 paires, par la premiere implementation (collisions8_X1.json, code 0) ET par la
#            seconde (independant/X1_int16 : ligne « type (8,8) ... : 0 », BILAN OK, code natif 0) ;
#     IMPAIRS les DEUX cotes : phi (types (6,6), (6,10)) et psi (type (10,6)), 656 certificats valides chacun, 0 collision,
#            par la premiere implementation (certificats_impairs_x1.json) ET par la seconde (X1_int16 pour psi ; pour phi,
#            le rejeu exact sortie_v2.log, BILAN OK, code 0, la sortie phi d'origine X1 ayant echoue sur le stockage int8) ;
#     F1     de CHAQUE cote : L56 (rejeu v1 : « L56 code 0 », une feuille, done) et L (sortie historique, et CODE NATIF du
#            rejeu R112_X1_F1L_REJEU_NATIF_20261026 = 0, meme binaire et meme entree, sortie identique) ;
#     COUVERTURE  orbites de norme 6 de L (656, 7 795 200 = |L_6|/2) et de norme 8 de L (1 517 130, somme |L_8|) ;
#     PARITE les 1 596 congruences de D = G_L - f G f^t (56 diagonales = 0 mod 4, 1 540 hors diagonale = 0 mod 2),
#            RECALCULEES ici en entiers Python (controle d'<REVIEWER> du 25 oct.).
#   « passed » ou « BILAN OK » seuls ne suffisent PAS (le meme code sert pour X4, ou des touches sont attendues).
# Aucun calcul lourd : lecture de fichiers, comparaisons, empreintes SHA-256 (manifeste ecrit a cote).
# Usage : python -I verdict_x1_v3.py LOT_X1 DOSSIER_REJEU_F1L SORTIE_DIR
import os, sys, json, hashlib, datetime
import numpy as np

LOT, REJEU, SORTIE = sys.argv[1:4]
os.makedirs(SORTIE, exist_ok=True)
MANIF = []
RES = []


def sha(p):
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    MANIF.append((os.path.relpath(p, os.path.dirname(LOT)), h, os.path.getsize(p)))
    return h


def lire(p):
    sha(p)
    return open(p, encoding="utf-8", errors="replace").read()


def cond(cle, libelle, etat, detail=""):
    RES.append((cle, libelle, etat, detail))


def P(*a):
    return os.path.join(LOT, *a)


# ---- (8,8), premiere implementation
try:
    j = json.loads(lire(P("sorties", "collisions8_X1", "collisions8_X1.json")))
    log = lire(P("sorties", "collisions8_X1", "sortie.log"))
    v = j["values"]
    n_p = v.get("paires x_i u_k testees")
    n_t = v.get("type (8,8) : classes (x_i u_k) f + 2 L56 contenant un vecteur de norme 8")
    okc = j.get("passed") is True and n_p == 1528956 and n_t == 0 and "\ncode 0\n" in log
    cond("88-impl1", "(8,8) premiere implementation : 0 touche sur 1 528 956 paires, code 0", "PASS" if okc else "FAIL",
         "paires %s, touches %s" % (n_p, n_t))
except Exception as e:
    cond("88-impl1", "(8,8) premiere implementation", "FAIL", repr(e))
# ---- (8,8) et impairs, seconde implementation (X1_int16)
try:
    s2 = lire(P("sorties", "independant", "X1_int16", "sortie.log"))
    h2 = lire(P("sorties", "independant", "X1_int16", "horodatage.txt"))
    ok88 = "type (8,8) : paires x de L(8) dont la classe x f contient un vecteur de norme 8 de L56 : 0\n" in s2
    okb = "BILAN : OK" in s2 and "code 0" in h2 and "[ECHEC]" not in s2
    ok8L = all(t in s2 for t in ("[ok]   L : 1528956 paires de norme 8", "[ok]   L : 1517130 orbites distinctes",
                                 "[ok]   L : toutes regulieres", "[ok]   L : somme des tailles = |L_8|"))
    cond("88-impl2", "(8,8) seconde implementation : 0 touche, F3 de L recompte (1 528 956 paires, 1 517 130 orbites), BILAN OK, code natif 0",
         "PASS" if (ok88 and okb and ok8L) else "FAIL")
    lignes_psi = ["psi_L56_vers_L : 7795200 vecteurs minimaux", "psi_L56_vers_L : tous de norme 6",
                  "psi_L56_vers_L : normes des certificats dans {14, 18}", "psi_L56_vers_L : chaque certificat est dans la classe",
                  "psi_L56_vers_L : max |<w0, u>| <= 6"]
    cond("psi-impl2", "type (10,6), cote psi, seconde implementation : 5 controles ok", "PASS" if all(("[ok]   " + t) in s2 for t in lignes_psi) and okb else "FAIL")
    lignes_phi = [t.replace("psi_L56_vers_L", "phi_L_vers_L56") for t in lignes_psi]
    cond("phi-impl2-int16", "types (6,6), (6,10), cote phi, seconde implementation corrigee (int16) : 5 controles ok",
         "PASS" if all(("[ok]   " + t) in s2 for t in lignes_phi) and okb else "FAIL")
except Exception as e:
    cond("impl2", "seconde implementation X1_int16", "FAIL", repr(e))
try:
    s3 = lire(P("sorties", "independant", "X1_phi_int64", "sortie_v2.log"))
    okp = all(t in s3 for t in ("[ok]   7795200 vecteurs minimaux", "[ok]   tous de norme 6", "[ok]   normes des certificats dans {14, 18}",
                                "[ok]   chaque certificat est dans la classe de son representant", "[ok]   max |<w0, u>| <= 6")) \
        and "BILAN : OK" in s3 and "code 0" in s3 and "[ECHEC]" not in s3
    cond("phi-int64", "cote phi, rejeu exact verif_phi_L56_int64.py (sortie_v2.log) : controles ok dont la classe, BILAN OK, code 0",
         "PASS" if okp else "FAIL")
except Exception as e:
    cond("phi-int64", "rejeu phi int64", "FAIL", repr(e))
# ---- impairs, premiere implementation
try:
    jc = json.loads(lire(P("sorties", "certificats_X1", "certificats_impairs_x1.json")))
    ch = {c["check"]: c["ok"] for c in jc["checks"]}
    vv = jc["values"]
    okphi = ch.get("type (6,6)/(6,10) : un certificat impair pour chacun des 656 representants de L_6") is True and \
        vv.get("phi_L_vers_L56 : certificats valides (norme 14 ou 18, max <= 6)") == 656 and \
        vv.get("phi_L_vers_L56 : descentes terminees sous la norme 14 (collisions)") == 0
    okpsi = ch.get("type (10,6) : un certificat impair pour chacun des 656 representants de L56_6") is True and \
        vv.get("psi_L56_vers_L : certificats valides (norme 14 ou 18, max <= 6)") == 656 and \
        vv.get("psi_L56_vers_L : descentes terminees sous la norme 14 (collisions)") == 0
    cond("phi-impl1", "types (6,6), (6,10), cote phi, premiere implementation : 656 certificats valides, 0 collision", "PASS" if okphi and jc.get("passed") else "FAIL")
    cond("psi-impl1", "type (10,6), cote psi, premiere implementation : 656 certificats valides, 0 collision", "PASS" if okpsi and jc.get("passed") else "FAIL")
except Exception as e:
    cond("impl1-impairs", "certificats impairs, premiere implementation", "FAIL", repr(e))
# ---- F1, cote L56 (rejeu v1 de roiban)
try:
    c56 = lire(P("sorties", "rejeu_x7", "v1", "codes.txt"))
    o56 = lire(P("sorties", "rejeu_x7", "v1", "L56.sortie"))
    ok56 = "L56 code 0" in c56 and "nodes 8454837756 leaves 1" in o56 and "untabulated vectors of norm >= 4096: 0" in o56 and o56.rstrip().endswith("done")
    sha(P("sorties", "rejeu_x7", "v1", "L56.entree"))
    sha(P("sorties", "rejeu_x7", "v1", "enum_interval"))
    cond("F1-L56", "F1 cote L56 : enum_interval (intervalles), une seule feuille, done, CODE NATIF 0 (codes.txt)", "PASS" if ok56 else "FAIL")
except Exception as e:
    cond("F1-L56", "F1 cote L56", "FAIL", repr(e))
# ---- F1, cote L : sortie historique (sans code natif) et rejeu natif
try:
    oL = lire(P("sorties", "F1_L", "L_bkz40_rayon4.sortie"))
    eL = sha(P("sorties", "F1_L", "L_bkz40_rayon4.entree"))
    bL = sha(P("sorties", "F1_L", "enum_interval"))
    histo = "nodes 9905828434 leaves 1" in oL and "untabulated vectors of norm >= 4096: 0" in oL and oL.rstrip().endswith("done")
    cn = os.path.join(REJEU, "code_natif.txt")
    if not os.path.isfile(cn):
        cond("F1-L", "F1 cote L : rejeu natif (meme binaire, meme entree)", "EN ATTENTE",
             "sortie historique « done » (%s) mais code natif ABSENT de l'ancien passage ; code_natif.txt du rejeu pas encore ecrit" % ("lue" if histo else "ANORMALE"))
    else:
        code = lire(cn).strip()
        oR = lire(os.path.join(REJEU, "L_bkz40_rayon4.sortie"))
        eR = sha(os.path.join(REJEU, "L_bkz40_rayon4.entree"))
        bR = sha(os.path.join(REJEU, "enum_interval"))
        okR = code.split()[-1] == "0" if code else False
        same = (eR == eL) and (bR == bL) and ("nodes 9905828434 leaves 1" in oR) and oR.rstrip().endswith("done")
        cond("F1-L", "F1 cote L : rejeu natif, CODE NATIF 0, meme entree et meme binaire (SHA), une feuille, done",
             "PASS" if (okR and same and histo) else "FAIL", "code_natif.txt = %r ; entree identique %s ; binaire identique %s" % (code, eR == eL, bR == bL))
except Exception as e:
    cond("F1-L", "F1 cote L", "FAIL", repr(e))
# ---- couverture
try:
    jm = json.loads(lire(P("sorties", "orbites_min_L", "orbites_min_L.json")))
    okm = jm.get("passed") is True and jm["values"].get("representants") == 656 and jm["values"].get("vecteurs r s au signe pres") == 7795200
    cond("cover6", "couverture des vecteurs minimaux de L : 656 orbites, 7 795 200 = |L_6|/2 (cover6)", "PASS" if okm else "FAIL")
    j8 = json.loads(lire(P("sorties", "orbites8_L_v2", "orbites8_L.json")))
    ok8 = j8.get("passed") is True and j8["values"].get("paires x_i u_k") == 1528956 and \
        j8["values"].get("formes canoniques distinctes (= orbites de S)") == 1517130 and \
        {c["check"]: c["ok"] for c in j8["checks"]}.get("somme = |L_8| = 36957286800") is True
    cond("cover8", "couverture des vecteurs de norme 8 de L : 1 517 130 orbites regulieres, somme 36 957 286 800 = |L_8| (cover8)", "PASS" if ok8 else "FAIL")
    sha(P("sorties", "orbites_min_L", "min_reps_L.npz"))
    sha(P("sorties", "orbites8_L_v2", "norm8_reps_L.npz"))
    sha(P("copie_execution", "roiban_112", "certificates", "min_reps.npz"))
except Exception as e:
    cond("cover", "couverture", "FAIL", repr(e))
# ---- parite (controle d'<REVIEWER> recalcule ici, entiers Python)
try:
    fst = P("sorties", "structure_x1", "structure_x1.npz")
    sha(fst)
    z = np.load(fst, allow_pickle=False)
    GL = [[int(t) for t in r] for r in z["G_L"]]
    F = [[int(t) for t in r] for r in z["f"]]
    G = [[int(t) for t in l.split()] for l in open(P("copie_execution", "roiban_112", "data", "L56_gram.txt")) if l.strip() and not l.startswith("#")]
    sha(P("copie_execution", "roiban_112", "data", "L56_gram.txt"))
    FG = [[sum(F[i][k] * G[k][j] for k in range(56)) for j in range(56)] for i in range(56)]
    Dm = [[GL[i][j] - sum(FG[i][k] * F[j][k] for k in range(56)) for j in range(56)] for i in range(56)]
    nd = sum(1 for i in range(56) if Dm[i][i] % 4 == 0)
    no = sum(1 for i in range(56) for j in range(i + 1, 56) if Dm[i][j] % 2 == 0)
    cond("parite", "parite du recollement : D = G_L - f G f^t, 56 diagonales = 0 mod 4 et 1 540 hors diagonale = 0 mod 2 (recalcule ici)",
         "PASS" if (nd == 56 and no == 1540) else "FAIL", "%d + %d congruences vraies sur 1 596" % (nd, no))
except Exception as e:
    cond("parite", "parite", "FAIL", repr(e))
# ---- verdict
etats = [r[2] for r in RES]
if all(e == "PASS" for e in etats):
    verdict = "CONFORME (toutes les conditions de la regle propre a X1 sont lues PASS)"
elif any(e == "FAIL" for e in etats):
    verdict = "NON CONFORME"
else:
    verdict = "INCOMPLET (condition(s) EN ATTENTE)"
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
lignes = ["VERDICT X1 (regle propre a X1, verdict_x1_v3.py) -- %s" % now, ""]
for cle, lib, et, det in RES:
    lignes.append("[%s] %-14s %s%s" % (et, cle, lib, ("  -- " + det) if det else ""))
lignes += ["", "VERDICT : " + verdict]
txt = "\n".join(lignes) + "\n"
open(os.path.join(SORTIE, "verdict_x1_v3.txt"), "w", encoding="utf-8").write(txt)
with open(os.path.join(SORTIE, "manifeste_verdict_x1_v3.tsv"), "w", encoding="utf-8") as h:
    h.write("fichier (relatif a <LOT>)\tsha256\toctets\n")
    for f, hh, n in sorted(set(MANIF)):
        h.write("%s\t%s\t%d\n" % (f, hh, n))
print(txt)
sys.exit(0 if verdict.startswith("CONFORME") else (3 if verdict.startswith("INCOMPLET") else 1))
