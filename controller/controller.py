# LIPGLOSS - Graphical user interface for constructing glaze recipes
# Copyright (C) 2017 Pieter Mostert

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# version 3 along with this program (see LICENCE.txt).  If not, see
# <http://www.gnu.org/licenses/>.

# Contact: pi.mostert@gmail.com

from model.core_data import CoreData
from view.main_window import MainWindow
from model.restrictions import Restriction
from model.lp_recipe_problem import LpRecipeProblem
import pulp
from model.recipes import Recipe

cd = CoreData()
mw = MainWindow()
Restriction.display_frame = mw.restriction_sf.interior
restr_dict = {}

# Create oxide restrictions:
for ox in cd.oxide_dict:   
    def_upp = 1   # Default upper bound for oxide UMF.
    dp = 3
    if ox == 'SiO2':
        def_upp = 100
        dp = 2
    elif ox == 'Al2O3':
        def_upp = 10
    restr_dict['umf_'+ox] = Restriction('umf_'+ox, ox, 'mole_'+ox, "lp_var['fluxes_total']", 0, def_upp, dec_pt=dp)
    restr_dict['mass_perc_'+ox] = Restriction('mass_perc_'+ox, ox, 'mass_'+ox, "0.01*lp_var['ox_mass_total']", 0, 100, dec_pt=2) 
    restr_dict['mole_perc_'+ox] = Restriction('mole_perc_'+ox, ox, 'mole_'+ox, "0.01*lp_var['ox_mole_total']", 0, 100, dec_pt=2)

# Create ingredient restrictions:
for i in cd.ingredient_dict:
    restr_dict['ingredient_'+i] = Restriction('ingredient_'+i, cd.ingredient_dict[i].name, 'ingredient_'+i, "0.01*lp_var['ingredient_total']", 0, 100)

# Create other restrictions:
for index, ot in cd.other_dict.items():
    restr_dict['other_'+index] = Restriction('other_'+index, ot.name, 'other_'+index, ot.normalization, ot.def_low, ot.def_upp, dec_pt=ot.dec_pt)

lprp = LpRecipeProblem("Glaze recipe", pulp.LpMaximize)

# Define default recipe"
lb = {} 
ub = {} 

for ox in ['SiO2', 'Al2O3', 'B2O3', 'MgO', 'CaO', 'Na2O', 'K2O', 'ZnO', 'Fe2O3', 'TiO2', 'P2O5']:
    for t in ['umf_', 'mass_perc_', 'mole_perc_']:
        lb[t+ox] = 0
        ub[t+ox] = 100
ub['umf_Al2O3'] = 10
for ox in ['B2O3', 'MgO', 'CaO', 'Na2O', 'K2O', 'ZnO', 'Fe2O3', 'TiO2', 'P2O5']:
    ub['umf_'+ox] = 1
    
for i in range(15):
    lb['ingredient_'+str(i)] = 0
    ub['ingredient_'+str(i)] = 100

current_recipe = Recipe('Default Recipe Bounds', 0, [str(i) for i in range(3)], [], lb, ub, 'umf_')

mw.setup(cd, restr_dict, lprp)

#open default recipe
