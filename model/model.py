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

try:
    from lipgloss.core_data import OxideData, CoreData, Ingredient
    from lipgloss.restrictions import Restriction
except:
    from .lipgloss.core_data import OxideData, CoreData, Ingredient
    from .lipgloss.restrictions import Restriction
    
try:
    from serializers.recipeserializer import RecipeSerializer
    from serializers.ingredientserializer import IngredientSerializer
    from serializers.oxideserializer import OxideSerializer
    from serializers.otherserializer import OtherSerializer
    from serializers.restrictionserializer import RestrictionSerializer
except:
    from .serializers.recipeserializer import RecipeSerializer
    from .serializers.ingredientserializer import IngredientSerializer
    from .serializers.oxideserializer import OxideSerializer
    from .serializers.otherserializer import OtherSerializer
    from .serializers.restrictionserializer import RestrictionSerializer

import json
from inspect import getsourcefile
import os
from os.path import abspath, dirname
from os import path
import sys
persistent_data_path = path.join(dirname(abspath(getsourcefile(lambda:0))), 'persistent_data')  # please tell me there's an easier way to import stuff in Python
#print(persistent_data_path)
sys.path.append(persistent_data_path)

import pulp
import copy

# initialize oxides, ingredients, recipe_dict, etc.
##lg.core_data.OxideData.set_default_oxides()
##cd = lg.core_data.CoreData()
##cd.set_default_data()
#CoreData.load_ingredients(path)

class Model(CoreData):
    "A partial model for the GUI. The full model consists of this together with the LpRecipeProblem class."

    def __init__(self):
        CoreData.__init__(self)
        #OxideData.set_default_oxides()
        with open(path.join(persistent_data_path, "JSONOxides.json"), 'r') as f:
            OxideData.oxide_dict = OxideSerializer.deserialize_dict(json.load(f))

        #self.set_default_data()
        
        with open(path.join(persistent_data_path, "JSONIngredients.json"), 'r') as f:
            self.ingredient_dict = IngredientSerializer.deserialize_dict(json.load(f))
            
        for i, ing in self.ingredient_dict.items():
            self.ingredient_analyses[i] = ing.analysis

        # The data contained in JSONOther can be obtained from JSONRestriction, so we don't really need this.
        with open(path.join(persistent_data_path, "JSONOther.json"), 'r') as f:
            self.other_dict = OtherSerializer.deserialize_dict(json.load(f))

        self.other_attr_dict = {'0': 'LOI', '2': 'Clay', '1': 'Cost'}  # Replace by functions that sets data saved by user 
        #self.set_default_default_bounds()

        with open(path.join(persistent_data_path, "JSONRecipes.json"), 'r') as f:
            self.recipe_dict = RecipeSerializer.deserialize_dict(json.load(f))

        self.current_recipe = None
        self.recipe_index = None
        self.set_current_recipe('0')

        with open(path.join(persistent_data_path, "JSONOrder.json"), 'r') as f:
            self.order = json.load(f)

        #Create Restriction dictionary
        with open(path.join(persistent_data_path, "JSONRestrictions.json"), 'r') as f:
            self.restr_dict = RestrictionSerializer.deserialize_dict(json.load(f))
        # It seems a bit silly to record the default lower and upper bounds in both self.restr_dict
        # and in self.default_lower_bounds and self.default_lower_bounds, but that's how things
        # stand at the moment
        for key in self.restr_keys():
            self.default_lower_bounds[key] = self.restr_dict[key].default_low
            self.default_upper_bounds[key] = self.restr_dict[key].default_upp
##        self.restr_dict = {}
##
##        # Create oxide restrictions:
##        for ox in self.order['oxides']:
##            key = 'umf_'+ox
##            self.restr_dict[key] = Restriction(key, ox, 'mole_'+ox, "self.lp_var['fluxes_total']", \
##                                               self.default_lower_bounds[key], self.default_upper_bounds[key], dec_pt=3)
##            key = 'mass_perc_'+ox
##            self.restr_dict[key] = Restriction(key, ox, 'mass_'+ox, "0.01*self.lp_var['ox_mass_total']", \
##                                               self.default_lower_bounds[key], self.default_upper_bounds[key], dec_pt=2)
##            key = 'mole_perc_'+ox
##            self.restr_dict[key] = Restriction(key, ox, 'mole_'+ox, "0.01*self.lp_var['ox_mole_total']", \
##                                               self.default_lower_bounds[key], self.default_upper_bounds[key], dec_pt=2)
##
##        # Create ingredient restrictions:
##        for i, ing in self.ingredient_dict.items():
##            key = 'ingredient_'+i
##            self.restr_dict[key] = Restriction(key, ing.name, key, "0.01*self.lp_var['ingredient_total']", \
##                                   self.default_lower_bounds[key], self.default_upper_bounds[key])
##
##        # Create other restrictions:
##        for i, ot in self.other_dict.items():
##            key = 'other_'+i
##            self.restr_dict[key] = Restriction(key, ot.name, key, ot.normalization, ot.def_low, ot.def_upp, dec_pt=ot.dec_pt)
##
##        self.json_write_restrictions()
        
    def set_current_recipe(self, index):
        self.current_recipe = copy.deepcopy(self.recipe_dict[index])
        self.recipe_index = index
        self.current_recipe.update_oxides(self)  # In case the ingredient compositions have changed.
                                                 # Can get rid of this if we ensure that all recipes are
                                                 # updated each time the ingredient compositions change

    def save_current_recipe(self):
        self.recipe_dict[self.recipe_index] = copy.deepcopy(self.current_recipe)
        self.json_write_recipes()

    def save_new_recipe(self):
        recipe_index = str(int(max(self.recipe_dict, key=int)) + 1)
        self.recipe_index = recipe_index
        self.current_recipe.name = 'Recipe Bounds ' + recipe_index
        self.current_recipe.pos = int(recipe_index)
        self.recipe_dict[recipe_index] = copy.deepcopy(self.current_recipe)
        self.json_write_recipes()

    def delete_recipe(self, index):
        if index != '0': # don't allow a user to delete the default 
            del self.recipe_dict[index]
            self.json_write_recipes()
        else:
            print('User tried to delete default recipe. This shouldn\'t be an option')
        
    def json_write_recipes(self):
        """Write all recipes from self.recipe_dict to file, overwriting previous data"""
