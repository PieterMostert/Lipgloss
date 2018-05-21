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
from os import path
from inspect import getsourcefile
model_path = path.join(dirname(dirname(abspath(getsourcefile(lambda:0)))), 'model')
#print('model_path = ' + model_path)
sys.path.append(model_path) # Allows us to import lipgloss like a built-in package.

try:    # This should work if lipgloss can be imported like a built-in package
    from lipgloss.core_data import OxideData, CoreData, Oxide, Ingredient, Other
    from lipgloss.lp_recipe_problem import LpRecipeProblem
    from lipgloss.recipes import Recipe, restr_keys
except:
    from model.lipgloss.core_data import OxideData, CoreData, Oxide, Ingredient, Other
    from model.lipgloss.lp_recipe_problem import LpRecipeProblem
    from model.lipgloss.recipes import Recipe, restr_keys

from model.model import Model

from view.main_window import MainWindow, RecipeMenu
from view.display_restriction import DisplayRestriction
from view.ingredient_editor import DisplayIngredient, IngredientEditor
from view.other_restriction_editor import DisplayOtherRestriction, OtherRestrictionEditor
from view.pretty_names import prettify, pretty_entry_type

import pulp
import tkinter as tk
from tkinter import ttk
from functools import partial
import copy
from numbers import Number
import ast
import time

