\* Glaze recipe *\
Maximize
SiO2_Al2O3: - other_0
Subject To
Al2O3: 0.2335 ingredient_1 + 0.0602 ingredient_11 + 0.099 ingredient_12
 + 0.1198 ingredient_14 + 0.2762 ingredient_2 + 0.188 ingredient_3
 + 0.244 ingredient_5 - mass_Al2O3 = 0
Al2O3_mol_%_lower: mole_Al2O3 >= 0
Al2O3_mol_%_upper: mole_Al2O3 - ox_mole_total <= 0
Al2O3_umf_lower: mole_Al2O3 >= 0
Al2O3_umf_upper: - fluxes_total + mole_Al2O3 <= 0
Al2O3_wt_%_lower: mass_Al2O3 >= 0
Al2O3_wt_%_upper: mass_Al2O3 - ox_mass_total <= 0
B2O3: 0.0289 ingredient_11 + 0.1377 ingredient_12 + 0.2309 ingredient_13
 + 0.2262 ingredient_14 - mass_B2O3 = 0
B2O3_mol_%_lower: mole_B2O3 >= 0
B2O3_mol_%_upper: mole_B2O3 - ox_mole_total <= 0
B2O3_umf_lower: - 0.15 fluxes_total + mole_B2O3 >= 0
B2O3_umf_upper: - 0.15 fluxes_total + mole_B2O3 <= 0
B2O3_wt_%_lower: mass_B2O3 >= 0
B2O3_wt_%_upper: mass_B2O3 - ox_mass_total <= 0
BaO: mass_BaO = 0
CaO: 0.0047 ingredient_1 + 0.0564 ingredient_11 + 0.1407 ingredient_12
 + 0.2013 ingredient_13 + 0.1136 ingredient_14 + 0.5422 ingredient_15
 + 0.0008 ingredient_2 + 0.008 ingredient_3 + 0.01 ingredient_5
 + 0.4828 ingredient_6 + 0.561 ingredient_7 - mass_CaO = 0
CaO_mol_%_lower: mole_CaO >= 0
CaO_mol_%_upper: mole_CaO - ox_mole_total <= 0
CaO_umf_lower: mole_CaO >= 0
CaO_umf_upper: - fluxes_total + mole_CaO <= 0
CaO_wt_%_lower: mass_CaO >= 0
CaO_wt_%_upper: mass_CaO - ox_mass_total <= 0
Fe2O3: 0.0098 ingredient_1 + 0.012 ingredient_2 + 0.95 ingredient_21
 + 0.0005 ingredient_3 + 0.001 ingredient_5 - mass_Fe2O3 = 0
Fe2O3_mol_%_lower: mole_Fe2O3 >= 0
Fe2O3_mol_%_upper: mole_Fe2O3 - ox_mole_total <= 0
Fe2O3_umf_lower: mole_Fe2O3 >= 0
Fe2O3_umf_upper: - fluxes_total + mole_Fe2O3 <= 0
Fe2O3_wt_%_lower: mass_Fe2O3 >= 0
Fe2O3_wt_%_upper: mass_Fe2O3 - ox_mass_total <= 0
K2O: 0.0344 ingredient_1 + 0.0345 ingredient_11 + 0.0068 ingredient_12
 + 0.0069 ingredient_2 + 0.121 ingredient_3 + 0.09 ingredient_5 - mass_K2O = 0
K2O_mol_%_lower: mole_K2O >= 0
K2O_mol_%_upper: mole_K2O - ox_mole_total <= 0
K2O_umf_lower: mole_K2O >= 0
K2O_umf_upper: - fluxes_total + mole_K2O <= 0
K2O_wt_%_lower: mass_K2O >= 0
K2O_wt_%_upper: mass_K2O - ox_mass_total <= 0
Li2O: 0.4074 ingredient_16 - mass_Li2O = 0
MgO: 0.0039 ingredient_1 + 0.0004 ingredient_2 + 0.0007 ingredient_3
 + 0.0005 ingredient_5 + 0.3187 ingredient_8 + 0.478 ingredient_9 - mass_MgO
 = 0
