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

# We define the Restriction, Oxide, Ingredient,and Other classes

from tkinter import *
from pretty_names import *
from functools import partial
import shelve
import copy

from gui_basic_framework import *  # we really just want restriction_sf.interior
from pulp import *

initialize_oxides = 0       # Run script with initialize_oxides = 1 whenever the Oxide class is changed
initialize_ingredients = 0  # Run script with initialize_ingredients = 1 whenever the Ingredient class is changed
initialize_other = 0        # Run script with initialize_other = 1 whenever the Other class is changed

class Restriction:
    'Oxide UMF, oxide % molar, oxide % weight, ingredient, SiO2:Al2O3 molar, LOI, cost, etc'
    
    def __init__(self, index, name, objective_func, normalization, default_low, default_upp, dec_pt = 1):

        self.index = index     # We will always have restr_dict[index] = Restriction(index, ...)
        self.name = name
        self.objective_func = objective_func
        self.normalization = normalization
        self.default_low = default_low
        self.default_upp = default_upp
        self.dec_pt = dec_pt
        
        self.calc_bounds = {}   

        self.left_label_text = StringVar()
        self.left_label_text.set('  '+prettify(self.name)+' : ')
        self.left_label = Label(restriction_sf.interior, textvariable = self.left_label_text)
        
        self.low = DoubleVar()
        self.lower_bound = Entry(restriction_sf.interior, textvariable = self.low, width=5, fg = 'blue') #user lower bound
        self.low.set(self.default_low)

        self.upp = DoubleVar()
        self.upper_bound = Entry(restriction_sf.interior, textvariable = self.upp, width=5, fg = 'blue') #user upper bound
        self.upp.set(self.default_upp)

        for eps in [-1,1]:
            self.calc_bounds[eps] = Label(restriction_sf.interior, bg = 'white', fg = 'red', width = 5) #calculated lower and upper bounds
            self.calc_bounds[eps].config(text = ' ')

        self.right_label_text = StringVar()
        self.right_label_text.set(' : '+prettify(self.name)+'   ')
        self.right_label = Label(restriction_sf.interior, textvariable = self.right_label_text)

    def select(self, t):
        if t == 'x':
            self.left_label_text.set('* '+prettify(self.name)+' : ')
        elif t == 'y':
            self.right_label_text.set(' : '+prettify(self.name)+' *')
        else:
            print('Something\'s wrong')

    def deselect(self, t):
        if t == 'x':
            self.left_label_text.set('  '+prettify(self.name)+' : ')
        elif t == 'y':
            self.right_label_text.set(' : '+prettify(self.name)+'  ')
        else:
            print('Something\'s wrong')
                    
    def display(self, line):

        self.left_label.grid(row = line, column=0, sticky=E)        # grid left restriction name
        
        self.lower_bound.grid(row = line, column=1)                 # grid lower bound entry box      
        self.upper_bound.grid(row = line, column=2)                 # grid upper bound entry box
    
        self.calc_bounds[-1].grid(row = line, column=4)             # grid calculated lower bound box
        self.calc_bounds[1].grid(row = line, column=5)             # grid calculated upper bound box

        self.right_label.grid(row = line, column=6, sticky=W)       # grid right restriction name

    def remove(self, recipe):
        for widget in [self.left_label, self.lower_bound, self.upper_bound, self.calc_bounds[-1], self.calc_bounds[1],
                       self.right_label]:
            widget.grid_forget()    # remove widgets corresponding to that restriction
        self.low.set(self.default_low)
        self.upp.set(self.default_upp)
        for eps in [-1,1]:
            self.calc_bounds[eps].config(text = '')
        v = dict(recipe.variables)
        for t in v:
            if self == recipe.variables[t]:
                self.deselect(t)
                del recipe.variables[t]

    def hide(self):  # to be used with oxide options
        for widget in [self.left_label, self.lower_bound, self.upper_bound, self.calc_bounds[-1], self.calc_bounds[1],
                       self.right_label]:
            widget.grid_forget()

    def display_calc_bounds(self):
        for eps in [-1,1]:
            self.calc_bounds[eps].config(text = ('%.'+str(self.dec_pt)+'f') % self.calc_value[eps])

class Oxide:
    
     def __init__(self, pos, molar_mass, flux, min_threshhold=0):
         'SiO2, Al2O3, B2O3, MgO, CaO, etc'

         self.pos = pos  # determines order in which oxides are displayed
         self.molar_mass = molar_mass
         self.flux = flux  # either 0 or 1 (for now)
         self.min_threshhold = min_threshhold  # don't display this oxide if none of the selected ingredients has more than min_threshhold % wt of that oxide

     def display(self, frame):     #To be used in the 'Edit oxides' window. Only apply this to copies of things in shelve
         pass

