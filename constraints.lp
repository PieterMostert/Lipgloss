\* Glaze *\
Maximize
SiO2_Al2O3: - SiO2_Al2O3_other
Subject To
Al2O3: - Al2O3_wt_% + 0.2502 Ball_Clay_ingredient + 0.099 Frit_3124_ingredient
 + 0.1198 Frit_3195_ingredient + 0.4021 Kaolin_ingredient
 + 0.233 Neph_Sy_ingredient + 0.1794 Potash_Feldspar_ingredient
 + 0.1944 Soda_Feldspar_ingredient = 0
B2O3: - B2O3_wt_% + 0.1377 Frit_3124_ingredient + 0.2309 Frit_3134_ingredient
 + 0.2262 Frit_3195_ingredient = 0
CaO: 0.003 Ball_Clay_ingredient - CaO_wt_% + 0.1407 Frit_3124_ingredient
 + 0.2013 Frit_3134_ingredient + 0.1136 Frit_3195_ingredient
 + 0.007 Neph_Sy_ingredient + 0.0041 Potash_Feldspar_ingredient
 + 0.561 Whiting_ingredient + 0.4828 Wollastonite_ingredient = 0
Fe2O3: 0.0102 Ball_Clay_ingredient - Fe2O3_wt_% + 0.001 Neph_Sy_ingredient
 + 0.001 Potash_Feldspar_ingredient = 0
K2O: 0.009 Ball_Clay_ingredient + 0.0068 Frit_3124_ingredient - K2O_wt_%
 + 0.046 Neph_Sy_ingredient + 0.1031 Potash_Feldspar_ingredient = 0
MgO: 0.003 Ball_Clay_ingredient + 0.478 Magnesite_ingredient - MgO_wt_%
 + 0.001 Neph_Sy_ingredient + 0.3187 Talc_ingredient = 0
Na2O: 0.002 Ball_Clay_ingredient + 0.0628 Frit_3124_ingredient
 + 0.1028 Frit_3134_ingredient + 0.0569 Frit_3195_ingredient - Na2O_wt_%
 + 0.098 Neph_Sy_ingredient + 0.031 Potash_Feldspar_ingredient
 + 0.1182 Soda_Feldspar_ingredient = 0
SiO2: 0.5906 Ball_Clay_ingredient + 0.553 Frit_3124_ingredient
 + 0.4651 Frit_3134_ingredient + 0.4835 Frit_3195_ingredient
 + 0.4729 Kaolin_ingredient + 0.607 Neph_Sy_ingredient
 + 0.679 Potash_Feldspar_ingredient - SiO2_wt_% + Silica_ingredient
 + 0.6874 Soda_Feldspar_ingredient + 0.6338 Talc_ingredient
 + 0.5172 Wollastonite_ingredient = 0
