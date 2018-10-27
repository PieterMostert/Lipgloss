\* Glaze recipe *\
Maximize
KNaO_UMF: - other_1
Subject To
Al2O3: 0.343 ingredient_1 + 0.1944 ingredient_10 + 0.244 ingredient_11
 + 0.1776 ingredient_12 + 0.0013 ingredient_15 + 0.137 ingredient_17
 + 0.2382 ingredient_2 + 0.12 ingredient_20 + 0.1885 ingredient_21
 + 0.003 ingredient_22 + 0.0211 ingredient_26 + 0.2542 ingredient_3
 + 0.27 ingredient_32 + 0.2448 ingredient_33 + 0.2185 ingredient_34
 + 0.218 ingredient_37 + 0.2671 ingredient_4 + 0.3183 ingredient_5
 + 0.195 ingredient_6 + 0.323 ingredient_7 + 0.2335 ingredient_8
 + 0.188 ingredient_9 - mass_Al2O3 = 0
Al2O3_mol_%_lower: mole_Al2O3 >= 0
Al2O3_mol_%_upper: mole_Al2O3 - ox_mole_total <= 0
Al2O3_umf_lower: - 0.34 fluxes_total + mole_Al2O3 >= 0
Al2O3_umf_upper: - 0.523 fluxes_total + mole_Al2O3 <= 0
Al2O3_wt_%_lower: mass_Al2O3 >= 0
Al2O3_wt_%_upper: mass_Al2O3 - ox_mass_total <= 0
B2O3: 0.3651 ingredient_18 + 0.42 ingredient_22 + 0.565 ingredient_23
 + 0.2878 ingredient_26 - mass_B2O3 = 0
BaO: 0.003 ingredient_11 - mass_BaO = 0
CaO: 0.001 ingredient_1 + 0.01 ingredient_11 + 0.0011 ingredient_12
 + 0.4828 ingredient_13 + 0.53 ingredient_14 + 0.0092 ingredient_15
 + 0.018 ingredient_16 + 0.02 ingredient_17 + 0.0018 ingredient_2
 + 0.01 ingredient_20 + 0.0123 ingredient_21 + 0.264 ingredient_22
 + 0.1159 ingredient_26 + 0.5582 ingredient_27 + 0.0019 ingredient_3
 + 0.5422 ingredient_31 + 0.008 ingredient_32 + 0.0027 ingredient_33
 + 0.0032 ingredient_34 + 0.003 ingredient_36 + 0.0045 ingredient_37
 + 0.0019 ingredient_7 + 0.0047 ingredient_8 + 0.008 ingredient_9 - mass_CaO
 = 0
CaO_mol_%_lower: mole_CaO >= 0
CaO_mol_%_upper: mole_CaO - ox_mole_total <= 0
CaO_umf_lower: mole_CaO >= 0
CaO_umf_upper: - fluxes_total + mole_CaO <= 0
CaO_wt_%_lower: mass_CaO >= 0
CaO_wt_%_upper: mass_CaO - ox_mass_total <= 0
Fe2O3: 0.0028 ingredient_1 + 0.001 ingredient_11 + 0.0005 ingredient_12
 + 0.0005 ingredient_14 + 0.006 ingredient_15 + 0.003 ingredient_16
 + 0.007 ingredient_17 + 0.95 ingredient_19 + 0.004 ingredient_2
 + 0.025 ingredient_20 + 0.0358 ingredient_21 + 0.001 ingredient_22
 + 0.0043 ingredient_3 + 0.057 ingredient_32 + 0.0196 ingredient_33
 + 0.0977 ingredient_34 + 0.002 ingredient_36 + 0.0192 ingredient_37
 + 0.0116 ingredient_4 + 0.014 ingredient_5 + 0.091 ingredient_6
 + 0.0095 ingredient_7 + 0.0098 ingredient_8 + 0.0005 ingredient_9
 - mass_Fe2O3 = 0
Fe2O3_mol_%_lower: mole_Fe2O3 >= 0
Fe2O3_mol_%_upper: mole_Fe2O3 - ox_mole_total <= 0
Fe2O3_umf_lower: - 0.48 fluxes_total + mole_Fe2O3 >= 0
Fe2O3_umf_upper: - 0.48 fluxes_total + mole_Fe2O3 <= 0
Fe2O3_wt_%_lower: mass_Fe2O3 >= 0
Fe2O3_wt_%_upper: mass_Fe2O3 - ox_mass_total <= 0
K2O: 0.019 ingredient_1 + 0.09 ingredient_11 + 0.0045 ingredient_12
 + 0.0002 ingredient_15 + 0.002 ingredient_17 + 0.0203 ingredient_2
 + 0.04 ingredient_20 + 0.0043 ingredient_21 + 0.022 ingredient_3
 + 0.057 ingredient_32 + 0.0207 ingredient_33 + 0.0291 ingredient_34
 + 0.0253 ingredient_37 + 0.0067 ingredient_4 + 0.0079 ingredient_5
 + 0.022 ingredient_6 + 0.015 ingredient_7 + 0.0344 ingredient_8
 + 0.121 ingredient_9 - mass_K2O = 0
