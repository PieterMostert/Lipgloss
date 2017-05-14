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

import shelve
from tkinter import *
import time
import copy

from pulp2dim import *
from restrictions import *

initialize_recipe = 0       # Run script with initialize_recipe = 1 whenever the Recipe class is changed

def get_ing_comp():                           # Redo. This function is defined in the main (gui) file
    ingredient_compositions = {}
    with shelve.open("IngredientShelf") as ingredient_shelf:
        for index in ingredient_shelf:
            ingredient_compositions[index] = ingredient_shelf[index].oxide_comp
    return ingredient_compositions

def associated_oxides(ingredients):

    assoc_oxides = set()
    ingredient_compositions = get_ing_comp()
    for index in ingredients:
        assoc_oxides = assoc_oxides.union(set(ingredient_compositions[index]))  # update the available oxides. Probably not the most
                                                                                                      # efficient way to do this

    #if 'Na2O' in assoc_oxides and 'K2O' in assoc_oxides:
     #   assoc_oxides.add('KNaO')

    return assoc_oxides

def fluxes_subset(oxides):

    with shelve.open("OxideShelf") as oxide_shelf:
        fluxes = [ox for ox in oxides if oxide_shelf[ox].flux == 1]
    return fluxes

def print_res_type(normalization):   # Used to display error message
    if normalization == "lp_var['fluxes_total']":
        prt = 'UMF '
    elif normalization == "lp_var['ox_mass_total']":
        prt = '% weight '
    elif normalization == "lp_var['ox_mole_total']":
        prt = '% molar '
    else:
        prt = ''
    return prt

def restr_keys(oxides, ingredients, other):
    return [t+ox for t in ['umf_', 'mass_perc_', 'mole_perc_'] for ox in oxides]+\
           ['ingredient_'+i for i in ingredients]+\
           ['other_'+ot for ot in other]

class Recipe:
    'This is actually a set of bounds on a collection of ingredients, together with bounds on the oxides present, and possibly bounds on other quantities'

    def __init__(self, name, pos, ingredients, other, lower_bounds, upper_bounds, entry_type, variables = {}):

        self.name = name
        self.pos = pos   # position in list of recipes to choose
        self.ingredients = ingredients
        self.other = other
        self.oxides = associated_oxides(self.ingredients)   # add a method that updates the oxides when ingredients are changed?
        self.lower_bounds = lower_bounds      # Of the form [{'umf':UMF, 'perc_wt':% wt, 'perc_mol':% mol}, ingredients, other], \
                                              # where UMF, % wt and % mol are dictionaries with self.oxides as inputs, and \
                                              # ingredients and other are dictionaries with self.ingredients and self.other as \
                                              # inputs respectively. Eg \
                                              # [{'umf':{'SiO2':0, 'Al2O3':0, ...}, 'perc_wt':{'SiO2':0, 'Al2O3':0, ...}, \
                                              # 'perc_mol':{'SiO2':0, 'Al2O3':0, ...}}, {'0':0, '1':0, ...}, {}] \
                                              # .
        self.upper_bounds = upper_bounds      # An instance of the restr_index class
        self.variables = variables            # A dictionary whose keys are a subset of the set {'x','y'}, and whose values
                                              # are restriction indices.
        self.entry_type = entry_type

    def update_bounds(self, restr_dict):       # To be used when saving a recipe.
        self.lower_bounds = {}
        self.upper_bounds = {}
        
        self.oxides = associated_oxides(self.ingredients)
        
        for t in ['umf_', 'mass_perc_', 'mole_perc_']:
            for ox in self.oxides:
                self.lower_bounds[t+ox] = restr_dict[t+ox].low.get()
                self.upper_bounds[t+ox] = restr_dict[t+ox].upp.get()
                
        for i in self.ingredients:
            self.lower_bounds['ingredient_'+i] = restr_dict['ingredient_'+i].low.get()
            self.upper_bounds['ingredient_'+i] = restr_dict['ingredient_'+i].upp.get()
            
        for ot in self.other:
            self.lower_bounds['other_'+ot] = restr_dict['other_'+ot].low.get()
            self.upper_bounds['other_'+ot] = restr_dict['other_'+ot].upp.get()

    def update_oxides(self):             # to be run whenever the ingredients are changed
        old_oxides = copy.copy(self.oxides)
        ass_oxides = associated_oxides(self.ingredients)
        for ox in self.oxides:
            if ox not in ass_oxides:
                for t in ['umf_', 'mass_perc_', 'mole_perc_']:
                    try:
                        del self.lower_bounds[t+ox]
                    except:
                        pass
                    try:
                        del self.upper_bounds[t+ox]
                    except:
                        pass

        self.oxides = ass_oxides

    def update_other(self, index):    # update other entry positions

        global other_select_button
        global selected_other

        if index in self.other:   # in this case we're removing the quantity
            self.other.remove(index)
            other_select_button[index].state(['!pressed'])
            restr_dict['other_'+index].remove()

        else:                # in this case we're adding the quantity
            self.other.append(index)
            other_select_button[ot].state(['pressed'])
            with shelve.open("OtherShelf") as other_shelf:
                restr_dict['other_'+index].display(1001 + other_shelf[index].pos)


    def calc_restrictions(self, prob, lp_var, restr_dict, proj_frame):    # This should be redone, so that all the variables and restrictions
                                                                          # in self.prob are defined elsewhere, except for the restrictions  
                                                                          # defined by the user
        
        with shelve.open("OxideShelf") as oxide_shelf:
            oxide_dict = dict(oxide_shelf)

        with shelve.open("IngredientShelf") as ingredient_shelf:
            ingredient_dict = dict(ingredient_shelf)

        ingredient_compositions = get_ing_comp()
        restrictions = [restr_dict[index] for index in restr_keys(self.oxides, self.ingredients, self.other)]
         
        # first, test for obvious errors

        selected_fluxes = fluxes_subset(self.oxides)

        if sum(oxide_dict[ox].flux for ox in self.oxides) == 0:
            messagebox.showerror(" ", 'No flux! You have to give a flux.')
            return

        for res in restrictions:
            if res.low.get() > res.upp.get():
                messagebox.showerror(" ", 'Incompatible ' + print_res_type(res.normalization) + 'bounds on ' + prettify(res.name))
                return

