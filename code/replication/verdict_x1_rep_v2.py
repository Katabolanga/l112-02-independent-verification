# verdict_x1_rep_v2.py -- paquet de replication X1 pour MACHINE_B (agent Claude n° 121, 26 oct. 2026 ; V2 : agent n° 122). Code ecrit ici.
# VERSION V2 (correction 2 d'<REVIEWER>, <INTERNAL_NOTE>, § 3 b et piece 2,
# point 2) : en V1, meme_resultat tolerait toute ligne « absente de b » sans mot de resultat (liste noire ; multiplicite ignoree :
# un DOUBLON d'une ligne [ok] existante suivi d'un avertissement passait). En V2, la comparaison est SEQUENTIELLE et consomme
# CHAQUE occurrence ; toute ligne non consommee doit appartenir a la liste EXPLICITE des avertissements admis (A1, A2), sinon FAIL.
# Le reste du verdict (conditions, motifs, valeurs attendues) est INCHANGE ; seuls les noms des fichiers ecrits passent en V2.
# REGLE DE VERDICT PROPRE A X1 pour la REPLICATION : la regle de verdict_x1_v3.py (agent 119 ; copie pour memoire dans
# scripts/verdict_x1_v3_POUR_MEMOIRE.py, NON executee ici car elle relit les sorties historiques de MACHINE_A), appliquee aux
# sorties de CETTE execution, et completee par les raccords, le binaire recompile et le controle positif X4.
# BIBLIOTHEQUE STANDARD SEULE, lecture seule, aucun calcul lourd. « BILAN OK » ou « passed » seuls ne suffisent JAMAIS.
# X1 est CONFORME seulement si TOUTES les conditions sont PASS :
#   E00 numpy present ; B01/B02 compilations natives ; B03 binaire controle (E8, Leech, Leech2_E8 identiques a MACHINE_A) ;
#   R01 raccords F1 (L et L56 : Gram = U G U^t, U unimodulaire, 1 596 intervalles exacts, D > 0) ; R02 parite (1 596 congruences) ;
#   R03 serie theta extremale 56 (PARI exact : |L_6|, |L_8|, nombres contre lesquels V02 compte la couverture) ;
#   F01/F02 F1 de CHAQUE cote : une seule feuille, 0 vecteur non tabule, done, sortie identique a l'octet a celle de MACHINE_A ;
#   V01 cote phi exact int64 : 7 controles sur 7, dont la classe ;
#   V02 X1 : groupes, couverture norme 8 de L56 et de L (1 517 130 orbites regulieres, somme |L_8|), couverture norme 6 et
#       certificats des DEUX cotes (phi : types (6,6), (6,10) ; psi : type (10,6)), 0 touche (8,8), regle propre X1 ;
#   V03 X4 (controle positif) : 20 paires en collision, 14 orbites, 682 080 vecteurs de norme 8 (valeurs de MACHINE_A) ;
#   lignes de resultat de V01, V02, V03 IDENTIQUES (horodatages retires) a celles de l'execution v3 de MACHINE_A ;
#   chaque etape : code natif 0 (fichier <etape>.native.exit) et marqueur <etape>.ok.
# Usage : python3 -I verdict_x1_rep_v2.py DOSSIER_EXEC     (0 = REPLICATION X1 CONFORME ; 1 = NON CONFORME)
import datetime, hashlib, os, re, sys

EX = sys.argv[1] if len(sys.argv) == 2 else None
if EX is None or not os.path.isdir(EX):
    print("usage : verdict_x1_rep_v2.py DOSSIER_EXEC"); sys.exit(2)
RES = []
MANIF = {}
ETAPES = ["E00_numpy", "B01_compil_enum", "B02_compil_formes", "B03_controles_enum", "R01_raccords", "R02_parite",
          "R03_theta56", "F01_F1_L", "F02_F1_L56", "V01_phi_X1", "V02_indep_X1", "V03_indep_X4"]


def P(*a):
    return os.path.join(EX, *a)


