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

from recipes import *
from polyplot import *
from dragmanager import *
from ingredient_data import *

from serializers.recipeserializer import RecipeSerializer

if False:  # Set to True whenever the Recipe class is changed
    default_recipe_dict = {}
    default_recipe_dict['0'] = Recipe.get_default_recipe()
    f = open('./data/JSONRecipeShelf.json', 'w')
    f.write(RecipeSerializer.serialize_dict(default_recipe_dict))
    f.close()
    
## SECTION 1
# Create stuff for restriction window

entry_type = StringVar()

def update_oxide_entry_type(recipe, entry_type):

    global current_recipe
    current_recipe.update_oxides(restr_dict, entry_type)

    for et in ['umf_', 'mass_perc_', 'mole_perc_']:
        if et == entry_type:
            for ox in current_recipe.oxides:
                restr_dict[et+ox].display(1 + oxide_dict[ox].pos)
        else:
            for ox in current_recipe.oxides:
                restr_dict[et+ox].hide()

# SECTION 2
# Selecting variables for 2 dim projection

def update_var(recipe, restr, t, event):  # t should be either 'x' or 'y'. Might be a better way of doing this
    if t in recipe.variables:
        v = restr_dict[recipe.variables[t]]
        if v == restr:
            del recipe.variables[t]
            restr.deselect(t)
        else:
            recipe.variables[t] = restr.index
            v.deselect(t)
            restr.select(t)      
    else:
        recipe.variables[t] = restr.index
        restr.select(t)

def bind_restrictions_to_recipe(recipe, restr_dict):    #   Set the command for x and y variable selection boxes
    for index in restr_keys(oxide_dict, ingredient_dict, other_dict):
        restr = restr_dict[index]
        restr.left_label.bind("<Button-1>", partial(update_var, recipe, restr, 'x'))
        restr.right_label.bind("<Button-1>", partial(update_var, recipe, restr, 'y'))

# SECTION 3
# Functions relating to opening and saving recipes.

recipe_name = StringVar()
Entry(recipe_name_frame, textvariable = recipe_name, font = ("Helvetica 12 italic")).grid()  # displays the name of the current recipe

def get_highest_recipe_key():
    """Return the highest recipe key in the recipe dict"""
    global recipe_dict
    return max(recipe_dict, key=int)

def delete_recipe(index, restr_dict, r_s=0):
    """Delete the recipe from the recipe_dict, then write out the updated recipe_dict to JSON file."""
    global recipe_dict
    global recipe_index

    if index != '0': # don't allow a user to delete the default 
        del recipe_dict[index]
        json_write_recipes()
    if index == recipe_index:
        # we have deleted the current recipe.  go to default recipe
        open_recipe('0', restr_dict)
    try:
        r_s.destroy() # destroy the open recipe window
    except:
        pass

def open_recipe(index, restr_dict, r_s=0):   # to be used when opening a recipe, (or when ingredients have been updated?). Be careful.

    global recipe_index
    global current_recipe
    recipe_index = index

    for t, res in current_recipe.variables.items():
        restr_dict[res].deselect(t)            # remove stars from old variables
    current_recipe = copy.deepcopy(recipe_dict[index])
    current_recipe.update_oxides(restr_dict, entry_type.get())            # in case the oxide compositions have changed
    
    recipe_name.set(current_recipe.name)      # update the displayed recipe name

    for i in restr_dict:
        restr_dict[i].remove(current_recipe)    # clear the entries from previous recipes, if opening a new recipe

    for i in restr_keys(current_recipe.oxides, current_recipe.ingredients, current_recipe.other):
        try:
            restr_dict[i].low.set(current_recipe.lower_bounds[i])
            restr_dict[i].upp.set(current_recipe.upper_bounds[i])
        except:
            restr_dict[i].low.set(restr_dict[i].default_low)    # this is just for the case where the oxides have changed
            restr_dict[i].upp.set(restr_dict[i].default_upp)    # ditto

    for t, res in current_recipe.variables.items():
        restr_dict[res].select(t)               # add stars to new variables
    
    et = current_recipe.entry_type
    entry_type.set(et)

    for ox in current_recipe.oxides:
        restr_dict[et+ox].display(1 + oxide_dict[ox].pos)
        
    for i in ingredient_order:
        if i in current_recipe.ingredients:
            ingredient_select_button[i].state(['pressed'])
            restr_dict['ingredient_'+i].display(101 + ingredient_order.index(i))
        else:
            ingredient_select_button[i].state(['!pressed'])

    for ot in other_dict:
        if ot in current_recipe.other:
            other_select_button[ot].state(['pressed'])
            restr_dict['other_'+ot].display(1001 + other_dict[ot].pos)
        else:
            other_select_button[ot].state(['!pressed'])

    try:
        r_s.destroy()
    except:
        pass
    bind_restrictions_to_recipe(current_recipe, restr_dict)

