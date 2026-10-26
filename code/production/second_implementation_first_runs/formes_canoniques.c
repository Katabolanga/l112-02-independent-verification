/*
 * formes_canoniques.c -- lot R112_X1_EFFORT_MAX_20261025 (agent Claude n° 116, 25 oct. 2026).
 * SECONDE IMPLEMENTATION, ecrite ici sans reprendre le code de roiban (lib/mod2.py), du calcul des formes canoniques des classes
 * modulo 2 sous un groupe fini de matrices sur F_2 : can(c) = min_{s} (c s), c dans F_2^56 code par un entier de 56 bits
 * (bit i = coordonnee i), et c s = XOR des lignes i de s pour les bits i de c.
 * Entree (binaire, petit-boutiste) : fichier GROUPE : uint64 m (nombre d'elements), puis m x 56 uint64 (ligne i de s, codee en bits) ;
 *   fichier CLASSES : uint64 N, puis N uint64.
 * Sortie (binaire) : N uint64 (formes canoniques), puis N uint32 (taille de l'orbite = m / #{s : c s = c}).
 * Methode : pour chaque element s, table par octet T_s[b][v] = XOR des lignes 8b+k (bits k de v), 7 x 256 entrees ;
 *   c s = XOR_b T_s[b][octet_b(c)].  Exact (entiers).  Usage : formes_canoniques GROUPE CLASSES SORTIE
 * Compilation : gcc -O2 -std=c11 -o formes_canoniques formes_canoniques.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char **argv) {
    if (argc != 4) { fprintf(stderr, "usage: %s GROUPE CLASSES SORTIE\n", argv[0]); return 2; }
    FILE *fg = fopen(argv[1], "rb"), *fc = fopen(argv[2], "rb"), *fo = fopen(argv[3], "wb");
    if (!fg || !fc || !fo) { fprintf(stderr, "ouverture impossible\n"); return 2; }
    uint64_t m, N;
    if (fread(&m, 8, 1, fg) != 1 || m == 0 || m > 100000) { fprintf(stderr, "groupe : en-tete\n"); return 3; }
    uint64_t *rows = malloc(m * 56 * 8);
    if (!rows || fread(rows, 8, m * 56, fg) != m * 56) { fprintf(stderr, "groupe : lecture\n"); return 3; }
    uint64_t *T = malloc(m * 7 * 256 * 8);
    if (!T) { fprintf(stderr, "memoire\n"); return 4; }
    for (uint64_t s = 0; s < m; s++)
        for (int b = 0; b < 7; b++) {
            uint64_t *t = T + (s * 7 + b) * 256;
            t[0] = 0;
            for (int v = 1; v < 256; v++) {
                int k = __builtin_ctz(v);
                t[v] = t[v & (v - 1)] ^ rows[s * 56 + 8 * b + k];
            }
        }
    if (fread(&N, 8, 1, fc) != 1) { fprintf(stderr, "classes : en-tete\n"); return 3; }
    uint64_t *C = malloc(N * 8), *can = malloc(N * 8);
    uint32_t *orb = malloc(N * 4);
    if (!C || !can || !orb || fread(C, 8, N, fc) != N) { fprintf(stderr, "classes : lecture\n"); return 3; }
    for (uint64_t i = 0; i < N; i++) {
        uint64_t c = C[i], best = UINT64_MAX;
        uint32_t stab = 0;
        unsigned char by[7];
        for (int b = 0; b < 7; b++) by[b] = (unsigned char)((c >> (8 * b)) & 255);
        for (uint64_t s = 0; s < m; s++) {
            const uint64_t *t = T + s * 7 * 256;
            uint64_t img = t[by[0]] ^ t[256 + by[1]] ^ t[512 + by[2]] ^ t[768 + by[3]] ^ t[1024 + by[4]] ^ t[1280 + by[5]] ^ t[1536 + by[6]];
            if (img < best) best = img;
            if (img == c) stab++;
        }
        can[i] = best;
        orb[i] = (stab > 0 && m % stab == 0) ? (uint32_t)(m / stab) : 0;
    }
    fwrite(can, 8, N, fo); fwrite(orb, 4, N, fo);
    fclose(fo);
    fprintf(stderr, "fini : %llu classes, groupe d'ordre %llu\n", (unsigned long long)N, (unsigned long long)m);
    return 0;
}
