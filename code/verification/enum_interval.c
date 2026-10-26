/*
 * Enumeration of all lattice vectors of norm <= R that cannot miss a vector
 * (Fincke-Pohst / Schnorr-Euchner in interval arithmetic; paper §6.1 (a), Table 5).
 * 取りこぼしの無い、ノルム R 以下の全格子ベクトルの列挙
 * （区間演算による Fincke-Pohst / Schnorr-Euchner。論文 §6.1 (a)、表 5）。
 *
 * Input (stdin), written by lib/enumerate.py (enumerator_input; used by v1_min_L.py and short_vectors):
 * 入力（標準入力。lib/enumerate.py の enumerator_input が書く。v1_min_L.py と short_vectors が使う）:
 *   n R                         dimension, radius (an integer)
 *                               次元、半径（整数）
 *   G (n lines of n integers)   the Gram matrix of the (reduced) basis
 *                               （簡約した）基底の Gram 行列
 *   n lines "lo hi"             intervals containing D_i, where G = V^T diag(D) V
 *                               (only lo is used by the enumeration; hi is read for the sanity check lo <= hi)
 *                               G = V^T diag(D) V の D_i を含む区間
 *                               （列挙に使うのは lo だけ。hi は lo <= hi の確認のために読む）
 *   n(n-1)/2 lines "lo hi"      intervals containing V_ij (i < j), row by row
 *                               V_ij (i < j) を含む区間（行ごと）
 *
 * The norm of x is <x, x> = sum_i D_i (x_i + sum_{j>i} V_ij x_j)^2.  Coordinates are fixed
 * from i = n-1 down to 0; at level i the partial norm P_i = sum_{k>=i} D_k (...)^2 must stay
 * <= R.  Every quantity is kept as an interval [lo, hi] that is guaranteed to contain the
 * true real value, and a branch is cut only when the LOWER end of the partial norm exceeds R.
 * Hence no vector of true norm <= R is ever cut.
 * x のノルムは <x, x> = Σ_i D_i (x_i + Σ_{j>i} V_ij x_j)^2。座標を i = n-1 から 0 へ決め、各段で部分ノルム P_i ≤ R を保つ。
 * すべての量を、真の実数値を必ず含む区間 [lo, hi] で持ち、部分ノルムの区間の「下端」が R を超えたときだけ枝を切る。
 * したがって、真のノルムが R 以下のベクトルが切られることはない。
 *
 * Outward rounding: after each floating-point operation (round-to-nearest, relative error
 * at most 2^-53, absolute error at most 2^-1075 for subnormals) the result is widened by
 *     dn(a) = a - |a| 2^-51 - 2^-1060,   up(a) = a + |a| 2^-51 + 2^-1060,
 * which more than covers the rounding error, so the true value stays inside.
 * 外向きの丸め: 浮動小数点の各演算（最近接丸め。相対誤差 2^-53 以下、非正規化数では絶対誤差 2^-1075 以下）のあと、
 * 結果を上の dn, up で広げる。丸め誤差より十分大きいので、真の値は区間の中に残る。
 *
 * At a leaf (all coordinates fixed) the norm x G x^T is computed exactly with 128-bit
 * integers, so the reported vectors and counts are exact.
 * 葉（全座標が決まったところ）では、ノルム x G x^T を 128 ビット整数で厳密に計算する。報告する本数は厳密。
 *
 * Only one of +-x is enumerated (when all higher coordinates are 0, x_i >= 0); the output
 * counts are doubled to count both signs.
 * ±x の片方だけを列挙する（上の座標がすべて 0 のときは x_i ≥ 0）。出力の本数は 2 倍して両方の符号を数える。
 *
 * Output (stdout): the vectors found (one of each +-pair; at most the number given as the first
 * command-line argument, default 5) as "vector of norm q: x_0 ... x_{n-1}", then "nodes N leaves M",
 * one line per norm "nonzero vectors of norm q: count" (q < 4096), the line
 * "untabulated vectors of norm >= 4096: count" (vectors of norm <= R that do not fit the table;
 * the callers require 0), and "done".
 * 出力（標準出力）: 見つけたベクトル（±の片方。最初のコマンドライン引数で与えた本数まで。既定 5）を
 * 「vector of norm q: x_0 … x_{n-1}」の形で、続いて「nodes N leaves M」、ノルムごとに「nonzero vectors of norm q: 本数」
 * （q < 4096）、「untabulated vectors of norm >= 4096: 本数」（ノルム R 以下で表に収まらないベクトル。呼び出し側は 0 を要求する）、
 * 最後に「done」。
 *
 * Compile / コンパイル:  gcc -O2 -std=c11 -fno-fast-math -ffp-contract=off -o enum_interval enum_interval.c -lm
 * (-fno-fast-math and -ffp-contract=off keep every operation a separately rounded IEEE operation,
 *  as the error analysis above assumes.)
 * （-fno-fast-math と -ffp-contract=off で、各演算を個別に丸める IEEE の演算に保つ。上の誤差解析はそれを仮定する。）
 */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 64