K2O_mol_%_lower: mole_K2O >= 0
K2O_mol_%_upper: mole_K2O - ox_mole_total <= 0
K2O_umf_lower: mole_K2O >= 0
K2O_umf_upper: - fluxes_total + mole_K2O <= 0
K2O_wt_%_lower: mass_K2O >= 0
K2O_wt_%_upper: mass_K2O - ox_mass_total <= 0
Li2O: 0.041 ingredient_12 + 0.4074 ingredient_25 + 0.4986 ingredient_39
 - mass_Li2O = 0
MgO: 0.0021 ingredient_1 + 0.0005 ingredient_11 + 0.02 ingredient_14
 + 0.312 ingredient_15 + 0.44 ingredient_16 + 0.027 ingredient_17
 + 0.005 ingredient_20 + 0.0454 ingredient_21 + 0.018 ingredient_22
 + 0.003 ingredient_32 + 0.0062 ingredient_33 + 0.0089 ingredient_34
 + 0.32 ingredient_36 + 0.0062 ingredient_37 + 0.0004 ingredient_4
 + 0.0005 ingredient_5 + 0.0068 ingredient_6 + 0.0029 ingredient_7
 + 0.0039 ingredient_8 + 0.0007 ingredient_9 - mass_MgO = 0
MgO_mol_%_lower: mole_MgO >= 0
MgO_mol_%_upper: mole_MgO - ox_mole_total <= 0
MgO_umf_lower: mole_MgO >= 0
MgO_umf_upper: - fluxes_total + mole_MgO <= 0
MgO_wt_%_lower: mass_MgO >= 0
MgO_wt_%_upper: mass_MgO - ox_mass_total <= 0
MnO2: 0.0002 ingredient_12 - mass_MnO2 = 0
Na2O: 0.0007 ingredient_1 + 0.1182 ingredient_10 + 0.078 ingredient_11
 + 0.0054 ingredient_12 + 0.0012 ingredient_15 + 0.001 ingredient_17
 + 0.1625 ingredient_18 + 0.0028 ingredient_2 + 0.04 ingredient_20
 + 0.0025 ingredient_21 + 0.001 ingredient_22 + 0.5 ingredient_24
 + 0.1281 ingredient_26 + 0.003 ingredient_3 + 0.022 ingredient_32
 + 0.0019 ingredient_33 + 0.0037 ingredient_34 + 0.0021 ingredient_37
 + 0.0008 ingredient_4 + 0.001 ingredient_5 + 0.0019 ingredient_7
 + 0.0024 ingredient_8 + 0.021 ingredient_9 - mass_Na2O = 0
Na2O_mol_%_lower: mole_Na2O >= 0
Na2O_mol_%_upper: mole_Na2O - ox_mole_total <= 0
Na2O_umf_lower: mole_Na2O >= 0
Na2O_umf_upper: - fluxes_total + mole_Na2O <= 0
Na2O_wt_%_lower: mass_Na2O >= 0
Na2O_wt_%_upper: mass_Na2O - ox_mass_total <= 0
P2O5: 0.0003 ingredient_12 + 0.4239 ingredient_27 + 0.4578 ingredient_31
 - mass_P2O5 = 0
SiO2: ingredient_0 + 0.466 ingredient_1 + 0.6874 ingredient_10
 + 0.558 ingredient_11 + 0.7611 ingredient_12 + 0.5172 ingredient_13
 + 0.002 ingredient_14 + 0.6131 ingredient_15 + 0.072 ingredient_16
 + 0.727 ingredient_17 + 0.6638 ingredient_2 + 0.735 ingredient_20
 + 0.6158 ingredient_21 + 0.044 ingredient_22 + 0.4471 ingredient_26
 + 0.7084 ingredient_3 + 0.58 ingredient_32 + 0.6074 ingredient_33
 + 0.5644 ingredient_34 + 0.61 ingredient_36 + 0.6428 ingredient_37
 + 0.3278 ingredient_38 + 0.5014 ingredient_39 + 0.5477 ingredient_4
 + 0.6526 ingredient_5 + 0.589 ingredient_6 + 0.456 ingredient_7
 + 0.639 ingredient_8 + 0.658 ingredient_9 - mass_SiO2 = 0
