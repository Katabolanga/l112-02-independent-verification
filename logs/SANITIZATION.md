# Sanitization of the published copies

The logs, and the copies of the scripts and data files taken from the working directories, were copied into this repository with the replacements below, applied in this order to text files only. Binary files (`.npz`, `.npy`) are copied unchanged; they were checked not to contain these strings. Nothing else was changed. The masked values are not given. The SHA-256 of each original is given so that a holder of the originals can check each copy.

| masked item | marker | replacements made |
|---|---|---|
| root of the working directories on machine A | `<LOT>` | 59 |
| home directory on machine A (Windows path) | `<MACHINE_A>` | 0 |
| home directory on machine A (WSL path) | `<MACHINE_A>` | 12 |
| working root on machine B | `<MACHINE_B>` | 19 |
| home directory on machine B | `<MACHINE_B>` | 0 |
| temporary directory of an assistant session | `<SCRATCH>` | 0 |
| notes directory on machine A | `<NOTES>` | 0 |
| shared cloud folder | `<SHARED_DRIVE>` | 0 |
| cloud drive | `<SHARED_DRIVE>` | 0 |
| name of an internal exchange folder | `<BRIDGE>` | 0 |
| file name of an internal note | `<INTERNAL_NOTE>` | 4 |
| run token, service invocation identifier, boot identifier | `<TOKEN>` | 8 |
| cloud file identifier | `<DRIVE_ID>` | 0 |
| e-mail address | `<EMAIL>` | 0 |
| private IP address | `<IP>` | 0 |
| name of machine A | `MACHINE_A` | 118 |
| name of machine B | `MACHINE_B` | 44 |
| name of an AI reviewer | `<REVIEWER>` | 14 |
| user name | `<USER>` | 0 |

In names of files and directories, `MACHINE_A`, `MACHINE_B` and `TOKEN` are used without angle brackets (for example `REFERENCE_MACHINE_A`).

Origins: **A** = file of machine A; **B** = member of the raw archive of machine B (`logs/machine_B/ARCHIVE.md`), path relative to `work/EXEC_MACHINE_B_X1REP_V2_<TOKEN>/` unless it starts with `/`; **A-new** = log written on 26 October 2026 on machine A while preparing this repository.