with shelve.open("OxideShelf") as oxide_shelf:
    oxides = [ox for ox in oxide_shelf]

other_attr_names = {'0':'LOI', '1':'cost','2':'clay'}  # This should probably be a dictionary where the values are instances of
                                                      # a yet-to-be-defined 'other_attribute' class. This class will have the
                                                      # attributes pos and name.

class Ingredient:    # Ingredients will be referenced by their index, a string consisting of a unique natural number
    
    def __init__(self, pos, name='New ingredient', notes = '', oxide_comp = {}, other_attributes = {'0':0, '1':0, '2':0}):

        self.pos = pos      # position of the ingredient in the list of ingredients to choose from, and in the ingredient editor
        self.name = name
        self.notes = notes  # not implemented yet. Intended to show up in the 'Edit ingredients' window.
        self.oxide_comp = oxide_comp  # dictionary giving weight percent of each oxide in the ingredient
        self.other_attributes = other_attributes
        self.display_widgets = {}

    def display(self, index, frame, delete_ingredient_fn):     #To be used in the 'Edit ingredients' window. Only apply this to copies of things in shelve
        r = self.pos + 1
        sdw = self.display_widgets
        sdw['del'] =  ttk.Button(master=frame, text = 'X', width=2,
                                 command = partial(delete_ingredient_fn, index))   
        sdw['del'].grid(row=r, column=0)
        sdw['name'] = Entry(master=frame, width=25)
        sdw['name'].grid(row = r, column=1)
        sdw['name'].insert(0, self.name)

        c=3
        for ox in oxides:
            sdw[ox] = Entry(master = frame,  width=5)  #percent weight of the oxide that the ingredient contains
            sdw[ox].grid(row = r, column=c)
            sdw[ox].delete(0,END)
            if ox in self.oxide_comp:
                sdw[ox].insert(0, self.oxide_comp[ox])
            else:
                pass
            c+=1

        for i in other_attr_names: # If we allow users to define their own attributes, we should have them indexed
                                                           # by positive integers, rather than the names of the attributes
            sdw[i] = Entry(master = frame, width=5)
            sdw[i].grid(row = r, column = c+int(i))             # replace int(i) by other_attr_dict[i].pos
            sdw[i].insert(0, self.other_attributes[i])

    def pickleable_version(self):
        temp = copy.copy(self)
        temp.display_widgets = {}    # the values in self.display_widgets that the ingredient editor introduces can't be pickled 
        return temp

class Other:
    
    #'special case of restriction class, with added ability to edit in "Edit other" window'
    
    def __init__(self, pos, name, numerator_coefs, normalization, def_low, def_upp, dec_pt):
        'SiO2:Al2O3, LOI, cost, total clay, etc'

        self.pos = pos  # determines order in which other restrictions are displayed
        self.name = name
        self.numerator_coefs = numerator_coefs   # a dictionary with keys of the form mass_ox, mole_ox, ingredient_i,
                                                 # and values real numbers that are the coefficients in the linear
                                                 # combination of basic variables that define the numerator.
        self.normalization = normalization     # For now, just a text string of the form 'lp_var[...]'
        self.def_low = def_low
        self.def_upp = def_upp
        self.dec_pt = dec_pt
    def display(self, frame):     # To be used in the 'Edit other' window.
        pass


# oxide_shelf should be a dictionary of the form
# {'SiO2' : Oxide(1, 60.083, 0), 'Al2O3' : Oxide(2, 101.961, 0), ...}

restr_dict = {}  # a dictionary with keys of the form 'umf_'+ox, 'mass_perc_'+ox, 'mole_perc_'+ox, 'ingredient_'+index or 'other_'+index

with shelve.open("OxideShelf") as oxide_shelf:
    for ox in oxide_shelf:   # create oxide restrictions
        def_upp = 1   # default upper bound for oxide UMF
        dp = 3
        if ox == 'SiO2':
            def_upp = 100
            dp = 2
        elif ox == 'Al2O3':
            def_upp = 10
        restr_dict['umf_'+ox] = Restriction('umf_'+ox, ox, 'mole_'+ox, "lp_var['fluxes_total']", 0, def_upp, dec_pt = dp)
        restr_dict['mass_perc_'+ox] = Restriction('mass_perc_'+ox, ox, 'mass_'+ox, "0.01*lp_var['ox_mass_total']", 0, 100, dec_pt = 2) 
        restr_dict['mole_perc_'+ox] = Restriction('mole_perc_'+ox, ox, 'mole_'+ox, "0.01*lp_var['ox_mole_total']", 0, 100, dec_pt = 2)