def display_recipe(index, frame, window):     # display recipe name in recipe_selector
    recipe = recipe_dict[index]
    name_button =  ttk.Button(master=frame, text = recipe.name, width=30,
                             command = partial(open_recipe, index, restr_dict, window))
    name_button.grid(row=recipe.pos+1, column=0)
    if index != '0': 
        # only allow deletion of user recipes.  index '0' denotes the default recipe bounds
        delete_button = ttk.Button(master=frame, text = "X", width=5,
                                  command = partial(delete_recipe, index, restr_dict, window))
        delete_button.grid(row=recipe.pos+1, column=1)

def open_recipe_menu():   # Opens window that lets you select a recipe to open
    global recipe_selector
    global r_s_scrollframe

    recipe_selector = Toplevel()

    r_s_scrollframe = VerticalScrolledFrame(recipe_selector)
    r_s_scrollframe.frame_height = 200
    r_s_scrollframe.pack()
    recipe_selector_buttons = Frame(recipe_selector)
    recipe_selector_buttons.pack()

    Label(master=r_s_scrollframe.interior, text='Recipes', width=35).grid(row=0, column=0)  
    Label(master=r_s_scrollframe.interior, text='Delete', width=5).grid(row=0, column=1)  

    for index in recipe_dict:
        display_recipe(index, r_s_scrollframe.interior, recipe_selector) 
            
    r_s_scrollframe.interior.focus_force()

def update_shelf(name, dictionary):
    with shelve.open(name) as shelf:
        for item in shelf:
            del shelf[item]
        shelf.update(dictionary)
        
def json_load_recipes():
    """Load recipes from a JSON file using our deserializer"""
    global recipe_dict
    global current_recipe
    f = open('./data/JSONRecipeShelf.json', 'r')
    json_str = f.read()
    f.close()
    recipe_dict = RecipeSerializer.deserialize_dict(json_str)
    # open first (default) recipe in list
    current_recipe = recipe_dict['0']

def json_write_recipes():
    """Write all recipes from the global recipe_dict to file, overwriting previous data"""
    global recipe_dict
    f = open('./data/JSONRecipeShelf.json', 'w')
    json_string = RecipeSerializer.serialize_dict(recipe_dict)
    f.write(json_string)
    f.close()
    
def save_recipe():
    """Save a recipe to the global recipe_dict, then update the JSON data file"""
    global recipe_dict
    current_recipe.name = recipe_name.get()
    current_recipe.update_bounds(restr_dict)
    current_recipe.entry_type = entry_type.get()
    recipe_dict[recipe_index] = copy.deepcopy(current_recipe)
    json_write_recipes()

def save_new_recipe(r_s=0):
    """Save a new recipe with new ID to the global recipe_dict, then update the JSON data file"""  
    global recipe_index
    global recipe_dict
    
    current_recipe.update_bounds(restr_dict)
    current_recipe.entry_type = entry_type.get()
    highest_recipe_key = get_highest_recipe_key()
    recipe_index = int(highest_recipe_key) + 1
    current_recipe.name = 'Recipe Bounds ' + str(recipe_index)
    current_recipe.pos = recipe_index
    recipe_dict[recipe_index] = copy.deepcopy(current_recipe)
    recipe_name.set(current_recipe.name)
    json_write_recipes()
    try:
        r_s.destroy()
    except:
        pass


# read in all recipes to global recipe_dict
json_load_recipes()

# SECTION 4
#
# Options in the Options menu: Edit Oxides, Edit Ingredients, Edit Other Restrictions, Restriction Settings.
# Currently only Edit Ingredients does anything

# SECTION 4.1
#
# Come back to this later. Include the option to only display an oxide when at least one of the ingredients contains at
# least x% of that oxide, where x can be modified by the user. Might not include this at all.