class Controller:
    def __init__(self):
        #OxideData.set_default_oxides()   # Replace by function that sets data saved by user
        self.mod = Model()
        #self.cd = self.mod
        self.lprp = LpRecipeProblem("Glaze recipe", pulp.LpMaximize, self.mod)
        
        self.mw = MainWindow()
  
        for button, t in [(self.mw.unity_radio_button, 'umf_'), \
                          (self.mw.percent_wt_radio_button, 'mass_perc_'), \
                          (self.mw.percent_mol_radio_button, 'mole_perc_')]:
            button.config(command=partial(self.update_oxide_entry_type, t))

        self.mw.file_menu.add_command(label="Recipes", command=self.open_recipe_menu)
        self.mw.file_menu.add_command(label="Save", command=self.save_recipe)
        self.mw.file_menu.add_command(label="Save as new recipe", command=self.save_new_recipe)

        #self.mw.options_menu.add_command(label="Edit Oxides", command=None)
        self.mw.options_menu.add_command(label="Edit Ingredients", command=self.open_ingredient_editor)
        self.mw.options_menu.add_command(label="Edit Other Restrictions", command=self.open_other_restriction_editor)
        #self.mw.options_menu.add_command(label="Restriction Settings", command=self.open_ingredient_editor)
        
        self.mw.calc_button.config(command=self.calc_restr)
        
        # Create and grid ingredient selection buttons:
        for r, i in enumerate(self.mod.order["ingredients"]):
            self.mw.ingredient_select_button[i] = ttk.Button(self.mw.ingredient_vsf.interior, text=self.mod.ingredient_dict[i].name, \
                                                             width=20, command=partial(self.toggle_ingredient, i))
            self.mw.ingredient_select_button[i].grid(row=r)

        # Create and grid other selection buttons:
        for r, j in enumerate(self.mod.order["other"]):
            self.mw.other_select_button[j] = ttk.Button(self.mw.other_vsf.interior, text=prettify(self.mod.other_dict[j].name), \
                                                        width=20, command=partial(self.toggle_other, j))
            self.mw.other_select_button[j].grid(row=r+1)

        # Create DisplayRestriction dictionary
        self.display_restr_dict = {}      
        for key in self.mod.restr_keys():
            self.display_restr_dict[key] = DisplayRestriction(self.mw.restriction_sf.interior, self.mw.x_lab, self.mw.y_lab, \
                                                              key, self.mod.restr_dict[key].name, self.mod.restr_dict[key].default_low, self.mod.restr_dict[key].default_upp)

        # Open default recipe.
        self.open_recipe('0')

    def calc_restr(self):
        t0 = time.process_time()
        self.get_bounds()
        calculated_bounds = self.lprp.calc_restrictions(self.mod.current_recipe, self.mod.restr_dict)
        for key in self.mod.current_recipe.restriction_keys:
            res = self.display_restr_dict[key]
            dp =  self.mod.restr_dict[key].dec_pt
            for eps in ['lower', 'upper']:               # display calculated lower and upper bounds.
                res.calc_bounds[eps].config(text=('%.'+str(dp)+'f') % no_neg_zero(calculated_bounds[eps][key]))

        self.mw.proj_canvas.delete("all")
        var = self.mod.current_recipe.variables
        if len(var) == 2:
            vertices = self.lprp.calc_2d_projection(self.mod.current_recipe, self.mod.restr_dict)
            if self.mod.restr_dict[var['x']].normalization == self.mod.restr_dict[var['y']].normalization:
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
        self.mw.root.lift()    # Doesn't work, and I don't know why
        #self.mw.root.attributes('-topmost', 1)
        #self.mw.root.attributes('-topmost', 0)
        try:
            self.ing_editor.toplevel.lower()
        except:
            pass
        t1 = time.process_time()
        #print(t1 - t0)

    def get_bounds(self):
        for key in self.mod.current_recipe.restriction_keys:
            self.mod.current_recipe.lower_bounds[key] = self.display_restr_dict[key].low.get()
            self.mod.current_recipe.upper_bounds[key] = self.display_restr_dict[key].upp.get()

    def open_recipe_menu(self):
        """Opens a pop-up window that lets users select which recipes bounds to display, or delete existing recipe bounds (except the default)"""
        try:
            self.mw.recipe_menu.recipe_selector.lift()
        except:
            self.mw.recipe_menu = RecipeMenu()
            for i in self.mod.recipe_dict:
                self.display_recipe(i) 
            self.mw.recipe_menu.r_s_scrollframe.interior.focus_force()

    def display_recipe(self, index):
        """Displays recipe name and delete button in recipe menu"""
        recipe = self.mod.recipe_dict[index]
        self.mw.recipe_menu.name_buttons[index] =  ttk.Button(master=self.mw.recipe_menu.r_s_scrollframe.interior, text=recipe.name, width=30,
                                 command=partial(self.open_recipe, index))
        self.mw.recipe_menu.name_buttons[index].grid(row=recipe.pos+1, column=0)
        if index != '0': 
            # Only allow deletion of user recipes.  Index '0' denotes the default recipe bounds
            self.mw.recipe_menu.delete_buttons[index] = ttk.Button(master=self.mw.recipe_menu.r_s_scrollframe.interior, text="X", width=5,
                                      command=partial(self.delete_recipe, index))
            self.mw.recipe_menu.delete_buttons[index].grid(row=recipe.pos+1, column=1)

    def open_recipe(self, index):   # To be used when opening a recipe, (or when ingredients have been updated?). Be careful.

        for t, res in self.mod.current_recipe.variables.items():
            self.display_restr_dict[res].deselect(t)            # Remove stars from old variables
            
        for res in self.display_restr_dict.values():
            res.remove(self.mod.current_recipe.variables)    # Clear the entries from previous recipes, if opening a new recipe

        self.mod.set_current_recipe(index)
                
        self.mw.recipe_name.set(self.mod.current_recipe.name)      # update the displayed recipe name

        r_k = self.mod.current_recipe.restriction_keys
        for i in r_k:
            try:
                self.display_restr_dict[i].low.set(self.mod.current_recipe.lower_bounds[i])
                self.display_restr_dict[i].upp.set(self.mod.current_recipe.upper_bounds[i])
            except:
                self.display_restr_dict[i].low.set(self.mod.restr_dict[i].default_low)    # this is just for the case where the oxides have changed
                self.display_restr_dict[i].upp.set(self.mod.restr_dict[i].default_upp)    # ditto

        for t, res in self.mod.current_recipe.variables.items():
            self.display_restr_dict[res].select(t)               # add stars to new variables
        
        et = self.mod.current_recipe.entry_type
        self.mw.entry_type.set(et)

        oxide_order = self.mod.order["oxides"]
        for ox in oxide_order:
            if ox in self.mod.current_recipe.oxides:
                self.display_restr_dict[et+ox].display(1 + oxide_order.index(ox))

        ingredient_order = self.mod.order["ingredients"]
        for i in ingredient_order:
            if i in self.mod.current_recipe.ingredients:
                self.mw.ingredient_select_button[i].state(['pressed'])
                self.display_restr_dict['ingredient_'+i].display(101 + ingredient_order.index(i))
            else:
                self.mw.ingredient_select_button[i].state(['!pressed'])

        other_order = self.mod.order["other"]
        for ot in other_order:
            if ot in self.mod.current_recipe.other:
                self.mw.other_select_button[ot].state(['pressed'])
                self.display_restr_dict['other_'+ot].display(1001 + other_order.index(ot))
            else:
                self.mw.other_select_button[ot].state(['!pressed'])
        
        # Set the command for x and y variable selection boxes
        for key, restr in self.display_restr_dict.items():
            restr.left_label.bind("<Button-1>", partial(self.update_var, key, 'x'))
            restr.right_label.bind("<Button-1>", partial(self.update_var, key, 'y'))

        try:
            self.mw.recipe_menu.recipe_selector.destroy()
        except:   # The recipe selector won't be open when the controller opens the default recipe on start-up
            pass  

    def save_recipe(self):
        """Save a recipe to the Model's recipe_dict, then update the JSON data file"""
        self.mod.current_recipe.name = self.mw.recipe_name.get()
        self.mod.current_recipe.entry_type = self.mw.entry_type.get()
        self.get_bounds()
        self.mod.current_recipe.update_bounds(self.mod.restr_dict)   # Do we need this?        
        self.mod.save_current_recipe()

    def save_new_recipe(self):
        """Save a new recipe with new ID to the self.mod.recipe_dict, then update the JSON data file"""
        self.get_bounds()
        self.mod.current_recipe.update_bounds(self.mod.restr_dict)   # Do we need this?
        self.mod.current_recipe.entry_type = self.mw.entry_type.get()
        self.mod.save_new_recipe()
        self.mw.recipe_name.set(self.mod.current_recipe.name)  # Sets the name to Recipe Bounds n, for a natural number n

    def delete_recipe(self, i):
        """Delete the recipe from the recipe_dict, then write out the updated recipe_dict to JSON file."""
        self.mod.delete_recipe(i)
        if i == self.mod.recipe_index:
            # We have deleted the current recipe.  Go to default recipe
            self.open_recipe('0')
        self.mw.recipe_menu.delete_recipe(i)

    def open_ingredient_editor(self):
        """Opens a window that lets users edit ingredients"""
        try:
            self.ing_editor.toplevel.lift() # lift the recipe selector, if it already exists
        except:
            self.ing_editor = IngredientEditor(self.mod, self.mod.order, self.reorder_ingredients)
            self.ing_editor.new_ingr_button.config(command=self.new_ingredient)
            self.ing_editor.update_button.config(command=self.update_ingredient_dict)
            for i in self.mod.order['ingredients']:
                self.ing_editor.display_ingredients[i].delete_button.config(command=partial(self.pre_delete_ingredient, i))

    def reorder_ingredients(self, y0, yr):
        """To be run when reordering the ingredients using dragmanager. This moves the ingredient in line y0
           to line yr, and shifts the ingredients between by one line up or down, as needed"""
        temp_list = self.mod.order["ingredients"]
        temp_list.insert(yr, temp_list.pop(y0))
        self.mod.json_write_order()

        #Regrid ingredients in ingredient editor, selection window and those that have been selected.
        for i, j in enumerate(temp_list):
            self.ing_editor.display_ingredients[j].display(i, self.mod.order)
            self.mw.ingredient_select_button[j].grid(row=i)
            if j in self.mod.current_recipe.ingredients:
                self.display_restr_dict['ingredient_'+j].display(101 + i)
            else:
                pass
            
    def new_ingredient(self):
        i, ing = self.mod.new_ingredient()    # i = index of new ingredient ing

        self.ing_editor.new_ingredient(i, self.mod, self.mod.order)
        # Moved next section to IngredientEditor