with shelve.open("IngredientShelf") as ingredient_shelf:   # If there are a large number of ingredients, maybe it's better to only create the corresponding restrictions
                                                         # once they're selected for a particular recipe.
    ingredient_dict = dict(ingredient_shelf)     # This is defined again in GUI.py. Will give trouble if initialize_ingredients == 1 in GUI.py.
                                                 # Need to rethink
    for index in ingredient_shelf:
        restr_dict['ingredient_'+index] = Restriction('ingredient_'+index, ingredient_shelf[index].name, 'ingredient_'+index, "0.01*lp_var['ingredient_total']", 0, 100)

if 1 == 1:
    with shelve.open("OtherShelf") as other_shelf:
        for index in other_shelf:
            del other_shelf[index]
        other_shelf['0'] = Other(0,'SiO2_Al2O3', {'mole_SiO2':1}, "lp_var['mole_Al2O3']", 3, 18, 2)   # Using 'SiO2:Al2O3' gives an error
        other_shelf['1'] = Other(1,'KNaO UMF', {'mole_K2O':1, 'mole_Na2O':1}, "lp_var['fluxes_total']", 0, 1, 3)
        other_shelf['2'] = Other(2,'KNaO % mol', {'mole_K2O':1, 'mole_Na2O':1}, "0.01*lp_var['ox_mole_total']", 0, 100, 1)
        other_att_3 = {'ingredient_'+index : 0.01*float(ingredient_dict[index].other_attributes['2']) for index in ingredient_dict}
        other_shelf['3'] = Other(3,'Total clay', {k:v for k,v in other_att_3.items() if v>0}, "0.01*lp_var['ingredient_total']", 0, 100, 1)
        other_att_4 = {'ingredient_'+index : 0.01*float(ingredient_dict[index].other_attributes['0']) for index in ingredient_dict}
        other_shelf['4'] = Other(4,'LOI',  {k:v for k,v in other_att_4.items() if v>0}, "0.01*lp_var['ingredient_total']", 0, 100, 1)
        other_att_5 = {'ingredient_'+index : 0.01*float(ingredient_dict[index].other_attributes['1']) for index in ingredient_dict}
        other_shelf['5'] = Other(5,'cost', {k:v for k,v in other_att_5.items() if v>0}, "0.01*lp_var['ingredient_total']", 0, 100, 1)
        
        other_dict = dict(other_shelf)
else:
    other_dict = update_other()
    
with shelve.open("OtherShelf") as other_shelf:
    for index in other_shelf:
        ot = other_shelf[index]    # instance of 'Other' class
        restr_dict['other_'+index] = Restriction('other_'+index, ot.name, 'other_'+index, ot.normalization, ot.def_low, ot.def_upp, dec_pt=ot.dec_pt)

## SECTION 0
# Initialize the oxide_dict, ingredient_dict, and other_dict dictionaries
# Define default recipe bounds (optional)
# Set up the linear programming problem. Define variables, and set constraints that always hold (unless any
# of the dictionaries above are modified)

# Initialize oxides:  

if initialize_oxides == 1:
    import oxidefile

    with shelve.open("OxideShelf") as oxide_shelf:
        for ox in oxide_shelf:
            del oxide_shelf[ox]
        for (pos, ox) in enumerate(oxidefile.oxides):
            if ox in oxidefile.fluxes:
                ox_init = Oxide(pos, molar_mass = oxidefile.molar_mass_dict[ox], flux = 1)
            else:
                ox_init = Oxide(pos, molar_mass = oxidefile.molar_mass_dict[ox], flux = 0)
            oxide_shelf[ox] = ox_init
else:
    pass

def update_ox():
    global oxides
    global molar_masses
    with shelve.open("OxideShelf") as oxide_shelf:
        oxides = [ox for ox in oxide_shelf]
        molar_masses = {ox:oxide_shelf[ox].molar_mass for ox in oxide_shelf}
        return dict(oxide_shelf)
    
oxide_dict = update_ox()

# Define ingredients.

def update_ing():
    with shelve.open("IngredientShelf") as ingredient_shelf:
        return dict(ingredient_shelf)

if initialize_ingredients == 1:
    from ingredientfile import *
    with shelve.open("IngredientShelf") as ingredient_shelf:
        for index in ingredient_shelf:
            del ingredient_shelf[index]
        for (pos, ing) in enumerate(ingredient_names):  # Here we're taking the position to be the index

            ing_init = Ingredient(pos, name=ing, oxide_comp = dict([(ox, ingredient_compositions[ing][ox]) \
                                                                    for ox in oxides if ox in ingredient_compositions[ing]]))

            for attr in ['0', '1', '2']:
                if attr in ingredient_compositions[ing]:
                    ing_init.other_attributes[attr] = ingredient_compositions[ing][attr]
                else:
                    ing_init.other_attributes[attr] = 0
            
            ingredient_shelf[str(pos)] = ing_init
