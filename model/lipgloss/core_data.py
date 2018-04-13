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

# We define the Restriction, Oxide, Ingredient,and Other classes.

from functools import partial
import shelve
#from .serializers.recipeserializer import RecipeSerializer
from inspect import getsourcefile
import os
from os.path import abspath, dirname
import sys


reset_oxides = 0
reset_ingredients = 0
reset_other = 0

##persistent_data_path = dirname(abspath(getsourcefile(lambda:0)))+'/persistent_data'  # please tell me there's an easier way to import stuff in Python
##sys.path.append(persistent_data_path)

class Observable:
    def __init__(self, initialValue=None):
        #self.data = initialValue
        self.callbacks = {}

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callback[func]

    def _docallbacks(self, attribute):
        for func in self.callbacks:
             func(getattr(self, attribute))

    def set(self, attribute, value):
        setattr(self, attribute, value)
        self._docallbacks(attribute)

    def get(self, attribute):              # Is this necessary?
        return getattr(self, attribute)

    def unset(self, attribute):
        self.attribute = None

class Oxide():

##    order = []
##
##    def update_order():
##        with shelve.open(persistent_data_path+"/OrderShelf") as order_shelf:
##            order_shelf['oxides'] = Oxide.order
    
    def __init__(self, pos, molar_mass, flux, min_threshhold=0):
        
        'SiO2, Al2O3, B2O3, MgO, CaO, etc'
    
        Observable.__init__(self)
        self.pos = pos  # Determines order in which oxides are displayed.
        self.molar_mass = molar_mass
        self.flux = flux  # Either 0 or 1 (for now).
        self.min_threshhold = min_threshhold  # Don't display this oxide if none of the selected ingredients has more than min_threshhold % wt of that oxide

##    def display(self, frame):     # To be used in the 'Edit oxides' window. Only apply this to copies of things in shelve.
##        pass

def oxide_reset():

    import oxidefile

    with shelve.open(persistent_data_path+"/OxideShelf") as oxide_shelf:
        for ox in oxide_shelf:
             del oxide_shelf[ox]
        #Oxide.order = []
        for (pos, ox) in enumerate(oxidefile.oxides):
             Oxide.order.append(ox)
             if ox in oxidefile.fluxes:
                  ox_init = Oxide(pos, molar_mass=oxidefile.molar_mass_dict[ox], flux=1)
             else:
                  ox_init = Oxide(pos, molar_mass=oxidefile.molar_mass_dict[ox], flux=0)
             oxide_shelf[ox] = ox_init

    Oxide.update_order()

if reset_oxides == 1:
    oxide_reset()
else:
    pass
        
class OxideData():
    
    '''Abstract class used to store a dictionary of oxides'''
    
    oxide_dict = {}

    @staticmethod
    def oxides():
        return OxideData.oxide_dict.keys()

    def set_default_oxides():
        OxideData.oxide_dict = {}
        from .default_data import oxidefile as oxidefile
        for (pos, ox) in enumerate(oxidefile.oxides):
             if ox in oxidefile.fluxes:
                  ox_init = Oxide(pos, molar_mass=oxidefile.molar_mass_dict[ox], flux=1)
             else:
                  ox_init = Oxide(pos, molar_mass=oxidefile.molar_mass_dict[ox], flux=0)
             OxideData.oxide_dict[ox] = ox_init

    def __init__(self):
        pass
        
##    def update_oxides(self, new_oxide_dict):
##	OxideData.oxide_dict = new_oxide_dict    # check that this works
##	                                         # add stuff to modify ingredient_dict, self.other_dict etc.

# Define Ingredient class.  Ingredients will be referenced by their index, a string consisting of a unique natural number.
class Ingredient(Observable):

##    order = []
##
##    def update_order():
##        with shelve.open(persistent_data_path+"/OrderShelf") as order_shelf:
##            order_shelf['ingredients'] = Ingredient.order
    
    def __init__(self, name='New ingredient', notes='', oxide_comp={}, other_attributes={}, glaze_calculator_ids={}):

        Observable.__init__(self)
        self.name = name
        # notes not implemented yet.
        self.notes = notes
        # oxide_comp is a dictionary giving the weight percent of each oxide in the ingredient.
        self.oxide_comp = oxide_comp
        # other attributes is a dictionary giving the values of each other attribute of the ingredient
        self.other_attributes = other_attributes
        # glaze_calculator_ids is a dictionary with keys being strings referring to various glaze calc software,
        # and values being the corresponding index in that software that encodes the ingredient
        self.glaze_calculator_ids = glaze_calculator_ids

