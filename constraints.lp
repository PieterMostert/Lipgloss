\* Glaze recipe *\
Maximize
KNaO_%_mol: - other_2
Subject To
Al2O3: 0.4021 ingredient_1 + 0.0602 ingredient_11 + 0.099 ingredient_12
 + 0.1198 ingredient_14 + 0.017 ingredient_18 + 0.1633 ingredient_19
 + 0.2502 ingredient_2 + 0.1832 ingredient_3 + 0.1944 ingredient_4
 + 0.233 ingredient_5 - mass_Al2O3 = 0
Al2O3_mol_%_lower: mole_Al2O3 >= 0
Al2O3_mol_%_upper: mole_Al2O3 - ox_mole_total <= 0
Al2O3_umf_lower: mole_Al2O3 >= 0
Al2O3_umf_upper: - 10 fluxes_total + mole_Al2O3 <= 0
Al2O3_wt_%_lower: mass_Al2O3 >= 0
Al2O3_wt_%_upper: mass_Al2O3 - ox_mass_total <= 0
B2O3: 0.0289 ingredient_11 + 0.1377 ingredient_12 + 0.2309 ingredient_13
 + 0.2262 ingredient_14 + 0.2449 ingredient_18 - mass_B2O3 = 0
B2O3_mol_%_lower: mole_B2O3 >= 0
B2O3_mol_%_upper: mole_B2O3 - ox_mole_total <= 0
B2O3_umf_lower: mole_B2O3 >= 0
B2O3_umf_upper: - fluxes_total + mole_B2O3 <= 0
B2O3_wt_%_lower: mass_B2O3 >= 0
B2O3_wt_%_upper: mass_B2O3 - ox_mass_total <= 0
BaO: 0.22 ingredient_22 - mass_BaO = 0
CaO: 0.0564 ingredient_11 + 0.1407 ingredient_12 + 0.2013 ingredient_13
 + 0.1136 ingredient_14 + 0.5422 ingredient_15 + 0.2299 ingredient_18
 + 0.0181 ingredient_19 + 0.003 ingredient_2 + 0.007 ingredient_5
 + 0.4828 ingredient_6 + 0.561 ingredient_7 - mass_CaO = 0
CaO_mol_%_lower: mole_CaO >= 0
CaO_mol_%_upper: mole_CaO - ox_mole_total <= 0
CaO_umf_lower: mole_CaO >= 0
CaO_umf_upper: - fluxes_total + mole_CaO <= 0
CaO_wt_%_lower: mass_CaO >= 0
CaO_wt_%_upper: mass_CaO - ox_mass_total <= 0
Fe2O3: 0.95 ingredient_17 + 0.0019 ingredient_19 + 0.0102 ingredient_2
 + 0.001 ingredient_5 - mass_Fe2O3 = 0
K2O: 0.0345 ingredient_11 + 0.0068 ingredient_12 + 0.043 ingredient_19
 + 0.009 ingredient_2 + 0.1692 ingredient_3 + 0.046 ingredient_5 - mass_K2O
 = 0
K2O_mol_%_lower: mole_K2O >= 0
K2O_mol_%_upper: mole_K2O - ox_mole_total <= 0
K2O_umf_lower: mole_K2O >= 0
K2O_umf_upper: - fluxes_total + mole_K2O <= 0
K2O_wt_%_lower: mass_K2O >= 0
K2O_wt_%_upper: mass_K2O - ox_mass_total <= 0
Li2O: 0.4074 ingredient_16 - mass_Li2O = 0
MgO: 0.039 ingredient_18 + 0.0014 ingredient_19 + 0.003 ingredient_2
 + 0.001 ingredient_5 + 0.3187 ingredient_8 + 0.478 ingredient_9 - mass_MgO
 = 0
MgO_mol_%_lower: mole_MgO >= 0
MgO_mol_%_upper: mole_MgO - ox_mole_total <= 0
MgO_umf_lower: mole_MgO >= 0
MgO_umf_upper: - fluxes_total + mole_MgO <= 0
MgO_wt_%_lower: mass_MgO >= 0
MgO_wt_%_upper: mass_MgO - ox_mass_total <= 0
MnO2: mass_MnO2 = 0
Na2O: 0.1512 ingredient_11 + 0.0628 ingredient_12 + 0.1028 ingredient_13
 + 0.0569 ingredient_14 + 0.0377 ingredient_18 + 0.033 ingredient_19
 + 0.002 ingredient_2 + 0.1182 ingredient_4 + 0.098 ingredient_5 - mass_Na2O
 = 0