def lire(rel):
    p = P(rel)
    b = open(p, "rb").read()
    MANIF[rel] = (hashlib.sha256(b).hexdigest(), len(b))
    return b.decode("utf-8", errors="replace")


def cond(cle, libelle, ok, detail=""):
    RES.append((cle, libelle, "PASS" if ok else "FAIL", detail))


def natif_ok(n):
    try:
        return lire(n + ".native.exit").strip() == "0" and os.path.isfile(P(n + ".ok"))
    except OSError:
        return False


def sans_heure(texte):
    return [re.sub(r"^\[\s*[0-9.]+ s\] ", "", l).rstrip() for l in texte.splitlines() if l.strip()]


CLES_RESULTAT = ("[ok]", "[ECHEC]", "BILAN", "VERDICT", "type (8,8)", "orbites de S", "controles executes", "CONTROLE POSITIF", "norme ", "paires")
# V2 : LISTE EXPLICITE DES AVERTISSEMENTS ADMIS. Une ligne de l'execution qui ne consomme pas la prochaine ligne de MACHINE_A n'est
# toleree QUE si elle a l'une des deux formes A1, A2 ; tout le reste est FAIL (ligne de resultat en trop, doublon d'une ligne
# existante, avertissement d'une autre categorie, ligne inconnue). CLES_RESULTAT n'est plus qu'une garde SUPPLEMENTAIRE sur le
# message de A1, pas la regle.
#  A1 en-tete d'avertissement Python d'EVOLUTION D'API, au format de warnings.formatwarning « fichier.py:N: Categorie: message »,
#     Categorie dans CATEGORIES_ADMISES, message sans aucun mot de CLES_RESULTAT. NON admis : RuntimeWarning (debordement, division
#     par zero, valeur invalide), UserWarning, SyntaxWarning, ResourceWarning, toute autre categorie, message sur plusieurs lignes,
#     toute sortie de gp ou de gcc.
#  A2 la ligne de source que Python imprime JUSTE APRES un en-tete A1 : admise seulement si elle vaut exactement deux espaces suivis
#     de la ligne N du fichier nomme par l'en-tete, sans blancs aux bords (fichier relu ici ; illisible = non admise), et si elle
#     n'est egale a AUCUNE ligne de MACHINE_A.
CATEGORIES_ADMISES = ("DeprecationWarning", "PendingDeprecationWarning", "FutureWarning", "VisibleDeprecationWarning")
RE_A1 = re.compile(r"^(?P<f>[^\s:][^:]*\.py):(?P<n>[1-9][0-9]*): (?P<c>%s): (?P<m>\S.*)$" % "|".join(CATEGORIES_ADMISES))


def avertissement_a1(l):
    m = RE_A1.match(l)
    return m if m is not None and not any(k in m.group("m") for k in CLES_RESULTAT) else None


def source_a2(m):
    """ligne que Python imprime apres l'en-tete A1 m : deux espaces + ligne N du fichier, sans blancs aux bords ; None si illisible ou vide"""
    try:
        with open(m.group("f"), encoding="utf-8", errors="replace") as h:
            for k, l in enumerate(h, 1):
                if k == int(m.group("n")):
                    return ("  " + l.strip()) if l.strip() else None
    except OSError:
        return None
    return None