##    def displayable_version(self, index, frame, delete_ingredient_fn):   # move to view
##        # To be used in the 'Edit ingredients' window.  Only apply this to copies of things in shelve.
##        sdw = self.display_widgets
##        sdw['del'] =  ttk.Button(master=frame, text='X', width=2, command = partial(delete_ingredient_fn, index))
####        sdw['del'] =  ttk.Label(master=frame, text='X', width=2)
####        sdw['del'].bind('<Button-1>', partial(delete_ingredient_fn, index))
##        sdw['name'] = Entry(master=frame, width=20)
##        sdw['name'].insert(0, self.name)
##
##        c = 3
##        
##        for ox in oxides:
##            # Use this entry widget to input the percent weight of the oxide that the ingredient contains.
##            sdw[ox] = Entry(master=frame,  width=5)  
##            sdw[ox].delete(0, END)
##            if ox in self.oxide_comp:
##                sdw[ox].insert(0, self.oxide_comp[ox])
##            else:
##                pass
##            c += 1
##
##        for i, other_attr in other_attr_dict.items(): 
##            sdw['other_attr_'+i] = Entry(master=frame, width=5)
##            if i in self.other_attributes:
##                sdw['other_attr_'+i].insert(0, self.other_attributes[i])
##
##    def display(self, pos):
##        sdw = self.display_widgets
##        sdw['del'].grid(row=pos, column=0)
##        sdw['name'].grid(row=pos, column=1, padx=3, pady=3)
##
##        c = 3
##        
##        for ox in oxides:
##            sdw[ox].grid(row=pos, column=c, padx=3, pady=1)
##            c += 1
##
##        for i, other_attr in other_attr_dict.items(): 
##            sdw['other_attr_'+i].grid(row=pos, column=c+other_attr.pos, padx=3, pady=3)
##
##    def pickleable_version(self):   
##        temp = copy.copy(self)
##        # The values in self.display_widgets that the ingredient editor introduces can't be pickled, so we discard them:
##        temp.display_widgets = {}    
##        return temp

def ingredient_reset():
    import ingredientfile
        
    with shelve.open(persistent_data_path+"/IngredientShelf") as ingredient_shelf:
        for index in ingredient_shelf:
            del ingredient_shelf[index]

        temp_order_list = []
        for (pos, ing) in enumerate(ingredientfile.ingredient_names):

            temp_order_list.append(str(pos))

            ing_init = Ingredient(name=ing, oxide_comp=dict([(ox, ingredientfile.ingredient_compositions[ing][ox]) \
                                                                   for ox in OxideData.oxides() if ox in ingredientfile.ingredient_compositions[ing]]),\
                                  other_attributes = {})

            for attr in []: #other_attr_dict:
                try:
                    ing_init.other_attributes[attr] = ingredientfile.ingredient_compositions[ing][attr]
                except:
                    pass
            
            ingredient_shelf[str(pos)] = ing_init

    Ingredient.order = temp_order_list
    Ingredient.update_order()

if reset_ingredients == 1:
    ingredient_reset()
else:
    pass

# Define Other class:
class Other(Observable):
    
    def __init__(self, pos, name, numerator_coefs, normalization, def_low, def_upp, dec_pt):
        'SiO2:Al2O3, LOI, cost, total clay, etc'

        # pos determines order in which other restrictions are displayed.
        self.pos = pos
           
        self.name = name
        
        # numerator_coefs is a dictionary with keys of the form mass_ox, mole_ox, ingredient_i,
        # and values real numbers that are the coefficients in the linear combination of basic
        # variables that define the numerator.
        self.numerator_coefs = numerator_coefs
        
        # For now, normalization is just a text string of the form 'self.lp_var[...]'.
        self.normalization = normalization
        
        self.def_low = def_low
        
        self.def_upp = def_upp
        
        self.dec_pt = dec_pt

def get_ing_comp(ingredient_dict):
    ingredient_compositions = {}
    for index in ingredient_dict:
        ingredient_compositions[index] = ingredient_dict[index].oxide_comp
    return ingredient_compositions

class CoreData(OxideData):
    '''Class used to store the dictionaries of ingredients and 'other' restrictions, as well as
       the dictionary of other attributes ingredients may have'''

