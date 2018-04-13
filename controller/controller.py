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
import sys
from os.path import abspath, dirname
from inspect import getsourcefile
sys.path.append(dirname(dirname(abspath(getsourcefile(lambda:0))))+'\model') # allows us to treat lipgloss like a built in package

from lipgloss.core_data import OxideData, CoreData, Oxide, Ingredient
from lipgloss.lp_recipe_problem import LpRecipeProblem
from lipgloss.recipes import Recipe, restr_keys

import model.serializers.recipeserializer
from model.model import Model
#from model.restrictions import Restriction

from view.main_window import MainWindow
from view.pretty_names import prettify, pretty_entry_type

import pulp
import tkinter as tk
from tkinter import ttk
from functools import partial
import shelve
import copy

class Restriction:
    'Oxide UMF, oxide % molar, oxide % weight, ingredient, SiO2:Al2O3 molar, LOI, cost, etc'
    display_frame = None   # Will be assigned later to be Controller.mw.restriction_sf.interior
    x_lab = None   # Will be assigned later to be Controller.mw.x_lab
    y_lab = None   # Will be assigned later to be Controller.mw.y_lab
    
    def __init__(self, index, name, objective_func, normalization, default_low, default_upp, dec_pt=1):

        self.index = index     # We will always have restr_dict[index] = Restriction(frame, index, ...)
        self.name = name
        self.objective_func = objective_func
        self.normalization = normalization
        self.default_low = default_low
        self.default_upp = default_upp
        self.dec_pt = dec_pt
        
        self.calc_bounds = {}   

        self.left_label_text = tk.StringVar()
        self.left_label_text.set('  '+prettify(self.name)+' : ')
        self.left_label = tk.Label(self.display_frame, textvariable=self.left_label_text)
        
        self.low = tk.DoubleVar()
        self.lower_bound = tk.Entry(self.display_frame, textvariable=self.low, width=5, fg='blue') #user lower bound
        self.low.set(self.default_low)

        self.upp = tk.DoubleVar()
        self.upper_bound = tk.Entry(self.display_frame, textvariable=self.upp, width=5, fg='blue') #user upper bound
        self.upp.set(self.default_upp)

        for eps in ['lower', 'upper']:
            self.calc_bounds[eps] = tk.Label(self.display_frame, bg='white', fg='red', width=5) #calculated lower and upper bounds
            self.calc_bounds[eps].config(text=' ')

        self.right_label_text = tk.StringVar()
        self.right_label_text.set(' : '+prettify(self.name)+'   ')
        self.right_label = tk.Label(self.display_frame, textvariable=self.right_label_text)

    def select(self, t):
        if t == 'x':
            self.left_label_text.set('* '+prettify(self.name)+' : ')
            self.x_lab.config(text='x variable: '+prettify(self.name)+pretty_entry_type(self.index[0:2]))
        elif t == 'y':
            self.right_label_text.set(' : '+prettify(self.name)+' *')
            self.y_lab.config(text='y variable: '+prettify(self.name)+pretty_entry_type(self.index[0:2]))
        else:
            print('Something\'s wrong')

    def deselect(self, t):
        if t == 'x':
            self.left_label_text.set('  '+prettify(self.name)+' : ')
            self.x_lab.config(text='x variable: Click right restriction name to select')
        elif t == 'y':
            self.right_label_text.set(' : '+prettify(self.name)+'  ')
            self.y_lab.config(text='y variable: Click left restriction name to select')
        else:
            print('Something\'s wrong')
                    
    def display(self, line):

        self.left_label.grid(row=line, column=0, sticky=tk.E)        # grid left restriction name
        
        self.lower_bound.grid(row=line, column=1)                 # grid lower bound entry box      
        self.upper_bound.grid(row=line, column=2)                 # grid upper bound entry box
    
        self.calc_bounds['lower'].grid(row=line, column=4)             # grid calculated lower bound box
        self.calc_bounds['upper'].grid(row=line, column=5)             # grid calculated upper bound box

        self.right_label.grid(row=line, column=6, sticky=tk.W)       # grid right restriction name

    def remove(self, recipe):
        for widget in [self.left_label, self.lower_bound, self.upper_bound, self.calc_bounds['lower'], self.calc_bounds['upper'],
                       self.right_label]:
            widget.grid_forget()    # remove widgets corresponding to that restriction
        self.low.set(self.default_low)
        self.upp.set(self.default_upp)
        for eps in ['lower', 'upper']:
            self.calc_bounds[eps].config(text='')
        v = dict(recipe.variables)
        for t in v:
            if self.index == v[t]:
                self.deselect(t)
                del recipe.variables[t]

    def hide(self):  # to be used with oxide options
        for widget in [self.left_label, self.lower_bound, self.upper_bound, self.calc_bounds['lower'], self.calc_bounds['upper'],
                       self.right_label]:
            widget.grid_forget()

    def display_calc_bounds(self, calc_value):
        for eps in [-1, 1]:
            self.calc_bounds[eps].config(text=('%.' + str(self.dec_pt) + 'f') % self.calc_value[eps])