def meme_resultat(a, b):
    """V2. a (execution) et b (MACHINE_A), listes de lignes sans horodatage. Comparaison SEQUENTIELLE : a est parcourue dans l'ordre ;
    une ligne egale a la PROCHAINE ligne non consommee de b la consomme (chaque occurrence de b est consommee une seule fois) ; une
    ligne qui ne consomme rien doit etre un avertissement ADMIS (A1, ou A2 juste apres son A1), sinon FAIL ; a la fin, TOUTES les
    lignes de b doivent avoir ete consommees, sinon FAIL. Donc PASS si et seulement si a, privee de ses avertissements admis, est
    EXACTEMENT b (meme ordre, memes multiplicites). Doublon, ligne nouvelle, ligne manquante, avertissement non liste : FAIL."""
    if any(RE_A1.match(y) for y in b):
        return False, "reference ambigue : une ligne de MACHINE_A a la forme d'un avertissement admis (A1)"
    refs = set(b)
    j, admis, a1 = 0, [], None
    for i, x in enumerate(a):
        if j < len(b) and x == b[j]:
            j, a1 = j + 1, None
            continue
        m = avertissement_a1(x)
        if m is not None:
            admis.append(x); a1 = m
            continue
        if a1 is not None and x not in refs and x == source_a2(a1):
            admis.append(x); a1 = None
            continue
        return False, "ligne %d de l'execution ni consommee ni admise : %r (prochaine ligne attendue de MACHINE_A, n° %d : %r)" % (
            i, x[:200], j, b[j][:200] if j < len(b) else None)
    if j < len(b):
        return False, "%d ligne(s) de MACHINE_A absente(s) de l'execution, a partir de la n° %d : %r" % (len(b) - j, j, b[j][:200])
    if not admis:
        return True, "%d lignes identiques" % len(a)
    return True, "lignes de resultat identiques (%d, ordre et multiplicites) ; %d ligne(s) supplementaire(s) hors resultat, toutes des avertissements ADMIS (liste explicite A1/A2) : %r" % (
        len(b), len(admis), [l[:160] for l in admis[:4]])


def contient(texte, lignes):
    manque = [l for l in lignes if l not in texte]
    return len(manque) == 0, manque[:2]


def essai(cle, libelle, f):
    try:
        ok, detail = f()
        cond(cle, libelle, ok, detail)
    except Exception as e:   # fichier absent, format inattendu : ECHEC explicite, jamais un PASS
        cond(cle, libelle, False, repr(e)[:300])


# ---- etapes : codes natifs et marqueurs
essai("natifs", "les 12 etapes ont un code natif 0 et un marqueur .ok",
      lambda: (all(natif_ok(n) for n in ETAPES), "en defaut : %s" % [n for n in ETAPES if not natif_ok(n)]))
# ---- E00
essai("numpy", "E00 : numpy present dans PYN", lambda: ("NUMPY DISPONIBLE" in lire("E00_numpy.log"),
      (lire("E00_numpy.log").splitlines() or ["?"])[0][:200]))


# ---- B01, B02, B03
def b_compil(n, binaire):
    t = lire(n + ".log")
    ok = "COMPILATION OK" in t and os.path.isfile(P("bin", binaire)) and os.access(P("bin", binaire), os.X_OK)
    sh = hashlib.sha256(open(P("bin", binaire), "rb").read()).hexdigest() if ok else "?"
    return ok and natif_ok(n), "sha256 du binaire %s = %s" % (binaire, sh)


essai("compil-enum", "B01 : enum_interval.c recompile nativement (gcc -O2 -std=c11 -fno-fast-math -ffp-contract=off)", lambda: b_compil("B01_compil_enum", "enum_interval"))
essai("compil-formes", "B02 : formes_canoniques.c recompile nativement (gcc -O2)", lambda: b_compil("B02_compil_formes", "formes_canoniques"))


def b03():
    diffs = [e for e in ("E8", "leech", "leech2_e8") if lire("sorties/B03_%s.sortie" % e) != lire("REFERENCE_MACHINE_A/F1_%s.sortie" % e)]
    return (not diffs) and natif_ok("B03_controles_enum") and "CONTROLES ENUM OK" in lire("B03_controles_enum.log"), "differences : %s" % diffs


essai("controle-enum", "B03 : binaire recompile, sorties E8, Leech, Leech2_E8 identiques a l'octet a celles de MACHINE_A", b03)