Na2O_mol_%_lower: mole_Na2O >= 0
Na2O_mol_%_upper: mole_Na2O - ox_mole_total <= 0
Na2O_umf_lower: mole_Na2O >= 0
Na2O_umf_upper: - fluxes_total + mole_Na2O <= 0
Na2O_wt_%_lower: mass_Na2O >= 0
Na2O_wt_%_upper: mass_Na2O - ox_mass_total <= 0
P2O5: 0.4578 ingredient_15 - mass_P2O5 = 0
SiO2: ingredient_0 + 0.4729 ingredient_1 + 0.6688 ingredient_11
 + 0.553 ingredient_12 + 0.4651 ingredient_13 + 0.4835 ingredient_14
 + 0.118 ingredient_18 + 0.7378 ingredient_19 + 0.5906 ingredient_2
 + 0.6472 ingredient_3 + 0.6874 ingredient_4 + 0.607 ingredient_5
 + 0.5172 ingredient_6 + 0.6338 ingredient_8 - mass_SiO2 = 0
SiO2_mol_%_lower: mole_SiO2 >= 0
SiO2_mol_%_upper: mole_SiO2 - ox_mole_total <= 0
SiO2_umf_lower: mole_SiO2 >= 0
SiO2_umf_upper: - 100 fluxes_total + mole_SiO2 <= 0
SiO2_wt_%_lower: mass_SiO2 >= 0
SiO2_wt_%_upper: mass_SiO2 - ox_mass_total <= 0
SrO: 0.67 ingredient_22 - mass_SrO = 0
TiO2: 0.0015 ingredient_19 + 0.01 ingredient_2 - mass_TiO2 = 0
ZnO: ingredient_10 + 0.43 ingredient_26 - mass_ZnO = 0
_C1: - mass_SiO2 + 60.085 mole_SiO2 = 0
_C10: - mass_Na2O + 61.979 mole_Na2O = 0
_C11: - mass_K2O + 94.196 mole_K2O = 0
_C12: - mass_P2O5 + 141.945 mole_P2O5 = 0
_C13: - mass_Fe2O3 + 159.688 mole_Fe2O3 = 0
_C14: - mass_TiO2 + 79.866 mole_TiO2 = 0
_C15: - mass_MnO2 + 86.937 mole_MnO2 = 0
_C16: fluxes_total - mole_BaO - mole_CaO - mole_K2O - mole_Li2O - mole_MgO
 - mole_Na2O - mole_SrO - mole_ZnO = 0
_C17: - mass_Al2O3 - mass_B2O3 - mass_BaO - mass_CaO - mass_Fe2O3 - mass_K2O
 - mass_Li2O - mass_MgO - mass_MnO2 - mass_Na2O - mass_P2O5 - mass_SiO2
 - mass_SrO - mass_TiO2 - mass_ZnO + ox_mass_total = 0
_C18: - mole_Al2O3 - mole_B2O3 - mole_BaO - mole_CaO - mole_Fe2O3 - mole_K2O
 - mole_Li2O - mole_MgO - mole_MnO2 - mole_Na2O - mole_P2O5 - mole_SiO2
 - mole_SrO - mole_TiO2 - mole_ZnO + ox_mole_total = 0
_C2: - mass_Al2O3 + 101.961 mole_Al2O3 = 0
_C3: - mass_B2O3 + 69.62 mole_B2O3 = 0
_C4: - mass_MgO + 40.304 mole_MgO = 0
_C5: - mass_CaO + 56.077 mole_CaO = 0
_C6: - mass_SrO + 103.62 mole_SrO = 0
_C7: - mass_BaO + 153.326 mole_BaO = 0
_C8: - mass_ZnO + 81.39 mole_ZnO = 0
_C9: - mass_Li2O + 29.881 mole_Li2O = 0
ing_total: - ingredient_0 - ingredient_1 - ingredient_10 - ingredient_11
 - ingredient_12 - ingredient_13 - ingredient_14 - ingredient_15
 - ingredient_16 - ingredient_17 - ingredient_18 - ingredient_19
 - ingredient_2 - ingredient_20 - ingredient_21 - ingredient_22
 - ingredient_23 - ingredient_24 - ingredient_25 - ingredient_26
 - ingredient_3 - ingredient_4 - ingredient_5 - ingredient_6 - ingredient_7
 - ingredient_8 - ingredient_9 + ingredient_total = 0
