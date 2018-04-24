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
from tkinter import *   # Only used for error messages. Eliminate
import time
import copy
from .core_data import Observable, CoreData


##def get_ing_comp():                           # Redo. This function is defined in the main (gui) file
##    ingredient_compositions = {}
##    with shelve.open("./data/IngredientShelf") as ingredient_shelf:
##        for index in ingredient_shelf:
##            ingredient_compositions[index] = ingredient_shelf[index].oxide_comp
##    return ingredient_compositions

##def associated_oxides(ingredients):  #move this to CoreData ?
##
##    assoc_oxides = set()
##    for index in ingredients:
##        assoc_oxides = assoc_oxides.union(set(CoreData().ingredient_compositions[index]))  # update the available oxides. Probably not the most
##                                                                                                      # efficient way to do this
##    return assoc_oxides

def fluxes_subset(oxides):

    return [ox for ox in oxides if CoreData.oxide_dict[ox].flux == 1]

##    with shelve.open("./data/OxideShelf") as oxide_shelf:
##        fluxes = [ox for ox in oxides if oxide_shelf[ox].flux == 1]
##    return fluxes

def print_res_type(normalization):   # Used to display error message
    if normalization == "self.lp_var['fluxes_total']":
        prt = 'UMF '
    elif normalization == "self.lp_var['ox_mass_total']":
        prt = '% weight '
    elif normalization == "self.lp_var['ox_mole_total']":
        prt = '% molar '
    else:
        prt = ''
    return prt

def restr_keys(oxides, ingredients, other):
    return [t+ox for t in ['umf_', 'mass_perc_', 'mole_perc_'] for ox in oxides]+\
           ['ingredient_'+i for i in ingredients]+\
           ['other_'+ot for ot in other]

class Recipe(Observable):
    """This is actually a set of bounds on a collection of ingredients, together with bounds on the oxides present, \\
    and possibly bounds on other quantities"""

    def __init__(self, name, pos, oxides, ingredients, other, lower_bounds, upper_bounds, entry_type, variables = {}):
        
        Observable.__init__(self)
        self.name = name
        self.pos = pos   # position in list of recipes to choose
        self.ingredients = ingredients        # List of ingredient indices
        self.other = other                    # List of other indices
        self.oxides = oxides
        self.lower_bounds = lower_bounds      # A dictionary whose keys are the entries in self.restriction_keys
        self.upper_bounds = upper_bounds      # Ditto
        self.entry_type = entry_type          # Should be one of 'umf_', 'mass_perc_' or 'mole_perc_'
        self.variables = variables            # A dictionary whose keys are a subset of the set {'x','y'}, and whose values
                                              # are restriction keys.
        self.restriction_keys = None
        self.update_restriction_keys()
        #run checks to see if oxides are still the associated oxides, in case the ingredient compositions have changed

