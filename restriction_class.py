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

from tkinter import *
from pretty_names import *
from functools import partial
import shelve
import copy
from gui_basic_framework import *  # we really just want restriction_sf.interior


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

class Ingredient:    # Ingredients will be referenced by their index, a string consisting of a unique natural number
    
    def __init__(self, pos, name='New ingredient', notes = '', oxide_comp = {}, other_attributes = {'LOI':0, 'cost':0, 'clay':0}):

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

        for i, attr in enumerate(['LOI', 'cost', 'clay']): # If we allow users to define their own attributes, we should have them indexed
                                                           # by positive integers, rather than the names of the attributes
            sdw[attr] = Entry(master = frame, width=5)
            sdw[attr].grid(row = r, column = c+i)
            sdw[attr].insert(0, self.other_attributes[attr])

    def pickleable_version(self):
        temp = copy.copy(self)
        temp.display_widgets = {}    # the values in self.display_widgets that the ingredient editor introduces can't be pickled 
        return temp

class Other:
    
    #'special case of restriction class, with added ability to edit in "Edit other" window'
    
    def __init__(self, pos, name, objective_defn, normalization, def_low, def_upp, dec_pt):
        'SiO2:Al2O3, LOI, cost, total clay, etc'

        self.pos = pos  # determines order in which other restrictions are displayed
        self.name = name
        self.objective_defn = objective_defn   # a text string that describes a linear combination of lp_var variables
                                               # we may have to change this to a list of four dictionaries giving the coefficients
                                               # of lp_var[ox_umf], lp_var[ox_wt_%], lp_var[ingredient.name+'ingredient']
        self.normalization = normalization     # similar comments as above
        self.def_low = def_low
        self.def_upp = def_upp
        self.dec_pt = dec_pt
    def display(self, frame):     # To be used in the 'Edit other' window.
        pass

if 1 == 1:
    with shelve.open("OtherShelf") as other_shelf:
        for index in other_shelf:
            del other_shelf[index]
        other_shelf['0'] = Other(0,'SiO2_Al2O3', "lp_var['mole_SiO2']", "lp_var['mole_Al2O3']", 13, 18, 2)   # Using 'SiO2:Al2O3' gives an error
        other_shelf['1'] = Other(1,'LOI', "sum(ingredient_data[index].other_attributes['0']* \
                                   lp_var['ingredient_'+index] for index in self.ingredients)", \
                                "lp_var['ingredient_total']", 0, 100, 1)    # Getting the error 'name 'ingredient_data' is not defined'
        other_shelf['2'] = Other(2,'cost', "lp_var['mole_SiO2']", "lp_var['ingredient_total']", 0, 100, 1)    # Not working yet
        other_shelf['3'] = Other(3,'Total clay', "lp_var['mole_SiO2']", "lp_var['ingredient_total']", 0, 100, 1)  # Not working yet
        
        other_dict = dict(other_shelf)
else:
    other_dict = update_other()

# oxide_shelf should be a dictionary of the form
# {'SiO2' : Oxide(1, 60.083, 0), 'Al2O3' : Oxide(2, 101.961, 0), ...}

restr_dict = {}  # a dictionary with keys of the form 'umf_'+ox, 'wt_perc_'+ox, 'mole_perc_'+ox, 'ingredient_'+index or 'other_'+index

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
        restr_dict['mass_perc_'+ox] = Restriction('mass_perc_'+ox, ox, 'mass_'+ox, "lp_var['ox_mass_total']", 0, 100, dec_pt = 2) 
        restr_dict['mole_perc_'+ox] = Restriction('mole_perc_'+ox, ox, 'mole_'+ox, "lp_var['ox_mole_total']", 0, 100, dec_pt = 2)


with shelve.open("IngredientShelf") as ingredient_shelf:   # If there are a large number of ingredients, maybe it's better to only create the corresponding restrictions
                                                         # once they're selected for a particular recipe.
    for index in ingredient_shelf:
        restr_dict['ingredient_'+index] = Restriction('ingredient_'+index, ingredient_shelf[index].name, 'ingredient_'+index, "lp_var['ingredient_total']", 0, 100)
   
with shelve.open("OtherShelf") as other_shelf:
    for index in other_shelf:
        ot = other_shelf[index]    # instance of 'Other' class
        restr_dict['other_'+index] = Restriction('other_'+index, ot.name, 'other_'+index, ot.normalization, ot.def_low, ot.def_upp, dec_pt=ot.dec_pt)




