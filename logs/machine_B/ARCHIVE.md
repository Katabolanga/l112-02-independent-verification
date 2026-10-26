# The raw archive of the replication run (not included)

The complete raw output of the run on machine B (working directory, frozen copy, outputs, service records and transport records) was collected once, after the run, in a single archive:

| | |
|---|---|
| file name | `X1_REP_V2_20261026_1758_OWNER_RAW.zip` |
| size | 301 910 607 bytes |
| members | 364 |
| SHA-256 | `e91636b90b26ba077ea684cd332280df71e152be04fddb35f8006bb0b327f617` |

It is not included in this repository: most of its size is made of intermediate binary files of the second implementation (canonical forms, classes and groups modulo 2: 102 631 240 bytes per run once uncompressed, for X1 and for X4), of two copies of the frozen data, and of records of the infrastructure (359 017 697 bytes uncompressed in all). The files of `run_20261026/` and `service_record/` are sanitized copies of members of this archive; `../SANITIZATION.md` gives, for each of them, the member it comes from (under `work/EXEC_MACHINE_B_X1REP_V2_<TOKEN>/` unless stated otherwise) and the SHA-256 of the original member. The archive may be deposited later (for example as a release asset or on Zenodo).
