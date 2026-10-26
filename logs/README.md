# Logs

All files here are **sanitized copies** of raw logs: local paths, user names, machine names, run identifiers and the name of an internal reviewer are replaced by neutral markers (`SANITIZATION.md` gives the rule, and the SHA-256 of each original and of each copy). Apart from these replacements the logs are unchanged; they are mostly in French. Hashes written inside a log refer to the original files. Times are local times (CET, UTC+1, on both machines) unless marked UTC or with an explicit offset.

## `machine_A/` (Windows 11 with WSL2)

| directory | contents |
|---|---|
| `first_pass_20261025/` | first implementation, 25 October: structure of the gluing, data of L, orbits of norms 6 and 8 (1 517 130 regular orbits, sum \|L₈\|), certificates in both directions, type (8,8) (0 hits on 1 528 956 pairs), first F1 run for L, first runs of the second implementation |
| `F1_L56_20261025/` | F1 for L56 and the three control inputs (replay of roiban1344's step v1): exit codes 0, 8 454 837 756 nodes |
| `F1_L_rerun_20261026/` | F1 for L rerun with the exit code captured: code 0, 9 905 828 434 nodes, output identical to the first run |
| `v3_runs_20261026/` | the corrected verifiers run in full on machine A (φ side 7/7, X1 0 hits, X4 20 hits), with three tests of the stop on missing data (code 2) |
| `verdict_v3_20261026/` | the verdict rule applied on machine A (12 conditions, CONFORME) and its manifest |
| `raccords_f1_20261026/` | exact correspondence between the inputs of F1 and the Gram matrices |
| `theta_20261026/` | theta series of extremal lattices of dimensions 56 and 112 (PARI/GP, exact) |
| `reduced_basis_check_20261026/` | checks of the reduced basis (`verify_X1.py`, figures of the README) |
| `reference_for_replication/` | the reference outputs of machine A given to the replication (the verdict of machine B compares its outputs with them), and short timing measurements |

## `machine_B/` (Linux)

| path | contents |
|---|---|
| `run_20261026/` | the replication run of 26 October 2026, 18:02–19:47 UTC: summary `BILAN_X1_REP_V2.txt`, verdict `VERDICT_X1_REP_V2.txt` (23 conditions out of 23 PASS), the log, exit code, duration and marker of each of the twelve steps, `GLOBAL.native.exit` and `VERDICT.native.exit`, the outputs of F1 and of the two runs of the second implementation, and the manifests |
| `service_record/UNIT_TERMINAL_BEFORE_STOP.txt` | the state of the service at the end of the run (exit status 0, `MemoryPeak=3807326208`, `MemorySwapPeak=0`, CPU time) |
| `ARCHIVE.md` | the complete raw archive of the run, which is not included |