##        self.ing_editor.display_ingredients[i] = DisplayIngredient(i, self.mod, self.ing_editor.i_e_scrollframe.interior) 
##        self.ing_editor.display_ingredients[i].display(int(i), self.mod, self.mod.order)
##        self.ing_editor.ing_dnd.add_dragable(self.ing_editor.display_ingredients[i].name_entry)    # This lets you drag the row corresponding to an ingredient by right-clicking on its name   
        self.ing_editor.display_ingredients[i].delete_button.config(command=partial(self.pre_delete_ingredient, i))
        
        self.display_restr_dict['ingredient_'+i] = DisplayRestriction(self.mw.restriction_sf.interior, self.mw.x_lab, self.mw.y_lab,
                                                                          'ingredient_'+i, ing.name, 0, 100)
        # Set the command for x and y variable selection boxes
        display_restr = self.display_restr_dict['ingredient_'+i]
        display_restr.left_label.bind("<Button-1>", partial(self.update_var, 'ingredient_'+i, 'x'))
        display_restr.right_label.bind("<Button-1>", partial(self.update_var, 'ingredient_'+i, 'y'))

        self.mw.ingredient_select_button[i] = ttk.Button(self.mw.ingredient_vsf.interior, text=ing.name, width=20,
                                                     command=partial(self.toggle_ingredient, i))
        self.mw.ingredient_select_button[i].grid(row=int(i))

    ##    i_e_scrollframe.vscrollbar.set(100,0)  # Doesn't do anything
        self.ing_editor.i_e_scrollframe.canvas.yview_moveto(1)  # Supposed to move the scrollbar to the bottom, but misses the last row
   
        # TODO: Move next section to model
        self.lprp.lp_var['ingredient_'+i] = pulp.LpVariable('ingredient_'+i, 0, None, pulp.LpContinuous)
        self.lprp.constraints['ing_total'] = \
                                           self.lprp.lp_var['ingredient_total'] \
                                           == sum(self.lprp.lp_var['ingredient_'+j] for j in self.mod.ingredient_dict)
     
    def update_ingredient_dict(self):
        """"Run when updating ingredients (via ingredient editor)"""

        for i, ing in self.mod.ingredient_dict.items():
            # Maybe the restriction class should have an update_data method
            ing.name = self.ing_editor.display_ingredients[i].name_entry.get()                 # update ingredient name
            self.mw.ingredient_select_button[i].config(text=ing.name)
            self.display_restr_dict['ingredient_'+i].set_name(ing.name)
            self.mod.restr_dict['ingredient_'+i].name = ing.name
            for ox in self.mod.order['oxides']:
                try:
                    val = eval(self.ing_editor.display_ingredients[i].oxide_entry[ox].get()   )
                except:
                    val = 0
                if isinstance(val, Number) and val != 0:
                    ing.analysis[ox] = val
                else:
                    self.ing_editor.display_ingredients[i].oxide_entry[ox].delete(0, tk.END)
                    try:
                        del ing.analysis[ox]
                    except:
                        pass

            for j, attr in self.mod.other_attr_dict.items():
                try:
                    val = eval(self.ing_editor.display_ingredients[i].other_attr_entry[j].get())
                except:
                    val = 0
                if isinstance(val, Number) and val != 0:
                    ing.other_attributes[j] = val
                else:
                    self.ing_editor.display_ingredients[i].other_attr_entry[j].delete(0, tk.END)
                    try:
                        del ing.other_attributes[j]
                    except:
                        pass

            self.mod.ingredient_dict[i] = ing
            self.mod.ingredient_analyses[i] = ing.analysis
        self.mod.json_write_ingredients()
        self.mod.json_write_restrictions()
                
        self.lprp.update_ingredient_analyses() 
                
        old_oxides = copy.copy(self.mod.current_recipe.oxides)
        old_variables = copy.copy(self.mod.current_recipe.variables)
        # Reinsert stars next to ingredients that are variables:
        for t, res in old_variables.items():
            if res[0:10] == 'ingredient':
                self.display_restr_dict[res].select(t)

        self.mod.current_recipe.update_oxides(self.mod)   # Do this for all recipes?
        
        for ox in old_oxides - self.mod.current_recipe.oxides:
            for et in ['umf_', 'mass_perc_', 'mole_perc_']:
                self.display_restr_dict[et+ox].remove(old_variables)

        et = self.mw.entry_type.get()
        for ox in self.mod.current_recipe.oxides - old_oxides:
            self.display_restr_dict[et+ox].display(1 + self.mod.order['oxides'].index(ox))

    def pre_delete_ingredient(self, i):
        """Deletes ingredient if not in any recipes, otherwise opens dialogue window asking for confirmation."""
        recipe_dict = self.mod.recipe_dict
        ingredient_dict = self.mod.ingredient_dict
        recipes_affected = [j for j in recipe_dict if i in recipe_dict[j].ingredients]
        n = len(recipes_affected)
        if n > 0:
            self.confirmation_window = tk.Toplevel()
            question_frame = tk.Frame(self.confirmation_window)
            question_frame.grid()
            text1 = ingredient_dict[i].name+' occurs in '+recipe_dict[recipes_affected[0]].name
            text2 = 'Are you sure you want to delete '+ingredient_dict[i].name+'?'
            if n == 1:
                tk.Label(master=question_frame, text=text1+'.').grid(row=0)
                tk.Label(master=question_frame, text=text2).grid(row=1)
            elif n == 2:
                tk.Label(master=question_frame, text=text1+' and '+recipe_dict[recipes_affected[1]].name+'.').grid(row=0)
                tk.Label(master=question_frame, text=text2).grid(row=1)
            elif n == 3:
                tk.Label(master=question_frame, text=text1+', '+recipe_dict[recipes_affected[1]].name).grid(row=0)
                tk.Label(master=question_frame, text=' and 1 other recipe.').grid(row=1)
                tk.Label(master=question_frame, text=text2).grid(row=2)
            else:
                tk.Label(master=question_frame, text=text1+', '+recipe_dict[recipes_affected[1]].name).grid(row=0)
                tk.Label(master=question_frame, text=' and '+str(n-2)+' other recipes.').grid(row=1)
                tk.Label(master=question_frame, text=text2).grid(row=2)  
            answer_frame = tk.Frame(self.confirmation_window)
            answer_frame.grid()
            ttk.Button(answer_frame, text='Yes', width=10, command=partial(self.close_conf_window_and_delete_ing, i, recipes_affected)).grid(column=0, row=0)
            ttk.Button(answer_frame, text='No', width=10, command=lambda : self.confirmation_window.destroy()).grid(column=1, row=0)
        else:
            self.delete_ingredient(i, [])

    def close_conf_window_and_delete_ing(self, i, recipes_affected):
        self.delete_ingredient(i, recipes_affected)
        self.confirmation_window.destroy()

    def delete_ingredient(self, i, recipes_affected):

        #self.update_basic_constraints(ingredient_analyses, other_dict)   # I should probably update other_dict, no?

        if i in self.mod.current_recipe.ingredients:
            self.toggle_ingredient(i)   # gets rid of stars, if the ingredient is a variable

        self.mod.delete_ingredient(i, recipes_affected)

        self.lprp.remove_ingredient(i, self.mod)

        self.ing_editor.display_ingredients[i].delete()
        for k, j in enumerate(self.mod.order['ingredients']):
            self.ing_editor.display_ingredients[j].display(k, self.mod.order)    # We actually only need to do this for the rows that are below the one that was deleted

        # Remove the deleted ingredient from the list of ingredients to select from:
        self.mw.ingredient_select_button[i].destroy()
        del self.display_restr_dict['ingredient_'+i]

        
    def toggle_ingredient(self, i):
        """Adds/removes ingredient_dict[i] to/from the current recipe, depending on whether it isn't/is an ingredient already."""
        recipe = self.mod.current_recipe
        if i in recipe.ingredients:
            old_variables = copy.copy(recipe.variables)
            recipe.remove_ingredient(self.mod, i)
            self.mw.ingredient_select_button[i].state(['!pressed'])
            self.display_restr_dict['ingredient_'+i].remove(old_variables)
            # Remove the restrictions on the oxides no longer present:
            for ox in set(self.mod.ingredient_analyses[i]) - recipe.oxides:
                for et in ['umf_', 'mass_perc_', 'mole_perc_']:
                    self.display_restr_dict[et+ox].remove(old_variables)

        else:
            recipe.add_ingredient(self.mod, i)
            self.mw.ingredient_select_button[i].state(['pressed'])
            self.display_restr_dict['ingredient_'+i].display(101 + self.mod.order["ingredients"].index(i))
            et = self.mw.entry_type.get()
            for ox in recipe.oxides:
                self.display_restr_dict[et+ox].display(1 + self.mod.order['oxides'].index(ox))

    def open_other_restriction_editor(self):
        """Opens a window that lets users edit other restrictions"""
        try:
            self.other_restr_editor.toplevel.lift() # lift the recipe selector, if it already exists
        except:
            self.other_restr_editor = OtherRestrictionEditor(self.mod, self.mod.order, self.reorder_other_restrictions)
            self.other_restr_editor.new_other_restr_button.config(command=self.new_other_restriction)
            self.other_restr_editor.update_button.config(command=self.update_other_restriction_dict)
            for i in self.mod.order['other']:
                self.other_restr_editor.display_other_restrictions[i].delete_button.config(command=partial(self.pre_delete_other_restriction, i))

    def reorder_other_restrictions(self, y0, yr):
        """To be run when reordering the ingredients using dragmanager. This moves the ingredient in line y0
           to line yr, and shifts the ingredients between by one line up or down, as needed"""
        temp_list = self.mod.order["other"]
        temp_list.insert(yr, temp_list.pop(y0))
        self.mod.json_write_order()

        #Regrid restrictions in other restriction editor, selection window and those that have been selected.
        for i, j in enumerate(temp_list):
            self.other_restr_editor.display_other_restrictions[j].display(i, self.mod.order)
            self.mw.other_select_button[j].grid(row=i)
            if j in self.mod.current_recipe.other:
                self.display_restr_dict['other_'+j].display(1001 + i)
            else:
                pass
            
    def new_other_restriction(self):
        i, ot = self.mod.new_other_restriction()    # i = index of new restriction ot

        self.other_restr_editor.new_other_restriction(i, self.mod, self.mod.order)
        self.other_restr_editor.display_other_restrictions[i].delete_button.config(command=partial(self.pre_delete_other_restriction, i))
        
        self.display_restr_dict['other_'+i] = DisplayRestriction(self.mw.restriction_sf.interior, self.mw.x_lab, self.mw.y_lab,
                                                                          'other_'+i, ot.name, 0, 100)
        # Set the command for x and y variable selection boxes
        display_restr = self.display_restr_dict['other_'+i]
        display_restr.left_label.bind("<Button-1>", partial(self.update_var, 'other_'+i, 'x'))
        display_restr.right_label.bind("<Button-1>", partial(self.update_var, 'other_'+i, 'y'))

        self.mw.other_select_button[i] = ttk.Button(self.mw.other_vsf.interior, text=ot.name, width=20,
                                                     command=partial(self.toggle_other, i))
        self.mw.other_select_button[i].grid(row=int(i)+1)

    ##    i_e_scrollframe.vscrollbar.set(100,0)  # Doesn't do anything
        self.other_restr_editor.i_e_scrollframe.canvas.yview_moveto(1)  # Supposed to move the scrollbar to the bottom, but misses the last row
   
        # TODO: Move next section to model
        self.lprp.lp_var['other_'+i] = pulp.LpVariable('other_'+i, 0, None, pulp.LpContinuous)
        # TODO relate the other variable to the standard variables
     
    def update_other_restriction_dict(self):
        """"Run when updating other restrictions (via other restriction editor)"""
        for i in self.mod.other_dict:
            disp_other = self.other_restr_editor.display_other_restrictions[i]
            ot = Other(disp_other.name_entry.get(),
                       ast.literal_eval(disp_other.numerator_coefs_entry.get()),  # Converts the string into a dictionary
                       ast.literal_eval(disp_other.normalization_entry.get()),
                       disp_other.def_low_entry.get(),
                       disp_other.def_upp_entry.get(),
                       disp_other.dec_pt_entry.get())
            self.mod.other_dict[i] = ot
            self.mod.restr_dict['other_'+i].name = ot.name
            self.mod.restr_dict['other_'+i].normalization = ot.normalization
            self.mod.restr_dict['other_'+i].default_low = ot.def_low
            self.mod.restr_dict['other_'+i].default_upp = ot.def_upp
            self.mod.restr_dict['other_'+i].dec_pt = ot.dec_pt
            
            self.mw.other_select_button[i].config(text=ot.name)
            self.display_restr_dict['other_'+i].set_name(ot.name)
            self.display_restr_dict['other_'+i].set_default_low(ot.def_low)
            self.display_restr_dict['other_'+i].set_default_upp(ot.def_upp)
            
        old_variables = copy.copy(self.mod.current_recipe.variables)
        # Reinsert stars next to other restrictions that are variables:
        for t, res in old_variables.items():
            if res[0:5] == 'other':
                self.display_restr_dict[res].select(t)
            
        self.mod.json_write_other()
        self.mod.json_write_restrictions()
                
        self.lprp.update_other_restrictions()

    def pre_delete_other_restriction(self, i):
        """Incomplete. Deletes restriction if not in any recipes, otherwise opens dialogue window asking for confirmation."""
        recipe_dict = self.mod.recipe_dict
        other_dict = self.mod.other_dict
        recipes_affected = [j for j in recipe_dict if i in recipe_dict[j].other]
        n = len(recipes_affected)
        if n > 0:
            self.confirmation_window = tk.Toplevel()
            question_frame = tk.Frame(self.confirmation_window)
            question_frame.grid()
            text1 = other_dict[i].name+' occurs in '+recipe_dict[recipes_affected[0]].name
            text2 = 'Are you sure you want to delete '+other_dict[i].name+'?'
            if n == 1:
                tk.Label(master=question_frame, text=text1+'.').grid(row=0)
                tk.Label(master=question_frame, text=text2).grid(row=1)
            elif n == 2:
                tk.Label(master=question_frame, text=text1+' and '+recipe_dict[recipes_affected[1]].name+'.').grid(row=0)
                tk.Label(master=question_frame, text=text2).grid(row=1)
            elif n == 3:
                tk.Label(master=question_frame, text=text1+', '+recipe_dict[recipes_affected[1]].name).grid(row=0)
                tk.Label(master=question_frame, text=' and 1 other recipe.').grid(row=1)
                tk.Label(master=question_frame, text=text2).grid(row=2)
            else:
                tk.Label(master=question_frame, text=text1+', '+recipe_dict[recipes_affected[1]].name).grid(row=0)
                tk.Label(master=question_frame, text=' and '+str(n-2)+' other recipes.').grid(row=1)
                tk.Label(master=question_frame, text=text2).grid(row=2)  
            answer_frame = tk.Frame(self.confirmation_window)
            answer_frame.grid()
            ttk.Button(answer_frame, text='Yes', width=10, command=partial(self.close_conf_window_and_delete_other_restr, i, recipes_affected)).grid(column=0, row=0)
            ttk.Button(answer_frame, text='No', width=10, command=lambda : self.confirmation_window.destroy()).grid(column=1, row=0)
        else:
            self.delete_other_restriction(i, [])

    def close_conf_windowc_and_delete_other_restr(self, i, recipes_affected):
        """Incomplete"""
        self.delete_other_restriction(i, recipes_affected)
        self.confirmation_window.destroy()

    def delete_other_restriction(self, i, recipes_affected):
        """Incomplete"""
        if i in self.mod.current_recipe.other:
            self.toggle_other(i)   # gets rid of stars, if the ingredient is a variable

        self.mod.delete_other_restriction(i, recipes_affected)

        self.lprp.remove_other_restriction(i, self.mod)

        self.other_restr_editor.display_other_restrictions[i].delete()
        for k, j in enumerate(self.mod.order['other']):
            self.other_restr_editor.display_other_restrictions[j].display(k, self.mod.order)    # We actually only need to do this for the rows that are below the one that was deleted
            
        # Remove the deleted restriction from the list of other restrictions to select from:
        self.mw.other_select_button[i].destroy()
        del self.display_restr_dict['other_'+i]


    def toggle_other(self, i):
        """Adds/removes other_dict[index] to/from the current recipe, depending on whether it isn't/is an other restriction already."""
        recipe = self.mod.current_recipe
        if i in recipe.other:
            old_variables = copy.copy(recipe.variables)            
            recipe.remove_other(self.mod, i)
            self.mw.other_select_button[i].state(['!pressed'])
            self.display_restr_dict['other_'+i].remove(old_variables)
        else:
            recipe.add_other(self.mod, i)
            self.mw.other_select_button[i].state(['pressed'])         
            self.display_restr_dict['other_'+i].display(1001 + self.mod.order['other'].index(i))
            self.mw.restriction_sf.canvas.yview_moveto(1)

    def update_var(self, key, t, mystery_variable):     # t should be either 'x' or 'y'. Might be a better way of doing this
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
                    self.display_restr_dict[et+ox].display(1 + self.mod.order['oxides'].index(ox))
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
    
