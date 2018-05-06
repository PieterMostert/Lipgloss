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

import tkinter.messagebox
from numbers import Number

from .dragmanager import *
from .main_window import MainWindow
from .vert_scrolled_frame import VerticalScrolledFrame
from .pretty_names import prettify
##
##from os.path import abspath, dirname
##from inspect import getsourcefile
##order_pathname = dirname(dirname(abspath(getsourcefile(lambda:0))))+'\model\persistent_data\OrderShelf'
##raw_order_pathname = "%r"%order_pathname

class DisplayIngredient:
    """A class used to display the line corresponding to an ingredient in the ingredient editor"""
    def __init__(self, index, core_data, frame):
        ing = core_data.ingredient_dict[index]
        self.delete_button =  ttk.Button(master=frame, text='X', width=2) #, command = partial(delete_ingredient_fn, index))
        self.name_entry = Entry(master=frame, width=20)
        self.name_entry.insert(0, ing.name)
        ox_comp = ing.analysis
        self.oxide_entry = {}
        
        c = 3
        for ox in core_data.oxide_dict:
            # Use this entry widget to input the percent weight of the oxide that the ingredient contains.
            self.oxide_entry[ox] = Entry(master=frame,  width=5)  
            self.oxide_entry[ox].delete(0, END)
            if ox in ox_comp:
                self.oxide_entry[ox].insert(0, ox_comp[ox])
            else:
                pass
            c += 1

        self.other_attr_entry = {}
        for i, other_attr in core_data.other_attr_dict.items(): 
            self.other_attr_entry[i] = Entry(master=frame, width=5)
        for i, value in ing.other_attributes.items():
            self.other_attr_entry[i].insert(0, value)

    def display(self, pos, order):
        self.delete_button.grid(row=pos, column=0)
        self.name_entry.grid(row=pos, column=1, padx=3, pady=3)

        c = 3
        for i, ox in enumerate(order["oxides"]):
            self.oxide_entry[ox].grid(row=pos, column=c+i, padx=3, pady=1)

        c = 100
        for i, other_attr in enumerate(order["other attributes"]): 
            self.other_attr_entry[other_attr].grid(row=pos, column=c+i, padx=3, pady=3)

    def delete(self):
        for widget in [self.delete_button, self.name_entry] + list(self.oxide_entry.values()) + list(self.other_attr_entry.values()):
            widget.destroy()

class IngredientEditor(MainWindow):
    """Window that lets users enter / delete ingredients, edit oxide compositions and other attributes, and rearrange \\
       the order in which ingredients are displayed"""

    def __init__(self, core_data, order, reorder_ingredients):
        self.toplevel = Toplevel()
        self.toplevel.title("Ingredient Editor")

        self.ingredient_editor_headings = Frame(self.toplevel)
        self.ingredient_editor_headings.pack()
        self.i_e_scrollframe = VerticalScrolledFrame(self.toplevel)
        self.i_e_scrollframe.frame_height = 500
        self.i_e_scrollframe.pack()
        ingredient_editor_buttons = Frame(self.toplevel)
        ingredient_editor_buttons.pack()

        # Place the headings on the ingredient_editor. There is some not-entirely-successful fiddling involved to try
        # to get the headings to match up with their respective columns:
        Label(master=self.ingredient_editor_headings, text='', width=5).grid(row=0, column=0)  # Blank label above the delete buttons
        Label(master=self.ingredient_editor_headings, text='', width=5).grid(row=0, column=1)  # Blank label above the delete buttons
        Label(master=self.ingredient_editor_headings, text='    Ingredient', width=20).grid(row=0, column=2)

        Label(master=self.ingredient_editor_headings, text='', width=5).grid(row=0, column=299)  # Blank label above the scrollbar
        Label(master=self.ingredient_editor_headings, text='', width=5).grid(row=0, column=300)  # Blank label above the scrollbar

        c = 3
        for i, ox in enumerate(order["oxides"]):
            Label(master=self.ingredient_editor_headings, text=prettify(ox), width=5).grid(row=0, column=c+i)

        c = 100
        for i, other_attr in enumerate(order["other attributes"]): 
            Label(master=self.ingredient_editor_headings, text=core_data.other_attr_dict[other_attr], width=5).grid(row=0, column=c+i)

        # Create drag manager for ingredient rows:
        self.ing_dnd = DragManager(reorder_ingredients)
        
        # Create and display the rows:
        self.display_ingredients = {}
        for r, i in enumerate(order["ingredients"]):
            self.display_ingredients[i] = DisplayIngredient(i, core_data, self.i_e_scrollframe.interior)
            self.display_ingredients[i].display(r, order)    
            self.ing_dnd.add_dragable(self.display_ingredients[i].name_entry)    # This lets you drag the row corresponding to an ingredient by right-clicking on its name   
                
        # This label is hack to make sure that when a new ingredient is added, you don't have to scroll down to see it:
        Label(master=self.i_e_scrollframe.interior).grid(row=9000) 

        self.new_ingr_button = ttk.Button(ingredient_editor_buttons, text='New ingredient', width=20)
        self.new_ingr_button.pack(side='left')   
        self.update_button = ttk.Button(ingredient_editor_buttons, text='Update', width=20)
        self.update_button.pack(side='right')

        self.i_e_scrollframe.interior.focus_force()

    def new_ingredient(self, i, core_data, order):
        self.display_ingredients[i] = DisplayIngredient(i, core_data, self.i_e_scrollframe.interior) 
        self.display_ingredients[i].display(int(i), order)
        self.ing_dnd.add_dragable(self.display_ingredients[i].name_entry)    # This lets you drag the row corresponding to an ingredient by right-clicking on its name   
 


