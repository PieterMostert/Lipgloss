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
#import shelve
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
    
    def __init__(self, molar_mass, flux, min_threshhold=0):
        
        'SiO2, Al2O3, B2O3, MgO, CaO, etc'
    
        Observable.__init__(self)
        self.molar_mass = molar_mass
        self.flux = flux  # Either 0 or 1 (for now).
        self.min_threshhold = min_threshhold  # Don't display this oxide if none of the selected ingredients has more than min_threshhold % wt of that oxide

def oxide_reset():

    import oxidefile

    with shelve.open(persistent_data_path+"/OxideShelf") as oxide_shelf:
        for ox in oxide_shelf:
             del oxide_shelf[ox]
        #Oxide.order = []
        for (pos, ox) in enumerate(oxidefile.oxides):
             Oxide.order.append(ox)
             if ox in oxidefile.fluxes:
                  ox_init = Oxide(molar_mass=oxidefile.molar_mass_dict[ox], flux=1)
             else:
                  ox_init = Oxide(molar_mass=oxidefile.molar_mass_dict[ox], flux=0)
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

    @staticmethod
    def set_default_oxides():
        OxideData.oxide_dict = {}
        from .default_data import oxidefile as oxidefile
        for (pos, ox) in enumerate(oxidefile.oxides):
             if ox in oxidefile.fluxes:
                  ox_init = Oxide(pos, molar_mass=oxidefile.molar_mass_dict[ox], flux=1)
             else:
                  ox_init = Oxide(pos, molar_mass=oxidefile.molar_mass_dict[ox], flux=0)
             OxideData.oxide_dict[ox] = ox_init

##    def __init__(self):
##        pass
        
##    def update_oxides(self, new_oxide_dict):
##	OxideData.oxide_dict = new_oxide_dict    # check that this works
##	                                         # add stuff to modify ingredient_dict, self.other_dict etc.

# Define Ingredient class.  Ingredients will be referenced by their index, a string consisting of a unique natural number.
class Ingredient(Observable):
    
    def __init__(self, name='New ingredient', notes='', analysis={}, other_attributes={}, glaze_calculator_ids={}):

        Observable.__init__(self)
        self.name = name
        # notes not implemented yet.
        self.notes = notes
        # analysis is a dictionary giving the weight percent of each oxide in the ingredient.
        self.analysis = analysis
        # other attributes is a dictionary giving the values of each other attribute of the ingredient
        self.other_attributes = other_attributes
        # glaze_calculator_ids is a dictionary with keys being strings referring to various glaze calc software,
        # and values being the corresponding index in that software that encodes the ingredient
        self.glaze_calculator_ids = glaze_calculator_ids

def ingredient_reset():
    import ingredientfile
        
    with shelve.open(persistent_data_path+"/IngredientShelf") as ingredient_shelf:
        for index in ingredient_shelf:
            del ingredient_shelf[index]

        temp_order_list = []
        for (pos, ing) in enumerate(ingredientfile.ingredient_names):

            temp_order_list.append(str(pos))

            ing_init = Ingredient(name=ing, analysis=dict([(ox, ingredientfile.ingredient_analyses[ing][ox]) \
                                                                   for ox in OxideData.oxides() if ox in ingredientfile.ingredient_analyses[ing]]),\
                                  other_attributes = {})

            for attr in []: #other_attr_dict:
                try:
                    ing_init.other_attributes[attr] = ingredientfile.ingredient_analyses[ing][attr]
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
    
    def __init__(self, name, numerator_coefs, normalization, def_low, def_upp, dec_pt):
        """SiO2:Al2O3, LOI, cost, total clay, etc"""
           
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
    ingredient_analyses = {}
    for index in ingredient_dict:
        ingredient_analyses[index] = ingredient_dict[index].analysis
    return ingredient_analyses

