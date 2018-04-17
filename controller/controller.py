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
from lipgloss.restrictions import Restriction

import model.serializers.recipeserializer
from model.model import Model
#from model.restrictions import Restriction

from view.main_window import MainWindow, DisplayRestriction, RecipeMenu
from view.pretty_names import prettify, pretty_entry_type

import pulp
import tkinter as tk
from tkinter import ttk
from functools import partial
import shelve
import copy

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

        self.lprp = LpRecipeProblem("Glaze recipe", pulp.LpMaximize, self.cd)
        
        self.mod = Model()
        #self.mod.set_current_recipe('0')
        
        self.mw = MainWindow()
  
        for button, t in [(self.mw.unity_radio_button, 'umf_'), \
                          (self.mw.percent_wt_radio_button, 'mass_perc_'), \
                          (self.mw.percent_mol_radio_button, 'mole_perc_')]:
            button.config(command=partial(self.update_oxide_entry_type, t))

        self.mw.file_menu.add_command(label="Recipes", command=self.open_recipe_menu)
        self.mw.file_menu.add_command(label="Save", command=self.save_recipe)
        self.mw.file_menu.add_command(label="Save as new recipe", command=self.save_new_recipe)
        
        
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

        #Create Restriction and DisplayRestriction dictionaries
        self.restr_dict = default_restriction_bounds(self.cd.oxide_dict, self.cd.ingredient_dict, self.cd.other_dict)

        self.display_restr_dict = {}      
        for key in self.cd.restr_keys():
            self.display_restr_dict[key] = DisplayRestriction(self.mw.restriction_sf.interior, self.mw.x_lab, self.mw.y_lab, \
                                                              key, self.restr_dict[key].name, self.restr_dict[key].default_low, self.restr_dict[key].default_upp)

        # Open default recipe.
        self.open_recipe('0')

    def calc_restr(self):
        self.get_bounds()
        calculated_bounds = self.lprp.calc_restrictions(self.mod.current_recipe, self.restr_dict)
        for key in self.mod.current_recipe.restriction_keys:
            res = self.display_restr_dict[key]
            dp =  self.restr_dict[key].dec_pt
            for eps in ['lower', 'upper']:               # display calculated lower and upper bounds.
                res.calc_bounds[eps].config(text=('%.'+str(dp)+'f') % no_neg_zero(calculated_bounds[eps][key]))

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

    def get_bounds(self):
        for key in self.mod.current_recipe.restriction_keys:
            self.mod.current_recipe.lower_bounds[key] = self.display_restr_dict[key].low.get()
            self.mod.current_recipe.upper_bounds[key] = self.display_restr_dict[key].upp.get()  

    def open_recipe(self, index):   # to be used when opening a recipe, (or when ingredients have been updated?). Be careful.

        self.mod.recipe_index = index

        for t, res in self.mod.current_recipe.variables.items():
            self.display_restr_dict[res].deselect(t)            # remove stars from old variables
        self.mod.current_recipe = copy.deepcopy(self.mod.recipe_dict[index])
        self.mod.current_recipe.update_oxides(self.cd, self.restr_dict)  # in case the oxide compositions have changed
        
        self.mw.recipe_name.set(self.mod.current_recipe.name)      # update the displayed recipe name

        for res in self.display_restr_dict.values():
            res.remove(self.mod.current_recipe)    # clear the entries from previous recipes, if opening a new recipe

        r_k = restr_keys(self.mod.current_recipe.oxides, self.mod.current_recipe.ingredients, self.mod.current_recipe.other)

        for i in r_k:
            try:
                self.display_restr_dict[i].low.set(self.mod.current_recipe.lower_bounds[i])
                self.display_restr_dict[i].upp.set(self.mod.current_recipe.upper_bounds[i])
            except:
                self.display_restr_dict[i].low.set(restr_dict[i].default_low)    # this is just for the case where the oxides have changed
                self.display_restr_dict[i].upp.set(restr_dict[i].default_upp)    # ditto

        for t, res in self.mod.current_recipe.variables.items():
            self.display_restr_dict[res].select(t)               # add stars to new variables
        
        et = self.mod.current_recipe.entry_type
        self.mw.entry_type.set(et)

        for ox in self.mod.current_recipe.oxides:
            self.display_restr_dict[et+ox].display(1 + self.cd.oxide_dict[ox].pos)

        ingredient_order = self.mod.order["ingredients"]
        for i in ingredient_order:
            if i in self.mod.current_recipe.ingredients:
                self.mw.ingredient_select_button[i].state(['pressed'])
                self.display_restr_dict['ingredient_'+i].display(101 + ingredient_order.index(i))
            else:
                self.mw.ingredient_select_button[i].state(['!pressed'])

        for ot in self.cd.other_dict:
            if ot in self.mod.current_recipe.other:
                self.mw.other_select_button[ot].state(['pressed'])
                self.display_restr_dict['other_'+ot].display(1001 + self.cd.other_dict[ot].pos)
            else:
                self.mw.other_select_button[ot].state(['!pressed'])

        try:
            self.mw.recipe_menu.recipe_selector.destroy()
        except:
            pass
        # Set the command for x and y variable selection boxes
        for key, restr in self.display_restr_dict.items():
            restr.left_label.bind("<Button-1>", partial(self.update_var, key, 'x'))
            restr.right_label.bind("<Button-1>", partial(self.update_var, key, 'y'))

        #bind_restrictions_to_recipe(self.mod.current_recipe, self.restr_dict)

    def open_recipe_menu(self):

        try:
            self.mw.recipe_menu.recipe_selector.destroy() # destroy the recipe selection window
        except:
            pass
            
        self.mw.recipe_menu = RecipeMenu()
        for index in self.mod.recipe_dict:
            self.display_recipe(index) 
        self.mw.recipe_menu.r_s_scrollframe.interior.focus_force()

    def display_recipe(self, index):

        recipe = self.mod.recipe_dict[index]
        name_button =  ttk.Button(master=self.mw.recipe_menu.r_s_scrollframe.interior, text=recipe.name, width=30,
                                 command=partial(self.open_recipe, index))
        name_button.grid(row=recipe.pos+1, column=0)
        if index != '0': 
            # only allow deletion of user recipes.  index '0' denotes the default recipe bounds
            delete_button = ttk.Button(master=self.mw.recipe_menu.r_s_scrollframe.interior, text="X", width=5,
                                      command=partial(self.delete_recipe, index))
            delete_button.grid(row=recipe.pos+1, column=1)

    def save_recipe(self):
        """Save a recipe to the global recipe_dict, then update the JSON data file"""
        self.mod.current_recipe.name = self.mw.recipe_name.get()
        self.get_bounds()
        self.mod.current_recipe.update_bounds(self.restr_dict)   # Do we need this?
        self.mod.current_recipe.entry_type = self.mw.entry_type.get()
        self.mod.recipe_dict[self.mod.recipe_index] = copy.deepcopy(self.mod.current_recipe)
        self.mod.json_write_recipes()

    def save_new_recipe(self):
        """Save a new recipe with new ID to the self.mod.recipe_dict, then update the JSON data file"""
        self.get_bounds()
        self.mod.current_recipe.update_bounds(self.restr_dict)   # Do we need this?
        self.mod.current_recipe.entry_type = self.mw.entry_type.get()
        recipe_index = str(int(max(self.mod.recipe_dict, key=int)) + 1)
        self.mod.recipe_index = recipe_index
        self.mod.current_recipe.name = 'Recipe Bounds ' + recipe_index
        self.mod.current_recipe.pos = int(recipe_index)
        self.mod.recipe_dict[recipe_index] = copy.deepcopy(self.mod.current_recipe)
        self.mw.recipe_name.set(self.mod.current_recipe.name)
        self.mod.json_write_recipes()

    def delete_recipe(self, index):
        """Delete the recipe from the recipe_dict, then write out the updated recipe_dict to JSON file."""
        if index != '0': # don't allow a user to delete the default 
            del self.mod.recipe_dict[index]
            self.mod.json_write_recipes()
        if index == self.mod.recipe_index:
            # We have deleted the current recipe.  Go to default recipe
            self.open_recipe('0')
        try:
            self.mw.recipe_menu.recipe_selector.destroy() # destroy the recipe selection window
        except:
            pass

    def toggle_ingredient(self, i):
        # Adds or removes ingredient_dict[i] to or from the current recipe, depending on whether it isn't or is an ingredient already.

        recipe = self.mod.current_recipe
        if i in recipe.ingredients:
            recipe.remove_ingredient(self.cd, i)
            self.mw.ingredient_select_button[i].state(['!pressed'])
            self.display_restr_dict['ingredient_'+i].remove(recipe)
            recipe.update_oxides(self.cd, self.restr_dict)

            # Remove the restrictions on the oxides no longer present:
            for ox in set(self.cd.ingredient_compositions[i]) - recipe.oxides:
                for et in ['umf_', 'mass_perc_', 'mole_perc_']:
                    self.display_restr_dict[et+ox].remove(recipe)

        else:
            recipe.add_ingredient(self.cd, i)
            self.mw.ingredient_select_button[i].state(['pressed'])
            self.display_restr_dict['ingredient_'+i].display(101 + self.mw.ingredient_order.index(i))
            for ox in self.cd.ingredient_compositions[i]:
                if ox not in recipe.oxides:  # i.e. if we're introducing a new oxide
                    for et in ['umf_', 'mass_perc_', 'mole_perc_']:
                        recipe.lower_bounds[et+ox] = self.restr_dict[et+ox].default_low
                        recipe.upper_bounds[et+ox] = self.restr_dict[et+ox].default_upp
            recipe.oxides = recipe.oxides.union(set(self.cd.ingredient_compositions[i]))    # update the available oxides
               
            et = self.mw.entry_type.get()
            for ox in recipe.oxides:
                self.display_restr_dict[et+ox].display(1 + self.cd.oxide_dict[ox].pos)
        #self.mod.current_recipe = recipe

    def toggle_other(self, i):
        # Adds or removes other_dict[index] to or from the current recipe, depending on whether it isn't or is an other restriction already.
        
        recipe = self.mod.current_recipe

        if i in recipe.other:
            recipe.remove_other(self.cd, i)
            self.mw.other_select_button[i].state(['!pressed'])
            self.display_restr_dict['other_'+i].remove(recipe)
            # TO DO: remove star if this was a variable

        else:
            recipe.add_other(self.cd, i)
            self.mw.other_select_button[i].state(['pressed'])         
            self.display_restr_dict['other_'+i].display(1001 + self.cd.other_dict[i].pos)
            self.mw.restriction_sf.canvas.yview_moveto(1)

    def update_var(self, key, t, uh):     # t should be either 'x' or 'y'. Might be a better way of doing this
        restr = self.display_restr_dict[key]
        if t in self.mod.current_recipe.variables:
            v = self.mod.current_recipe.variables[t]
            if v == key:
                del self.mod.current_recipe.variables[t]
                self.display_restr_dict[key].deselect(t)
            else:
                self.mod.current_recipe.variables[t] = restr.index
                self.display_restr_dict[v].deselect(t)
                self.display_restr_dict[key].select(t)      
        else:
            self.mod.current_recipe.variables[t] = restr.index
            restr.select(t)

    def update_oxide_entry_type(self, entry_type):
        self.mod.current_recipe.set('entry_type', entry_type)
        for et in ['umf_', 'mass_perc_', 'mole_perc_']:
            if et == entry_type:
                for ox in self.mod.current_recipe.oxides:
                    self.display_restr_dict[et+ox].display(1 + self.cd.oxide_dict[ox].pos)
            else:
                for ox in self.mod.current_recipe.oxides:
                    self.display_restr_dict[et+ox].hide()

def no_neg_zero(t):
    if t != 0:
        return t
    elif str(t)[0]=='-':
        return -t
    else:
        return t
    