##        if 'SiO2:Al2O3' in selected_other and not ('SiO2' in selected_oxides and 'Al2O3' in selected_oxides):  #replace this with general check to see if normalization is inconsistent
##            tkinter.messagebox.showerror(" ", 'No SiO\u2082 and/or Al\u2082O\u2083')
##            return

        delta = 0.1**9

        if sum(restr_dict['umf_'+ox].low.get() for ox in selected_fluxes) > 1 + delta:
            messagebox.showerror(" ", 'Sum of UMF flux lower bounds > 1')
            return
            
        if sum(restr_dict['umf_'+ox].upp.get() for ox in selected_fluxes) < 1 - delta:
            messagebox.showerror(" ", 'Sum of UMF flux upper bounds < 1')
            return

        for t in ['mass_perc_', 'mole_perc_']:
            if sum(restr_dict[t+ox].low.get() for ox in self.oxides if ox != 'KNaO') > 100 + delta:
                messagebox.showerror(" ", 'Sum of ' + t + 'lower bounds > 100')
                return

            if sum(restr_dict[t+ox].upp.get() for ox in self.oxides if ox != 'KNaO') < 100 - delta:
                messagebox.showerror(" ", 'Sum of ' + t + 'upper bounds < 100')
                return

        if sum(restr_dict['ingredient_'+index].low.get() for index in self.ingredients) > 100 + delta:
            messagebox.showerror(" ", 'Sum of ingredient lower bounds > 100')
            return
            
        if sum(restr_dict['ingredient_'+index].upp.get() for index in self.ingredients) < 100 - delta:
            messagebox.showerror(" ", 'Sum of ingredient upper bounds < 100')
            return
         
        t0 = time.process_time()  

        with shelve.open("IngredientShelf") as ingredient_shelf:
            ingredient_dict = dict(ingredient_shelf)
            
        for index in ingredient_dict:
            ing = 'ingredient_'+index
            if index in self.ingredients:
                ing_low = 0.01*restr_dict[ing].low.get()
                ing_upp = 0.01*restr_dict[ing].upp.get()
            else:
                ing_low = 0
                ing_upp = 0
            prob.constraints[ing+'_lower'] = lp_var[ing] >= ing_low*lp_var['ingredient_total']      # ingredient lower bounds    
            prob.constraints[ing+'_upper'] = lp_var[ing] <= ing_upp*lp_var['ingredient_total']      # ingredient upper bounds


        t1 = time.process_time() # The next section takes a while, perhaps because the dictionary lp_var is long. May be better to split it.
         
        for ox in oxide_dict:          
            if ox in self.oxides:     
                prob.constraints[ox+'_umf_lower'] = lp_var['mole_'+ox] >= restr_dict['umf_'+ox].low.get()*lp_var['fluxes_total']   # oxide UMF lower bounds
                prob.constraints[ox+'_umf_upper'] = lp_var['mole_'+ox] <= restr_dict['umf_'+ox].upp.get()*lp_var['fluxes_total']   # oxide UMF upper bounds
                prob.constraints[ox+'_wt_%_lower'] = lp_var['mass_'+ox] >= 0.01*restr_dict['mass_perc_'+ox].low.get()*lp_var['ox_mass_total']    # oxide weight % lower bounds
                prob.constraints[ox+'_wt_%_upper'] = lp_var['mass_'+ox] <= 0.01*restr_dict['mass_perc_'+ox].upp.get()*lp_var['ox_mass_total']    # oxide weight % upper bounds
                prob.constraints[ox+'_mol_%_lower'] = lp_var['mole_'+ox] >= 0.01*restr_dict['mole_perc_'+ox].low.get()*lp_var['ox_mole_total']   # oxide mol % lower bounds
                prob.constraints[ox+'_mol_%_upper'] = lp_var['mole_'+ox] <= 0.01*restr_dict['mole_perc_'+ox].upp.get()*lp_var['ox_mole_total']   # oxide mol % upper bounds

            else:
                try:
                    del prob.constraints[ox+'_umf_lower']
                    del prob.constraints[ox+'_umf_upper']
                    del prob.constraints[ox+'_wt_%_lower']
                    del prob.constraints[ox+'_wt_%_upper']
                    del prob.constraints[ox+'_mol_%_lower']
                    del prob.constraints[ox+'_mol_%_upper']
                except:
                    pass
                 