SiO2_mol_%_lower: mole_SiO2 >= 0
SiO2_mol_%_upper: mole_SiO2 - ox_mole_total <= 0
SiO2_umf_lower: - 3 fluxes_total + mole_SiO2 >= 0
SiO2_umf_upper: - 3.1 fluxes_total + mole_SiO2 <= 0
SiO2_wt_%_lower: mass_SiO2 >= 0
SiO2_wt_%_upper: mass_SiO2 - ox_mass_total <= 0
SrO: 0.004 ingredient_11 + 0.702 ingredient_29 - mass_SrO = 0
TiO2: 0.0002 ingredient_1 + 0.0006 ingredient_11 + 0.002 ingredient_17
 + 0.0061 ingredient_2 + 0.005 ingredient_20 + 0.0023 ingredient_21
 + ingredient_28 + 0.0065 ingredient_3 + 0.009 ingredient_33
 + 0.0086 ingredient_34 + 0.0115 ingredient_37 + 0.0049 ingredient_4
 + 0.0057 ingredient_5 + 0.013 ingredient_6 + 0.0086 ingredient_7
 + 0.0108 ingredient_8 - mass_TiO2 = 0
ZnO: ingredient_30 - mass_ZnO = 0
ZrO2: 0.6722 ingredient_38 - mass_ZrO2 = 0
_C1: - mass_SiO2 + 60.085 mole_SiO2 = 0
_C10: - mass_Na2O + 61.979 mole_Na2O = 0
_C11: - mass_K2O + 94.196 mole_K2O = 0
_C12: - mass_P2O5 + 141.945 mole_P2O5 = 0
_C13: - mass_Fe2O3 + 159.688 mole_Fe2O3 = 0
_C14: - mass_TiO2 + 79.866 mole_TiO2 = 0
_C15: - mass_MnO2 + 86.937 mole_MnO2 = 0
_C16: - mass_ZrO2 + 123.222 mole_ZrO2 = 0
_C17: fluxes_total - mole_BaO - mole_CaO - mole_K2O - mole_Li2O - mole_MgO
 - mole_Na2O - mole_SrO - mole_ZnO = 0
_C18: - mass_Al2O3 - mass_B2O3 - mass_BaO - mass_CaO - mass_Fe2O3 - mass_K2O
 - mass_Li2O - mass_MgO - mass_MnO2 - mass_Na2O - mass_P2O5 - mass_SiO2
 - mass_SrO - mass_TiO2 - mass_ZnO - mass_ZrO2 + ox_mass_total = 0
_C19: - mole_Al2O3 - mole_B2O3 - mole_BaO - mole_CaO - mole_Fe2O3 - mole_K2O
 - mole_Li2O - mole_MgO - mole_MnO2 - mole_Na2O - mole_P2O5 - mole_SiO2
 - mole_SrO - mole_TiO2 - mole_ZnO - mole_ZrO2 + ox_mole_total = 0
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
 - ingredient_27 - ingredient_28 - ingredient_29 - ingredient_3
 - ingredient_30 - ingredient_31 - ingredient_32 - ingredient_33
 - ingredient_34 - ingredient_35 - ingredient_36 - ingredient_37
 - ingredient_38 - ingredient_39 - ingredient_4 - ingredient_40 - ingredient_5
 - ingredient_6 - ingredient_7 - ingredient_8 - ingredient_9
 + ingredient_total = 0
