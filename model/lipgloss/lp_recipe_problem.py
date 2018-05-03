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
# <http://www.gnu.org/licenses/>.186


# Contact: pi.mostert@gmail.com

import tkinter
from tkinter import messagebox      # eliminate
from view.pretty_names import prettify   # eliminate
from functools import partial
import shelve
import copy

from .core_data import CoreData
from .recipes import restr_keys
from .pulp2dim import *
from pulp import *
import time

solver = GLPK()
#solver = None

class LpRecipeProblem(LpProblem):

    def __init__(self, name, max_or_min, core_data):
        '''Basic LP problem constraints that always hold'''

        #super().__init__()
        LpProblem.__init__(self, name, max_or_min)
        #CoreData.__init__(self)
        self.ingredient_dict = core_data.ingredient_dict
        self.oxide_dict = core_data.oxide_dict
        self.other_dict = core_data.other_dict
        self.ingredient_analyses = core_data.ingredient_analyses
        
        self.lp_var = {}     # self.lp_var is a dictionary for the variables in the linear programming problem

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
        self.update_ingredient_analyses(core_data)

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

    def update_ingredient_analyses(self, core_data):
        "To be run when the composition of any ingredient is changed. May be better to do this for a specific ingredient"
        #self.ingredient_analyses = core_data.ingredient_analyses #unnecessary
        for ox in self.oxide_dict:
            self.constraints[ox] = sum(self.ingredient_analyses[j][ox] * self.lp_var['ingredient_'+j]/100 \
                                   for j in self.ingredient_dict if ox in self.ingredient_analyses[j]) \
                                   == self.lp_var['mass_'+ox]

    def remove_ingredient(self, i, core_data):
        try:
            core_data.remove_ingredient(i)
        except:
            pass
        ##    self._variables.remove(self.lp_var['ingredient_'+i])
        # The commented-out line above doesn't work in general since self.lp_var['ingredient_'+i] is regarded as
        # being equal to all entries of self._variables, so it removes the first entry. Instead, we need to use 'is'.
        for k, j in enumerate(self._variables):
            if j is self.lp_var['ingredient_'+i]:
                del self._variables[k]  
        try:
            del self.constraints['ingredient_'+i+'_lower']  # Is this necessary?
            del self.constraints['ingredient_'+i+'_upper']  # Is this necessary?
        except:
            pass

        #del self.ingredient_dict[i]
        #del self.ingredient_analyses[i]
        self.constraints['ing_total'] = self.lp_var['ingredient_total'] == \
                                        sum(self.lp_var['ingredient_'+j] for j in self.ingredient_dict)

