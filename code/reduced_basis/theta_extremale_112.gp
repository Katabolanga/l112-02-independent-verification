\\ theta_extremale_112.gp -- lot R112_X1_FICHE_CATALOGUE_20261026 (agent Claude n° 119, 26 oct. 2026).
\\ Serie theta extremale d'un reseau pair unimodulaire de dimension 112, CALCULEE EXACTEMENT (entiers et rationnels de PARI)
\\ dans l'espace M_56(SL_2(Z)) (dimension 5), base E4^(14-3b) Delta^b, b = 0..4 ; extremale = 1 + O(q^5).
\\ Recoupement 1 : expression de roiban1344 (article, annexe B, table B1) en A = E4, B = theta(Leech) = E4^3 - 720 Delta.
\\ Recoupement 2 : coefficients publies par roiban (normes 10 et 12).
\\ Usage : gp -q -f theta_extremale_112.gp   (ecrit sur la sortie standard)
N = 12;   \\ coefficients jusqu'a q^N (norme 2N)
E4 = 1 + 240*sum(n = 1, N, sigma(n, 3)*q^n) + O(q^(N+1));
D  = q*eta(q + O(q^(N+1)))^24;   \\ Delta = q prod (1 - q^n)^24
check(lab, c) = if (c, print("[ok]    ", lab), print("[ECHEC] ", lab); quit(1));
check("Delta = q - 24 q^2 + 252 q^3 - 1472 q^4 + ...", polcoef(D,1)==1 && polcoef(D,2)==-24 && polcoef(D,3)==252 && polcoef(D,4)==-1472 && polcoef(D,5)==4830);
check("E4 = 1 + 240 q + 2160 q^2 + ...", polcoef(E4,1)==240 && polcoef(E4,2)==2160);
B = vector(5, b, E4^(14-3*(b-1)) * D^(b-1));            \\ base de M_56
M = matrix(5, 5, i, j, polcoef(B[j], i-1));             \\ coefficients q^0..q^4
c = matsolve(M, [1,0,0,0,0]~);                          \\ conditions d'extremalite
check("systeme triangulaire inversible (det = 1)", matdet(M) == 1);
th = sum(b = 1, 5, c[b]*B[b]);
check("coefficients rationnels -> entiers", vector(N+1, k, denominator(polcoef(th, k-1))) == vector(N+1, k, 1));
print("coefficients de la base E4^(14-3b) Delta^b, b = 0..4 : ", c~);
\\ recoupement avec l'expression de roiban (annexe B, table B1)
A  = E4; BB = E4^3 - 720*D;
thr = (7883087*A^14 - 18165308*A^11*BB - 38110758*A^8*BB^2 + 74301892*A^5*BB^3 + 11415887*A^2*BB^4)/37324800;
check("egalite avec l'expression de roiban en A, B (jusqu'a q^N)", th == thr);
check("norme 10 : 10 888 335 360 (roiban)", polcoef(th, 5) == 10888335360);
check("norme 12 : 247 006 775 232 000 (roiban)", polcoef(th, 6) == 247006775232000);
print("SERIE THETA EXTREMALE, DIMENSION 112 (coefficient de q^m = nombre de vecteurs de norme 2m) :");
for (m = 0, N, print("  norme ", 2*m, " : ", polcoef(th, m)));
\\ contrôle de coherence : somme des coefficients positive, valeurs au-dela de q^4 positives
check("coefficients des normes 10 a 2N strictement positifs", vecmin(vector(N-4, k, polcoef(th, k+4))) > 0);
print("FIN");
quit(0);