##    def update_bounds(self, restr_dict):       # To be used when saving a recipe.
##        self.lower_bounds = {}
##        self.upper_bounds = {}
##        
##        self.oxides = associated_oxides(self.ingredients)
##        
##        for t in ['umf_', 'mass_perc_', 'mole_perc_']:
##            for ox in self.oxides:
##                self.lower_bounds[t+ox] = restr_dict[t+ox].low.get()
##                self.upper_bounds[t+ox] = restr_dict[t+ox].upp.get()
##                
##        for i in self.ingredients:
##            self.lower_bounds['ingredient_'+i] = restr_dict['ingredient_'+i].low.get()
##            self.upper_bounds['ingredient_'+i] = restr_dict['ingredient_'+i].upp.get()
##            
##        for ot in self.other:
##            self.lower_bounds['other_'+ot] = restr_dict['other_'+ot].low.get()
##            self.upper_bounds['other_'+ot] = restr_dict['other_'+ot].upp.get()
##

    def update_restriction_keys(self):
        self.restriction_keys = restr_keys(self.oxides, self.ingredients, self.other)
        
    def fluxes(self):
        return fluxes_subset(self.oxides)

    def add_ingredient(self, core_data, i):
        if i in self.ingredients:
            print(core_data.ingredient_dict[i].name+' already occurs in recipe')
        else:
            self.ingredients.append(i) 
            self.oxides = self.oxides.union(set(core_data.ingredient_compositions[i]))
            self.update_restriction_keys()       # Could just make the changes by hand
            for key in self.restriction_keys:
                if key not in self.lower_bounds:
                    self.lower_bounds[key] = core_data.default_lower_bounds[key]
                    self.upper_bounds[key] = core_data.default_upper_bounds[key] 

    def remove_ingredient(self, core_data, i):
        if i in self.ingredients:
            self.ingredients.remove(i)
            self.oxides = core_data.associated_oxides(self.ingredients)
            old_res_keys = self.restriction_keys
            self.update_restriction_keys()
            for key in old_res_keys:
                if key not in self.restriction_keys:
                    del self.lower_bounds[key]
                    del self.upper_bounds[key]
            var = copy.copy(self.variables)
            for t in var:
                if (var[t] in old_res_keys) and (var[t] not in self.restriction_keys):
                    del self.variables[t]
        else:
            print(core_data.ingredient_dict[i].name+' not in recipe')

    def add_other(self, core_data, index):
        if index in self.other:
            print(core_data.other_dict[index].name+' already occurs in recipe')
        else:
            self.other.append(index)
            ot = 'other_'+index
            self.restriction_keys.append(ot)
            self.lower_bounds[ot] = core_data.default_lower_bounds[ot]
            self.upper_bounds[ot] = core_data.default_upper_bounds[ot] 

    def remove_other(self, core_data, index):
        if index in self.other:
            self.other.remove(index)
            ot = 'other_'+index
            self.restriction_keys.remove(ot)
            del self.lower_bounds[ot]
            del self.upper_bounds[ot]
            var = copy.copy(self.variables)
            for t in var:
                if var[t] == ot:
                    del self.variables[t]
        else:
            print(core_data.other_dict[index].name+' not in recipe')

    def update_bounds(self, core_data):      # To be used when ingredient compositions have changed. Could also be used in add_ingredient and remove_ingredient above
        for key in self.restriction_keys:
            if key not in self.lower_bounds:
                self.lower_bounds[key] = core_data.default_lower_bounds[key]
                self.upper_bounds[key] = core_data.default_upper_bounds[key]
        old_res_keys = copy.copy(list(self.lower_bounds.keys()))
        for key in old_res_keys:
            if key not in self.restriction_keys:
                del self.lower_bounds[key]
                del self.upper_bounds[key]    
        
    def update_oxides(self, core_data):   # to be run whenever the ingredients are changed
        old_oxides = copy.copy(self.oxides)
        ass_oxides = core_data.associated_oxides(self.ingredients)
        var = copy.copy(self.variables)
        for ox in self.oxides:
            if ox not in ass_oxides:
                for t in ['umf_', 'mass_perc_', 'mole_perc_']:
                    key = t + ox
                    del self.lower_bounds[key]
                    del self.upper_bounds[key]
                    # Replace the following with something that checks the type of the variables, and deletes those that are oxides in self.oxides but not in ass_oxides
                    for t in var:
                        if var[t] == key:
                            del self.variables[t]
##                    restr_dict[t+ox].remove(self)
##                    try:
##                        del self.lower_bounds[t+ox]
##                        restr_dict[t+ox].remove(self)
##                        print('deleted '+ox+' lower bound')
##                    except:
##                        pass
##                    try:
##                        del self.upper_bounds[t+ox]
##                    except:
##                        pass

        for ox in ass_oxides:
            if ox not in old_oxides:
                for t in ['umf_', 'mass_perc_', 'mole_perc_']:
                    key = t + ox
                    self.lower_bounds[key] = core_data.default_lower_bounds[key]
                    self.upper_bounds[key] = core_data.default_upper_bounds[key]
                #restr_dict[et+ox].display(1 + oxide_dict[ox].pos)

        self.oxides = ass_oxides
        self.update_restriction_keys()

    def update_core_data(self, core_data):
        pass
    