##        f = open(path.join(persistent_data_path, "JSONRecipeShelf.json"), 'w')
##        json_string = RecipeSerializer.serialize_dict(self.recipe_dict)
##        f.write(json_string)
##        f.close()
        with open(path.join(persistent_data_path, "JSONRecipes.json"), 'w') as f:
            json_string = RecipeSerializer.serialize_dict(self.recipe_dict)
            json.dump(json_string, f, indent=4)

##    def json_read_recipes(self):
##        """Set self.recipe_dict equal to the deserialized recipe dictionary in JSONRecipes.json"""
##        with open(path.join(persistent_data_path, "JSONRecipes.json"), 'r') as f:
##            self.recipe_dict = RecipeSerializer.deserialize_dict(json.load(f))

    def update_recipe_dict(self):
        for recipe in self.recipe_dict.values():
            recipe.update_core_data(self)
        self.json_write_recipes()
        
    def json_write_order(self):
        with open(path.join(persistent_data_path, "JSONOrder.json"), 'w') as f:
            json.dump(self.order, f, indent = 4)

    def new_ingredient(self):
        ing = Ingredient('', notes='', analysis={}, other_attributes={})
                            # If we just had Ingredient('Ingredient #'+index) above, the default values of the notes, analysis
                            # and other_attributes attributes would change when the last instance of the class defined had those
                            # attributes changed
        self.add_ingredient(ing)
        i = list(self.ingredient_dict.keys())[-1]     # index of new ingredient
        ing.name = 'Ingredient #'+i
        self.order['ingredients'].append(i)
        self.restr_dict['ingredient_'+i] = Restriction('ingredient_'+i, ing.name, 'ingredient_'+i, "0.01*self.lp_var['ingredient_total']", 0, 100)

        self.json_write_ingredients()  # replace by function that just updates a single ingredient
        self.json_write_order()
        self.json_write_restrictions()
##        with shelve.open(persistent_data_path+"/IngredientShelf") as ingredient_shelf:
##            ingredient_shelf[i] = self.ingredient_dict[i]

##        with shelve.open(path.join(persistent_data_path, "OrderShelf")) as order_shelf:
##            temp_list = order_shelf['ingredients']
##            temp_list.append(i)
##            order_shelf['ingredients'] = temp_list
##        self.order['ingredients'] = temp_list
        
        
        return i, ing

    def delete_ingredient(self, i, recipes_affected):
        """Uses remove_ingredient() method of CoreData"""
        self.remove_ingredient(i)
        self.json_write_ingredients()
        self.order['ingredients'].remove(i)
        self.json_write_order()
        del self.restr_dict['ingredient_'+i]
        self.json_write_restrictions()
##        with shelve.open(path.join(persistent_data_path, "OrderShelf")) as order_shelf:
##            temp_list = order_shelf['ingredients']
##            temp_list.remove(i)
##            order_shelf['ingredients'] = temp_list
        # Remove the ingredient from all recipes that contain it.
        for j in recipes_affected:
            self.recipe_dict[j].remove_ingredient(self, i)
        self.json_write_recipes()
            
    def json_write_ingredients(self):
        """Write all ingredients from self.ingredient_dict to file, overwriting previous data"""
        with open(path.join(persistent_data_path, "JSONIngredients.json"), 'w') as f:
            json.dump(IngredientSerializer.serialize_dict(self.ingredient_dict), f, indent=4)
##        f = open(path.join(persistent_data_path, "JSONIngredients.json"), 'w')
##        json_string = IngredientSerializer.serialize_dict(self.ingredient_dict)
##        f.write(json_string)
##        f.close()
 
    def json_write_oxides(self):
        """Write all oxides from self.oxide_dict to file, overwriting previous data"""
        with open(path.join(persistent_data_path, "JSONOxides.json"), 'w') as f:
            json.dump(OxideSerializer.serialize_dict(self.oxide_dict), f, indent=4)

    def json_write_other(self):
        """Write all other restrictions from self.other_dict to file, overwriting previous data"""
        with open(path.join(persistent_data_path, "JSONOther.json"), 'w') as f:
            json.dump(OtherSerializer.serialize_dict(self.other_dict), f, indent=4)

    def json_write_restrictions(self):
        """Write all other restrictions from self.other_dict to file, overwriting previous data"""
        with open(path.join(persistent_data_path, "JSONRestrictions.json"), 'w') as f:
            json.dump(RestrictionSerializer.serialize_dict(self.restr_dict), f, indent=4)