def edit_oxides():
    pass                       

# SECTION 4.2
# Functions relating to the ingredient editor window (accessed through Options > Edit Ingredients)

ing_dat = Ingredient_Data(ingredient_order, ingredient_dict, oxides, other_attr_dict) 

##def update_basic_constraints(ingredient_compositions, ingredient_dict, other_dict):
##    # We could remove the dependence on ingredient_compositions.
##    # I think the current implementation is more efficient, but I'm not sure.
##    
##    global prob
##    for ox in oxide_dict:
##        prob.constraints[ox] = sum(ingredient_compositions[index][ox]*lp_var['ingredient_'+index]/100 \
##                                   for index in ingredient_dict if ox in ingredient_compositions[index]) \
##                               == lp_var['mass_'+ox]     # relate ingredients and oxides
##        
##    # We only need to update the constraints that depend on the other attributes, since the ones depending only on the
##    # oxides have already been updated.  However, I don't feel like writing code to identify these constraints, so I'm
##    # just going to update all other constraints.
##    for index in other_dict:      
##        ot = 'other_'+index
##        coefs = other_dict[index].numerator_coefs
##        linear_combo = [(lp_var[key], coefs[key]) for key in coefs]
##        prob.constraints[ot] = lp_var[ot] == LpAffineExpression(linear_combo)         # Relate this variable to the other variables.
##
##def reorder_ingredients(ing_list):
##    # Run when reordering the ingredients using dragmanager.
##
##    global ingredient_order
##    
##    #Regrid ingredients in selection window and those that have been selected.
##    for i, j in enumerate(ing_list):
##        ingredient_select_button[j].grid(row = i)
##        if j in current_recipe.ingredients:
##            restr_dict['ingredient_'+j].display(101 + i)
##        else:
##            pass
##
##    ingredient_order = ing_list
##
##def update_ingredient_dict():
##    # Run when updating ingredients.  Needs improvement since it removes stars from ingredients that correspond to x or y variables.
##
##    global ingredient_dict
##    global ingredient_compositions
##    global prob
##
##    for index in ingredient_dict:
##        # Maybe the restriction class should have an update_data method
##        ing = ingredient_dict[index]
##        ing.name = ing.display_widgets['name'].get()                 # update ingredient name
##        restr_dict['ingredient_'+index].name = ing.name              # update corresponding restriction name
##        restr_dict['ingredient_'+index].left_label_text.set(ing.name+' : ')
##        restr_dict['ingredient_'+index].right_label_text.set(' : '+ing.name)
##        ingredient_select_button[index].config(text = ing.name)
##        for ox in oxides:
##            try:
##                val = eval(ing.display_widgets[ox].get())
##            except:
##                val = 0
##            if isinstance(val,Number) and val != 0:
##                ing.oxide_comp[ox] = val
##            else:
##                ing.display_widgets[ox].delete(0,END)
##                try:
##                    del ing.oxide_comp[ox]
##                except:
##                    pass
##
####        for t, i in current_recipe.variables.items():
####            restr_dict[i].select(t)
##
##        for i, attr in other_attr_dict.items():
##            try:
##                val = eval(ing.display_widgets['other_attr_'+i].get())
##            except:
##                val = 0
##            if isinstance(val,Number) and val != 0:
##                ing.other_attributes[i] = val
##            else:
##                ing.display_widgets['other_attr_'+i].delete(0,END)
##                try:
##                    del ing.other_attributes[i]
##                except:
##                    pass
##
##        ingredient_dict[index] = ing
##    
##    with shelve.open("./data/IngredientShelf") as ingredient_shelf:
##        for index in ingredient_shelf:
##            ingredient_shelf[index] = ingredient_dict[index].pickleable_version()
##    ingredient_compositions = get_ing_comp(ingredient_dict)
##
##    update_basic_constraints(ingredient_compositions, ingredient_dict, other_dict)
##
##    current_recipe.update_oxides(restr_dict, entry_type.get())
##
##def close_conf_window_and_delete_ing(index, window, recipes_affected):
##    delete_ingredient(index, recipes_affected)
##    window.destroy()
##
##def pre_delete_ingredient(index):
##    """Deletes ingredient if not in any recipes, otherwise opens dialogue window asking for confirmation."""
##    recipes_affected = [i for i in recipe_dict if index in recipe_dict[i].ingredients]
##    n = len(recipes_affected)
##    if n > 0:
##        confirmation_window = Toplevel()
##        question_frame = Frame(confirmation_window)
##        question_frame.grid()
##        if n == 1:
##            Label(master=question_frame, text=ingredient_dict[index].name+' occurs in '+recipe_dict[recipes_affected[0]].name+'.').grid(row=0)
##            Label(master=question_frame, text='Are you sure you want to delete '+ingredient_dict[index].name+'?').grid(row=1)
##        elif n == 2:
##            Label(master=question_frame, text=ingredient_dict[index].name+' occurs in '+recipe_dict[recipes_affected[0]].name+' and '+recipe_dict[recipes_affected[1]].name+'.').grid(row=0)
##            Label(master=question_frame, text='Are you sure you want to delete '+ingredient_dict[index].name+'?').grid(row=1)
##        elif n == 3:
##            Label(master=question_frame, text=ingredient_dict[index].name+' occurs in '+recipe_dict[recipes_affected[0]].name+', '+recipe_dict[recipes_affected[1]].name).grid(row=0)
##            Label(master=question_frame, text=' and 1 other recipe.').grid(row=1)
##            Label(master=question_frame, text='Are you sure you want to delete '+ingredient_dict[index].name+'?').grid(row=2)
##        else:
##            Label(master=question_frame, text=ingredient_dict[index].name+' occurs in '+recipe_dict[recipes_affected[0]].name+', '+recipe_dict[recipes_affected[1]].name).grid(row=0)
##            Label(master=question_frame, text=' and '+str(n-2)+' other recipes.').grid(row=1)
##            Label(master=question_frame, text='Are you sure you want to delete '+ingredient_dict[index].name+'?').grid(row=2)  
##        answer_frame = Frame(confirmation_window)
##        answer_frame.grid()
##        ttk.Button(answer_frame, text='Yes', width=10, command=partial(close_conf_window_and_delete_ing, index, confirmation_window, recipes_affected)).grid(column=0, row=0)
##        ttk.Button(answer_frame, text='No', width=10, command=lambda : confirmation_window.destroy()).grid(column=1, row=0)
##    else:
##        delete_ingredient(index, [])
##
##def delete_ingredient(index, recipes_affected):
##
##    global ingredient_dict
##    global ingredient_order
##
##    oxides_to_update = ingredient_dict[index].oxide_comp
##
####    prob._variables.remove(lp_var['ingredient_'+index])
##    # The commented-out line above doesn't work in general since lp_var['ingredient_'+index] is regarded as
##    # being equal to all entries of prob._variables, so it removes the first entry. Instead, we need to use 'is'.
##    for i,j in enumerate(prob._variables):
##        if j is lp_var['ingredient_'+index]:
##            del prob._variables[i]  
##
##    update_basic_constraints(ingredient_compositions, ingredient_dict, other_dict)   # I should probably update other_dict, no?
##
##    for widget in ['del', 'name'] + oxides + ['other_attr_'+i for i in other_attr_dict]:
##        ingredient_dict[index].display_widgets[widget].destroy()
##
##    if index in current_recipe.ingredients:
##        toggle_ingredient(index)
##
##    del ingredient_dict[index]
##    with shelve.open("./data/IngredientShelf") as ingredient_shelf:
##        del ingredient_shelf[index]
##
##    with shelve.open("./data/OrderShelf") as order_shelf:
##        temp_list = order_shelf['ingredients']
##        temp_list.remove(index)
##        order_shelf['ingredients'] = temp_list
##        ingredient_order = temp_list
##
##    for i,j in enumerate(ingredient_order):
##        ingredient_dict[j].display(i)    # We actually only need to do this for the rows that are below the one that was deleted
##
##    # Remove the deleted ingredient from the list of ingredients to select from:
##    ingredient_select_button[index].destroy()
##    
##    try:
##        del prob.constraints['ingredient_'+index+'_lower']  # Is this necessary?
##    except:
##        pass
##    try:
##        del prob.constraints['ingredient_'+index+'_upper']  # Is this necessary?
##    except:
##        pass
##    prob.constraints['ing_total'] = lp_var['ingredient_total'] == sum(lp_var['ingredient_'+i] for i in ingredient_dict)
##
##    del restr_dict['ingredient_'+index]
##
##    # Remove the ingredient from all recipes that contain it.
##    for i in recipes_affected:
##        rec = recipe_dict[i]
##        rec.ingredients.remove(index)
##        rec.update_oxides(restr_dict, entry_type.get())
##        #recipe_dict[i]=rec
##        rec.update_variables(restr_keys(rec.oxides, rec.ingredients, rec.other))
##    json_write_recipes()
##  
##def new_ingredient():
##
##    global ingredient_dict
##    global ingredient_order
##    
##    with shelve.open("./data/IngredientShelf") as ingredient_shelf:
##        r = max([int(index) for index in ingredient_shelf]) + 1
##        index = str(r)
##        ing = ingredient_shelf[str(r)] = Ingredient('Ingredient #'+index, notes='', oxide_comp={}, other_attributes={})
##                        # If we just had Ingredient('Ingredient #'+index) above, the default values of the notes, oxide_comp
##                        # and other_attributes attributes would change when the last instance of the class defined had those
##                        # attributes changed
####        ing = Ingredient('Ingredient #'+index, oxide_comp = {})
####        print(ing.oxide_comp)
####        print(ing.name)
####        ingredient_shelf[str(r)] = copy.deepcopy(ing)
##
##    with shelve.open("./data/OrderShelf") as order_shelf:
##        temp_list = order_shelf['ingredients']
##        temp_list.append(index)
##        order_shelf['ingredients'] = temp_list
##        ingredient_order = temp_list
##    
##    ingredient_dict[index] = ing
##    ing.displayable_version(index, i_e_scrollframe.interior, pre_delete_ingredient)
##    ing.display(len(temp_list)-1)
##    ing_dnd.add_dragable(ingredient_dict[index].display_widgets['name'])    # This lets you drag the row corresponding to an ingredient by right-clicking on its name   
##    restr_dict['ingredient_'+index] = Restriction('ingredient_'+index, ing.name, 'ingredient_'+index, "0.01*lp_var['ingredient_total']", 0, 100)
##
##    lp_var['ingredient_'+index] = pulp.LpVariable('ingredient_'+index, 0, None, pulp.LpContinuous)
##    prob.constraints['ing_total'] = lp_var['ingredient_total'] == sum(lp_var['ingredient_'+index] for index in ingredient_dict)
##
##    ingredient_select_button[index] = ttk.Button(vsf.interior, text = ing.name, width=20,
##                                                 command = partial(toggle_ingredient, index))
##    ingredient_select_button[index].grid(row = r)
##
####    i_e_scrollframe.vscrollbar.set(100,0)  # Doesn't do anything
##    i_e_scrollframe.canvas.yview_moveto(1)  # Supposed to move the scrollbar to the bottom, but misses the last row
##    
##    restr = restr_dict['ingredient_'+index]
##    restr.left_label.bind("<Button-1>", partial(update_var, current_recipe, restr, 'x'))
##    restr.right_label.bind("<Button-1>", partial(update_var, current_recipe, restr, 'y'))
##
##def edit_ingredients():
##    # Opens window that lets you add, delete, and edit oxide compositions of ingredients. Turn this into a class?
##    global ingredient_dict   # Get rid of this eventually?
##    global ingredient_editor
##    global i_e_scrollframe
##    global ing_dnd
##
##    try:
##        ingredient_editor.winfo_exists()
##        ingredient_editor.lift()
##    except:
##        ingredient_editor = Toplevel()
##
##        ingredient_editor_headings = Frame(ingredient_editor)
##        ingredient_editor_headings.pack()
##        i_e_scrollframe = VerticalScrolledFrame(ingredient_editor)
##        i_e_scrollframe.frame_height = 500
##        i_e_scrollframe.pack()
##        ingredient_editor_buttons = Frame(ingredient_editor)
##        ingredient_editor_buttons.pack()
##
##        # Place the headings on the ingredient_editor. There is some not-entirely-successful fiddling involved to try
##        # to get the headings to match up with their respective columns:
##        Label(master=ingredient_editor_headings, text='', width=5).grid(row=0, column=0)  # Blank label above the delete buttons
##        Label(master=ingredient_editor_headings, text='', width=5).grid(row=0, column=1)  # Blank label above the delete buttons
##        Label(master=ingredient_editor_headings, text='    Ingredient', width=20).grid(row=0, column=2)
##
##        c=3+1
##        for ox in oxides:
##            Label(master=ingredient_editor_headings, text=prettify(ox), width=5).grid(row=0, column=c)
##            c+=1
##
##        for i, attr in other_attr_dict.items():
##            Label(master=ingredient_editor_headings, text=attr.name, width=5).grid(row=0, column=c+attr.pos)
##
##        Label(master=ingredient_editor_headings, text='', width=5).grid(row=0, column=99)  # Blank label above the scrollbar
##        Label(master=ingredient_editor_headings, text='', width=5).grid(row=0, column=100)  # Blank label above the scrollbar
##
##        # Create drag manager for ingredient rows:
##        ing_dnd = DragManager(ingredient_dict, "./data/OrderShelf", 'ingredients', lambda ing, i: ing.display(i), reorder_ingredients)
##
##        # Create and display the rows:
##        for i, index in enumerate(ingredient_order):
##            ingredient_dict[index].displayable_version(index, i_e_scrollframe.interior, pre_delete_ingredient)
##            ingredient_dict[index].display(i)
##            ing_dnd.add_dragable(ingredient_dict[index].display_widgets['name'])    # This lets you drag the row corresponding to an ingredient by right-clicking on its name   
##                
##        # This label is hack to make sure that when a new ingredient is added, you don't have to scroll down to see it:
##        Label(master=i_e_scrollframe.interior).grid(row=9000) 
##
##        new_ingr_button = ttk.Button(ingredient_editor_buttons, text = 'New ingredient', width=20, command = new_ingredient)
##        new_ingr_button.pack(side='left')   
##        update_button = ttk.Button(ingredient_editor_buttons, text = 'Update', width=20, command = update_ingredient_dict)
##        update_button.pack(side='right')
##
##        i_e_scrollframe.interior.focus_force()