static int n;
static long long R;
static long long G[MAXN][MAXN];
static double Dlo[MAXN], Dhi[MAXN];
static double Vlo[MAXN][MAXN], Vhi[MAXN][MAXN];
static long long x[MAXN];
/* ps[i][j] = interval containing sum_{l>=j} V_il x_l (the centre sums of row i).
 * ps[i][j] = Σ_{l≥j} V_il x_l（第 i 行の中心の部分和）を含む区間。 */
static double pslo[MAXN][MAXN + 1], pshi[MAXN][MAXN + 1];
/* pbeg[i]: highest coordinate whose change has not yet been propagated into the centre sums
 * of row i-1 (lazy update, as center_partsum_begin in fplll).
 * pbeg[i]: 第 i-1 行の中心の部分和にまだ反映していない変更のうち、最も上の座標（fplll の center_partsum_begin と同じ遅延更新）。 */
static int pbeg[MAXN];
/* zero_above[i]: all coordinates x_j with j >= i are 0. / zero_above[i]: j ≥ i の座標 x_j がすべて 0。 */
static int zero_above[MAXN + 1];
static unsigned long long nodes = 0, leaves = 0;
#define QMAX 4096
static unsigned long long found[QMAX];
static unsigned long long untabulated = 0; /* leaves of norm <= R outside 0 .. QMAX-1 / ノルム R 以下で 0 .. QMAX-1 の外にある葉 */
static long long printed = 0, maxprint = 5;

static inline double dn(double a) { return a - fabs(a) * 0x1p-51 - 0x1p-1060; }
static inline double up(double a) { return a + fabs(a) * 0x1p-51 + 0x1p-1060; }

/* A leaf: compute the norm exactly and record it.  / 葉: ノルムを厳密に計算して記録する。 */
static void leaf(void) {
    leaves++;
    int allzero = 1;
    for (int i = 0; i < n; i++)
        if (x[i]) { allzero = 0; break; }
    if (allzero) return;
    __int128 q = 0;
    for (int i = 0; i < n; i++) {
        if (!x[i]) continue;
        __int128 s = 0;
        for (int j = 0; j < n; j++) s += (__int128)G[i][j] * x[j];
        q += s * x[i];
    }
    if (q <= (__int128)R) {
        if (q >= 0 && q < QMAX) found[(int)q]++;
        else untabulated++;
        if (printed < maxprint) {
            printed++;
            printf("vector of norm %lld:", (long long)q);
            for (int i = 0; i < n; i++) printf(" %lld", x[i]);
            printf("\n");
        }
    }
}

/* Level i: all coordinates above i are fixed and their partial norm is >= P (P is a lower bound).
 * 段 i: i より上の座標は決まっていて、その部分ノルムは P 以上（P は下界）。 */