def default_restriction_bounds(ox_dict, ing_dict, other_dict):
    """This will eventually be replaced by a function the reads the default restriction bounds from a JSON file"""
    restr_dict = {}
    # Create oxide restrictions:
    for ox in ox_dict:   
        def_upp = 1   # Default upper bound for oxide UMF.
        dp = 3
        if ox == 'SiO2':
            def_upp = 100
            dp = 2
        elif ox == 'Al2O3':
            def_upp = 10
        restr_dict['umf_'+ox] = Restriction('umf_'+ox, ox, 'mole_'+ox, "self.lp_var['fluxes_total']", 0, def_upp, dec_pt=dp)
        restr_dict['mass_perc_'+ox] = Restriction('mass_perc_'+ox, ox, 'mass_'+ox, "0.01*self.lp_var['ox_mass_total']", 0, 100, dec_pt=2) 
        restr_dict['mole_perc_'+ox] = Restriction('mole_perc_'+ox, ox, 'mole_'+ox, "0.01*self.lp_var['ox_mole_total']", 0, 100, dec_pt=2)

    # Create ingredient restrictions:
    for i in ing_dict:
        restr_dict['ingredient_'+i] = Restriction('ingredient_'+i, ing_dict[i].name, 'ingredient_'+i, "0.01*self.lp_var['ingredient_total']", 0, 100)

    # Create other restrictions:
    for index, ot in other_dict.items():
        restr_dict['other_'+index] = Restriction('other_'+index, ot.name, 'other_'+index, ot.normalization, ot.def_low, ot.def_upp, dec_pt=ot.dec_pt)

    return restr_dict