# SECTION 4.3
#
# Introduce the option of adding custom restrictions.  Users will define the numerator and denominator, which will be linear
# combinations of the lp_var[] variables.

def edit_other_restrictions():
    pass                           

# SECTION 4.4
# Set default user lower and upper bounds for all restrictions, and rearrange the order in which they are listed (with each group).
# Also set the number of decimal places to display for calculated bounds.
        
def restriction_settings():
    pass

# SECTION 5:
#
# Defines structures for the window on the left which allows users to add and remove ingredients and other restrictions to the problem.

ingredient_select_button={}

def toggle_ingredient(i):
    # Adds or removes ingredient_dict[i] to or from the current recipe, depending on whether it isn't or is an ingredient already.
    global current_recipe
    #global ingredient_select_button
    ingredient_compositions = get_ing_comp(ingredient_dict)
    
    if i in current_recipe.ingredients:
        current_recipe.ingredients.remove(i)
        ingredient_select_button[i].state(['!pressed'])
        restr_dict['ingredient_'+i].remove(current_recipe)
        current_recipe.update_oxides(restr_dict, entry_type.get())

##        if 'Na2O' in selected_oxides and 'K2O' in selected_oxides:
##            selected_oxides.add('KNaO')

        # Remove the restrictions on the oxides no longer present:
        for ox in set(ingredient_compositions[i]) - current_recipe.oxides:
            for et in ['umf_', 'mass_perc_', 'mole_perc_']:
                restr_dict[et+ox].remove(current_recipe)

    else:
        current_recipe.ingredients.append(i)
        ingredient_select_button[i].state(['pressed'])
        restr_dict['ingredient_'+i].display(101 + ingredient_order.index(i))
        for ox in ingredient_compositions[i]:
            if ox not in current_recipe.oxides:  # i.e. if we're introducing a new oxide
                for t in ['umf_', 'mass_perc_', 'mole_perc_']:
                    current_recipe.lower_bounds[t+ox] = restr_dict[t+ox].default_low
                    current_recipe.upper_bounds[t+ox] = restr_dict[t+ox].default_upp
        current_recipe.oxides = current_recipe.oxides.union(set(ingredient_compositions[i]))    # update the available oxides
           
        et = entry_type.get()
        for ox in current_recipe.oxides:
            restr_dict[et+ox].display(1 + oxide_dict[ox].pos)

    

