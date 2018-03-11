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

# We define the Restriction, Oxide, Ingredient,and Other classes.

from tkinter import *
from view.pretty_names import prettify
from functools import partial
import shelve
import copy

from .core_data import CoreData
from pulp import *


##class Crud:
##    static = 1
##    def __init__(self, stuff):
##        self.stuff = stuff
##    def update_static(self, new):
##	Crud.static = new
##
##class Crap(Crud):
##    def __init__(self, stuff, tuff):
##	super(Crap, self, stuff).__init__()
##
### instances of Crap can be used to change Crud.static and c.static for any instance c of any child of Crud

class LpRecipeProblem(LpProblem, CoreData):

    def __init__(self, name, max_or_min):
        '''Basic LP problem constraints that always hold'''

        LpProblem.__init__(self, name, max_or_min)

        self.lp_var = {}     # lp_var is a dictionary for the variables in the linear programming problem

        # Create variables used to normalize:
        for total in ['ingredient_total', 'fluxes_total', 'ox_mass_total', 'ox_mole_total']:
            self.lp_var[total] = pulp.LpVariable(total, 0, None, pulp.LpContinuous)

        for index in self.ingredient_dict:
            ing = 'ingredient_'+index
            self.lp_var[ing] = pulp.LpVariable(ing, 0, None, pulp.LpContinuous)
            
        for ox in self.oxide_dict:
            self.lp_var['mole_'+ox] = pulp.LpVariable('mole_'+ox, 0, None, pulp.LpContinuous)
            self.lp_var['mass_'+ox] = pulp.LpVariable('mass_'+ox, 0, None, pulp.LpContinuous)
            # Relate mole percent and unity:
            self += self.lp_var['mole_'+ox] * self.oxide_dict[ox].molar_mass == self.lp_var['mass_'+ox]   
            # Relate ingredients and oxides:
            self += sum(self.ingredient_compositions[index][ox] * self.lp_var['ingredient_'+index]/100 \
                        for index in self.ingredient_dict if ox in self.ingredient_compositions[index]) \
                    == self.lp_var['mass_'+ox], ox

        for index in self.other_dict:
            ot = 'other_'+index
            coefs = self.other_dict[index].numerator_coefs
            linear_combo = [(self.lp_var[key], coefs[key]) for key in coefs]
            self.lp_var[ot] = pulp.LpVariable(ot, 0, None, pulp.LpContinuous)
            # Relate this variable to the other variables:
            self += self.lp_var[ot] == LpAffineExpression(linear_combo), ot

        self += self.lp_var['ingredient_total'] == sum(self.lp_var['ingredient_'+index] for index in self.ingredient_dict), 'ing_total'
        self += self.lp_var['fluxes_total'] == sum(self.oxide_dict[ox].flux * self.lp_var['mole_'+ox] for ox in self.oxide_dict)
        self += self.lp_var['ox_mass_total'] == sum(self.lp_var['mass_'+ox] for ox in self.oxide_dict)
        self += self.lp_var['ox_mole_total'] == sum(self.lp_var['mole_'+ox] for ox in self.oxide_dict)

    def calc_restrictions(self, recipe):   # first update current recipe? Method in GUI main_window class

        restrictions = [restr_dict[index] for index in restr_keys(self.oxides, self.ingredients, self.other)]
         
        # first, test for obvious errors

        selected_fluxes = fluxes_subset(recipe.oxides)

        if sum(self.oxide_dict[ox].flux for ox in self.oxides) == 0:
            messagebox.showerror(" ", 'No flux! You have to give a flux.')
            return
    
        # Run tests to see if the denominators of other restrictions are identically zero?

        for res in restrictions:
            if res.low.get() > res.upp.get():
                messagebox.showerror(" ", 'Incompatible ' + print_res_type(res.normalization) + 'bounds on ' + prettify(res.name))
                return

        delta = 0.1**9

        sum_UMF_low = sum(restr_dict['umf_'+ox].low.get() for ox in selected_fluxes)
        if sum_UMF_low > 1 + delta:
            messagebox.showerror(" ", 'The sum of the UMF flux lower bounds is '+str(sum_UMF_low)
                                       +'. It should be at most 1. Decrease one of the lower bounds by '+str(sum_UMF_low-1)
                                       +' or more.')     #will be a problem if they're all < sum_UMF_low-1))
            return

        sum_UMF_upp = sum(restr_dict['umf_'+ox].upp.get() for ox in selected_fluxes)            
        if sum_UMF_upp < 1 - delta:
            messagebox.showerror(" ", 'The sum of the UMF flux upper bounds is '+str(sum_UMF_upp)
                                       +'. It should be at least 1. Increase one of the upper bounds by '+str(1-sum_UMF_low)
                                       +' or more.')
            return

        for t in ['mass_perc_', 'mole_perc_']:
            sum_t_low = sum(restr_dict[t+ox].low.get() for ox in self.oxides)
            if sum_t_low > 100 + delta:
                messagebox.showerror(" ", 'The sum of the ' + prettify(t) + ' lower bounds is '+str(sum_t_low)
                                           +'. It should be at most 100. Decrease one of the lower bounds by '+str(sum_t_low-100)
                                           +' or more.')     #will be a problem if they're all < sum_t_low-100)
                return

            sum_t_upp = sum(restr_dict[t+ox].upp.get() for ox in self.oxides)
            if  sum_t_upp < 100 - delta:
                messagebox.showerror(" ", 'The sum of the ' + prettify(t) + ' upper bounds is '+str(sum_t_upp)
                                           +'. It should be at least 100. Increase one of the upper bounds by '+str(100-sum_t_upp)
                                           +' or more.') 
                return
            
        sum_ing_low = sum(restr_dict['ingredient_'+index].low.get() for index in self.ingredients)
        if sum_ing_low > 100 + delta:
            messagebox.showerror(" ", 'The sum of the ingredient lower bounds is '+str(sum_ing_low)
                                      +'. It should be at most 100. Decrease one of the lower bounds by '+str(sum_ing_low-100)
                                      +' or more.')     #will be a problem if they're all < sum_ing_low-100)
            return
            
        sum_ing_upp = sum(restr_dict['ingredient_'+index].upp.get() for index in self.ingredients)
        if sum_ing_upp < 100 - delta:
            messagebox.showerror(" ", 'The sum of the ingredient upper bounds is '+str(sum_ing_upp)
                                       +'. It should be at least 100. Increase one of the upper bounds by '+str(100-sum_ing_upp)
                                       +' or more.')  
            return
         
        t0 = time.process_time()  
            
        for index in self.ingredient_dict:
            ing = 'ingredient_'+index
            if index in recipe.ingredients:
                ing_low = 0.01*restr_dict[ing].low.get()
                ing_upp = 0.01*restr_dict[ing].upp.get()
            else:
                ing_low = 0
                ing_upp = 0
            self.constraints[ing+'_lower'] = lp_var[ing] >= ing_low*lp_var['ingredient_total']      # ingredient lower bounds    
            self.constraints[ing+'_upper'] = lp_var[ing] <= ing_upp*lp_var['ingredient_total']      # ingredient upper bounds


        t1 = time.process_time()      # The next section takes a while, perhaps because the dictionary lp_var is long.
                                      # May be better to split it.
         
        for ox in self.oxide_dict:          
            if ox in self.oxides:     
                self.constraints[ox+'_umf_lower'] = lp_var['mole_'+ox] >= restr_dict['umf_'+ox].low.get()*lp_var['fluxes_total']   # oxide UMF lower bounds
                self.constraints[ox+'_umf_upper'] = lp_var['mole_'+ox] <= restr_dict['umf_'+ox].upp.get()*lp_var['fluxes_total']   # oxide UMF upper bounds
                self.constraints[ox+'_wt_%_lower'] = lp_var['mass_'+ox] >= 0.01*restr_dict['mass_perc_'+ox].low.get()*lp_var['ox_mass_total']    # oxide weight % lower bounds
                self.constraints[ox+'_wt_%_upper'] = lp_var['mass_'+ox] <= 0.01*restr_dict['mass_perc_'+ox].upp.get()*lp_var['ox_mass_total']    # oxide weight % upper bounds
                self.constraints[ox+'_mol_%_lower'] = lp_var['mole_'+ox] >= 0.01*restr_dict['mole_perc_'+ox].low.get()*lp_var['ox_mole_total']   # oxide mol % lower bounds
                self.constraints[ox+'_mol_%_upper'] = lp_var['mole_'+ox] <= 0.01*restr_dict['mole_perc_'+ox].upp.get()*lp_var['ox_mole_total']   # oxide mol % upper bounds

            else:
                try:
                    del self.constraints[ox+'_umf_lower']
                    del self.constraints[ox+'_umf_upper']
                    del self.constraints[ox+'_wt_%_lower']
                    del self.constraints[ox+'_wt_%_upper']
                    del self.constraints[ox+'_mol_%_lower']
                    del self.constraints[ox+'_mol_%_upper']
                except:
                    pass
                 