##    recipe_dict = {}
##
##    current_recipe = None
    
    def __init(self):
        self.other_attr = {}
        self.ingredient_dict = {}
        self.ingredient_compositions = {}    # Could do without this  
        self.other_dict = {}
        self.default_lower_bounds = {}
        self.default_upper_bounds = {}

    def restr_keys(self):
        return [t+ox for t in ['umf_', 'mass_perc_', 'mole_perc_'] for ox in self.oxide_dict]+\
           ['ingredient_'+i for i in self.ingredient_dict]+\
           ['other_'+ot for ot in self.other_dict]

    def associated_oxides(self, ingredients):
        assoc_oxides = set()
        for index in ingredients:
            assoc_oxides = assoc_oxides.union(set(self.ingredient_compositions[index]))  # update the available oxides. Probably not the most
                                                                                                      # efficient way to do this
        return assoc_oxides

    def set_default_data(self):
             
        self.other_attr_dict = {'0': 'LOI', '2': 'Clay', '1': 'Cost'}

        self.ingredient_dict = {}
        from .default_data import ingredientfile as ingredientfile
        for pos, ing in enumerate(ingredientfile.ingredient_names):
            ox_comp = dict([(ox, ingredientfile.ingredient_compositions[ing][ox]) \
                            for ox in self.oxides() if ox in ingredientfile.ingredient_compositions[ing]])
            ing_init = Ingredient(name=ing, oxide_comp=ox_comp, other_attributes={})
            for attr in self.other_attr_dict:
                try:
                    ing_init.other_attributes[attr] = ingredientfile.ingredient_compositions[ing][attr]
                except:
                    pass  
            self.ingredient_dict[str(pos)] = ing_init
        self.ingredient_compositions = get_ing_comp(self.ingredient_dict) 

        self.other_dict = {}
        self.other_dict['0'] = Other(0, 'SiO2_Al2O3', {'mole_SiO2':1}, "self.lp_var['mole_Al2O3']", 3, 18, 2)   # Using 'SiO2:Al2O3' gives an error
        self.other_dict['1'] = Other(1, 'KNaO UMF', {'mole_K2O':1, 'mole_Na2O':1}, "self.lp_var['fluxes_total']", 0, 1, 3)
        self.other_dict['2'] = Other(2, 'KNaO % mol', {'mole_K2O':1, 'mole_Na2O':1}, "0.01*self.lp_var['ox_mole_total']", 0, 100, 2)
        self.other_dict['3'] = Other(3, 'RO UMF', {'mole_MgO':1, 'mole_CaO':1, 'mole_BaO':1, 'mole_SrO':1}, "self.lp_var['fluxes_total']", 0, 1, 3)

        other_att_4 = {'ingredient_'+index : 0.01*float(self.ingredient_dict[index].other_attributes['2'])\
                       for index in self.ingredient_dict if '2' in self.ingredient_dict[index].other_attributes}
        self.other_dict['4'] = Other(4, 'Total clay', {k:v for k,v in other_att_4.items() if v>0}, "0.01*self.lp_var['ingredient_total']", 0, 100, 1)
        other_att_5 = {'ingredient_'+index : 0.01*float(self.ingredient_dict[index].other_attributes['0'])\
                       for index in self.ingredient_dict if '0' in self.ingredient_dict[index].other_attributes}
        self.other_dict['5'] = Other(5, 'LOI',  {k:v for k,v in other_att_5.items() if v>0}, "0.01*self.lp_var['ingredient_total']", 0, 100, 1)
        other_att_6 = {'ingredient_'+index : 0.01*float(self.ingredient_dict[index].other_attributes['1'])\
                       for index in self.ingredient_dict if '1' in self.ingredient_dict[index].other_attributes}
        self.other_dict['6'] = Other(6, 'cost', {k:v for k,v in other_att_6.items() if v>0}, "0.01*self.lp_var['ingredient_total']", 0, 100, 1)

        self.default_lower_bounds = {}
        self.default_upper_bounds = {}
        for key in self.restr_keys():
            self.default_lower_bounds[key] = 0
            self.default_upper_bounds[key] = 100

        #with the exception of the following:
        self.default_upper_bounds['umf_Al2O3'] = 10
        for ox in ['B2O3', 'MgO', 'CaO', 'Na2O', 'K2O', 'ZnO', 'Fe2O3', 'TiO2', 'P2O5']:
            self.default_upper_bounds['umf_'+ox] = 1
        self.default_lower_bounds['other_0'] = 1

    def set_ingredient_dict(self, path):    # change to JSON?
        with shelve.open(path) as ingredient_shelf:
            self.ingredient_dict = dict(ingredient_shelf)
        self.ingredient_compositions = get_ing_comp(self.ingredient_dict) 

    def set_other_dict(self, path):
        with shelve.open(path) as other_shelf:
            self.other_dict = dict(other_shelf)

    def set_default_bounds(self, path):
        with shelve.open(path) as other_shelf:
            self.other_dict = dict(other_shelf)

    def add_ingredient(self, ing):
        m = max([int(j) for j in self.ingredient_dict]) + 1
        i = str(m)
        self.ingredient_dict[i] = ing
        self.ingredient_compositions[i] = ingredient_dict[i].oxide_comp

    def remove_ingredient(self, i):
        del self.ingredient_dict[i]
        del self.ingredient_compositions[i]
    
            
##        self.set_current_recipe('0')
##
##    def set_current_recipe(self, i):
##        CoreData.current_recipe = self.recipe_dict[i]  
##
##    def update_ingredient_data(self, new_dict):
##        self.ingredient_dict = new_dict
##        self.ingredient_compositions = get_ing_comp(new_dict)
##
##    def update_other_data(self, new_dict):
##        self.self.other_dict = new_dict


    #def add/delete ingredient /other
        