| published file | origin | changed | SHA-256 of the original | SHA-256 of the published copy |
|---|---|---|---|---|
| `code/production/c1_verif_x1.py` | A | no | `77892a7f7b4a5e5116a844659d36e9cd7fa959c007a3c532d86be204ff072be7` | `77892a7f7b4a5e5116a844659d36e9cd7fa959c007a3c532d86be204ff072be7` |
| `code/production/certificats_impairs.py` | A | no | `2540615d70e41f280668b9724924527c1de94e0db73f64e4211a9ae31d26253e` | `2540615d70e41f280668b9724924527c1de94e0db73f64e4211a9ae31d26253e` |
| `code/production/certificats_impairs_x1.py` | A | no | `6eb5b35875f28914afc0fe4887d7e432868ce60486e35f5787043c4d296906d1` | `6eb5b35875f28914afc0fe4887d7e432868ce60486e35f5787043c4d296906d1` |
| `code/production/collisions8_x1.py` | A | no | `eb9d1b31284f97adc4f0115dc81527c8340ed62203c1a301fac24699e8be420a` | `eb9d1b31284f97adc4f0115dc81527c8340ed62203c1a301fac24699e8be420a` |
| `code/production/collisions8_x1_v3.py` | A | yes | `0f4630c239c2ecea37673388a22e435a025eabdafde3594ae7dc9e681b04eb1f` | `a21ea9162851b4f6277406c2b083c946adcd0b9ecbb345a89d2c5ce48cf0f7a3` |
| `code/production/donnees_L.py` | A | no | `13e277b8be89c8b1749fc85943e1bfe23aab3270a457bafd88048a5c5fb60204` | `13e277b8be89c8b1749fc85943e1bfe23aab3270a457bafd88048a5c5fb60204` |
| `code/production/isometrie_L4_L1.py` | A | no | `f2cbceee6ab53fd1cbaaf5d4552bd34c894a640f133774b92d532fee2415a473` | `f2cbceee6ab53fd1cbaaf5d4552bd34c894a640f133774b92d532fee2415a473` |
| `code/production/lancer_phase_finale_v2.sh` | A | yes | `40914225f7bb65d0dc7312d73f9b0c29f18de0653bf15da3f1d6f02a2cb5a77a` | `fc010398f8c27abf3d004c66c61d3e130c6b5f993cd8c9f4497fe279399ed25e` |
| `code/production/orbites8_L.py` | A | no | `310c7365171f113ee8d774424fcebf3ea4f9c4fcec8a35698e184fdfb45c57ce` | `310c7365171f113ee8d774424fcebf3ea4f9c4fcec8a35698e184fdfb45c57ce` |
| `code/production/orbites_min_L.py` | A | no | `d02491a1491c6199d88cff1f014fd3a28950a6b4bdf77522b4fb9299aabd4a19` | `d02491a1491c6199d88cff1f014fd3a28950a6b4bdf77522b4fb9299aabd4a19` |
| `code/production/raccord_f1.py` | A | yes | `880f8b8a643ed9c1780ff02f0dc93cdf9feada252baabacef17cce225782162d` | `17fd84ed4cde871c07fab1e28fa51c3904d06890ef65c3d63d74618b7d4df965` |
| `code/production/reduction_L.py` | A | no | `8bb957d03546d4c27da5213ea530b30805b2735ab7eb1e627d1c534d59c289da` | `8bb957d03546d4c27da5213ea530b30805b2735ab7eb1e627d1c534d59c289da` |
| `code/production/rejeu_roiban/rejouer_v1.sh` | A | no | `cfd2ecb5071a3d624e1800f265ae29d1b362f9da786bb50915347484cfbd89e8` | `cfd2ecb5071a3d624e1800f265ae29d1b362f9da786bb50915347484cfbd89e8` |
| `code/production/rejeu_roiban/rejouer_verify.sh` | A | no | `23adab47198cd98c55a5418344333302e692fbe2837066a3ede49384e0649487` | `23adab47198cd98c55a5418344333302e692fbe2837066a3ede49384e0649487` |
| `code/production/rejeu_roiban/v1_entrees_manuel.py` | A | no | `87b806c9bd813dd6df63f2afa01fa10ff880611e1f2ea86a86be07a3ba62f87f` | `87b806c9bd813dd6df63f2afa01fa10ff880611e1f2ea86a86be07a3ba62f87f` |
| `code/production/second_implementation_first_runs/formes_canoniques.c` | A | no | `f11282a5765d53f6f5f19a1ab8b04952c58ca76f9145189072b6c6a73dec7182` | `f11282a5765d53f6f5f19a1ab8b04952c58ca76f9145189072b6c6a73dec7182` |
| `code/production/second_implementation_first_runs/lancer_verif_independante_v3.sh` | A | yes | `a89ab7cd8e64627cdceefea97c23182012b875394b4788428cf5f7f3a071a605` | `d3ce186a7bf8304d004584f1c4575481375c9e562adebcf7570ccec85a5547ba` |
| `code/production/second_implementation_first_runs/test_formes.py` | A | no | `dee47665e1341fc8bc609f1ed421623148bad05fdf1572ca9e62dc72c7033fd6` | `dee47665e1341fc8bc609f1ed421623148bad05fdf1572ca9e62dc72c7033fd6` |
| `code/production/second_implementation_first_runs/verif_independante_int16.py` | A | no | `bb48fa0d25b2630bada7c90cc1f9383d8bcb25d874eca95a737d4ca243bcda11` | `bb48fa0d25b2630bada7c90cc1f9383d8bcb25d874eca95a737d4ca243bcda11` |
| `code/production/second_implementation_first_runs/verif_phi_L56_int64.py` | A | no | `53526cdc4678977a27f14f3f9a0dff1377e52c86e37a524ca8e9353ecd14831f` | `53526cdc4678977a27f14f3f9a0dff1377e52c86e37a524ca8e9353ecd14831f` |
| `code/production/structure_classe.py` | A | no | `6f76663a26eadd171bbca6d8ba801f6a068318f8ccaa9dc3b8663071e861a94c` | `6f76663a26eadd171bbca6d8ba801f6a068318f8ccaa9dc3b8663071e861a94c` |
| `code/production/structure_x1.py` | A | no | `94075136be1cc78144c62ce99f4251903923298b934314cb5d05cb837b34af28` | `94075136be1cc78144c62ce99f4251903923298b934314cb5d05cb837b34af28` |
| `code/production/suite_apres_p3_v2.sh` | A | yes | `3f2f8725f618a50041408e9baedab3af21974db4c0d6afd71015fcb0c6169319` | `c2f72df1be0dab7caac543c615477c5a63be331ca6be12a1b7f4915c7f97150b` |
| `code/production/transporter_L4.py` | A | no | `4035277dad6dace11fe7244bb51b35b801ca1b740810ca58a7ed344b78aa58ef` | `4035277dad6dace11fe7244bb51b35b801ca1b740810ca58a7ed344b78aa58ef` |
| `code/production/verdict_x1_v3.py` | A | yes | `86f5f523dfdcebbbdb02613edb1ec7150e1a40984246db7b336970f3bdf25090` | `b12da85e49fe498f3a2a35ab7de532da2820463118e2adf7163f69ee6cc80553` |
| `code/reduced_basis/bkz_x1.py` | A | no | `0932a6b09be8ad2ccacca4e191d08eb2e61ab4b0b61f950859a9d933c251f4d7` | `0932a6b09be8ad2ccacca4e191d08eb2e61ab4b0b61f950859a9d933c251f4d7` |
| `code/reduced_basis/export_fiche_x1.py` | A | no | `e90479ca2948b8d254637af7895a5359a7550eb828f753207ec7f2aabb0ce58c` | `e90479ca2948b8d254637af7895a5359a7550eb828f753207ec7f2aabb0ce58c` |
| `code/reduced_basis/groupe_x1.py` | A | no | `c52035d4e90ead8d42289998c492c82a0cd039a0d557dcbbde3060cda50b584f` | `c52035d4e90ead8d42289998c492c82a0cd039a0d557dcbbde3060cda50b584f` |
| `code/reduced_basis/ordre_par_orbite.py` | A | no | `3d878d94c9db897724290eb6bd88aa819ebe20a7a7d6f8162d2007cbd1d6c829` | `3d878d94c9db897724290eb6bd88aa819ebe20a7a7d6f8162d2007cbd1d6c829` |
| `code/reduced_basis/reservoir_x1.py` | A | no | `c5f9077dfd477f0a82edbaacf39404a2435c6722b6ddefbdf2d769b91f1d5c01` | `c5f9077dfd477f0a82edbaacf39404a2435c6722b6ddefbdf2d769b91f1d5c01` |
| `code/reduced_basis/seysen_pondere_x1.py` | A | no | `7f3f0c342935e22acf5cfee9d64a1b84fa5186a68756afcc599f2b95a6c18f4d` | `7f3f0c342935e22acf5cfee9d64a1b84fa5186a68756afcc599f2b95a6c18f4d` |
| `code/reduced_basis/theta_extremale_112.gp` | A | no | `aea37d59306062d2999e28d9ea63d5910629313c64a110981b6abd100537611e` | `aea37d59306062d2999e28d9ea63d5910629313c64a110981b6abd100537611e` |
| `code/replication/lancer_x1_rep_v2.sh` | A | yes | `407e5abd3d7a05994d605e7d4a15b5075639658f1c45d8e9ffdac4fd285ca82f` | `c2293788e922207a09a8a2787e6c809f6b5dcf868041e78987a2cdbdeef8d3c5` |
| `code/replication/verdict_x1_rep_v2.py` | A | yes | `a099f80e29c5e35d2a7de907b09dc64a081afdaa2279c2c0e341aa7cfdb4f591` | `a2c7a44682a6047fb011e29a1d50da53932ef332a6d26ba1a509357c551e2aa4` |
| `code/verification/enum_interval.c` | A | no | `80d0ffcacd79863ac6fb55c4afa2ed3df1251339691209bf73f91a60ca897098` | `80d0ffcacd79863ac6fb55c4afa2ed3df1251339691209bf73f91a60ca897098` |
| `code/verification/formes_canoniques.c` | A | no | `f11282a5765d53f6f5f19a1ab8b04952c58ca76f9145189072b6c6a73dec7182` | `f11282a5765d53f6f5f19a1ab8b04952c58ca76f9145189072b6c6a73dec7182` |
| `code/verification/parite_x1_rep_v1.py` | A | yes | `41eea587a552b08f188536f4a3dbc6c95d5b60e129508e5c4acd9c9ca7fecca2` | `1616a9526d5a12ec15b040e98c7aa5a54f85f9a61dbb17d6a2692d2f56cd729b` |
| `code/verification/raccord_entrees_f1_rep_v1.py` | A | yes | `9747ae72bfadb4f29612e50940e80abbe6ac00ad1fc2d5ca4ff1db398f338911` | `25a0e184d1ae900bcea15d67ac457e342b54a731c09df9719c94754674dffa3f` |
| `code/verification/theta_extremale_56.gp` | A | no | `cd24c01b9461eabc0cb74ee78c40b442d6b6d105f753af0210701ce878104714` | `cd24c01b9461eabc0cb74ee78c40b442d6b6d105f753af0210701ce878104714` |
| `code/verification/verdict_x1_v3_POUR_MEMOIRE.py` | A | yes | `86f5f523dfdcebbbdb02613edb1ec7150e1a40984246db7b336970f3bdf25090` | `b12da85e49fe498f3a2a35ab7de532da2820463118e2adf7163f69ee6cc80553` |
| `code/verification/verif_independante_int16_v3.py` | A | yes | `a0a823862b063efb7dfda6674cbf73e4ec272f0794b3d4816d2df9b9a746cce3` | `38d4245605f8f39e6a5bfb67247d51d87ea1b5c1d5d609e8b3198c6716ad42da` |
| `code/verification/verif_phi_L56_int64_v3.py` | A | yes | `4f94f6ec72ee3fc9ca4b72e1f251cbe0c294f8059802307cd9073d0d7d384077` | `483bd01d7758f748006985f0ba9b4ef077e04040ef92e92002250776a450b7eb` |
| `data/frozen/F1/E8.entree` | A | no | `700aa54b52e6c2f9c33fb32271f83b7749913bfff2e6dfa365e52a9d59f4d97e` | `700aa54b52e6c2f9c33fb32271f83b7749913bfff2e6dfa365e52a9d59f4d97e` |
| `data/frozen/F1/L56.entree` | A | no | `7a484d9506a3b5871c063d3b8ef98e464cbd890a35d00aa0c964bfb0eb920ed9` | `7a484d9506a3b5871c063d3b8ef98e464cbd890a35d00aa0c964bfb0eb920ed9` |
| `data/frozen/F1/L_bkz40_rayon4.entree` | A | no | `9c3ff4530faa75a97ef39a14e0ac098f6e841882d7431b51bb79a4c140752dac` | `9c3ff4530faa75a97ef39a14e0ac098f6e841882d7431b51bb79a4c140752dac` |
| `data/frozen/F1/leech.entree` | A | no | `d930b1f97cc448f31bdcf3c7f1ffc59c1a88a5afd0bb051e45f955696f2ee626` | `d930b1f97cc448f31bdcf3c7f1ffc59c1a88a5afd0bb051e45f955696f2ee626` |
| `data/frozen/F1/leech2_e8.entree` | A | no | `458892d6949ccf8c03d367787958c3ae059109ffe40035ca9f6a11dc9b82074a` | `458892d6949ccf8c03d367787958c3ae059109ffe40035ca9f6a11dc9b82074a` |
| `data/frozen/F1/reduction_L_bkz40.npz` | A | no | `bf0b7057459b12f1d9b010a85ee7fc1b16f3f6ae69e508037213eb363dc4a991` | `bf0b7057459b12f1d9b010a85ee7fc1b16f3f6ae69e508037213eb363dc4a991` |
| `data/frozen/X1/certificats_X1/certificats_phi_L_vers_L56.npz` | A | no | `0d67074d53a0beff5b55b85b6f36e0b787817481d3d471adfa9bfa6ac13aeec6` | `0d67074d53a0beff5b55b85b6f36e0b787817481d3d471adfa9bfa6ac13aeec6` |
| `data/frozen/X1/certificats_X1/certificats_psi_L56_vers_L.npz` | A | no | `94d0171a10eda461c2b2b59b3e0821b21a29442852fe5d704854a79f46974d99` | `94d0171a10eda461c2b2b59b3e0821b21a29442852fe5d704854a79f46974d99` |
| `data/frozen/X1/donnees_L.npz` | A | no | `c62aa6e14bf2857d4f07e879d7aac0093b77c3863359079c27da5fd5be0aaf61` | `c62aa6e14bf2857d4f07e879d7aac0093b77c3863359079c27da5fd5be0aaf61` |
| `data/frozen/X1/min_reps_L.npz` | A | no | `cb973f33c6d878e30c29193217e17002ba89677315a1d1715b99cea8827120cc` | `cb973f33c6d878e30c29193217e17002ba89677315a1d1715b99cea8827120cc` |
| `data/frozen/X1/norm8_reps_L.npz` | A | no | `d80385e498ffa7f66df16c764b2e57bff131baaddac446341b15fd84387f8a7a` | `d80385e498ffa7f66df16c764b2e57bff131baaddac446341b15fd84387f8a7a` |
| `data/frozen/X1/structure_x1.npz` | A | no | `33ec8ffda0cb3ec5094f2ac88e31614f74746d63d7e28c621db60398f1cebe4c` | `33ec8ffda0cb3ec5094f2ac88e31614f74746d63d7e28c621db60398f1cebe4c` |
| `data/frozen/X4/certificats/certificats_phi_L_vers_L56.npz` | A | no | `9c7d363361c5514496263771dda3ab48cca74161b6ccbad6bbed5fc5a9abf925` | `9c7d363361c5514496263771dda3ab48cca74161b6ccbad6bbed5fc5a9abf925` |
| `data/frozen/X4/certificats/certificats_psi_L56_vers_L.npz` | A | no | `bc9ebea6805777d1b1245dbbcf9cbeb687198def957d216098affcbbc6c13981` | `bc9ebea6805777d1b1245dbbcf9cbeb687198def957d216098affcbbc6c13981` |
| `data/frozen/X4/donnees_L4.npz` | A | no | `80b198cac8e8d4e5c0a0713f77c716d4c93a5b664430d1ad9423fc8ce9dd9f17` | `80b198cac8e8d4e5c0a0713f77c716d4c93a5b664430d1ad9423fc8ce9dd9f17` |
| `data/frozen/X4/min_reps_L4.npz` | A | no | `8222d326ad6aa44b21224f97fce71bed661b4a73eb9b4626aeca7a30e43d9ee2` | `8222d326ad6aa44b21224f97fce71bed661b4a73eb9b4626aeca7a30e43d9ee2` |
| `data/frozen/X4/norm8_reps_L4.npz` | A | no | `d27788ba951ea92cad4f5399eedc353126fb8cb04b809bb8bb93d8a4032808dc` | `d27788ba951ea92cad4f5399eedc353126fb8cb04b809bb8bb93d8a4032808dc` |
| `data/frozen/X4/structure_X4.npz` | A | no | `e2885ada7ce8fcf65e85dacb8eee6752507f36aa3512da79d547621d8630de5f` | `e2885ada7ce8fcf65e85dacb8eee6752507f36aa3512da79d547621d8630de5f` |
| `data/reduced_basis/X1_generators.txt` | A | no | `208f84c9738c7d00bb7f68de129f3a5a7ebe7fa5011416314f1b5e78b5d5809b` | `208f84c9738c7d00bb7f68de129f3a5a7ebe7fa5011416314f1b5e78b5d5809b` |
| `data/reduced_basis/X1_generators_gap.txt` | A | no | `e1eb638dd3a0f5846e3841dda52f52321a6ffb9511118e77a92cb390a160430c` | `e1eb638dd3a0f5846e3841dda52f52321a6ffb9511118e77a92cb390a160430c` |
| `data/reduced_basis/X1_gram.txt` | A | no | `245dfd73e36fef88df7a7bdbabf20d097b5ac7aebdd4a2805b54e50b0fdeec36` | `245dfd73e36fef88df7a7bdbabf20d097b5ac7aebdd4a2805b54e50b0fdeec36` |
| `data/reduced_basis/X1_gram_gap_magma.txt` | A | no | `20249cd61760f64afe1da317027c577f2f33a1c7ed0690b1cae993032fd706c3` | `20249cd61760f64afe1da317027c577f2f33a1c7ed0690b1cae993032fd706c3` |
| `data/reduced_basis/X1_passage_from_roiban.txt` | A | no | `391e83b10e999cbbb7b9a5d51a8ec8adf00e797167491f2570a72a419b356e7e` | `391e83b10e999cbbb7b9a5d51a8ec8adf00e797167491f2570a72a419b356e7e` |
| `data/reduced_basis/verify_X1.py` | A | no | `de4a86b6dbbc715d93894cd63205096dd693663fd377413b10933fa54badc8fe` | `de4a86b6dbbc715d93894cd63205096dd693663fd377413b10933fa54badc8fe` |
| `lean/ChainX1.lean` | A | no | `ea110b2d472808c6a02a76d3b617ec3fece89770609967067ffeadbfb766bf43` | `ea110b2d472808c6a02a76d3b617ec3fece89770609967067ffeadbfb766bf43` |
| `lean/ChainX1_avec_axiomes.lean` | A | no | `7caa947ff246fc51575aeec4ad4ff37a486c5422f87e2e8aa9e4561d7ef5540e` | `7caa947ff246fc51575aeec4ad4ff37a486c5422f87e2e8aa9e4561d7ef5540e` |
| `lean/ChainX1_axiomes_4_32.log` | A | no | `21d254ea45f3941f692b0a651f93e05b06eb6c25fa5684817b5dac7cff890442` | `21d254ea45f3941f692b0a651f93e05b06eb6c25fa5684817b5dac7cff890442` |
| `lean/ChainX1_compilation_4_32.log` | A | no | `b9210a494c88fb4b1cf76263f32b85ca05e61bf32f76df08be054d54f4e44fe5` | `b9210a494c88fb4b1cf76263f32b85ca05e61bf32f76df08be054d54f4e44fe5` |
| `lean/compiler_lean.sh` | A | no | `f23ddd95738c5fb00ee77537d80a33d9698f7a424169b1ef45d9f772205159ad` | `f23ddd95738c5fb00ee77537d80a33d9698f7a424169b1ef45d9f772205159ad` |
| `logs/machine_A/F1_L56_20261025/E8.sortie` | A | no | `06e6de43a5e92107d352ccbae51a9ec280fc81641e6dfbcbcb6ff6cbb5d8b3c4` | `06e6de43a5e92107d352ccbae51a9ec280fc81641e6dfbcbcb6ff6cbb5d8b3c4` |
| `logs/machine_A/F1_L56_20261025/L56.err` | A | no | `4ea7eb18ba1eded220b9d6aee8eeadf7e4fe315c05bfb7a2776c09d97ae90757` | `4ea7eb18ba1eded220b9d6aee8eeadf7e4fe315c05bfb7a2776c09d97ae90757` |
| `logs/machine_A/F1_L56_20261025/L56.sortie` | A | no | `74ee726854f4525991ef7a7faa65eb5bc863d84f9feead8d2b62cd54b69f7f27` | `74ee726854f4525991ef7a7faa65eb5bc863d84f9feead8d2b62cd54b69f7f27` |
| `logs/machine_A/F1_L56_20261025/codes.txt` | A | no | `c77ecaafdbf7577b9a926fd8c4d7cca293db27d55079e5fb27b29599409b393e` | `c77ecaafdbf7577b9a926fd8c4d7cca293db27d55079e5fb27b29599409b393e` |
| `logs/machine_A/F1_L56_20261025/compilation.sha256` | A | yes | `f17353ca4bc1e039032530ea98ffe011c0ecd3f1c5ed00e5ac3dc6fab218ea24` | `10c17f1bf94a23c8cbbacd3b1bf52330a56931f044ea226d434f7a2e58fffb62` |
| `logs/machine_A/F1_L56_20261025/horodatage.txt` | A | no | `2426fc79ffbb410c3efefc34a2882f0bcc0f4beeccd5558b237bc02ab1393cd7` | `2426fc79ffbb410c3efefc34a2882f0bcc0f4beeccd5558b237bc02ab1393cd7` |
| `logs/machine_A/F1_L56_20261025/leech.sortie` | A | no | `2ff00f89fe395c03bf9f2a72564f7ee351548b2db3218b78450a267e121f478a` | `2ff00f89fe395c03bf9f2a72564f7ee351548b2db3218b78450a267e121f478a` |
| `logs/machine_A/F1_L56_20261025/leech2_e8.sortie` | A | no | `db77c9a12aa29d35951454899932505468724c880f159236af6a6e6032ea5c70` | `db77c9a12aa29d35951454899932505468724c880f159236af6a6e6032ea5c70` |
| `logs/machine_A/F1_L_rerun_20261026/L_bkz40_rayon4.err` | A | no | `2ca807ce607ac949fc22c548bce4b50c8aeaa810ff2961848746d92e55a91c7e` | `2ca807ce607ac949fc22c548bce4b50c8aeaa810ff2961848746d92e55a91c7e` |
| `logs/machine_A/F1_L_rerun_20261026/L_bkz40_rayon4.sortie` | A | no | `219ba069bdf53e353b7a5ea96297a558d79f36d02499c69617ca11f66a1f6b24` | `219ba069bdf53e353b7a5ea96297a558d79f36d02499c69617ca11f66a1f6b24` |
| `logs/machine_A/F1_L_rerun_20261026/SHA256SUMS.txt` | A | no | `6bea80ec948a09b97085f9363b68f18c5c26dddda0e20fbf59ad65a7aa396e0a` | `6bea80ec948a09b97085f9363b68f18c5c26dddda0e20fbf59ad65a7aa396e0a` |
| `logs/machine_A/F1_L_rerun_20261026/SHA_ENTREES.txt` | A | no | `29d9ccaf2266b124c4c2cf2a4613de338eee26667be0b73d9a5d7a3f14963ede` | `29d9ccaf2266b124c4c2cf2a4613de338eee26667be0b73d9a5d7a3f14963ede` |
| `logs/machine_A/F1_L_rerun_20261026/code_natif.txt` | A | no | `fa8d778fcde98ccb5659c7237febc24f05d9048f4994252866a25678be4d4515` | `fa8d778fcde98ccb5659c7237febc24f05d9048f4994252866a25678be4d4515` |
| `logs/machine_A/F1_L_rerun_20261026/horodatage.txt` | A | no | `1af21393ffc1bff03fb4dda2f1b941248de3d2e3075e07133a7bce041a2602e5` | `1af21393ffc1bff03fb4dda2f1b941248de3d2e3075e07133a7bce041a2602e5` |
| `logs/machine_A/F1_L_rerun_20261026/lancer_f1l_natif.sh` | A | yes | `e7251c8d61edbfa665188064d303147f8dfe19f262b659b12c7a313c421bd020` | `10ee1a71959ebbe3abfc54d53c5e02dd28de204194228e7cfc7ffbf596ca9326` |
| `logs/machine_A/first_pass_20261025/F1_L/L_bkz40_rayon4.err` | A | no | `2ca807ce607ac949fc22c548bce4b50c8aeaa810ff2961848746d92e55a91c7e` | `2ca807ce607ac949fc22c548bce4b50c8aeaa810ff2961848746d92e55a91c7e` |
| `logs/machine_A/first_pass_20261025/F1_L/L_bkz40_rayon4.sortie` | A | no | `219ba069bdf53e353b7a5ea96297a558d79f36d02499c69617ca11f66a1f6b24` | `219ba069bdf53e353b7a5ea96297a558d79f36d02499c69617ca11f66a1f6b24` |
| `logs/machine_A/first_pass_20261025/F1_L/horodatage.txt` | A | no | `92f0e8b7d1befdf45d1761dc7c74dacf36f97041676720475dd21e3ef836d9f9` | `92f0e8b7d1befdf45d1761dc7c74dacf36f97041676720475dd21e3ef836d9f9` |
| `logs/machine_A/first_pass_20261025/F1_L/reduction.log` | A | yes | `aea92f1f3d2918fb00f86b2b54f0d809c1411d3f350707523e03c2d084acb876` | `a1840e7f4893c36f07c2c6a4a3f25364500924d3ef003caa6f5606bcc5cd78f8` |
| `logs/machine_A/first_pass_20261025/c1_verif/sortie.log` | A | no | `7ad2b94cb565b962d73d242b9a4017d98aff03fe6a7c7337d04420b95c85c52d` | `7ad2b94cb565b962d73d242b9a4017d98aff03fe6a7c7337d04420b95c85c52d` |
| `logs/machine_A/first_pass_20261025/certificats_X1/certificats_impairs_x1.json` | A | no | `74e6f759d19d0f457e506d0155ab8950b9393c08ab9a3ed9cc5727337a1877dd` | `74e6f759d19d0f457e506d0155ab8950b9393c08ab9a3ed9cc5727337a1877dd` |
| `logs/machine_A/first_pass_20261025/certificats_X1/sortie.log` | A | yes | `4e4ff6c834592aada94b023ed82e7a54eac31ace538b46ed6e13c2b7fdc013c0` | `1f25ed107f936102ce1d91f77a5212a8e1f83a984562774632fc56a6c5227f96` |
| `logs/machine_A/first_pass_20261025/collisions8_X1/collisions8_X1.json` | A | no | `9c115a96560930a25704052b1e2f97df1a59e43ccf00b38725e8c0269369b5dc` | `9c115a96560930a25704052b1e2f97df1a59e43ccf00b38725e8c0269369b5dc` |
| `logs/machine_A/first_pass_20261025/collisions8_X1/sortie.log` | A | yes | `09524ad07a77e478824bc5cdcc0c9de9656c046577608e36a9b54e161a3010a5` | `eb3ebf41eff3df94e474516bd607f9d7abdedad213db5c5f9418f1e7c865832f` |
| `logs/machine_A/first_pass_20261025/donnees_L/sortie.log` | A | yes | `8cbea3ee648dc5ce2f8fad08a60953e3c47d52071556af01e2a9d3ee1d88cc1a` | `4a3fa92d14400be4d969d6cbb6bf28ee188e234fda3db3471f571fa6b71787f7` |
| `logs/machine_A/first_pass_20261025/independant/X1_int16/horodatage.txt` | A | no | `b6ee4ba6e972250c640f31d103fcde64914d8f2de6c0d2a92901cfc681850fa3` | `b6ee4ba6e972250c640f31d103fcde64914d8f2de6c0d2a92901cfc681850fa3` |
| `logs/machine_A/first_pass_20261025/independant/X1_int16/sortie.log` | A | no | `12f7f81365f8ff1fbadca417df53743a756ccf6694d25de4f4dca17e52c94570` | `12f7f81365f8ff1fbadca417df53743a756ccf6694d25de4f4dca17e52c94570` |
| `logs/machine_A/first_pass_20261025/independant/X1_phi_int64/sortie_v2.log` | A | no | `0d5be64d4f551f22302f0bac29fea72bb8f0ccc3428012cae733e00a9a337e91` | `0d5be64d4f551f22302f0bac29fea72bb8f0ccc3428012cae733e00a9a337e91` |
| `logs/machine_A/first_pass_20261025/independant/X4_int16/horodatage.txt` | A | no | `eba691d11a607a18e3b80ac7b0a772b754a8560f6f31bd2ab500b3f86fa2234a` | `eba691d11a607a18e3b80ac7b0a772b754a8560f6f31bd2ab500b3f86fa2234a` |
| `logs/machine_A/first_pass_20261025/independant/X4_int16/sortie.log` | A | no | `4a557116a6bb360fe89ffc4111a788fc32f02075da2a8e7d4bef54791cb04f37` | `4a557116a6bb360fe89ffc4111a788fc32f02075da2a8e7d4bef54791cb04f37` |
| `logs/machine_A/first_pass_20261025/orbites8_L_v2/orbites8_L.json` | A | no | `56ebad955ec700f7d944e162672f4cc5fd72020b8835f153f439565ae401b7bb` | `56ebad955ec700f7d944e162672f4cc5fd72020b8835f153f439565ae401b7bb` |
| `logs/machine_A/first_pass_20261025/orbites8_L_v2/sortie.log` | A | yes | `6aceb0e9a908db0f1ad1778ac6061f9150ed39b641ed023c9b932e0071828017` | `96e4637f21d23b1ff1c5c3f956ff5b932f3fe6a1b3e9620eef4e1d36732aa4bc` |
| `logs/machine_A/first_pass_20261025/orbites_min_L/orbites_min_L.json` | A | no | `1da413df371964a2051572c932d42b16a55e1be91abfcc84161fd4a966d0cc91` | `1da413df371964a2051572c932d42b16a55e1be91abfcc84161fd4a966d0cc91` |
| `logs/machine_A/first_pass_20261025/orbites_min_L/sortie.log` | A | yes | `8e9cf6855cebac8d671bd30104d3af9b75e66720149b49e905f0cf314bcb0c6b` | `44f9e5e03b1a3e12f325dbe0e5b6878db20810f30edb39f5405ae5dca791908a` |
| `logs/machine_A/first_pass_20261025/rejeu_x7/journal_verify.txt` | A | no | `a340cdf348bce0ce60b92864245c1cf39c5d7e58f7d89f12ea640098a8e3a10d` | `a340cdf348bce0ce60b92864245c1cf39c5d7e58f7d89f12ea640098a8e3a10d` |
| `logs/machine_A/first_pass_20261025/structure_X4/sortie.log` | A | yes | `7168c1021d93bb37372c41b68e6f418c9af299870f7ad17c5203ad77fae35cea` | `261dad255473eb9befaa37afe59bf8e3b29e9275cf5e8a122c2c56d6ba8a8586` |
| `logs/machine_A/first_pass_20261025/structure_x1/sortie.log` | A | yes | `7f93444b1fdfed4ee52d1eb32811211db0947c7e6bf270b8a21a6977329abd87` | `9442aa0b5c91ec7f55c1230b9bae777634dd5c103f908c2e14ed6829efb03a2a` |
| `logs/machine_A/first_pass_20261025/structure_x1/structure_x1.txt` | A | yes | `1f6c1002d3deb6861a3c1a8b1892e1e5f73c00ae490f972185c5d1162a4d5f4b` | `03e8cdf6709329864612eb3bc0f04cb04c37a84175f7a9e8478999018090af16` |
| `logs/machine_A/raccords_f1_20261026/raccord_L.txt` | A | no | `5213a6b12f1e0ce973764d1569d890d33f09a8c30a91da11c944867b6ed8613d` | `5213a6b12f1e0ce973764d1569d890d33f09a8c30a91da11c944867b6ed8613d` |
| `logs/machine_A/raccords_f1_20261026/raccord_L56.txt` | A | no | `15e17e4f65bb4c5b7d5d8d023e03d5567fd4ba0b8033592d5e277fc88d5045ec` | `15e17e4f65bb4c5b7d5d8d023e03d5567fd4ba0b8033592d5e277fc88d5045ec` |
| `logs/machine_A/reduced_basis_check_20261026/compute_reduced_basis_figures.log` | A-new | no | `8778689c85cba35e854be07abec649d0b66a0a68a97738e98cae3e90b0038570` | `8778689c85cba35e854be07abec649d0b66a0a68a97738e98cae3e90b0038570` |
| `logs/machine_A/reduced_basis_check_20261026/horodatage.txt` | A | no | `3bf7fb88b33ebc74ad16df6315367390fcaa756dc8ac317dd90042405280a283` | `3bf7fb88b33ebc74ad16df6315367390fcaa756dc8ac317dd90042405280a283` |
| `logs/machine_A/reduced_basis_check_20261026/verify_L112.02_reduced_against_published_gram.log` | A-new | no | `2df401f6f1a654f6b7e6c500b6e827cbc966f9a3f68c0cf4596ef0ec90013223` | `2df401f6f1a654f6b7e6c500b6e827cbc966f9a3f68c0cf4596ef0ec90013223` |
| `logs/machine_A/reduced_basis_check_20261026/verify_X1.log` | A | no | `b0d2a7b4dcf4f0641cb51a2e68f0eabeffb0714582cfcce2157501d5a82a1983` | `b0d2a7b4dcf4f0641cb51a2e68f0eabeffb0714582cfcce2157501d5a82a1983` |
| `logs/machine_A/reference_for_replication/F1_E8.sortie` | A | no | `06e6de43a5e92107d352ccbae51a9ec280fc81641e6dfbcbcb6ff6cbb5d8b3c4` | `06e6de43a5e92107d352ccbae51a9ec280fc81641e6dfbcbcb6ff6cbb5d8b3c4` |
| `logs/machine_A/reference_for_replication/F1_L56.sortie` | A | no | `74ee726854f4525991ef7a7faa65eb5bc863d84f9feead8d2b62cd54b69f7f27` | `74ee726854f4525991ef7a7faa65eb5bc863d84f9feead8d2b62cd54b69f7f27` |
| `logs/machine_A/reference_for_replication/F1_L56_horodatage.txt` | A | no | `2426fc79ffbb410c3efefc34a2882f0bcc0f4beeccd5558b237bc02ab1393cd7` | `2426fc79ffbb410c3efefc34a2882f0bcc0f4beeccd5558b237bc02ab1393cd7` |
| `logs/machine_A/reference_for_replication/F1_L_bkz40_rayon4.sortie` | A | no | `219ba069bdf53e353b7a5ea96297a558d79f36d02499c69617ca11f66a1f6b24` | `219ba069bdf53e353b7a5ea96297a558d79f36d02499c69617ca11f66a1f6b24` |
| `logs/machine_A/reference_for_replication/F1_L_rejeu_horodatage.txt` | A | no | `1af21393ffc1bff03fb4dda2f1b941248de3d2e3075e07133a7bce041a2602e5` | `1af21393ffc1bff03fb4dda2f1b941248de3d2e3075e07133a7bce041a2602e5` |
| `logs/machine_A/reference_for_replication/F1_leech.sortie` | A | no | `2ff00f89fe395c03bf9f2a72564f7ee351548b2db3218b78450a267e121f478a` | `2ff00f89fe395c03bf9f2a72564f7ee351548b2db3218b78450a267e121f478a` |
| `logs/machine_A/reference_for_replication/F1_leech2_e8.sortie` | A | no | `db77c9a12aa29d35951454899932505468724c880f159236af6a6e6032ea5c70` | `db77c9a12aa29d35951454899932505468724c880f159236af6a6e6032ea5c70` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/B01_compil_enum.log` | A | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/B01_compil_enum.time` | A | yes | `ad2976546da765762eb61a39ebb2b61430719c118e4d8700956c6d38309023a3` | `3528bc5c7e0ea73ec0f27d9b961fb8d3189645b73a41a0ef0232a3ddfaeb6944` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/B02_compil_formes.log` | A | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/B02_compil_formes.time` | A | yes | `51ff514b9275c0096018b2328279b4d185292fea3b9acd62e99b6319d7616fa3` | `431f43c8902e6f83dfad1b355b29c894197f5924d210adcbb4abf6ba9da94972` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/B03_E8.log` | A | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/B03_E8.sortie` | A | no | `06e6de43a5e92107d352ccbae51a9ec280fc81641e6dfbcbcb6ff6cbb5d8b3c4` | `06e6de43a5e92107d352ccbae51a9ec280fc81641e6dfbcbcb6ff6cbb5d8b3c4` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/B03_E8.time` | A | yes | `85bd99ae531f9b320bb4aeb9897bbb87ba935c917ab1f08858fb749996297399` | `bbf52b1265ffc888361523aa1f6f33dc165964ee2110f66b4f5e21e965f0e279` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/B03_leech.log` | A | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/B03_leech.sortie` | A | no | `2ff00f89fe395c03bf9f2a72564f7ee351548b2db3218b78450a267e121f478a` | `2ff00f89fe395c03bf9f2a72564f7ee351548b2db3218b78450a267e121f478a` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/B03_leech.time` | A | yes | `b1ca93f4f3ab140ba0c63da6f4e9ab615cd759edc46a5ac6afbbb96a80c9c30b` | `c9439c218d2733497752db0266d5f706fb27ee15362cfc0ec4251f82fcb9b392` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/B03_leech2_e8.log` | A | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/B03_leech2_e8.sortie` | A | no | `db77c9a12aa29d35951454899932505468724c880f159236af6a6e6032ea5c70` | `db77c9a12aa29d35951454899932505468724c880f159236af6a6e6032ea5c70` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/B03_leech2_e8.time` | A | yes | `5f2a832e8722a7e78544f98334c32f6d6385c62aa2606436c925de2e07878eb4` | `6ab549918f3da95e56f4d1b8a61ca2d091cb52f95a3aeb03fa0f18b50d78a8fc` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/R01_raccords.log` | A | no | `fe788f4736f96dd9ecaf626d5a64fc087e28efd19ec51b9a7456aa67cb6d1047` | `fe788f4736f96dd9ecaf626d5a64fc087e28efd19ec51b9a7456aa67cb6d1047` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/R01_raccords.time` | A | yes | `4ee9c094a17d7635c517964ff4c330f20443a6f8dccceddb6b84e8f402fdea7f` | `366624891c69b61264864bd7366624854b2337e6633b22f3a891ccb22e77f42f` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/R01_raccords_lf.log` | A | no | `fe788f4736f96dd9ecaf626d5a64fc087e28efd19ec51b9a7456aa67cb6d1047` | `fe788f4736f96dd9ecaf626d5a64fc087e28efd19ec51b9a7456aa67cb6d1047` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/R01_raccords_lf.time` | A | yes | `b43de2ae35f673b80e3489502fd83c445c592fc73c594a08e836506ff5c8c45a` | `68fcb3c6862c31e1d149713d0806376cc7e4de80e041b25fd8ea0402a90985b1` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/R02_parite.log` | A | no | `b5f90cda260feefcc6c1dba32d5f40d3bde22b7d5b4ec78f5f0ad704233af1b1` | `b5f90cda260feefcc6c1dba32d5f40d3bde22b7d5b4ec78f5f0ad704233af1b1` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/R02_parite.time` | A | yes | `990d38f14d030d208ecc76c806abc00a00100b4b0b1581abee044c4a2e7754cf` | `c63b1a68c4eba75e09ca3fac014d954d71e1d450f50bbbb54f1d550d5296296d` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/R02_parite_lf.log` | A | no | `b5f90cda260feefcc6c1dba32d5f40d3bde22b7d5b4ec78f5f0ad704233af1b1` | `b5f90cda260feefcc6c1dba32d5f40d3bde22b7d5b4ec78f5f0ad704233af1b1` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/R02_parite_lf.time` | A | yes | `bab06eb7b6aabeff2f94fa3d0b6a8f0a1bde4d0e8ee99f6c01fb3c22178d6cf3` | `a2a72558cad85729d05909316c92a93f01977a6a36e982f64e2b91fa8f8762c1` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/R03_theta56.log` | A | no | `3f0796143f6bdadeac8e9fcb9621e2e64af174603c2831e99057e6feebcccdf8` | `3f0796143f6bdadeac8e9fcb9621e2e64af174603c2831e99057e6feebcccdf8` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/R03_theta56.time` | A | yes | `770d152eb3f1ce9a08181298fbc7f1e962e61c2c2259a4c97bc9998b3a7cc743` | `448cb7e33e2501647c95eb5c5476a0510946e7a7ed31a29a3f64dc9bc43b229b` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/V01_phi_X1.log` | A | no | `c0642982696df89e641cb0ee8ad2cc75d341fcb0fb3c5f9f01ca782715389b7b` | `c0642982696df89e641cb0ee8ad2cc75d341fcb0fb3c5f9f01ca782715389b7b` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/V01_phi_X1.time` | A | yes | `3651e0cc5576eadbf50865558a92e0213f1c0299131cb973c2ed8f66c3292f55` | `f18ef0df91dc3eeaa2313794718ae3f83d0fd1d98131b82b41253e8db0d93137` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/V02_partiel_420s.log` | A | no | `93f1026416c13efb9758aa378390ee357b4bb81e8f34bda5de4a5bf3b85fdfde` | `93f1026416c13efb9758aa378390ee357b4bb81e8f34bda5de4a5bf3b85fdfde` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/V02_partiel_420s.time` | A | yes | `765c8789b64292f78228b6b855945ff2ce2d07b053ac9c9cb86d719f2e6fddbc` | `ccade23e2596d14319b5d38cb777588290945d32a1454bb23cbec474110fd665` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/binaires.sha256` | A | yes | `f457abaf65149f672e22a8f8745685eac678dcbc875914a5564f753ac2af1a1a` | `d0cd6809ff8c03739529fdd65e23271aa88b76fa29a84c5f73c0a2f1d197c265` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/codes_natifs.txt` | A | no | `195f7e0f24908ab619093e183ab442650c2caf0a665b12eb7bb269d6c8e9d08f` | `195f7e0f24908ab619093e183ab442650c2caf0a665b12eb7bb269d6c8e9d08f` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/codes_natifs_lf.txt` | A | no | `e3ab52a85351783eecf91184fb2b8e76e18db57cb58d30accaa9984eefa8219e` | `e3ab52a85351783eecf91184fb2b8e76e18db57cb58d30accaa9984eefa8219e` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/horodatage.txt` | A | no | `938d25fe7f323884836c9ca73193512d72ae0baf890388867b1e46d3c7d95a69` | `938d25fe7f323884836c9ca73193512d72ae0baf890388867b1e46d3c7d95a69` |
| `logs/machine_A/reference_for_replication/MESURES_20261026/mesurer_etapes_courtes.sh` | A | yes | `3f60bbebfe17ec5ab07555ff15f258c4fdfe264afe849c8765bd21e1491129dc` | `088dee7afc8e5ce17b39e7a461c530615cce84ac7de8448f96cfdfac2c8854a1` |
| `logs/machine_A/reference_for_replication/raccord_entrees_f1.log` | A | no | `1d2cb477e67d689fb5f8aa4a865c009255c5d48e1a01c6d334e7335bf994fff5` | `1d2cb477e67d689fb5f8aa4a865c009255c5d48e1a01c6d334e7335bf994fff5` |
| `logs/machine_A/reference_for_replication/theta_56.txt` | A | no | `8ff25eb0429e02284a2b7104a960e25b39aed0d22f813dc3236197f0dfabd0a9` | `8ff25eb0429e02284a2b7104a960e25b39aed0d22f813dc3236197f0dfabd0a9` |
| `logs/machine_A/reference_for_replication/v3_X1_v3.log` | A | no | `09e627513caf7c3cdde6438d359caeb09d183f7ec71a3978d8e76f2a12004c37` | `09e627513caf7c3cdde6438d359caeb09d183f7ec71a3978d8e76f2a12004c37` |
| `logs/machine_A/reference_for_replication/v3_X4_v3.log` | A | no | `16e74d4b02e89f6352da65839b1180bf33dbcba5de8571473a86881aa454f825` | `16e74d4b02e89f6352da65839b1180bf33dbcba5de8571473a86881aa454f825` |
| `logs/machine_A/reference_for_replication/v3_codes_natifs.txt` | A | no | `950112447828fa0c9f94daed2628c236d29a1eb55ee84e899f2847ae80b8b929` | `950112447828fa0c9f94daed2628c236d29a1eb55ee84e899f2847ae80b8b929` |
| `logs/machine_A/reference_for_replication/v3_horodatage.txt` | A | no | `163c8f5421eb078196d068fe869ed59490416cbf51a76fdb8ba4611d68f4b701` | `163c8f5421eb078196d068fe869ed59490416cbf51a76fdb8ba4611d68f4b701` |
| `logs/machine_A/reference_for_replication/v3_phi_v3_X1.log` | A | no | `c0642982696df89e641cb0ee8ad2cc75d341fcb0fb3c5f9f01ca782715389b7b` | `c0642982696df89e641cb0ee8ad2cc75d341fcb0fb3c5f9f01ca782715389b7b` |
| `logs/machine_A/theta_20261026/theta_112.txt` | A | no | `8035f27d467802e312b433936185294bf58b49349b7c968475e404bd0d19af7b` | `8035f27d467802e312b433936185294bf58b49349b7c968475e404bd0d19af7b` |
| `logs/machine_A/theta_20261026/theta_56.txt` | A | no | `8ff25eb0429e02284a2b7104a960e25b39aed0d22f813dc3236197f0dfabd0a9` | `8ff25eb0429e02284a2b7104a960e25b39aed0d22f813dc3236197f0dfabd0a9` |
| `logs/machine_A/v3_runs_20261026/X1_v3.log` | A | no | `09e627513caf7c3cdde6438d359caeb09d183f7ec71a3978d8e76f2a12004c37` | `09e627513caf7c3cdde6438d359caeb09d183f7ec71a3978d8e76f2a12004c37` |
| `logs/machine_A/v3_runs_20261026/X1_v3/touches_88_X1.npy` | A | no | `e734dac55ea9fbbe782af2d8c02c3c5992131906228afb2aaaf137d6f3ed74db` | `e734dac55ea9fbbe782af2d8c02c3c5992131906228afb2aaaf137d6f3ed74db` |
| `logs/machine_A/v3_runs_20261026/X1_v3/verif_independante_X1.txt` | A | no | `1eb7b84810fbd337f13a56b7f600ed690e45a482f01be8897657cabf3091b6f8` | `1eb7b84810fbd337f13a56b7f600ed690e45a482f01be8897657cabf3091b6f8` |
| `logs/machine_A/v3_runs_20261026/X4_v3.log` | A | no | `16e74d4b02e89f6352da65839b1180bf33dbcba5de8571473a86881aa454f825` | `16e74d4b02e89f6352da65839b1180bf33dbcba5de8571473a86881aa454f825` |
| `logs/machine_A/v3_runs_20261026/X4_v3/touches_88_X4.npy` | A | no | `ef20c92d86e8e0b99b44fe07f344092b20f4d33b71362c7f66e6176c618835ad` | `ef20c92d86e8e0b99b44fe07f344092b20f4d33b71362c7f66e6176c618835ad` |
| `logs/machine_A/v3_runs_20261026/X4_v3/verif_independante_X4.txt` | A | no | `68c199822e50e5710505cc8196f243b3942ab4da6b9856281def3c047d2f8780` | `68c199822e50e5710505cc8196f243b3942ab4da6b9856281def3c047d2f8780` |
| `logs/machine_A/v3_runs_20261026/codes_natifs.txt` | A | no | `950112447828fa0c9f94daed2628c236d29a1eb55ee84e899f2847ae80b8b929` | `950112447828fa0c9f94daed2628c236d29a1eb55ee84e899f2847ae80b8b929` |
| `logs/machine_A/v3_runs_20261026/horodatage.txt` | A | no | `163c8f5421eb078196d068fe869ed59490416cbf51a76fdb8ba4611d68f4b701` | `163c8f5421eb078196d068fe869ed59490416cbf51a76fdb8ba4611d68f4b701` |
| `logs/machine_A/v3_runs_20261026/lancer_v3.sh` | A | yes | `a720e26d9140f5edb34178bb311c6bd4353f6d0302dfb7d6a49b561fffbcf6fc` | `e7cb6100992b6d0c85d5075f0e3c948a5ee82a857304f9981a3a034e596e03b5` |
| `logs/machine_A/v3_runs_20261026/lanceur.log` | A | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_A/v3_runs_20261026/phi_v3_X1.log` | A | no | `c0642982696df89e641cb0ee8ad2cc75d341fcb0fb3c5f9f01ca782715389b7b` | `c0642982696df89e641cb0ee8ad2cc75d341fcb0fb3c5f9f01ca782715389b7b` |
| `logs/machine_A/v3_runs_20261026/scripts_v3.sha256` | A | yes | `94ad96b8656e395990df118b4b8972aa4d4484a0f51d7cf87931ebf84f389794` | `cde468c369f1ce48944e2482faf777751261602b707b5b27fefd8592b2856b17` |
| `logs/machine_A/v3_runs_20261026/test0a.log` | A | no | `bca8231438c4befd08dcc88219a8fa606e9602a7d41ee83d2d8cae2de6feb483` | `bca8231438c4befd08dcc88219a8fa606e9602a7d41ee83d2d8cae2de6feb483` |
| `logs/machine_A/v3_runs_20261026/test0b.log` | A | no | `2d3803e0ad087746e3a8a49cbdf96a101f4df7b71b771768d3c1666f4ebd4271` | `2d3803e0ad087746e3a8a49cbdf96a101f4df7b71b771768d3c1666f4ebd4271` |
| `logs/machine_A/v3_runs_20261026/test0c.log` | A | no | `f90359c68f5757b3464fe22184f155fd77a4005d56b5fd1627954a435c35ecab` | `f90359c68f5757b3464fe22184f155fd77a4005d56b5fd1627954a435c35ecab` |
| `logs/machine_A/verdict_v3_20261026/manifeste_verdict_x1_v3.tsv` | A | yes | `998bb7b7df8267919a7500c53743da2b08cea6803949b9089583172d874d4529` | `3040d22f045b8b07d8ad7c23f5526836bddd4b54d836ce5e6bbb1f635264fd76` |
| `logs/machine_A/verdict_v3_20261026/verdict_x1_v3.txt` | A | no | `6918d8b38fa5a6f815baf8fee06a0ea8d1967592471732308a1518d9cf4ed79e` | `6918d8b38fa5a6f815baf8fee06a0ea8d1967592471732308a1518d9cf4ed79e` |
| `logs/machine_B/run_20261026/B01_compil_enum.duree` | B: `B01_compil_enum.duree` | no | `bb5a0801190ee96272980bea8c580d20fd1ff6f89f65b9b5df17b9bfead9dd51` | `bb5a0801190ee96272980bea8c580d20fd1ff6f89f65b9b5df17b9bfead9dd51` |
| `logs/machine_B/run_20261026/B01_compil_enum.log` | B: `B01_compil_enum.log` | no | `1c8e3e8104f009e32e45f6983f0fd49a801e1cc76532401389160d60e2529f04` | `1c8e3e8104f009e32e45f6983f0fd49a801e1cc76532401389160d60e2529f04` |
| `logs/machine_B/run_20261026/B01_compil_enum.native.exit` | B: `B01_compil_enum.native.exit` | no | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `logs/machine_B/run_20261026/B01_compil_enum.ok` | B: `B01_compil_enum.ok` | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_B/run_20261026/B02_compil_formes.duree` | B: `B02_compil_formes.duree` | no | `bb5a0801190ee96272980bea8c580d20fd1ff6f89f65b9b5df17b9bfead9dd51` | `bb5a0801190ee96272980bea8c580d20fd1ff6f89f65b9b5df17b9bfead9dd51` |
| `logs/machine_B/run_20261026/B02_compil_formes.log` | B: `B02_compil_formes.log` | no | `285901c41fd78cabdea5d38010448d40ea5083bc6e97b0ae2ffdafd23f21cdd3` | `285901c41fd78cabdea5d38010448d40ea5083bc6e97b0ae2ffdafd23f21cdd3` |
| `logs/machine_B/run_20261026/B02_compil_formes.native.exit` | B: `B02_compil_formes.native.exit` | no | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `logs/machine_B/run_20261026/B02_compil_formes.ok` | B: `B02_compil_formes.ok` | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_B/run_20261026/B03_controles_enum.duree` | B: `B03_controles_enum.duree` | no | `e32b52f8e003f454f56aea48563111414b75bafce649e7b430340210207448c9` | `e32b52f8e003f454f56aea48563111414b75bafce649e7b430340210207448c9` |
| `logs/machine_B/run_20261026/B03_controles_enum.log` | B: `B03_controles_enum.log` | yes | `897e0ece460036b08618a146b45baf9325b8e43fc7ed079d2072616c10d3f43c` | `ae958ab90c5f2f3d653e3d9f396fc5776e70521ece533292dc313eacf715df79` |
| `logs/machine_B/run_20261026/B03_controles_enum.native.exit` | B: `B03_controles_enum.native.exit` | no | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `logs/machine_B/run_20261026/B03_controles_enum.ok` | B: `B03_controles_enum.ok` | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_B/run_20261026/BILAN_X1_REP_V2.txt` | B: `BILAN_X1_REP_V2.txt` | yes | `d7ff1758b4e01db7579468b74c0dcae4c6e7523347d2bc2ea0a590b219b23983` | `d6de8200e734480aa6df64e955e42b03f4a5ad339a111da5719433ecd27ad7c1` |
| `logs/machine_B/run_20261026/E00_numpy.duree` | B: `E00_numpy.duree` | no | `270eec0399ad300ebbe246ef606066487d04827b7a4c609e29722bcac1c78faa` | `270eec0399ad300ebbe246ef606066487d04827b7a4c609e29722bcac1c78faa` |
| `logs/machine_B/run_20261026/E00_numpy.log` | B: `E00_numpy.log` | yes | `0093a98eddef97b7ec1f2cb10456a563168c3e3f6ff0bb544c999878b65e2064` | `03b7d27cd06c52b1020665bed586ce8816b9467583d6d027363122f4155ad9ba` |
| `logs/machine_B/run_20261026/E00_numpy.native.exit` | B: `E00_numpy.native.exit` | no | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `logs/machine_B/run_20261026/E00_numpy.ok` | B: `E00_numpy.ok` | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_B/run_20261026/ECHEANCES_MONO.txt` | B: `ECHEANCES_MONO.txt` | no | `9b2446e6c5818cacf63f9a2f1278eab47587d58f1fd37a77509f4de55dd4e2d5` | `9b2446e6c5818cacf63f9a2f1278eab47587d58f1fd37a77509f4de55dd4e2d5` |
| `logs/machine_B/run_20261026/F01_F1_L.duree` | B: `F01_F1_L.duree` | no | `ec4a9a9746046a136a5ae0abfe928417237d8a1a4b9dbe75543dd28c740e85f6` | `ec4a9a9746046a136a5ae0abfe928417237d8a1a4b9dbe75543dd28c740e85f6` |
| `logs/machine_B/run_20261026/F01_F1_L.log` | B: `F01_F1_L.log` | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_B/run_20261026/F01_F1_L.native.exit` | B: `F01_F1_L.native.exit` | no | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `logs/machine_B/run_20261026/F01_F1_L.ok` | B: `F01_F1_L.ok` | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_B/run_20261026/F02_F1_L56.duree` | B: `F02_F1_L56.duree` | no | `80ec0d3a29de074e10c181c46f77aa1eeb8f554f576f8a677b000e152e93cbe7` | `80ec0d3a29de074e10c181c46f77aa1eeb8f554f576f8a677b000e152e93cbe7` |
| `logs/machine_B/run_20261026/F02_F1_L56.log` | B: `F02_F1_L56.log` | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_B/run_20261026/F02_F1_L56.native.exit` | B: `F02_F1_L56.native.exit` | no | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `logs/machine_B/run_20261026/F02_F1_L56.ok` | B: `F02_F1_L56.ok` | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_B/run_20261026/FIN_MONO.txt` | B: `FIN_MONO.txt` | no | `b4c21a1db6c2860187e6b698c7343b1d9ea65d21ba1c78b9eadd19dc833601ee` | `b4c21a1db6c2860187e6b698c7343b1d9ea65d21ba1c78b9eadd19dc833601ee` |
| `logs/machine_B/run_20261026/GLOBAL.native.exit` | B: `GLOBAL.native.exit` | no | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `logs/machine_B/run_20261026/MANIFESTE_COPIE_FIGEE.sha256` | B: `MANIFESTE_COPIE_FIGEE.sha256` | yes | `81c3612143103726eaba59a2f5561876c70580ab6a6420c2cebb1012e0f155e3` | `6a0d4da35211cd7b7fd8e6d0790f4a6760e2fc649a5720db3a2f4bbf3edbab40` |
| `logs/machine_B/run_20261026/MANIFESTE_VERDICT_X1_REP_V2.tsv` | B: `MANIFESTE_VERDICT_X1_REP_V2.tsv` | yes | `cfd51bdb1c9768aa5e49148a99232dd37c034ea63761eccd0c761cbaa3f34974` | `680e7d99b9e9ba72906afa7e8f0f9c8e8466bcf43f131edc36c0c11bcf776e37` |
| `logs/machine_B/run_20261026/R01_raccords.duree` | B: `R01_raccords.duree` | no | `f1e96cac96c93321ce4f5bf5a73fc8cd2ca3bcf4e80295bf786cae3e8c85db1f` | `f1e96cac96c93321ce4f5bf5a73fc8cd2ca3bcf4e80295bf786cae3e8c85db1f` |
| `logs/machine_B/run_20261026/R01_raccords.log` | B: `R01_raccords.log` | no | `fe788f4736f96dd9ecaf626d5a64fc087e28efd19ec51b9a7456aa67cb6d1047` | `fe788f4736f96dd9ecaf626d5a64fc087e28efd19ec51b9a7456aa67cb6d1047` |
| `logs/machine_B/run_20261026/R01_raccords.native.exit` | B: `R01_raccords.native.exit` | no | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `logs/machine_B/run_20261026/R01_raccords.ok` | B: `R01_raccords.ok` | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_B/run_20261026/R02_parite.duree` | B: `R02_parite.duree` | no | `aabe900a5f3f38d94dfee0dd9afab8372bec2416a19bd0f18b51e71802ac8868` | `aabe900a5f3f38d94dfee0dd9afab8372bec2416a19bd0f18b51e71802ac8868` |
| `logs/machine_B/run_20261026/R02_parite.log` | B: `R02_parite.log` | no | `b5f90cda260feefcc6c1dba32d5f40d3bde22b7d5b4ec78f5f0ad704233af1b1` | `b5f90cda260feefcc6c1dba32d5f40d3bde22b7d5b4ec78f5f0ad704233af1b1` |
| `logs/machine_B/run_20261026/R02_parite.native.exit` | B: `R02_parite.native.exit` | no | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `logs/machine_B/run_20261026/R02_parite.ok` | B: `R02_parite.ok` | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_B/run_20261026/R03_theta56.duree` | B: `R03_theta56.duree` | no | `bb5a0801190ee96272980bea8c580d20fd1ff6f89f65b9b5df17b9bfead9dd51` | `bb5a0801190ee96272980bea8c580d20fd1ff6f89f65b9b5df17b9bfead9dd51` |
| `logs/machine_B/run_20261026/R03_theta56.log` | B: `R03_theta56.log` | no | `3f0796143f6bdadeac8e9fcb9621e2e64af174603c2831e99057e6feebcccdf8` | `3f0796143f6bdadeac8e9fcb9621e2e64af174603c2831e99057e6feebcccdf8` |
| `logs/machine_B/run_20261026/R03_theta56.native.exit` | B: `R03_theta56.native.exit` | no | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `logs/machine_B/run_20261026/R03_theta56.ok` | B: `R03_theta56.ok` | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_B/run_20261026/V01_phi_X1.duree` | B: `V01_phi_X1.duree` | no | `1549bf3e807119be6cb3e9e1a75946ac56436dff497c549a2c75d12657d388bc` | `1549bf3e807119be6cb3e9e1a75946ac56436dff497c549a2c75d12657d388bc` |
| `logs/machine_B/run_20261026/V01_phi_X1.log` | B: `V01_phi_X1.log` | no | `c0642982696df89e641cb0ee8ad2cc75d341fcb0fb3c5f9f01ca782715389b7b` | `c0642982696df89e641cb0ee8ad2cc75d341fcb0fb3c5f9f01ca782715389b7b` |
| `logs/machine_B/run_20261026/V01_phi_X1.native.exit` | B: `V01_phi_X1.native.exit` | no | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `logs/machine_B/run_20261026/V01_phi_X1.ok` | B: `V01_phi_X1.ok` | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_B/run_20261026/V02_indep_X1.duree` | B: `V02_indep_X1.duree` | no | `be2498f87716dbadad825ca9326220129cb63cc7dc6011dd531335f7d33bda3d` | `be2498f87716dbadad825ca9326220129cb63cc7dc6011dd531335f7d33bda3d` |
| `logs/machine_B/run_20261026/V02_indep_X1.log` | B: `V02_indep_X1.log` | no | `815a5b0bfd76596338cbd7635bcaa55d897f9e69a867bec55e19a7d071cda067` | `815a5b0bfd76596338cbd7635bcaa55d897f9e69a867bec55e19a7d071cda067` |
| `logs/machine_B/run_20261026/V02_indep_X1.native.exit` | B: `V02_indep_X1.native.exit` | no | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `logs/machine_B/run_20261026/V02_indep_X1.ok` | B: `V02_indep_X1.ok` | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_B/run_20261026/V03_indep_X4.duree` | B: `V03_indep_X4.duree` | no | `093c91e571024bc8c8ddc446f9fb7bb6477af3e48580f6b912409c35b288b106` | `093c91e571024bc8c8ddc446f9fb7bb6477af3e48580f6b912409c35b288b106` |
| `logs/machine_B/run_20261026/V03_indep_X4.log` | B: `V03_indep_X4.log` | no | `3ed3debcabd4ee2b38e984737a651939401c75b15e6b1d2ecffe054ab240488d` | `3ed3debcabd4ee2b38e984737a651939401c75b15e6b1d2ecffe054ab240488d` |
| `logs/machine_B/run_20261026/V03_indep_X4.native.exit` | B: `V03_indep_X4.native.exit` | no | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `logs/machine_B/run_20261026/V03_indep_X4.ok` | B: `V03_indep_X4.ok` | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_B/run_20261026/VERDICT.log` | B: `VERDICT.log` | yes | `d0f883fc27f68cdf0e5fc375d2a3123855abe13419f010380ae4ed4534cf1c41` | `e253fb8db45250d3cc955715036ffff304e7377570c46d1ec58c4277027a8d57` |
| `logs/machine_B/run_20261026/VERDICT.native.exit` | B: `VERDICT.native.exit` | no | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `logs/machine_B/run_20261026/VERDICT_X1_REP_V2.txt` | B: `VERDICT_X1_REP_V2.txt` | yes | `d0f883fc27f68cdf0e5fc375d2a3123855abe13419f010380ae4ed4534cf1c41` | `e253fb8db45250d3cc955715036ffff304e7377570c46d1ec58c4277027a8d57` |
| `logs/machine_B/run_20261026/sorties/B03_E8.err` | B: `sorties/B03_E8.err` | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_B/run_20261026/sorties/B03_E8.sortie` | B: `sorties/B03_E8.sortie` | no | `06e6de43a5e92107d352ccbae51a9ec280fc81641e6dfbcbcb6ff6cbb5d8b3c4` | `06e6de43a5e92107d352ccbae51a9ec280fc81641e6dfbcbcb6ff6cbb5d8b3c4` |
| `logs/machine_B/run_20261026/sorties/B03_leech.err` | B: `sorties/B03_leech.err` | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_B/run_20261026/sorties/B03_leech.sortie` | B: `sorties/B03_leech.sortie` | no | `2ff00f89fe395c03bf9f2a72564f7ee351548b2db3218b78450a267e121f478a` | `2ff00f89fe395c03bf9f2a72564f7ee351548b2db3218b78450a267e121f478a` |
| `logs/machine_B/run_20261026/sorties/B03_leech2_e8.err` | B: `sorties/B03_leech2_e8.err` | no | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `logs/machine_B/run_20261026/sorties/B03_leech2_e8.sortie` | B: `sorties/B03_leech2_e8.sortie` | no | `db77c9a12aa29d35951454899932505468724c880f159236af6a6e6032ea5c70` | `db77c9a12aa29d35951454899932505468724c880f159236af6a6e6032ea5c70` |
| `logs/machine_B/run_20261026/sorties/F1_L.err` | B: `sorties/F1_L.err` | no | `2ca807ce607ac949fc22c548bce4b50c8aeaa810ff2961848746d92e55a91c7e` | `2ca807ce607ac949fc22c548bce4b50c8aeaa810ff2961848746d92e55a91c7e` |
| `logs/machine_B/run_20261026/sorties/F1_L.sortie` | B: `sorties/F1_L.sortie` | no | `219ba069bdf53e353b7a5ea96297a558d79f36d02499c69617ca11f66a1f6b24` | `219ba069bdf53e353b7a5ea96297a558d79f36d02499c69617ca11f66a1f6b24` |
| `logs/machine_B/run_20261026/sorties/F1_L56.err` | B: `sorties/F1_L56.err` | no | `4ea7eb18ba1eded220b9d6aee8eeadf7e4fe315c05bfb7a2776c09d97ae90757` | `4ea7eb18ba1eded220b9d6aee8eeadf7e4fe315c05bfb7a2776c09d97ae90757` |
| `logs/machine_B/run_20261026/sorties/F1_L56.sortie` | B: `sorties/F1_L56.sortie` | no | `74ee726854f4525991ef7a7faa65eb5bc863d84f9feead8d2b62cd54b69f7f27` | `74ee726854f4525991ef7a7faa65eb5bc863d84f9feead8d2b62cd54b69f7f27` |
| `logs/machine_B/run_20261026/sorties/X1_int16/touches_88_X1.npy` | B: `sorties/X1_int16/touches_88_X1.npy` | no | `e734dac55ea9fbbe782af2d8c02c3c5992131906228afb2aaaf137d6f3ed74db` | `e734dac55ea9fbbe782af2d8c02c3c5992131906228afb2aaaf137d6f3ed74db` |
| `logs/machine_B/run_20261026/sorties/X1_int16/verif_independante_X1.txt` | B: `sorties/X1_int16/verif_independante_X1.txt` | no | `1eb7b84810fbd337f13a56b7f600ed690e45a482f01be8897657cabf3091b6f8` | `1eb7b84810fbd337f13a56b7f600ed690e45a482f01be8897657cabf3091b6f8` |
| `logs/machine_B/run_20261026/sorties/X4_int16/touches_88_X4.npy` | B: `sorties/X4_int16/touches_88_X4.npy` | no | `ef20c92d86e8e0b99b44fe07f344092b20f4d33b71362c7f66e6176c618835ad` | `ef20c92d86e8e0b99b44fe07f344092b20f4d33b71362c7f66e6176c618835ad` |
| `logs/machine_B/run_20261026/sorties/X4_int16/verif_independante_X4.txt` | B: `sorties/X4_int16/verif_independante_X4.txt` | no | `68c199822e50e5710505cc8196f243b3942ab4da6b9856281def3c047d2f8780` | `68c199822e50e5710505cc8196f243b3942ab4da6b9856281def3c047d2f8780` |
| `logs/machine_B/service_record/UNIT_TERMINAL_BEFORE_STOP.txt` | B: `/UNIT_TERMINAL_BEFORE_STOP.txt` | yes | `7d94ff16fd53db758b9c0e8ae8c3609a9e113dbf3d829aa6b67212c50c21aaaa` | `b57af39a08f2674d2702b55d1555472802fb1207ab057aec08ecd486b8614d06` |

New files written for this repository (READMEs, licences, `CITATION.cff`, `THIRD_PARTY_NOTICES.md`, `data/roiban/*`, `code/replication/assemble_package.sh`, `code/reduced_basis/compute_reduced_basis_figures.py`, `data/reduced_basis/L112.02_reduced.std`, this file) are not copies and are not listed; `data/reduced_basis/L112.02_reduced.std` is derived from a draft catalogue entry as explained in `data/reduced_basis/README.md`.