##        if 'KNaO' in self.oxides:
##            prob += lp_var['KNaO_umf'] == lp_var['K2O_umf'] + lp_var['Na2O_umf']     
##            prob += lp_var['KNaO_wt_%'] == lp_var['K2O_wt_%'] + lp_var['Na2O_wt_%']  

        for index in other_dict:
            if index in self.other:  
                other_norm = eval(other_dict[index].normalization)               
                self.constraints['other_'+index+'_lower'] = self.lp_var['other_'+index] >= restr_dict['other_'+index].low.get()*other_norm   # lower bound
                self.constraints['other_'+index+'_upper'] = self.lp_var['other_'+index] <= restr_dict['other_'+index].upp.get()*other_norm   # upper bound
            else:
                try:
                    del self.constraints['other_'+index+'_lower']
                    del self.constraints['other_'+index+'_upper']
                except:
                    pass

# Finally, we're ready to calculate the upper and lower bounds imposed on all the variables
         
        for res in restrictions:    
            self.constraints['normalization'] = eval(res.normalization) == 1  # Apply the normalization of the restriction in question
                                                                                   # Apparently this doesn't slow things down a whole lot
            for eps in [1,-1]:               # calculate lower and upper bounds.
                self += eps*lp_var[res.objective_func], res.name
                self.writeLP('constraints.lp')
                self.solve(solver)
                if self.status == 1:
                    res.calc_bounds[eps].config(text = ('%.'+str(res.dec_pt)+'f') % abs(eps*pulp.value(self.objective)))
                                                        # we use abs above to avoid showing -0.0, but this could cause problems
                                                        # if we introduce other attributes that can be negative
                    #prob.writeLP('constraints.lp')
                else:
                    messagebox.showerror(" ", LpStatus[self.status])
                    self.writeLP('constraints.lp')
                    return