def grid_ingr_select_buttons(frame):
    global ingredient_select_button
    for child in frame.winfo_children():
        child.destroy()

    for i, index in enumerate(ingredient_order):
        ingredient_select_button[index] = ttk.Button(frame, text=ingredient_dict[index].name, width=20,
                                                     command=partial(toggle_ingredient, index))
        ingredient_select_button[index].grid(row=i)

grid_ingr_select_buttons(vsf.interior)

# Other restrictions

other_select_button={}

def toggle_other(index):
    # Adds or removes other_dict[index] to or from the current recipe, depending on whether it isn't or is an other restriction already.
    
    global current_recipe
    global other_select_button

    if index in current_recipe.other:
        current_recipe.other.remove(index)
        other_select_button[index].state(['!pressed'])
        restr_dict['other_'+index].remove(current_recipe)
        # TO DO: remove star if this was a variable

    else:
        current_recipe.other.append(index)
        other_select_button[index].state(['pressed'])         
        restr_dict['other_'+index].display(1001 + other_dict[index].pos)
        restriction_sf.canvas.yview_moveto(1)

for index in other_dict:
    ot = other_dict[index]
    other_select_button[index] = ttk.Button(other_selection_window, text=prettify(ot.name),
                                               width=18, command=partial(toggle_other, index))
    other_select_button[index].grid(row=ot.pos+1)