ingredient_0_lower: ingredient_0 >= 0
ingredient_0_upper: ingredient_0 - ingredient_total <= 0
ingredient_10_lower: ingredient_10 >= 0
ingredient_10_upper: ingredient_10 <= 0
ingredient_11_lower: ingredient_11 >= 0
ingredient_11_upper: ingredient_11 <= 0
ingredient_12_lower: ingredient_12 >= 0
ingredient_12_upper: ingredient_12 <= 0
ingredient_13_lower: ingredient_13 >= 0
ingredient_13_upper: ingredient_13 <= 0
ingredient_14_lower: ingredient_14 - 0.1 ingredient_total >= 0
ingredient_14_upper: ingredient_14 - ingredient_total <= 0
ingredient_15_lower: ingredient_15 >= 0
ingredient_15_upper: ingredient_15 <= 0
ingredient_16_lower: ingredient_16 >= 0
ingredient_16_upper: ingredient_16 <= 0
ingredient_17_lower: ingredient_17 >= 0
ingredient_17_upper: ingredient_17 <= 0
ingredient_18_lower: ingredient_18 >= 0
ingredient_18_upper: ingredient_18 <= 0
ingredient_19_lower: ingredient_19 >= 0
ingredient_19_upper: ingredient_19 - ingredient_total <= 0
ingredient_1_lower: ingredient_1 >= 0
ingredient_1_upper: ingredient_1 <= 0
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
ingredient_27_lower: ingredient_27 >= 0
ingredient_27_upper: ingredient_27 <= 0
ingredient_28_lower: ingredient_28 >= 0
ingredient_28_upper: ingredient_28 <= 0
ingredient_29_lower: ingredient_29 >= 0
ingredient_29_upper: ingredient_29 <= 0
ingredient_2_lower: ingredient_2 >= 0
ingredient_2_upper: ingredient_2 <= 0
ingredient_30_lower: ingredient_30 >= 0
ingredient_30_upper: ingredient_30 <= 0
ingredient_31_lower: ingredient_31 >= 0
ingredient_31_upper: ingredient_31 <= 0
ingredient_32_lower: ingredient_32 >= 0
ingredient_32_upper: ingredient_32 <= 0
ingredient_33_lower: ingredient_33 >= 0
ingredient_33_upper: ingredient_33 <= 0
ingredient_34_lower: ingredient_34 >= 0
ingredient_34_upper: ingredient_34 <= 0
ingredient_35_lower: ingredient_35 >= 0
ingredient_35_upper: ingredient_35 <= 0
ingredient_36_lower: ingredient_36 >= 0
ingredient_36_upper: ingredient_36 - ingredient_total <= 0
ingredient_37_lower: ingredient_37 >= 0
ingredient_37_upper: ingredient_37 <= 0
ingredient_38_lower: ingredient_38 >= 0
ingredient_38_upper: ingredient_38 <= 0
ingredient_39_lower: ingredient_39 >= 0
ingredient_39_upper: ingredient_39 <= 0
ingredient_3_lower: ingredient_3 >= 0
ingredient_3_upper: ingredient_3 <= 0
ingredient_40_lower: ingredient_40 >= 0
ingredient_40_upper: ingredient_40 <= 0
ingredient_4_lower: ingredient_4 >= 0
ingredient_4_upper: ingredient_4 <= 0
ingredient_5_lower: ingredient_5 >= 0
ingredient_5_upper: ingredient_5 <= 0
ingredient_6_lower: ingredient_6 >= 0
ingredient_6_upper: ingredient_6 <= 0
ingredient_7_lower: ingredient_7 >= 0
ingredient_7_upper: ingredient_7 <= 0
ingredient_8_lower: ingredient_8 >= 0
ingredient_8_upper: ingredient_8 <= 0
ingredient_9_lower: ingredient_9 >= 0
ingredient_9_upper: ingredient_9 - ingredient_total <= 0
normalization: fluxes_total = 1
other_0: - mole_SiO2 + other_0 = 0
other_0_lower: - 3 mole_Al2O3 + other_0 >= 0
other_0_upper: - 18 mole_Al2O3 + other_0 <= 0
other_1: - mole_K2O - mole_Na2O + other_1 = 0
other_1_lower: - 0.31 fluxes_total + other_1 >= 0
other_1_upper: - 0.32 fluxes_total + other_1 <= 0
other_2: - mole_K2O - mole_Na2O + other_2 = 0
other_3: - mole_BaO - mole_CaO - mole_MgO - mole_SrO + other_3 = 0
other_4: other_4 - other_attr_2 = 0
other_5: other_5 - other_attr_0 = 0
other_6: other_6 - other_attr_1 = 0
other_7: - ingredient_33 - ingredient_4 - ingredient_7 + other_7 = 0
other_attr_0: 0.165 ingredient_1 + 0.009 ingredient_11 + 0.0059 ingredient_12
 + 0.44 ingredient_14 + 0.0527 ingredient_15 + 0.463 ingredient_16
 + 0.077 ingredient_17 + 0.4724 ingredient_18 + 0.05 ingredient_19
 + 0.063 ingredient_2 + 0.239 ingredient_22 + 0.435 ingredient_23
 + 0.5 ingredient_24 + 0.5926 ingredient_25 + 0.0179 ingredient_27
 + 0.298 ingredient_29 + 0.0564 ingredient_34 + ingredient_35
 + 0.065 ingredient_36 + 0.0696 ingredient_37 + 0.16 ingredient_4
 + 0.091 ingredient_6 + 0.181 ingredient_7 + 0.061 ingredient_8
 + 0.0028 ingredient_9 - other_attr_0 = 0
other_attr_1: 0.41 ingredient_1 + 2.144 ingredient_17 - other_attr_1 = 0
other_attr_2: ingredient_1 + ingredient_17 + ingredient_2 + ingredient_33
 + ingredient_34 + ingredient_37 + ingredient_4 + ingredient_6 + ingredient_7
 + ingredient_8 - other_attr_2 = 0
End
