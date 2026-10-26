\\ theta_extremale_56.gp -- lot R112_X1_FICHE_CATALOGUE_20261026 (agent Claude n. 119, 26 oct. 2026).
\\ Serie theta extremale de dimension 56 (M_28 : base E4^(7-3b) Delta^b, b = 0..2 ; extremale = 1 + O(q^3)), calculee EXACTEMENT :
\\ coefficients |L_6| et |L_8| utilises par cover6 et cover8 de la chaine X1 (L et L' sont extremaux de dimension 56).
\\ Usage : gp -q -f theta_extremale_56.gp < /dev/null
N = 6;
E4 = 1 + 240*sum(n = 1, N, sigma(n, 3)*q^n) + O(q^(N+1));
D  = q*eta(q + O(q^(N+1)))^24;
B = vector(3, b, E4^(7-3*(b-1)) * D^(b-1));
M = matrix(3, 3, i, j, polcoef(B[j], i-1));
c = matsolve(M, [1,0,0]~);
th = sum(b = 1, 3, c[b]*B[b]);
check(lab, t) = if (t, print("[ok]    ", lab), print("[ECHEC] ", lab); quit(1));
check("norme 6 : 15 590 400 (= 2 x 7 795 200, orbites de F2)", polcoef(th, 3) == 15590400);
check("norme 8 : 36 957 286 800 (somme des orbites de F3)", polcoef(th, 4) == 36957286800);
check("expression de roiban (annexe B, table B1) : (-159 A^7 + 238 A^4 B + 161 A B^2)/240", th == (-159*E4^7 + 238*E4^4*(E4^3-720*D) + 161*E4*(E4^3-720*D)^2)/240);
for (m = 0, N, print("  norme ", 2*m, " : ", polcoef(th, m)));
quit(0);