# ---- R01 raccords
def r01():
    t = lire("R01_raccords.log").splitlines()
    lL = [l for l in t if l.startswith("L   : ")]; l56 = [l for l in t if l.startswith("L56 : ")]
    if len(lL) != 1 or len(l56) != 1:
        return False, "lignes L / L56 absentes"
    det = lambda l: ("det U = -1 ;" in l) or ("det U = 1 ;" in l)
    okL = all(s in lL[0] for s in ("n=56 rayon=4", "entree == Gr : True", "entree == U G_L U^T : True", "1596 intervalles contiennent les valeurs exactes : True []", "D > 0 : True")) and det(lL[0])
    ok56 = all(s in l56[0] for s in ("n=56 rayon=4", "entree == U G U^T : True", "1596 intervalles contiennent les valeurs exactes : True []", "D > 0 : True")) and det(l56[0])
    return okL and ok56 and "BILAN : OK" in t and natif_ok("R01_raccords"), "L %s ; L56 %s" % (okL, ok56)


essai("raccords", "R01 : raccords des entrees F1 (L et L56 : Gram = U G U^t, |det U| = 1, 1 596 intervalles exacts, D > 0)", r01)


def r02():
    t = lire("R02_parite.log")
    ok = "PARITE : 56 + 1540 congruences vraies sur 1596" in t and "G (L56) symetrique : True ; paire : True ; G_L symetrique : True ; paire : True" in t \
        and "tailles 56 x 56 (G_L, f, G) : True" in t and "BILAN : OK" in t
    return ok and natif_ok("R02_parite"), ""


essai("parite", "R02 : parite du recollement, D = G_L - f G f^t : 56 diagonales = 0 mod 4, 1 540 hors diagonale = 0 mod 2", r02)
L_THETA = ["[ok]    norme 6 : 15 590 400 (= 2 x 7 795 200, orbites de F2)", "[ok]    norme 8 : 36 957 286 800 (somme des orbites de F3)",
           "[ok]    expression de roiban (annexe B, table B1) : (-159 A^7 + 238 A^4 B + 161 A B^2)/240", "  norme 6 : 15590400", "  norme 8 : 36957286800"]


def r03():
    t = lire("R03_theta56.log"); ok, m = contient(t, L_THETA)
    ref = [l.rstrip() for l in lire("REFERENCE_MACHINE_A/theta_56.txt").splitlines() if l.strip() and not l.startswith("code=")]
    same, det = meme_resultat([l.rstrip() for l in t.splitlines() if l.strip()], ref)
    return ok and same and "[ECHEC]" not in t and natif_ok("R03_theta56"), "manque : %s ; comparaison a MACHINE_A : %s" % (m, det)


essai("theta56", "R03 : serie theta extremale 56 (PARI exact) : |L_6| = 15 590 400, |L_8| = 36 957 286 800, expression de roiban, identique a MACHINE_A", r03)


# ---- F01, F02
def f1(n, fichier, ref, noeuds):
    o = lire("sorties/" + fichier); r = lire("REFERENCE_MACHINE_A/" + ref)
    ok = ("nodes %d leaves 1\n" % noeuds) in o and "untabulated vectors of norm >= 4096: 0" in o and o.rstrip().endswith("done")
    return ok and o == r and natif_ok(n), "une feuille / 0 non tabule / done : %s ; identique a MACHINE_A : %s" % (ok, o == r)


essai("F1-L", "F01 : F1 cote L (min L = 6) : nodes 9905828434 leaves 1, 0 non tabule, done, identique a MACHINE_A, code natif 0",
      lambda: f1("F01_F1_L", "F1_L.sortie", "F1_L_bkz40_rayon4.sortie", 9905828434))
essai("F1-L56", "F02 : F1 cote L56 (min L56 = 6) : nodes 8454837756 leaves 1, 0 non tabule, done, identique a MACHINE_A, code natif 0",
      lambda: f1("F02_F1_L56", "F1_L56.sortie", "F1_L56.sortie", 8454837756))