# SECTION 6
# Create menus
file_menu = Menu(menubar, tearoff=0)    
file_menu.add_command(label="Recipes", command=open_recipe_menu)
file_menu.add_command(label="Save", command=save_recipe)
file_menu.add_command(label="Save as new recipe", command=save_new_recipe)
menubar.add_cascade(label="File", menu=file_menu)

option_menu.add_command(label="Edit Oxides", command=edit_oxides)
option_menu.add_command(label="Edit Ingredients",
                        command=lambda : ing_dat.open_ingredient_editor(current_recipe, recipe_dict,
                                                                        ingredient_select_button, toggle_ingredient, update_var, entry_type))
option_menu.add_command(label="Edit Other Restricitions", command=edit_other_restrictions)
option_menu.add_command(label="Restriction Settings", command=restriction_settings)
menubar.add_cascade(label="Options", menu=option_menu)

# SECTION 7
#
# Calculations. See the recipe_class file for definitions of calc_restrictions and calc_2d_projection

def calc():
    # Runs when you click on 'Calculate restrictions' (calcButton)

    root.lift()  # If this isn't here, the ingredient editor covers the main window whenever it's open. Sometimes it still does this.
                 # Don't ask me why.

    current_recipe.calc_restrictions(prob, lp_var, restr_dict)