##        try:
##            del core_data.ingredient_analyses[i]
##        except:
##            pass
        self.update_ingredient_analyses(core_data)

    def add_ingredient(self, i, core_data):
        pass     

    def calc_restrictions(self, recipe, restr_dict):   # first update recipe
        
        # first, test for obvious errors

        if sum(self.oxide_dict[ox].flux for ox in recipe.oxides) == 0:
            messagebox.showerror(" ", 'No flux! You have to give a flux.')
            return
  
        # Run tests to see if the denominators of other restrictions are identically zero?

        for key in recipe.restriction_keys:
            if recipe.lower_bounds[key] > recipe.upper_bounds[key]:
                res = restr_dict[key]
                messagebox.showerror(" ", 'Incompatible ' + print_res_type(res.normalization) + 'bounds on ' + prettify(res.name))
                return

        delta = 0.1**9

        selected_fluxes = recipe.fluxes()

        sum_UMF_low = sum(recipe.lower_bounds['umf_'+ox] for ox in selected_fluxes)
        if sum_UMF_low > 1 + delta:
            messagebox.showerror(" ", 'The sum of the UMF flux lower bounds is '+str(sum_UMF_low)
                                       +'. It should be at most 1. Decrease one of the lower bounds by '+str(sum_UMF_low-1)
                                       +' or more.')     #will be a problem if they're all < sum_UMF_low-1))
            return

        sum_UMF_upp = sum(recipe.upper_bounds['umf_'+ox] for ox in selected_fluxes)            
        if sum_UMF_upp < 1 - delta:
            messagebox.showerror(" ", 'The sum of the UMF flux upper bounds is '+str(sum_UMF_upp)
                                       +'. It should be at least 1. Increase one of the upper bounds by '+str(1-sum_UMF_low)
                                       +' or more.')
            return

        for t in ['mass_perc_', 'mole_perc_']:
            sum_t_low = sum(recipe.lower_bounds[t+ox] for ox in recipe.oxides)
            if sum_t_low > 100 + delta:
                messagebox.showerror(" ", 'The sum of the ' + prettify(t) + ' lower bounds is '+str(sum_t_low)
                                           +'. It should be at most 100. Decrease one of the lower bounds by '+str(sum_t_low-100)
                                           +' or more.')     #will be a problem if they're all < sum_t_low-100)
                return

            sum_t_upp = sum(recipe.upper_bounds[t+ox] for ox in recipe.oxides)
            if  sum_t_upp < 100 - delta:
                messagebox.showerror(" ", 'The sum of the ' + prettify(t) + ' upper bounds is '+str(sum_t_upp)
                                           +'. It should be at least 100. Increase one of the upper bounds by '+str(100-sum_t_upp)
                                           +' or more.') 
                return
            
        sum_ing_low = sum(recipe.lower_bounds['ingredient_'+index] for index in recipe.ingredients)
        if sum_ing_low > 100 + delta:
            messagebox.showerror(" ", 'The sum of the ingredient lower bounds is '+str(sum_ing_low)
                                      +'. It should be at most 100. Decrease one of the lower bounds by '+str(sum_ing_low-100)
                                      +' or more.')     #will be a problem if they're all < sum_ing_low-100)
            return
            
        sum_ing_upp = sum(recipe.upper_bounds['ingredient_'+index] for index in recipe.ingredients)
        if sum_ing_upp < 100 - delta:
            messagebox.showerror(" ", 'The sum of the ingredient upper bounds is '+str(sum_ing_upp)
                                       +'. It should be at least 100. Increase one of the upper bounds by '+str(100-sum_ing_upp)
                                       +' or more.')  
            return
         
        t0 = time.process_time()  
            
        for index in self.ingredient_dict:
            ing = 'ingredient_'+index
            if index in recipe.ingredients:
                ing_low = 0.01*recipe.lower_bounds[ing]
                ing_upp = 0.01*recipe.upper_bounds[ing]
            else:
                ing_low = 0
                ing_upp = 0
            self.constraints[ing+'_lower'] = self.lp_var[ing] >= ing_low*self.lp_var['ingredient_total']      # ingredient lower bounds    
            self.constraints[ing+'_upper'] = self.lp_var[ing] <= ing_upp*self.lp_var['ingredient_total']      # ingredient upper bounds


        t1 = time.process_time()      # The next section takes a while, perhaps because the dictionary self.lp_var is long.
                                      # May be better to split it.
         
        for ox in self.oxide_dict:          
            if ox in recipe.oxides:     
                self.constraints[ox+'_umf_lower'] = self.lp_var['mole_'+ox] >= recipe.lower_bounds['umf_'+ox]*self.lp_var['fluxes_total']   # oxide UMF lower bounds
                self.constraints[ox+'_umf_upper'] = self.lp_var['mole_'+ox] <= recipe.upper_bounds['umf_'+ox]*self.lp_var['fluxes_total']   # oxide UMF upper bounds
                self.constraints[ox+'_wt_%_lower'] = self.lp_var['mass_'+ox] >= 0.01*recipe.lower_bounds['mass_perc_'+ox]*self.lp_var['ox_mass_total']    # oxide weight % lower bounds
                self.constraints[ox+'_wt_%_upper'] = self.lp_var['mass_'+ox] <= 0.01*recipe.upper_bounds['mass_perc_'+ox]*self.lp_var['ox_mass_total']    # oxide weight % upper bounds
                self.constraints[ox+'_mol_%_lower'] = self.lp_var['mole_'+ox] >= 0.01*recipe.lower_bounds['mole_perc_'+ox]*self.lp_var['ox_mole_total']   # oxide mol % lower bounds
                self.constraints[ox+'_mol_%_upper'] = self.lp_var['mole_'+ox] <= 0.01*recipe.upper_bounds['mole_perc_'+ox]*self.lp_var['ox_mole_total']   # oxide mol % upper bounds

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
##            prob += self.lp_var['KNaO_umf'] == self.lp_var['K2O_umf'] + self.lp_var['Na2O_umf']     
##            prob += self.lp_var['KNaO_wt_%'] == lp_var['K2O_wt_%'] + lp_var['Na2O_wt_%']  

        for index in self.other_dict:
            if index in recipe.other:  
                other_norm = eval(self.other_dict[index].normalization)               
                self.constraints['other_'+index+'_lower'] = self.lp_var['other_'+index] >= recipe.lower_bounds['other_'+index]*other_norm   # lower bound
                self.constraints['other_'+index+'_upper'] = self.lp_var['other_'+index] <= recipe.upper_bounds['other_'+index]*other_norm   # upper bound
            else:
                try:
                    del self.constraints['other_'+index+'_lower']
                    del self.constraints['other_'+index+'_upper']
                except:
                    pass

# Finally, we're ready to calculate the upper and lower bounds imposed on all the variables

        calc_bounds = {-1:{}, 1:{}}
        for key in recipe.restriction_keys:
            res = restr_dict[key]
            self.constraints['normalization'] = eval(res.normalization) == 1  # Apply the normalization of the restriction in question
                                                                                   # Apparently this doesn't slow things down a whole lot
            for eps in [1, -1]:               # calculate lower and upper bounds.
                self += eps*self.lp_var[res.objective_func], res.name
                self.writeLP('constraints.lp')
                self.solve(solver)
                if self.status == 1:
                    calc_bounds[eps][key] = eps*pulp.value(self.objective)
                    #prob.writeLP('constraints.lp')
                else:
                    messagebox.showerror(" ", LpStatus[self.status])
                    self.writeLP('constraints.lp')
                    return
                
        return {'lower':calc_bounds[-1], 'upper':calc_bounds[1]}

    def calc_2d_projection(self, recipe, restr_dict):  # This is designed to be run when only the x and y variables have changed; it does not take
                                               # into account changes to upper and lower bounds. It should be possible to detect when the
                                               # user has clicked in one of the entry boxes since the last time calc_restrictions was run,
                                               # and give a warning in this case. Something like, if you have changed any bounds, click
                                               # 'Calculate restrictions' to apply them.

        if len(recipe.variables) == 2:
            x_var = restr_dict[recipe.variables['x']]
            y_var = restr_dict[recipe.variables['y']]
            x_norm = x_var.normalization
            y_norm = y_var.normalization

            vertices = self.two_dim_projection(self.lp_var[x_var.objective_func], self.lp_var[y_var.objective_func], x_norm, y_norm)   # defined in pulp2dim file
            return vertices

        else:
            print("Select two variables first")