static void rec(int i, double P) {
    nodes++;
    if ((nodes & ((1ULL << 28) - 1)) == 0) {
        fprintf(stderr, "progress: %llu nodes, top coordinates", nodes);
        for (int j = n - 1; j >= n - 4 && j >= 0; j--) fprintf(stderr, " %lld", x[j]);
        fprintf(stderr, "\n");
        fflush(stderr);
    }
    /* centre c_i = -sum_{j>i} V_ij x_j lies in [-shi, -slo]. / 中心 c_i = -Σ_{j>i} V_ij x_j は [-shi, -slo] にある。 */
    double slo = pslo[i][i + 1], shi = pshi[i][i + 1];
    /* Remaining budget R - P (upper bound) and the radius sqrt(budget / D_i) (upper bound).
     * 残りの予算 R - P（上界）と半径 sqrt(予算 / D_i)（上界）。 */
    double rem = up((double)R - P);
    if (rem < 0) return;
    double r = up(sqrt(up(rem / Dlo[i])));
    /* All admissible x_i lie in [a, b]; one extra integer on each side for safety.
     * 許される x_i はすべて [a, b] に入る。念のため両側に整数を 1 つずつ足す。 */
    long long a = (long long)floor(dn(-shi - r)) - 1;
    long long b = (long long)ceil(up(-slo + r)) + 1;
    if (zero_above[i + 1] && a < 0) a = 0; /* one of +-x only / ±x の片方だけ */
    for (long long k = a; k <= b; k++) {
        /* t = x_i + sum_{j>i} V_ij x_j in [tlo, thi]; lower bound of t^2. / t の区間と t^2 の下界。 */
        double tlo = dn((double)k + slo), thi = up((double)k + shi);
        double t2;
        if (tlo <= 0.0 && thi >= 0.0)
            t2 = 0.0;
        else {
            double m = (tlo > 0.0) ? tlo : -thi;
            t2 = dn(m * m);
        }
        /* Lower bound of the new partial norm; cut only if it exceeds R.
         * 新しい部分ノルムの下界。これが R を超えるときだけ切る。 */
        double Pn = dn(P + dn(Dlo[i] * t2));
        if (Pn > (double)R) continue;
        x[i] = k;
        if (i == 0) {
            leaf();
            continue;
        }
        zero_above[i] = zero_above[i + 1] && (k == 0);
        /* Update the centre sums of row i-1 for the coordinates pbeg[i] .. i that changed.
         * 第 i-1 行の中心の部分和を、変化した座標 pbeg[i] .. i について更新する。 */
        for (int j = pbeg[i]; j >= i; j--) {
            if (x[j] == 0) {
                pslo[i - 1][j] = pslo[i - 1][j + 1];
                pshi[i - 1][j] = pshi[i - 1][j + 1];
                continue;
            }
            double u1 = Vlo[i - 1][j] * (double)x[j], u2 = Vhi[i - 1][j] * (double)x[j];
            double plo = (u1 <= u2) ? u1 : u2, phi = (u1 <= u2) ? u2 : u1;
            pslo[i - 1][j] = dn(pslo[i - 1][j + 1] + dn(plo));
            pshi[i - 1][j] = up(pshi[i - 1][j + 1] + up(phi));
        }
        if (pbeg[i] > pbeg[i - 1]) pbeg[i - 1] = pbeg[i];
        pbeg[i] = i;
        rec(i - 1, Pn);
    }
    x[i] = 0;
    /* x_i was reset to 0; row i-2 (governed by pbeg[i-1]) must later be updated from coordinate i.
     * (Row i-1 is always updated from coordinate i, see the loop above.)
     * x_i を 0 に戻したので、第 i-2 行（pbeg[i-1] が受け持つ）は後で座標 i から更新する必要がある。
     * （第 i-1 行は上のループで必ず座標 i から更新される。） */
    if (i > 0 && pbeg[i - 1] < i) pbeg[i - 1] = i;
}

int main(int argc, char **argv) {
    if (argc > 1) maxprint = atoll(argv[1]);
    if (scanf("%d %lld", &n, &R) != 2 || n < 1 || n > MAXN) {
        fprintf(stderr, "bad header\n");
        return 1;
    }
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            if (scanf("%lld", &G[i][j]) != 1) return 1;
    for (int i = 0; i < n; i++)
        if (scanf("%lf %lf", &Dlo[i], &Dhi[i]) != 2) return 1;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (scanf("%lf %lf", &Vlo[i][j], &Vhi[i][j]) != 2) return 1;
    for (int i = 0; i < n; i++)
        if (!(Dlo[i] > 0) || !(Dlo[i] <= Dhi[i])) {
            fprintf(stderr, "bad interval for D_%d\n", i);
            return 1;
        }
    memset(x, 0, sizeof x);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j <= n; j++) { pslo[i][j] = 0.0; pshi[i][j] = 0.0; }
        pbeg[i] = n - 1;
    }
    zero_above[n] = 1;
    rec(n - 1, 0.0);
    printf("nodes %llu leaves %llu\n", nodes, leaves);
    for (int q = 0; q < QMAX; q++)
        if (found[q]) printf("nonzero vectors of norm %d: %llu\n", q, 2 * found[q]);
    printf("untabulated vectors of norm >= %d: %llu\n", QMAX, 2 * untabulated);
    printf("done\n");
    return 0;
}