# ---- V01
L_PHI64 = ["[ok]   generateurs isometries de L56", "[ok]   |<g1, g2>| = 24360",
           "[ok]   7795200 vecteurs minimaux au signe pres, distincts (hachage), 2 x = |L_6| = 15590400",
           "[ok]   tous de norme 6 (int64 exact)", "[ok]   normes des certificats dans {14, 18}",
           "[ok]   chaque certificat est dans la classe de son representant (w0 = r f mod 2)",
           "[ok]   max |<w0, u>| <= 6 sur tous les vecteurs minimaux (int64 exact)", "controles executes : 7 / 7 attendus", "BILAN : OK"]
essai("phi-int64", "V01 : cote phi (types (6,6), (6,10)), exact int64 : 7 controles sur 7 dont la classe, BILAN OK, code natif 0",
      lambda: (lambda t: (contient(t, L_PHI64)[0] and "[ECHEC]" not in t and natif_ok("V01_phi_X1"), "manque : %s" % contient(t, L_PHI64)[1]))(lire("V01_phi_X1.log")))
# ---- V02
L_GRP = ["[ok]   |<g1, g2>| = 24360 sur L56", "[ok]   generateurs isometries de L56", "[ok]   image modulo 2 d'ordre 12180 sur L56/2L56",
         "[ok]   |<h1, h2>| = 24360 sur L", "[ok]   generateurs isometries de L", "[ok]   image modulo 2 d'ordre 12180 sur L/2L",
         "[ok]   f equivariante modulo 2 (generateurs)"]
L_C56 = ["[ok]   L56 : 1527984 paires de norme 8", "[ok]   L56 : 1517130 orbites distinctes",
         "[ok]   L56 : toutes regulieres (12180 classes, 24360 vecteurs)", "[ok]   L56 : somme des tailles = |L_8|"]
L_CL = ["[ok]   L : 1528956 paires de norme 8", "[ok]   L : 1517130 orbites distinctes", "[ok]   L : toutes regulieres",
        "[ok]   L : somme des tailles = |L_8|"]
L_PSI = ["psi_L56_vers_L : 7795200 vecteurs minimaux au signe pres, distincts (hachage), 2 x = |L_6|", "psi_L56_vers_L : tous de norme 6",
         "psi_L56_vers_L : normes des certificats dans {14, 18}", "psi_L56_vers_L : chaque certificat est dans la classe de son representant",
         "psi_L56_vers_L : max |<w0, u>| <= 6 sur tous les vecteurs minimaux"]
L_PSI = ["[ok]   " + l for l in L_PSI]
L_PHI = [l.replace("psi_L56_vers_L", "phi_L_vers_L56") for l in L_PSI]
L88 = "type (8,8) : paires x de L(8) dont la classe x f contient un vecteur de norme 8 de L56 : "
REGLE_X1 = "VERDICT X1 (regle propre a X1) : nb_touches88 = 0 ; deux cotes impairs : True ; controles : OK -> CONFORME"
DEUX = "[ok]   les DEUX cotes impairs (phi : types (6,6), (6,10) ; psi : type (10,6)) ont ete traites"


def v_lignes(n, lignes):
    t = lire(n + ".log"); ok, m = contient(t, lignes)
    return ok and "[ECHEC]" not in t and natif_ok(n), "manque : %s" % m


def touches(n):
    t = sans_heure(lire(n + ".log"))
    v = [l[len(L88):] for l in t if l.startswith(L88)]
    return v