##    if len(current_recipe.variables) == 2: # and restr_dict[current_recipe.variables['x']].normalization == restr_dict[current_recipe.variables['y']].normalization:
##        proj_frame = ttk.Frame(main_frame, padding=(15, 5, 10, 5))       

    current_recipe.calc_2d_projection(prob, lp_var, proj_canvas)
    
calc_button = ttk.Button(main_frame, text='Calculate restrictions', command=calc)

# SECTION 8
#
# Grid remaining widgets.

# Create and grid the percent/unity radio buttons:
unity_radio_button = Radiobutton(oxide_heading_frame, text="UMF", variable=entry_type, value='umf_',
                                 command=partial(update_oxide_entry_type, current_recipe, 'umf_'))
unity_radio_button.grid(column=0, row=1)

percent_wt_radio_button = Radiobutton(oxide_heading_frame, text="% weight", variable=entry_type, value='mass_perc_', \
                                      command=partial(update_oxide_entry_type, current_recipe, 'mass_perc_'))
percent_wt_radio_button.grid(column=1, row=1)

percent_mol_radio_button = Radiobutton(oxide_heading_frame, text="% mol", variable=entry_type, value='mole_perc_', \
                                       command=partial(update_oxide_entry_type, current_recipe, 'mole_perc_'))
percent_mol_radio_button.grid(column=2, row=1)

unity_radio_button.select()

# Grid calc button:
calc_button.grid()

# Grid the message frame.  At the moment, this isn't used.
message_frame.grid(row = 3)

# Display the first (default) recipe in list.
open_recipe('0', restr_dict)
    
root.config(menu=menubar)

#root.mainloop()  # Can be commented out on windows, but not linux or mac, it seems