##    def update_basic_constraints(self, ingredient_analyses, other_dict):
##        # We could remove the dependence on ingredient_analyses.
##        # I think the current implementation is more efficient, but I'm not sure.
##        
##        for ox in oxide_dict:
##            prob.constraints[ox] = sum(ingredient_analyses[index][ox]*lp_var['ingredient_'+index]/100 \
##                                       for index in self.ingredient_dict if ox in ingredient_analyses[index]) \
##                                   == lp_var['mass_'+ox]     # relate ingredients and oxides
##            
##        # We only need to update the constraints that depend on the other attributes, since the ones depending only on the
##        # oxides have already been updated.  However, I don't feel like writing code to identify these constraints, so I'm
##        # just going to update all other constraints.
##        for index in other_dict:      
##            ot = 'other_'+index
##            coefs = other_dict[index].numerator_coefs
##            linear_combo = [(lp_var[key], coefs[key]) for key in coefs]
##            prob.constraints[ot] = lp_var[ot] == LpAffineExpression(linear_combo)         # Relate this variable to the other variables.      

##    def update_ingredient_dict(self, current_recipe, ingredient_select_button, entry_type):
##        # Run when updating ingredients.  Needs improvement since it removes stars from ingredients that correspond to x or y variables.
##
##        for index in self.ingredient_dict:
##            # Maybe the restriction class should have an update_data method
##            ing = self.ingredient_dict[index]
##            ing.name = ing.display_widgets['name'].get()                 # update ingredient name
##            restr_dict['ingredient_'+index].name = ing.name              # update corresponding restriction name
##            restr_dict['ingredient_'+index].left_label_text.set(ing.name+' : ')
##            restr_dict['ingredient_'+index].right_label_text.set(' : '+ing.name)
##            ingredient_select_button[index].config(text = ing.name)
##            for ox in oxides:
##                try:
##                    val = eval(ing.display_widgets[ox].get())
##                except:
##                    val = 0
##                if isinstance(val,Number) and val != 0:
##                    ing.analysis[ox] = val
##                else:
##                    ing.display_widgets[ox].delete(0,END)
##                    try:
##                        del ing.analysis[ox]
##                    except:
##                        pass
##
##    ##        for t, i in current_recipe.variables.items():
##    ##            restr_dict[i].select(t)
##
##            for i, attr in other_attr_dict.items():
##                try:
##                    val = eval(ing.display_widgets['other_attr_'+i].get())
##                except:
##                    val = 0
##                if isinstance(val,Number) and val != 0:
##                    ing.other_attributes[i] = val
##                else:
##                    ing.display_widgets['other_attr_'+i].delete(0,END)
##                    try:
##                        del ing.other_attributes[i]
##                    except:
##                        pass
##
##            self.ingredient_dict[index] = ing
##        
##        with shelve.open("./data/IngredientShelf") as ingredient_shelf:
##            for index in ingredient_shelf:
##                ingredient_shelf[index] = self.ingredient_dict[index].pickleable_version()
##        ingredient_analyses = get_ing_comp(self.ingredient_dict)
##
##        self.update_basic_constraints(ingredient_analyses, other_dict)
##
##        current_recipe.update_oxides(restr_dict, entry_type.get())