else:
    pass

ingredient_dict = update_ing()

def get_ing_comp():
    ingredient_compositions = {}
    for index in ingredient_dict:
        ingredient_compositions[index] = ingredient_dict[index].oxide_comp
    return ingredient_compositions

ingredient_compositions = get_ing_comp()

# Initialize other

def update_other():
    with shelve.open("OtherShelf") as other_shelf:
        other_dict = dict(other_shelf)
        return other_dict
        
if initialize_other == 1:
    with shelve.open("OtherShelf") as other_shelf:
        for index in other_shelf:
            del other_shelf[index]
        other_shelf['0'] = Other(0,'SiO2_Al2O3', {'mole_SiO2':1}, "lp_var['mole_Al2O3']", 3, 18, 2)   # Using 'SiO2:Al2O3' gives an error
        other_shelf['1'] = Other(1,'LOI', {'ingredient_'+index : 0.01*float(ingredient_dict[index].other_attributes['LOI']) for index in ingredient_dict if float(ingredient_dict[index].other_attributes['LOI'])>0}, \
                                "lp_var['ingredient_total']", 0, 100, 1)
        other_shelf['2'] = Other(2,'cost', {'ingredient_'+index : 0.01*float(ingredient_dict[index].other_attributes['cost']) for index in ingredient_dict if float(ingredient_dict[index].other_attributes['cost'])>0}, \
                                "lp_var['ingredient_total']", 0, 100, 1)
        other_shelf['3'] = Other(3,'Total clay', {'ingredient_'+index : 0.01*float(ingredient_dict[index].other_attributes['clay']) for index in ingredient_dict if float(ingredient_dict[index].other_attributes['clay'])>0}, \
                                "lp_var['ingredient_total']", 0, 100, 1)
        
        other_dict = dict(other_shelf)
else:
    other_dict = update_other()


# Set up variables and universal restrictions for LP problem

prob = pulp.LpProblem('Glaze recipe', pulp.LpMaximize)
lp_var = {}     # dictionary for the variables in the linear programming problem prob. Should this be an instance of the Restr_Index class?

for total in ['ingredient_total', 'fluxes_total', 'ox_mass_total', 'ox_mole_total']:
    lp_var[total] = pulp.LpVariable(total, 0, None, pulp.LpContinuous)           # used to normalize

for index in ingredient_dict:
    ing = 'ingredient_'+index
    lp_var[ing] = pulp.LpVariable(ing, 0, None, pulp.LpContinuous)
    
for ox in oxide_dict:
    lp_var['mole_'+ox] = pulp.LpVariable('mole_'+ox, 0, None, pulp.LpContinuous)
    lp_var['mass_'+ox] = pulp.LpVariable('mass_'+ox, 0, None, pulp.LpContinuous)
    prob += lp_var['mole_'+ox]*oxide_dict[ox].molar_mass == lp_var['mass_'+ox]   # relate mole percent and unity
    prob += sum(ingredient_compositions[index][ox]*lp_var['ingredient_'+index]/100 \
                for index in ingredient_dict if ox in ingredient_compositions[index]) \
            == lp_var['mass_'+ox], ox     # relate ingredients and oxides

##for index in other_attributes:
##    lp_var['other_attr_'+index] = pulp.LpVariable('other_attr_'+index, 0, None, pulp.LpContinuous)
##    # For each 'other attribute' we will generate a corresponding 'other variable'

for index in other_dict:
    ot = 'other_'+index
    coefs = other_dict[index].numerator_coefs
    #print(coefs)
    linear_combo = [(lp_var[key], coefs[key]) for key in coefs]
    #print(linear_combo)
    lp_var[ot] = pulp.LpVariable(ot, 0, None, pulp.LpContinuous)
    prob += lp_var[ot] == LpAffineExpression(linear_combo)         # relate this variable to the other variables.

prob += lp_var['ingredient_total'] == sum(lp_var['ingredient_'+index] for index in ingredient_dict), 'ing_total'
prob += lp_var['fluxes_total'] == sum(oxide_dict[ox].flux*lp_var['mole_'+ox] for ox in oxide_dict)
prob += lp_var['ox_mass_total'] == sum(lp_var['mass_'+ox] for ox in oxide_dict)
prob += lp_var['ox_mole_total'] == sum(lp_var['mole_'+ox] for ox in oxide_dict)