class CoreData(OxideData):
    '''Class used to store the dictionaries of ingredients and 'other' restrictions, as well as
       the dictionary of other attributes ingredients may have'''
    
    def __init__(self):
        self.ingredient_dict = {}
        self.ingredient_analyses = {}    # Could do without this  
        self.other_dict = {}
        self.other_attr_dict = {}
        self.default_lower_bounds = {}
        self.default_upper_bounds = {}

    def restr_keys(self):
        return [t+ox for t in ['umf_', 'mass_perc_', 'mole_perc_'] for ox in self.oxide_dict]+\
           ['ingredient_'+i for i in self.ingredient_dict]+\
           ['other_'+ot for ot in self.other_dict]

    def associated_oxides(self, ingredients):
        assoc_oxides = set()
        for index in ingredients:
            assoc_oxides = assoc_oxides.union(set(self.ingredient_analyses[index]))  # update the available oxides. Probably not the most
                                                                                                      # efficient way to do this
        return assoc_oxides

    def set_default_data(self):
             
        self.other_attr_dict = {'0': 'LOI', '2': 'Clay', '1': 'Cost'}

        self.ingredient_dict = {}
        from .default_data import ingredientfile as ingredientfile
        for pos, ing in enumerate(ingredientfile.ingredient_names):
            ox_comp = dict([(ox, ingredientfile.ingredient_analyses[ing][ox]) \
                            for ox in self.oxides() if ox in ingredientfile.ingredient_analyses[ing]])
            ing_init = Ingredient(name=ing, analysis=ox_comp, other_attributes={})
            for attr in self.other_attr_dict:
                try:
                    ing_init.other_attributes[attr] = ingredientfile.ingredient_analyses[ing][attr]
                except:
                    pass  
            self.ingredient_dict[str(pos)] = ing_init
        self.ingredient_analyses = get_ing_comp(self.ingredient_dict) 

        self.other_dict = {}
        self.other_dict['0'] = Other('SiO2_Al2O3', {'mole_SiO2':1}, "self.lp_var['mole_Al2O3']", 3, 18, 2)   # Using 'SiO2:Al2O3' gives an error
        self.other_dict['1'] = Other('KNaO UMF', {'mole_K2O':1, 'mole_Na2O':1}, "self.lp_var['fluxes_total']", 0, 1, 3)
        self.other_dict['2'] = Other('KNaO % mol', {'mole_K2O':1, 'mole_Na2O':1}, "0.01*self.lp_var['ox_mole_total']", 0, 100, 2)
        self.other_dict['3'] = Other('RO UMF', {'mole_MgO':1, 'mole_CaO':1, 'mole_BaO':1, 'mole_SrO':1}, "self.lp_var['fluxes_total']", 0, 1, 3)

        other_att_4 = {'ingredient_'+index : 0.01*float(self.ingredient_dict[index].other_attributes['2'])\
                       for index in self.ingredient_dict if '2' in self.ingredient_dict[index].other_attributes}
        self.other_dict['4'] = Other('Total clay', {k:v for k,v in other_att_4.items() if v>0}, "0.01*self.lp_var['ingredient_total']", 0, 100, 1)
        other_att_5 = {'ingredient_'+index : 0.01*float(self.ingredient_dict[index].other_attributes['0'])\
                       for index in self.ingredient_dict if '0' in self.ingredient_dict[index].other_attributes}
        self.other_dict['5'] = Other('LOI',  {k:v for k,v in other_att_5.items() if v>0}, "0.01*self.lp_var['ingredient_total']", 0, 100, 1)
        other_att_6 = {'ingredient_'+index : 0.01*float(self.ingredient_dict[index].other_attributes['1'])\
                       for index in self.ingredient_dict if '1' in self.ingredient_dict[index].other_attributes}
        self.other_dict['6'] = Other('cost', {k:v for k,v in other_att_6.items() if v>0}, "0.01*self.lp_var['ingredient_total']", 0, 100, 1)

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

    def set_default_default_bounds(self):
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

    def save_ingredient_dict(self, path):    # change to JSON?
        with shelve.open(path) as ingredient_shelf:
            for i in self.ingredient_dict:
                ingredient_shelf[i] = self.ingredient_dict[i] 

    def set_ingredient_dict(self, path):    # change to JSON?
        with shelve.open(path) as ingredient_shelf:
            self.ingredient_dict = dict(ingredient_shelf)
        self.ingredient_analyses = get_ing_comp(self.ingredient_dict)

    def save_other_dict(self, path):    # change to JSON?
        with shelve.open(path) as other_shelf:
            for i in self.other_dict:
                other_shelf[i] = self.other_dict[i] 

    def set_other_dict(self, path):
        with shelve.open(path) as other_shelf:
            self.other_dict = dict(other_shelf)

##    def set_default_bounds(self, path):
##        with shelve.open(path) as other_shelf:
##            self.other_dict = dict(other_shelf)

    def add_ingredient(self, ing, default_low = 0, default_upp = 100):
        """Adds ingredient ing to the ingredient dictionary. The index is determined automatically"""
        m = max([int(j) for j in self.ingredient_dict]) + 1
        i = str(m)
        self.ingredient_dict[i] = ing
        self.ingredient_analyses[i] = ing.analysis
        self.default_lower_bounds['ingredient_'+i] = default_low
        self.default_upper_bounds['ingredient_'+i] = default_upp

    def remove_ingredient(self, i):
        del self.ingredient_dict[i]
        del self.ingredient_analyses[i]
        del self.default_lower_bounds['ingredient_'+i]
        del self.default_upper_bounds['ingredient_'+i]
            
##        self.set_current_recipe('0')
##
##    def set_current_recipe(self, i):
##        CoreData.current_recipe = self.recipe_dict[i]  
##
##    def update_ingredient_data(self, new_dict):
##        self.ingredient_dict = new_dict
##        self.ingredient_analyses = get_ing_comp(new_dict)
##
##    def update_other_data(self, new_dict):
##        self.self.other_dict = new_dict


    #def add/delete ingredient /other
        