##    def close_conf_window_and_delete_ing(self, index, recipes_affected):
##        self.delete_ingredient(index, recipes_affected)
##        self.confirmation_window.destroy()
##
##    def pre_delete_ingredient(self, index, recipe_dict):
##        """Deletes ingredient if not in any recipes, otherwise opens dialogue window asking for confirmation."""
##        recipes_affected = [i for i in recipe_dict if index in recipe_dict[i].ingredients]
##        n = len(recipes_affected)
##        if n > 0:
##            self.confirmation_window = Toplevel()
##            question_frame = Frame(self.confirmation_window)
##            question_frame.grid()
##            if n == 1:
##                Label(master=question_frame, text=ingredient_dict[index].name+' occurs in '+recipe_dict[recipes_affected[0]].name+'.').grid(row=0)
##                Label(master=question_frame, text='Are you sure you want to delete '+ingredient_dict[index].name+'?').grid(row=1)
##            elif n == 2:
##                Label(master=question_frame, text=ingredient_dict[index].name+' occurs in '+recipe_dict[recipes_affected[0]].name+' and '+recipe_dict[recipes_affected[1]].name+'.').grid(row=0)
##                Label(master=question_frame, text='Are you sure you want to delete '+ingredient_dict[index].name+'?').grid(row=1)
##            elif n == 3:
##                Label(master=question_frame, text=ingredient_dict[index].name+' occurs in '+recipe_dict[recipes_affected[0]].name+', '+recipe_dict[recipes_affected[1]].name).grid(row=0)
##                Label(master=question_frame, text=' and 1 other recipe.').grid(row=1)
##                Label(master=question_frame, text='Are you sure you want to delete '+ingredient_dict[index].name+'?').grid(row=2)
##            else:
##                Label(master=question_frame, text=ingredient_dict[index].name+' occurs in '+recipe_dict[recipes_affected[0]].name+', '+recipe_dict[recipes_affected[1]].name).grid(row=0)
##                Label(master=question_frame, text=' and '+str(n-2)+' other recipes.').grid(row=1)
##                Label(master=question_frame, text='Are you sure you want to delete '+ingredient_dict[index].name+'?').grid(row=2)  
##            answer_frame = Frame(confirmation_window)
##            answer_frame.grid()
##            ttk.Button(answer_frame, text='Yes', width=10, command=partial(close_conf_window_and_delete_ing, index, recipes_affected)).grid(column=0, row=0)
##            ttk.Button(answer_frame, text='No', width=10, command=lambda : self.confirmation_window.destroy()).grid(column=1, row=0)
##        else:
##            self.delete_ingredient(index, [])