ingredient_0_lower: ingredient_0 >= 0
ingredient_0_upper: ingredient_0 - ingredient_total <= 0
ingredient_10_lower: ingredient_10 >= 0
ingredient_10_upper: ingredient_10 <= 0
ingredient_11_lower: ingredient_11 >= 0
ingredient_11_upper: ingredient_11 - ingredient_total <= 0
ingredient_12_lower: ingredient_12 >= 0
ingredient_12_upper: ingredient_12 <= 0
ingredient_13_lower: ingredient_13 >= 0
ingredient_13_upper: ingredient_13 <= 0
ingredient_14_lower: ingredient_14 >= 0
ingredient_14_upper: ingredient_14 <= 0
ingredient_15_lower: ingredient_15 >= 0
ingredient_15_upper: ingredient_15 <= 0
ingredient_16_lower: ingredient_16 >= 0
ingredient_16_upper: ingredient_16 <= 0
ingredient_17_lower: ingredient_17 >= 0
ingredient_17_upper: ingredient_17 <= 0
ingredient_18_lower: ingredient_18 >= 0
ingredient_18_upper: ingredient_18 <= 0
ingredient_19_lower: ingredient_19 >= 0
ingredient_19_upper: ingredient_19 <= 0
ingredient_1_lower: ingredient_1 >= 0
ingredient_1_upper: ingredient_1 - ingredient_total <= 0
ingredient_20_lower: ingredient_20 >= 0
ingredient_20_upper: ingredient_20 <= 0
ingredient_21_lower: ingredient_21 >= 0
ingredient_21_upper: ingredient_21 <= 0
ingredient_22_lower: ingredient_22 >= 0
ingredient_22_upper: ingredient_22 <= 0
ingredient_23_lower: ingredient_23 >= 0
ingredient_23_upper: ingredient_23 <= 0
ingredient_24_lower: ingredient_24 >= 0
ingredient_24_upper: ingredient_24 <= 0
ingredient_25_lower: ingredient_25 >= 0
ingredient_25_upper: ingredient_25 <= 0
ingredient_26_lower: ingredient_26 >= 0
ingredient_26_upper: ingredient_26 <= 0
ingredient_2_lower: ingredient_2 >= 0
ingredient_2_upper: ingredient_2 <= 0
ingredient_3_lower: ingredient_3 >= 0
ingredient_3_upper: ingredient_3 <= 0
ingredient_4_lower: ingredient_4 >= 0
ingredient_4_upper: ingredient_4 <= 0
ingredient_5_lower: ingredient_5 >= 0
ingredient_5_upper: ingredient_5 <= 0
ingredient_6_lower: ingredient_6 >= 0
ingredient_6_upper: ingredient_6 - ingredient_total <= 0
ingredient_7_lower: ingredient_7 >= 0
ingredient_7_upper: ingredient_7 <= 0
ingredient_8_lower: ingredient_8 >= 0
ingredient_8_upper: ingredient_8 - ingredient_total <= 0
ingredient_9_lower: ingredient_9 >= 0
ingredient_9_upper: ingredient_9 <= 0
normalization: 0.01 ox_mole_total = 1
other_0: - mole_SiO2 + other_0 = 0
other_1: - mole_K2O - mole_Na2O + other_1 = 0
other_2: - mole_K2O - mole_Na2O + other_2 = 0
other_2_lower: other_2 >= 0
other_2_upper: other_2 - ox_mole_total <= 0
other_3: - mole_BaO - mole_CaO - mole_MgO - mole_SrO + other_3 = 0
other_3_lower: other_3 >= 0
other_3_upper: - fluxes_total + other_3 <= 0
other_4: - ingredient_1 - ingredient_2 + other_4 = 0
other_5: - 0.125 ingredient_1 - 0.5926 ingredient_16 - 0.05 ingredient_17
 - 0.309 ingredient_18 - 0.12 ingredient_2 - 0.007 ingredient_5
 - 0.439 ingredient_7 - 0.0475 ingredient_8 - 0.522 ingredient_9 + other_5 = 0
other_6: other_6 = 0
End