TiO2: 0.01 Ball_Clay_ingredient - TiO2_wt_% = 0
_C1: Silica_ingredient >= 0
_C10: Soda_Feldspar_ingredient - 100 total_ing <= 0
_C11: Neph_Sy_ingredient >= 0
_C12: Neph_Sy_ingredient - 100 total_ing <= 0
_C13: Wollastonite_ingredient >= 0
_C14: Wollastonite_ingredient - 100 total_ing <= 0
_C15: Whiting_ingredient >= 0
_C16: Whiting_ingredient - 100 total_ing <= 0
_C17: Talc_ingredient >= 0
_C18: Talc_ingredient - 100 total_ing <= 0
_C19: Magnesite_ingredient >= 0
_C2: Silica_ingredient - 100 total_ing <= 0
_C20: Magnesite_ingredient - 100 total_ing <= 0
_C21: Frit_3124_ingredient >= 0
_C22: Frit_3124_ingredient - 100 total_ing <= 0
_C23: Frit_3134_ingredient >= 0
_C24: Frit_3134_ingredient - 100 total_ing <= 0
_C25: Frit_3195_ingredient >= 0
_C26: Frit_3195_ingredient - 100 total_ing <= 0
_C27: 61.979 Na2O_umf - Na2O_wt_% = 0
_C28: Na2O_umf >= 0
_C29: Na2O_umf - total_fluxes <= 0
_C3: Kaolin_ingredient >= 0
_C30: Na2O_wt_% >= 0
_C31: Na2O_wt_% - 100 total_ox_wt_% <= 0
_C32: Na2O_umf >= 0
_C33: Na2O_umf - 100 total_ox_mol_% <= 0
_C34: 40.304 MgO_umf - MgO_wt_% = 0
_C35: MgO_umf >= 0
_C36: MgO_umf - total_fluxes <= 0
_C37: MgO_wt_% >= 0
_C38: MgO_wt_% - 100 total_ox_wt_% <= 0
_C39: MgO_umf >= 0
_C4: Kaolin_ingredient - 100 total_ing <= 0
_C40: MgO_umf - 100 total_ox_mol_% <= 0
_C41: 79.865 TiO2_umf - TiO2_wt_% = 0
_C42: TiO2_umf >= 0
_C43: TiO2_umf - total_fluxes <= 0
_C44: TiO2_wt_% >= 0
_C45: TiO2_wt_% - 100 total_ox_wt_% <= 0
_C46: TiO2_umf >= 0
_C47: TiO2_umf - 100 total_ox_mol_% <= 0
_C48: 69.617 B2O3_umf - B2O3_wt_% = 0
_C49: B2O3_umf >= 0
_C5: Ball_Clay_ingredient >= 0
_C50: B2O3_umf - total_fluxes <= 0
_C51: B2O3_wt_% >= 0
_C52: B2O3_wt_% - 100 total_ox_wt_% <= 0
_C53: B2O3_umf >= 0
_C54: B2O3_umf - 100 total_ox_mol_% <= 0
_C55: 159.687 Fe2O3_umf - Fe2O3_wt_% = 0
_C56: Fe2O3_umf >= 0
_C57: Fe2O3_umf - total_fluxes <= 0
_C58: Fe2O3_wt_% >= 0
_C59: Fe2O3_wt_% - 100 total_ox_wt_% <= 0
_C6: Ball_Clay_ingredient - 100 total_ing <= 0
_C60: Fe2O3_umf >= 0
_C61: Fe2O3_umf - 100 total_ox_mol_% <= 0
_C62: 94.191 K2O_umf - K2O_wt_% = 0
_C63: K2O_umf >= 0
_C64: K2O_umf - total_fluxes <= 0
_C65: K2O_wt_% >= 0
_C66: K2O_wt_% - 100 total_ox_wt_% <= 0
_C67: K2O_umf >= 0
_C68: K2O_umf - 100 total_ox_mol_% <= 0
_C69: 60.083 SiO2_umf - SiO2_wt_% = 0
_C7: Potash_Feldspar_ingredient >= 0
_C70: SiO2_umf >= 0
_C71: SiO2_umf - 100 total_fluxes <= 0
_C72: SiO2_wt_% >= 0
_C73: SiO2_wt_% - 100 total_ox_wt_% <= 0
_C74: SiO2_umf >= 0
_C75: SiO2_umf - 100 total_ox_mol_% <= 0
_C76: 101.961 Al2O3_umf - Al2O3_wt_% = 0
_C77: Al2O3_umf >= 0
_C78: Al2O3_umf - 10 total_fluxes <= 0
_C79: Al2O3_wt_% >= 0
_C8: Potash_Feldspar_ingredient - 100 total_ing <= 0
_C80: Al2O3_wt_% - 100 total_ox_wt_% <= 0
_C81: Al2O3_umf >= 0
_C82: Al2O3_umf - 100 total_ox_mol_% <= 0
_C83: 56.077 CaO_umf - CaO_wt_% = 0
_C84: CaO_umf >= 0
_C85: CaO_umf - total_fluxes <= 0
_C86: CaO_wt_% >= 0
_C87: CaO_wt_% - 100 total_ox_wt_% <= 0
_C88: CaO_umf >= 0
_C89: CaO_umf - 100 total_ox_mol_% <= 0
_C9: Soda_Feldspar_ingredient >= 0
_C90: SiO2_Al2O3_other - SiO2_umf = 0
_C91: - 3 Al2O3_umf + SiO2_Al2O3_other >= 0
_C92: - 18 Al2O3_umf + SiO2_Al2O3_other <= 0
_C93: - 0.01 Ball_Clay_ingredient - 0.01 Frit_3124_ingredient
 - 0.01 Frit_3134_ingredient - 0.01 Frit_3195_ingredient
 - 0.01 Kaolin_ingredient - 0.01 Magnesite_ingredient
 - 0.01 Neph_Sy_ingredient - 0.01 Potash_Feldspar_ingredient
 - 0.01 Silica_ingredient - 0.01 Soda_Feldspar_ingredient
 - 0.01 Talc_ingredient - 0.01 Whiting_ingredient
 - 0.01 Wollastonite_ingredient + total_ing = 0
_C94: - CaO_umf - K2O_umf - MgO_umf - Na2O_umf + total_fluxes = 0
_C95: - 0.01 Al2O3_wt_% - 0.01 B2O3_wt_% - 0.01 CaO_wt_% - 0.01 Fe2O3_wt_%
 - 0.01 K2O_wt_% - 0.01 MgO_wt_% - 0.01 Na2O_wt_% - 0.01 SiO2_wt_%
 - 0.01 TiO2_wt_% + total_ox_wt_% = 0
_C96: - 0.01 Al2O3_umf - 0.01 B2O3_umf - 0.01 CaO_umf - 0.01 Fe2O3_umf
 - 0.01 K2O_umf - 0.01 MgO_umf - 0.01 Na2O_umf - 0.01 SiO2_umf - 0.01 TiO2_umf
 + total_ox_mol_% = 0
normalization: Al2O3_umf = 1
End