##    def delete_ingredient(self, index, recipes_affected):
##
##        oxides_to_update = self.ingredient_dict[index].analysis
##
##    ##    prob._variables.remove(lp_var['ingredient_'+index])
##        # The commented-out line above doesn't work in general since lp_var['ingredient_'+index] is regarded as
##        # being equal to all entries of prob._variables, so it removes the first entry. Instead, we need to use 'is'.
##        for i,j in enumerate(prob._variables):
##            if j is lp_var['ingredient_'+index]:
##                del prob._variables[i]  
##
##        self.update_basic_constraints(ingredient_analyses, other_dict)   # I should probably update other_dict, no?
##
##        for widget in ['del', 'name'] + self.oxides + ['other_attr_'+i for i in other_attr_dict]:
##            self.ingredient_dict[index].display_widgets[widget].destroy()
##
##        if index in current_recipe.ingredients:
##            toggle_ingredient(index)
##
##        del self.ingredient_dict[index]
##        with shelve.open("./data/IngredientShelf") as ingredient_shelf:
##            del ingredient_shelf[index]
##
##        with shelve.open("./data/OrderShelf") as order_shelf:
##            temp_list = order_shelf['ingredients']
##            temp_list.remove(index)
##            order_shelf['ingredients'] = temp_list
##            self.ingredient_order = temp_list
##
##        for i,j in enumerate(self.ingredient_order):
##            self.ingredient_dict[j].display(i)    # We actually only need to do this for the rows that are below the one that was deleted
##
##        # Remove the deleted ingredient from the list of ingredients to select from:
##        ingredient_select_button[index].destroy()
##        
##        try:
##            del prob.constraints['ingredient_'+index+'_lower']  # Is this necessary?
##        except:
##            pass
##        try:
##            del prob.constraints['ingredient_'+index+'_upper']  # Is this necessary?
##        except:
##            pass
##        prob.constraints['ing_total'] = lp_var['ingredient_total'] == sum(lp_var['ingredient_'+i] for i in self.ingredient_dict)
##
##        del restr_dict['ingredient_'+index]
##
##        # Remove the ingredient from all recipes that contain it.
##        for i in recipes_affected:
##            rec = recipe_dict[i]
##            rec.ingredients.remove(index)
##            rec.update_oxides(restr_dict, entry_type.get())
##            #recipe_dict[i] = rec
##            rec.update_variables(restr_keys(rec.oxides, rec.ingredients, rec.other))
##        json_write_recipes()
##      
##    def new_ingredient(self, toggle_ingredient):
##
##        with shelve.open("./data/IngredientShelf") as ingredient_shelf:
##            r = max([int(index) for index in ingredient_shelf]) + 1
##            index = str(r)
##            ing = ingredient_shelf[str(r)] = Ingredient('Ingredient #'+index, notes='', analysis={}, other_attributes={})
##                            # If we just had Ingredient('Ingredient #'+index) above, the default values of the notes, analysis
##                            # and other_attributes attributes would change when the last instance of the class defined had those
##                            # attributes changed
##    ##        ing = Ingredient('Ingredient #'+index, analysis = {})
##    ##        print(ing.analysis)
##    ##        print(ing.name)
##    ##        ingredient_shelf[str(r)] = copy.deepcopy(ing)
##
##        with shelve.open("./data/OrderShelf") as order_shelf:
##            temp_list = order_shelf['ingredients']
##            temp_list.append(index)
##            order_shelf['ingredients'] = temp_list
##            self.ingredient_order = temp_list
##        
##        self.ingredient_dict[index] = ing
##        ing.displayable_version(index, self.i_e_scrollframe.interior, lambda i : self.pre_delete_ingredient(i, recipe_dict))
##        ing.display(len(temp_list)-1)
##        self.ing_dnd.add_dragable(self.ingredient_dict[index].display_widgets['name'])    # This lets you drag the row corresponding to an ingredient by right-clicking on its name   
##        restr_dict['ingredient_'+index] = Restriction('ingredient_'+index, ing.name, 'ingredient_'+index, "0.01*lp_var['ingredient_total']", 0, 100)
##
##        lp_var['ingredient_'+index] = pulp.LpVariable('ingredient_'+index, 0, None, pulp.LpContinuous)
##        prob.constraints['ing_total'] = lp_var['ingredient_total'] == sum(lp_var['ingredient_'+index] for index in self.ingredient_dict)
##
##        ingredient_select_button[index] = ttk.Button(vsf.interior, text=ing.name, width=20,
##                                                     command=partial(toggle_ingredient, index))
##        ingredient_select_button[index].grid(row=r)
##
##    ##    i_e_scrollframe.vscrollbar.set(100,0)  # Doesn't do anything
##        self.i_e_scrollframe.canvas.yview_moveto(1)  # Supposed to move the scrollbar to the bottom, but misses the last row
##        
##        restr = restr_dict['ingredient_'+index]
##        restr.left_label.bind("<Button-1>", partial(update_var, current_recipe, restr, 'x'))
##        restr.right_label.bind("<Button-1>", partial(update_var, current_recipe, restr, 'y'))