MgO_mol_%_lower: mole_MgO >= 0
MgO_mol_%_upper: mole_MgO - ox_mole_total <= 0
MgO_umf_lower: - 0.3 fluxes_total + mole_MgO >= 0
MgO_umf_upper: - 0.3 fluxes_total + mole_MgO <= 0
MgO_wt_%_lower: mass_MgO >= 0
MgO_wt_%_upper: mass_MgO - ox_mass_total <= 0
MnO2: mass_MnO2 = 0
Na2O: 0.0024 ingredient_1 + 0.1512 ingredient_11 + 0.0628 ingredient_12
 + 0.1028 ingredient_13 + 0.0569 ingredient_14 + 0.0008 ingredient_2
 + 0.021 ingredient_3 + 0.078 ingredient_5 - mass_Na2O = 0
Na2O_mol_%_lower: mole_Na2O >= 0
Na2O_mol_%_upper: mole_Na2O - ox_mole_total <= 0
Na2O_umf_lower: mole_Na2O >= 0
Na2O_umf_upper: - fluxes_total + mole_Na2O <= 0
Na2O_wt_%_lower: mass_Na2O >= 0
Na2O_wt_%_upper: mass_Na2O - ox_mass_total <= 0
P2O5: 0.4578 ingredient_15 - mass_P2O5 = 0
SiO2: ingredient_0 + 0.639 ingredient_1 + 0.6688 ingredient_11
 + 0.553 ingredient_12 + 0.4651 ingredient_13 + 0.4835 ingredient_14
 + 0.5663 ingredient_2 + 0.658 ingredient_3 + 0.558 ingredient_5
 + 0.5172 ingredient_6 + 0.6338 ingredient_8 - mass_SiO2 = 0
SiO2_mol_%_lower: mole_SiO2 >= 0
SiO2_mol_%_upper: mole_SiO2 - ox_mole_total <= 0
SiO2_umf_lower: mole_SiO2 >= 0
SiO2_umf_upper: - 5 fluxes_total + mole_SiO2 <= 0
SiO2_wt_%_lower: mass_SiO2 >= 0
SiO2_wt_%_upper: mass_SiO2 - ox_mass_total <= 0
SrO: mass_SrO = 0
TiO2: 0.0108 ingredient_1 + 0.0051 ingredient_2 + 0.0006 ingredient_5
 - mass_TiO2 = 0
TiO2_mol_%_lower: mole_TiO2 >= 0
TiO2_mol_%_upper: mole_TiO2 - ox_mole_total <= 0
TiO2_umf_lower: mole_TiO2 >= 0
TiO2_umf_upper: - fluxes_total + mole_TiO2 <= 0
TiO2_wt_%_lower: mass_TiO2 >= 0
TiO2_wt_%_upper: mass_TiO2 - ox_mass_total <= 0
ZnO: ingredient_10 - mass_ZnO = 0
_C1: - mass_SiO2 + 60.083 mole_SiO2 = 0
_C10: - mass_Na2O + 61.979 mole_Na2O = 0
_C11: - mass_K2O + 94.191 mole_K2O = 0
_C12: - mass_P2O5 + 141.943 mole_P2O5 = 0
_C13: - mass_Fe2O3 + 159.687 mole_Fe2O3 = 0
_C14: - mass_TiO2 + 79.865 mole_TiO2 = 0
_C15: - mass_MnO2 + 86.937 mole_MnO2 = 0
_C16: - mole_SiO2 + other_0 = 0
_C17: - mole_K2O - mole_Na2O + other_1 = 0
_C18: - mole_K2O - mole_Na2O + other_2 = 0
_C19: - mole_BaO - mole_CaO - mole_MgO - mole_SrO + other_3 = 0
_C2: - mass_Al2O3 + 101.961 mole_Al2O3 = 0
_C20: - ingredient_1 - ingredient_2 + other_4 = 0
_C21: - 0.1189 ingredient_1 - 0.5926 ingredient_16 - 0.1232 ingredient_2
 - 0.05 ingredient_21 - 0.0028 ingredient_3 - 0.009 ingredient_5
 - 0.439 ingredient_7 - 0.0475 ingredient_8 - 0.522 ingredient_9 + other_5 = 0
_C22: other_6 = 0
_C23: fluxes_total - mole_BaO - mole_CaO - mole_K2O - mole_Li2O - mole_MgO
 - mole_Na2O - mole_SrO - mole_ZnO = 0