essai("groupes-X1", "V02 : groupes <g1, g2> sur L56 et <h1, h2> sur L d'ordre 24360, isometries, images mod 2 d'ordre 12180, f equivariante", lambda: v_lignes("V02_indep_X1", L_GRP))
essai("cover8-L56", "V02 : couverture norme 8 de L56 : 1 527 984 paires, 1 517 130 orbites regulieres, somme = |L_8|", lambda: v_lignes("V02_indep_X1", L_C56))
essai("cover8-L", "V02 : couverture norme 8 de L (cover8) : 1 528 956 paires, 1 517 130 orbites regulieres, somme = |L_8|", lambda: v_lignes("V02_indep_X1", L_CL))
essai("phi-X1", "V02 : cote phi (types (6,6), (6,10)) : couverture norme 6 de L (7 795 200 = |L_6|/2) et 656 certificats : 5 controles", lambda: v_lignes("V02_indep_X1", L_PHI))
essai("psi-X1", "V02 : cote psi (type (10,6)) : couverture norme 6 de L56 et 656 certificats : 5 controles", lambda: v_lignes("V02_indep_X1", L_PSI))
essai("deux-cotes", "V02 : les DEUX cotes impairs ont ete traites", lambda: v_lignes("V02_indep_X1", [DEUX]))
essai("nocoll88-X1", "V02 : type (8,8) : 0 touche sur les 1 528 956 paires (ligne lue, pas deduite de BILAN OK)",
      lambda: (lambda v: (v == ["0"], "valeurs lues : %s" % v))(touches("V02_indep_X1")))
essai("regle-X1", "V02 : regle propre a X1 (BILAN OK et « nb_touches88 = 0 ; deux cotes impairs : True -> CONFORME »), code natif 0",
      lambda: v_lignes("V02_indep_X1", ["BILAN : OK", REGLE_X1]))
# ---- V03 (controle positif X4)
essai("positif-X4", "V03 : controle positif X4 : 20 paires (8,8) en collision, 14 orbites, 682 080 vecteurs de norme 8, regle J = 4, code natif 0",
      lambda: (lambda v, r: (v == ["20"] and r[0], "touches lues : %s ; %s" % (v, r[1])))(touches("V03_indep_X4"), v_lignes("V03_indep_X4", [
          "orbites de S sur L(8) en collision : 14 ; vecteurs de norme 8 de X : 682080", "BILAN : OK",
          "CONTROLE POSITIF X4 : nb_touches88 = 20 -> CONFORME (touches trouvees)"])))


# ---- identite avec MACHINE_A (lignes de resultat, horodatages retires)
def identique(n, ref):
    return meme_resultat(sans_heure(lire(n + ".log")), sans_heure(lire("REFERENCE_MACHINE_A/" + ref)))


essai("ident-V01", "V01 : journal identique a celui de MACHINE_A (v3, 26 oct. 9 h 56), horodatages retires", lambda: identique("V01_phi_X1", "v3_phi_v3_X1.log"))
essai("ident-V02", "V02 : journal identique a celui de MACHINE_A (v3, 26 oct. 10 h 54), horodatages retires", lambda: identique("V02_indep_X1", "v3_X1_v3.log"))
essai("ident-V03", "V03 : journal identique a celui de MACHINE_A (v3, 26 oct. 11 h 46), horodatages retires", lambda: identique("V03_indep_X4", "v3_X4_v3.log"))
# ---- verdict
nf = sum(1 for r in RES if r[2] != "PASS")
if nf == 0:
    verdict = "VERDICT GLOBAL : REPLICATION X1 CONFORME (%d conditions sur %d PASS)" % (len(RES), len(RES))
else:
    verdict = "VERDICT GLOBAL : NON CONFORME (%d condition(s) en FAIL sur %d)" % (nf, len(RES))
lignes = ["VERDICT X1 REPLICATION (verdict_x1_rep_v2.py, regle propre a X1) -- %s -- %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), EX), ""]
for cle, lib, et, det in RES:
    lignes.append("[%s] %-14s %s%s" % (et, cle, lib, ("  -- " + det) if det else ""))
lignes += ["", verdict]
txt = "\n".join(lignes) + "\n"
open(P("VERDICT_X1_REP_V2.txt"), "w", encoding="utf-8").write(txt)
with open(P("MANIFESTE_VERDICT_X1_REP_V2.tsv"), "w", encoding="utf-8") as h:
    h.write("fichier (relatif au dossier d'execution)\tsha256\toctets\n")
    for f in sorted(MANIF):
        h.write("%s\t%s\t%d\n" % (f, MANIF[f][0], MANIF[f][1]))
print(txt, end="")
sys.exit(0 if nf == 0 else 1)