##        if 'KNaO' in self.oxides:
##            prob += lp_var['KNaO_umf'] == lp_var['K2O_umf'] + lp_var['Na2O_umf']     
##            prob += lp_var['KNaO_wt_%'] == lp_var['K2O_wt_%'] + lp_var['Na2O_wt_%']  

        for index in other_dict:
            if index in self.other:  
                other_norm = eval(other_dict[index].normalization)               
                prob.constraints['other_'+index+'_lower'] = lp_var['other_'+index] >= restr_dict['other_'+index].low.get()*other_norm   # lower bound
                prob.constraints['other_'+index+'_upper'] = lp_var['other_'+index] <= restr_dict['other_'+index].upp.get()*other_norm   # upper bound
            else:
                try:
                    del prob.constraints['other_'+index+'_lower']
                    del prob.constraints['other_'+index+'_upper']
                except:
                    pass
             
        t5 = time.process_time()

# Finally, we are ready to calculate the upper and lower bounds imposed on all the variables
         
        for res in restrictions:    
            prob.constraints['normalization'] = eval(res.normalization) == 1  # Apply the normalization of the restriction in question
                                                                                   # Apparently this doesn't slow things down a whole lot
            for eps in [1,-1]:               # calculate lower and upper bounds.
                prob += eps*lp_var[res.objective_func], res.name
                prob.writeLP('constraints.lp')
                prob.solve(solver)
                if prob.status == 1:
                    res.calc_bounds[eps].config(text = ('%.'+str(res.dec_pt)+'f') % abs(eps*pulp.value(prob.objective)))
                                                        # we use abs above to avoid showing -0.0, but this could cause problems
                                                        # if we introduce other attributes that can be negative
                    #prob.writeLP('constraints.lp')
                else:
                    messagebox.showerror(" ", LpStatus[prob.status])
                    prob.writeLP('constraints.lp')
                    return

        t6 = time.process_time()
        #print(t1-t0, t5-t1, t6-t5)

    def calc_2d_projection(self, prob, lp_var, proj_frame):  # This is designed to be run when only the x and y variables have changed; it does not take
                                               # into account changes to upper and lower bounds. It should be possible to detect when the
                                               # user has clicked in one of the entry boxes since the last time calc_restrictions was run,
                                               # and give a warning in this case. Something like, if you have changed any bounds, click
                                               # 'Calculate restrictions' to apply them.
         
        #Need this for 2d projection
        tdp = 1

        if len(self.variables) == 2:
            x_var = restr_dict[self.variables['x']]
            y_var = restr_dict[self.variables['y']]
            if x_var.normalization == y_var.normalization:
                prob.constraints['normalization'] =  eval(x_var.normalization) == 1
                var_x = lp_var[x_var.objective_func]
                var_y = lp_var[y_var.objective_func]

            else:
                messagebox.showwarning(" ", '2-dim projection of restrictions with different normalizations not implemented yet')
                tdp = 0
        else:
            tdp = 0
             
        if tdp == 1:
            vertices = prob.two_dim_projection(var_x, var_y)            # defined in pulp2dim file
            #print(vertices)

     # Display 2-d projection of feasible region onto 'x'-'y' axes
        if tdp == 1:
            canvas = Canvas(proj_frame, width=450, height=450, bg = 'white', borderwidth = 1, relief = 'solid')
            canvas.create_polygon_plot(vertices)
            canvas.pack(expand='yes', fill='both')

# Define default recipe, in the case where class definitions have changed, or when things have just generally gotten messy
if initialize_recipe == 1:
    with shelve.open("RecipeShelf") as recipe_shelf:
        for index in recipe_shelf:
            del recipe_shelf[index]
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
            
        recipe_shelf['0'] = Recipe('Default Recipe Bounds', 0, [str(i) for i in range(3)], [], lb, ub, 'umf_')