_C24: - mass_Al2O3 - mass_B2O3 - mass_BaO - mass_CaO - mass_Fe2O3 - mass_K2O
 - mass_Li2O - mass_MgO - mass_MnO2 - mass_Na2O - mass_P2O5 - mass_SiO2
 - mass_SrO - mass_TiO2 - mass_ZnO + ox_mass_total = 0
_C25: - mole_Al2O3 - mole_B2O3 - mole_BaO - mole_CaO - mole_Fe2O3 - mole_K2O
 - mole_Li2O - mole_MgO - mole_MnO2 - mole_Na2O - mole_P2O5 - mole_SiO2
 - mole_SrO - mole_TiO2 - mole_ZnO + ox_mole_total = 0
_C3: - mass_B2O3 + 69.617 mole_B2O3 = 0
_C4: - mass_MgO + 40.304 mole_MgO = 0
_C5: - mass_CaO + 56.077 mole_CaO = 0
_C6: - mass_SrO + 103.619 mole_SrO = 0
_C7: - mass_BaO + 153.329 mole_BaO = 0
_C8: - mass_ZnO + 81.379 mole_ZnO = 0
_C9: - mass_Li2O + 29.879 mole_Li2O = 0
ing_total: - ingredient_0 - ingredient_1 - ingredient_10 - ingredient_11
 - ingredient_12 - ingredient_13 - ingredient_14 - ingredient_15
 - ingredient_16 - ingredient_2 - ingredient_21 - ingredient_22
 - ingredient_23 - ingredient_3 - ingredient_5 - ingredient_6 - ingredient_7
 - ingredient_8 - ingredient_9 + ingredient_total = 0
ingredient_0_lower: ingredient_0 >= 0
ingredient_0_upper: ingredient_0 - ingredient_total <= 0
ingredient_10_lower: ingredient_10 >= 0
ingredient_10_upper: ingredient_10 <= 0
ingredient_11_lower: ingredient_11 >= 0
ingredient_11_upper: ingredient_11 <= 0
ingredient_12_lower: ingredient_12 >= 0
ingredient_12_upper: ingredient_12 <= 0
ingredient_13_lower: ingredient_13 >= 0
ingredient_13_upper: ingredient_13 - ingredient_total <= 0
ingredient_14_lower: ingredient_14 >= 0
ingredient_14_upper: ingredient_14 <= 0
ingredient_15_lower: ingredient_15 >= 0
ingredient_15_upper: ingredient_15 <= 0
ingredient_16_lower: ingredient_16 >= 0
ingredient_16_upper: ingredient_16 <= 0
ingredient_1_lower: ingredient_1 >= 0
ingredient_1_upper: ingredient_1 - ingredient_total <= 0
ingredient_21_lower: ingredient_21 >= 0
ingredient_21_upper: ingredient_21 <= 0
ingredient_22_lower: ingredient_22 >= 0
ingredient_22_upper: ingredient_22 <= 0
ingredient_23_lower: ingredient_23 >= 0
ingredient_23_upper: ingredient_23 <= 0
ingredient_2_lower: ingredient_2 >= 0
ingredient_2_upper: ingredient_2 - ingredient_total <= 0
ingredient_3_lower: ingredient_3 >= 0
ingredient_3_upper: ingredient_3 - ingredient_total <= 0
ingredient_5_lower: ingredient_5 >= 0
ingredient_5_upper: ingredient_5 - ingredient_total <= 0
ingredient_6_lower: ingredient_6 >= 0
ingredient_6_upper: ingredient_6 - ingredient_total <= 0
ingredient_7_lower: ingredient_7 >= 0
ingredient_7_upper: ingredient_7 - ingredient_total <= 0
ingredient_8_lower: ingredient_8 >= 0
ingredient_8_upper: ingredient_8 - ingredient_total <= 0
ingredient_9_lower: ingredient_9 >= 0
ingredient_9_upper: ingredient_9 - ingredient_total <= 0
normalization: mole_Al2O3 = 1
other_0_lower: other_0 >= 0
other_0_upper: - 12 mole_Al2O3 + other_0 <= 0
other_3_lower: - 0.7 fluxes_total + other_3 >= 0
other_3_upper: - 0.7 fluxes_total + other_3 <= 0
other_4_lower: - 0.1 ingredient_total + other_4 >= 0
other_4_upper: - ingredient_total + other_4 <= 0
End