##    def update_variables(self, restr_keys):    # delete variables no longer present
##
##        var = copy.copy(self.variables)
##        for v in var:
##            if var[v] not in restr_keys:
##                del self.variables[v]
##
##    def calc_restrictions(self, prob, lp_var, restr_dict):    # Get rid of lp_var here, and replace lp_var below by prob.lp_var
##        
##        with shelve.open("./data/OxideShelf") as oxide_shelf:
##            oxide_dict = dict(oxide_shelf)
##
##        with shelve.open("./data/IngredientShelf") as ingredient_shelf:
##            ingredient_dict = dict(ingredient_shelf)
##
##        ingredient_compositions = get_ing_comp(ingredient_dict)
##        restrictions = [restr_dict[index] for index in restr_keys(self.oxides, self.ingredients, self.other)]
##         
##        # first, test for obvious errors
##
##        selected_fluxes = fluxes_subset(self.oxides)
##
##        if sum(oxide_dict[ox].flux for ox in self.oxides) == 0:
##            messagebox.showerror(" ", 'No flux! You have to give a flux.')
##            return
##    
##        # Run tests to see if the denominators of other restrictions are identically zero?
##
##        for res in restrictions:
##            if res.low.get() > res.upp.get():
##                messagebox.showerror(" ", 'Incompatible ' + print_res_type(res.normalization) + 'bounds on ' + prettify(res.name))
##                return
##
##        delta = 0.1**9
##
##        sum_UMF_low = sum(restr_dict['umf_'+ox].low.get() for ox in selected_fluxes)
##        if sum_UMF_low > 1 + delta:
##            messagebox.showerror(" ", 'The sum of the UMF flux lower bounds is '+str(sum_UMF_low)
##                                       +'. It should be at most 1. Decrease one of the lower bounds by '+str(sum_UMF_low-1)
##                                       +' or more.')     #will be a problem if they're all < sum_UMF_low-1))
##            return
##
##        sum_UMF_upp = sum(restr_dict['umf_'+ox].upp.get() for ox in selected_fluxes)            
##        if sum_UMF_upp < 1 - delta:
##            messagebox.showerror(" ", 'The sum of the UMF flux upper bounds is '+str(sum_UMF_upp)
##                                       +'. It should be at least 1. Increase one of the upper bounds by '+str(1-sum_UMF_low)
##                                       +' or more.')
##            return
##
##        for t in ['mass_perc_', 'mole_perc_']:
##            sum_t_low = sum(restr_dict[t+ox].low.get() for ox in self.oxides)
##            if sum_t_low > 100 + delta:
##                messagebox.showerror(" ", 'The sum of the ' + prettify(t) + ' lower bounds is '+str(sum_t_low)
##                                           +'. It should be at most 100. Decrease one of the lower bounds by '+str(sum_t_low-100)
##                                           +' or more.')     #will be a problem if they're all < sum_t_low-100)
##                return
##
##            sum_t_upp = sum(restr_dict[t+ox].upp.get() for ox in self.oxides)
##            if  sum_t_upp < 100 - delta:
##                messagebox.showerror(" ", 'The sum of the ' + prettify(t) + ' upper bounds is '+str(sum_t_upp)
##                                           +'. It should be at least 100. Increase one of the upper bounds by '+str(100-sum_t_upp)
##                                           +' or more.') 
##                return
##            
##        sum_ing_low = sum(restr_dict['ingredient_'+index].low.get() for index in self.ingredients)
##        if sum_ing_low > 100 + delta:
##            messagebox.showerror(" ", 'The sum of the ingredient lower bounds is '+str(sum_ing_low)
##                                      +'. It should be at most 100. Decrease one of the lower bounds by '+str(sum_ing_low-100)
##                                      +' or more.')     #will be a problem if they're all < sum_ing_low-100)
##            return
##            
##        sum_ing_upp = sum(restr_dict['ingredient_'+index].upp.get() for index in self.ingredients)
##        if sum_ing_upp < 100 - delta:
##            messagebox.showerror(" ", 'The sum of the ingredient upper bounds is '+str(sum_ing_upp)
##                                       +'. It should be at least 100. Increase one of the upper bounds by '+str(100-sum_ing_upp)
##                                       +' or more.')  
##            return
##         
##        t0 = time.process_time()  
##
##        with shelve.open("./data/IngredientShelf") as ingredient_shelf:
##            ingredient_dict = dict(ingredient_shelf)               # Might be better to include ingredient_dict as a parameter
##                                                                   # in calc_restrictions.
##            
##        for index in ingredient_dict:
##            ing = 'ingredient_'+index
##            if index in self.ingredients:
##                ing_low = 0.01*restr_dict[ing].low.get()
##                ing_upp = 0.01*restr_dict[ing].upp.get()
##            else:
##                ing_low = 0
##                ing_upp = 0
##            prob.constraints[ing+'_lower'] = lp_var[ing] >= ing_low*lp_var['ingredient_total']      # ingredient lower bounds    
##            prob.constraints[ing+'_upper'] = lp_var[ing] <= ing_upp*lp_var['ingredient_total']      # ingredient upper bounds
##
##
##        t1 = time.process_time()      # The next section takes a while, perhaps because the dictionary lp_var is long.
##                                      # May be better to split it.
##         
##        for ox in oxide_dict:          
##            if ox in self.oxides:     
##                prob.constraints[ox+'_umf_lower'] = lp_var['mole_'+ox] >= restr_dict['umf_'+ox].low.get()*lp_var['fluxes_total']   # oxide UMF lower bounds
##                prob.constraints[ox+'_umf_upper'] = lp_var['mole_'+ox] <= restr_dict['umf_'+ox].upp.get()*lp_var['fluxes_total']   # oxide UMF upper bounds
##                prob.constraints[ox+'_wt_%_lower'] = lp_var['mass_'+ox] >= 0.01*restr_dict['mass_perc_'+ox].low.get()*lp_var['ox_mass_total']    # oxide weight % lower bounds
##                prob.constraints[ox+'_wt_%_upper'] = lp_var['mass_'+ox] <= 0.01*restr_dict['mass_perc_'+ox].upp.get()*lp_var['ox_mass_total']    # oxide weight % upper bounds
##                prob.constraints[ox+'_mol_%_lower'] = lp_var['mole_'+ox] >= 0.01*restr_dict['mole_perc_'+ox].low.get()*lp_var['ox_mole_total']   # oxide mol % lower bounds
##                prob.constraints[ox+'_mol_%_upper'] = lp_var['mole_'+ox] <= 0.01*restr_dict['mole_perc_'+ox].upp.get()*lp_var['ox_mole_total']   # oxide mol % upper bounds
##
##            else:
##                try:
##                    del prob.constraints[ox+'_umf_lower']
##                    del prob.constraints[ox+'_umf_upper']
##                    del prob.constraints[ox+'_wt_%_lower']
##                    del prob.constraints[ox+'_wt_%_upper']
##                    del prob.constraints[ox+'_mol_%_lower']
##                    del prob.constraints[ox+'_mol_%_upper']
##                except:
##                    pass
##                 
####        if 'KNaO' in self.oxides:
####            prob += lp_var['KNaO_umf'] == lp_var['K2O_umf'] + lp_var['Na2O_umf']     
####            prob += lp_var['KNaO_wt_%'] == lp_var['K2O_wt_%'] + lp_var['Na2O_wt_%']  
##
##        for index in other_dict:
##            if index in self.other:  
##                other_norm = eval(other_dict[index].normalization)               # Change to LpAffine thingy?
##                prob.constraints['other_'+index+'_lower'] = lp_var['other_'+index] >= restr_dict['other_'+index].low.get()*other_norm   # lower bound
##                prob.constraints['other_'+index+'_upper'] = lp_var['other_'+index] <= restr_dict['other_'+index].upp.get()*other_norm   # upper bound
##            else:
##                try:
##                    del prob.constraints['other_'+index+'_lower']
##                    del prob.constraints['other_'+index+'_upper']
##                except:
##                    pass
##             
##        t5 = time.process_time()
##
### Finally, we're ready to calculate the upper and lower bounds imposed on all the variables
##         
##        for res in restrictions:    
##            prob.constraints['normalization'] = eval(res.normalization) == 1  # Apply the normalization of the restriction in question
##                                                                                   # Apparently this doesn't slow things down a whole lot
##            for eps in [1,-1]:               # calculate lower and upper bounds.
##                prob += eps*lp_var[res.objective_func], res.name
##                prob.writeLP('constraints.lp')
##                prob.solve(solver)
##                if prob.status == 1:
##                    res.calc_bounds[eps].config(text = ('%.'+str(res.dec_pt)+'f') % abs(eps*pulp.value(prob.objective)))
##                                                        # we use abs above to avoid showing -0.0, but this could cause problems
##                                                        # if we introduce other attributes that can be negative
##                    #prob.writeLP('constraints.lp')
##                else:
##                    messagebox.showerror(" ", LpStatus[prob.status])
##                    prob.writeLP('constraints.lp')
##                    return
##
##        t6 = time.process_time()
##        #print(t1-t0, t5-t1, t6-t5)
##
##    def calc_2d_projection(self, prob, lp_var, proj_canvas):  # This is designed to be run when only the x and y variables have changed; it does not take
##                                               # into account changes to upper and lower bounds. It should be possible to detect when the
##                                               # user has clicked in one of the entry boxes since the last time calc_restrictions was run,
##                                               # and give a warning in this case. Something like, if you have changed any bounds, click
##                                               # 'Calculate restrictions' to apply them.
##
##        if len(self.variables) == 2:
##            x_var = restr_dict[self.variables['x']]
##            y_var = restr_dict[self.variables['y']]
##            x_norm = x_var.normalization
##            y_norm = y_var.normalization
##
##            vertices = prob.two_dim_projection(lp_var, lp_var[x_var.objective_func], lp_var[y_var.objective_func], x_norm, y_norm)   # defined in pulp2dim file
##
##            if x_norm == y_norm:
##                scaling = 1
##            else:
##                x_pts = [p[0] for p in vertices]
##                y_pts = [p[1] for p in vertices]
##                delta_x = max(x_pts) - min(x_pts)
##                delta_y = max(y_pts) - min(y_pts)
##                if delta_y == 0 or delta_x == 0:
##                    scaling = 1
##                else:
##                    scaling = delta_x / delta_y
##
##
##            # Display 2-d projection of feasible region onto 'x'-'y' axes
##            proj_canvas.delete("all")
##            proj_canvas.create_polygon_plot(vertices, scaling)
##
##        else:
##            pass

    def convert_to_recipe(self):
        # Assumes calc_restrictions has been run
        converted_recipe={}
        s = 0   # sum of averages
        for index in self.ingredients:
            cb = restr_dict['ingredient_'+index].calc_bounds
            avg = (float(cb[1]['text']) + float(cb[-1]['text'])) / 2    
            converted_recipe[index] =  avg
            s += avg
        s *= 0.01
        for index in self.ingredients:
            converted_recipe[index] /= s    # rescale so that percentages add up to 100.
        return converted_recipe     # may want to round to one decimal place.

##    @staticmethod
##    def get_default_recipe():
##        """Define default recipe, in the case where class definitions have changed, or when things have just generally gotten messy"""
##        lb = {} 
##        ub = {} 
##        
##        for ox in ['SiO2', 'Al2O3', 'B2O3', 'MgO', 'CaO', 'Na2O', 'K2O', 'ZnO', 'Fe2O3', 'TiO2', 'P2O5']:
##            for t in ['umf_', 'mass_perc_', 'mole_perc_']:
##                lb[t+ox] = 0
##                ub[t+ox] = 100
##        ub['umf_Al2O3'] = 10
##        for ox in ['B2O3', 'MgO', 'CaO', 'Na2O', 'K2O', 'ZnO', 'Fe2O3', 'TiO2', 'P2O5']:
##            ub['umf_'+ox] = 1
##            
##        for i in range(15):
##            lb['ingredient_'+str(i)] = 0
##            ub['ingredient_'+str(i)] = 100
##            
##        return Recipe('Default Recipe Bounds', 0, [str(i) for i in range(3)], [], lb, ub, 'umf_')
##