class Controller:
    def __init__(self):
        OxideData.set_default_oxides()
        self.cd = CoreData()
        self.cd.set_default_data()

        self.mod = Model(self.cd)
        self.mod.set_recipe_dict()
        self.mod.set_current_recipe('0')
        self.mod.set_order()
        
        self.mw = MainWindow()
        Restriction.display_frame = self.mw.restriction_sf.interior
        Restriction.x_lab = self.mw.x_lab
        Restriction.y_lab = self.mw.y_lab
        self.restr_dict = default_restriction_bounds(self.cd.oxide_dict, self.cd.ingredient_dict, self.cd.other_dict)
        
        for button, t in [(self.mw.unity_radio_button, 'umf_'), \
                          (self.mw.percent_wt_radio_button, 'mass_perc_'), \
                          (self.mw.percent_mol_radio_button, 'mole_perc_')]:
            button.config(command=partial(self.update_oxide_entry_type, t))

        self.lprp = LpRecipeProblem("Glaze recipe", pulp.LpMaximize, self.cd)
        
        self.mw.calc_button.config(command=self.calc_restr)
        
        # Create and grid ingredient selection buttons:
        #for r, i in enumerate(Ingredient.order):
        for r, i in enumerate(self.mod.order["ingredients"]):
            self.mw.ingredient_select_button[i] = ttk.Button(self.mw.vsf.interior, text=self.cd.ingredient_dict[i].name, width=20, \
                                                             command=partial(self.toggle_ingredient, i))
            self.mw.ingredient_select_button[i].grid(row=r)

        # Create and grid other selection buttons:
        for i, ot in self.cd.other_dict.items():
            self.mw.other_select_button[i] = ttk.Button(self.mw.other_selection_window, text=prettify(ot.name), width=18, \
                                                        command=partial(self.toggle_other, i))
            self.mw.other_select_button[i].grid(row=ot.pos+1)

        # Open default recipe.
        self.open_recipe('0')

    def calc_restr(self):
        for key in self.mod.current_recipe.restriction_keys:
            self.mod.current_recipe.lower_bounds[key] = self.restr_dict[key].low.get()
            self.mod.current_recipe.upper_bounds[key] = self.restr_dict[key].upp.get()
        calculated_bounds = self.lprp.calc_restrictions(self.mod.current_recipe, self.restr_dict)
        for key in self.mod.current_recipe.restriction_keys:
            res = self.restr_dict[key]
            for eps in ['lower', 'upper']:               # display calculated lower and upper bounds.
                res.calc_bounds[eps].config(text=('%.'+str(res.dec_pt)+'f') % no_neg_zero(calculated_bounds[eps][key]))

        self.mw.proj_canvas.delete("all")
        var = self.mod.current_recipe.variables
        if len(var) == 2:
            vertices = self.lprp.calc_2d_projection(self.mod.current_recipe, self.restr_dict)
            if self.restr_dict[var['x']].normalization == self.restr_dict[var['y']].normalization:
                scaling = 1
            else:
                x_pts = [p[0] for p in vertices]
                y_pts = [p[1] for p in vertices]
                delta_x = max(x_pts) - min(x_pts)
                delta_y = max(y_pts) - min(y_pts)
                if delta_y == 0 or delta_x == 0:
                    scaling = 1
                else:
                    scaling = delta_x / delta_y

            # Display 2-d projection of feasible region onto 'x'-'y' axes           
            self.mw.proj_canvas.create_polygon_plot(vertices, scaling)
        else:
            pass
        

    def open_recipe(self, index):   # to be used when opening a recipe, (or when ingredients have been updated?). Be careful.

        recipe_index = index

        for t, res in self.mod.current_recipe.variables.items():
            self.restr_dict[res].deselect(t)            # remove stars from old variables
        self.mod.current_recipe = copy.deepcopy(self.mod.recipe_dict[index])
        self.mod.current_recipe.update_oxides(self.cd, self.restr_dict)  # in case the oxide compositions have changed
        
        self.mw.recipe_name.set(self.mod.current_recipe.name)      # update the displayed recipe name

        for res in self.restr_dict.values():
            res.remove(self.mod.current_recipe)    # clear the entries from previous recipes, if opening a new recipe

        r_k = restr_keys(self.mod.current_recipe.oxides, self.mod.current_recipe.ingredients, self.mod.current_recipe.other)

        for i in r_k:
            try:
                self.restr_dict[i].low.set(self.mod.current_recipe.lower_bounds[i])
                self.restr_dict[i].upp.set(self.mod.current_recipe.upper_bounds[i])
            except:
                self.restr_dict[i].low.set(restr_dict[i].default_low)    # this is just for the case where the oxides have changed
                self.restr_dict[i].upp.set(restr_dict[i].default_upp)    # ditto

        for t, res in self.mod.current_recipe.variables.items():
            self.restr_dict[res].select(t)               # add stars to new variables
        
        et = self.mod.current_recipe.entry_type
        self.mw.entry_type.set(et)

        for ox in self.mod.current_recipe.oxides:
            self.restr_dict[et+ox].display(1 + self.cd.oxide_dict[ox].pos)

        ingredient_order = self.mod.order["ingredients"]
        for i in ingredient_order:
            if i in self.mod.current_recipe.ingredients:
                self.mw.ingredient_select_button[i].state(['pressed'])
                self.restr_dict['ingredient_'+i].display(101 + ingredient_order.index(i))
            else:
                self.mw.ingredient_select_button[i].state(['!pressed'])

        for ot in self.cd.other_dict:
            if ot in self.mod.current_recipe.other:
                self.mw.other_select_button[ot].state(['pressed'])
                self.restr_dict['other_'+ot].display(1001 + self.cd.other_dict[ot].pos)
            else:
                self.mw.other_select_button[ot].state(['!pressed'])

        try:
            r_s.destroy()
        except:
            pass
        #   Set the command for x and y variable selection boxes
        for restr in self.restr_dict.values():
            restr.left_label.bind("<Button-1>", partial(self.update_var, restr, 'x'))
            restr.right_label.bind("<Button-1>", partial(self.update_var, restr, 'y'))

        #bind_restrictions_to_recipe(self.mod.current_recipe, self.restr_dict)

    def toggle_ingredient(self, i):
        # Adds or removes ingredient_dict[i] to or from the current recipe, depending on whether it isn't or is an ingredient already.

        recipe = self.mod.current_recipe
        if i in recipe.ingredients:
            recipe.remove_ingredient(self.cd, i)
            self.mw.ingredient_select_button[i].state(['!pressed'])
            self.restr_dict['ingredient_'+i].remove(recipe)
            recipe.update_oxides(self.cd, self.restr_dict)

            # Remove the restrictions on the oxides no longer present:
            for ox in set(self.cd.ingredient_compositions[i]) - recipe.oxides:
                for et in ['umf_', 'mass_perc_', 'mole_perc_']:
                    self.restr_dict[et+ox].remove(recipe)

        else:
            recipe.add_ingredient(self.cd, i)
            self.mw.ingredient_select_button[i].state(['pressed'])
            self.restr_dict['ingredient_'+i].display(101 + self.mw.ingredient_order.index(i))
            for ox in self.cd.ingredient_compositions[i]:
                if ox not in recipe.oxides:  # i.e. if we're introducing a new oxide
                    for et in ['umf_', 'mass_perc_', 'mole_perc_']:
                        recipe.lower_bounds[et+ox] = self.restr_dict[et+ox].default_low
                        recipe.upper_bounds[et+ox] = self.restr_dict[et+ox].default_upp
            recipe.oxides = recipe.oxides.union(set(self.cd.ingredient_compositions[i]))    # update the available oxides
               
            et = self.mw.entry_type.get()
            for ox in recipe.oxides:
                self.restr_dict[et+ox].display(1 + self.cd.oxide_dict[ox].pos)
        #self.mod.current_recipe = recipe

    def toggle_other(self, i):
        # Adds or removes other_dict[index] to or from the current recipe, depending on whether it isn't or is an other restriction already.
        
        recipe = self.mod.current_recipe

        if i in recipe.other:
            recipe.remove_other(self.cd, i)
            self.mw.other_select_button[i].state(['!pressed'])
            self.restr_dict['other_'+i].remove(recipe)
            # TO DO: remove star if this was a variable

        else:
            recipe.add_other(self.cd, i)
            self.mw.other_select_button[i].state(['pressed'])         
            self.restr_dict['other_'+i].display(1001 + self.cd.other_dict[i].pos)
            self.mw.restriction_sf.canvas.yview_moveto(1)

    def update_var(self, restr, t, uh):     # t should be either 'x' or 'y'. Might be a better way of doing this
        if t in self.mod.current_recipe.variables:
            v = self.restr_dict[self.mod.current_recipe.variables[t]]
            if v == restr:
                del self.mod.current_recipe.variables[t]
                restr.deselect(t)
            else:
                self.mod.current_recipe.variables[t] = restr.index
                v.deselect(t)
                restr.select(t)      
        else:
            self.mod.current_recipe.variables[t] = restr.index
            restr.select(t)

    def update_oxide_entry_type(self, entry_type):
        self.mod.current_recipe.set('entry_type', entry_type)
        for et in ['umf_', 'mass_perc_', 'mole_perc_']:
            if et == entry_type:
                for ox in self.mod.current_recipe.oxides:
                    self.restr_dict[et+ox].display(1 + self.cd.oxide_dict[ox].pos)
            else:
                for ox in self.mod.current_recipe.oxides:
                    self.restr_dict[et+ox].hide()

def no_neg_zero(t):
    if t != 0:
        return t
    elif str(t)[0]=='-':
        return -t
    else:
        return t
    
