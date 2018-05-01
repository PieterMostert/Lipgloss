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
    from lipgloss.core_data import CoreData, Ingredient
except:
    from .lipgloss.core_data import CoreData, Ingredient
    
try:
    from serializers.recipeserializer import RecipeSerializer
    from serializers.ingredientserializer import IngredientSerializer
except:
    from .serializers.recipeserializer import RecipeSerializer
    from .serializers.ingredientserializer import IngredientSerializer
    
from inspect import getsourcefile
import os
from os.path import abspath, dirname
from os import path
import sys
persistent_data_path = path.join(dirname(abspath(getsourcefile(lambda:0))), 'persistent_data')  # please tell me there's an easier way to import stuff in Python
#print(persistent_data_path)
sys.path.append(persistent_data_path)

import pulp
import shelve
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

        self.set_default_data()  # Replace by functions that sets data saved by user
        self.set_default_default_bounds() # Replace by function that sets data saved by user
        
        f = open(path.join(persistent_data_path, "JSONRecipeShelf.json"), 'r')
        json_str = f.read()
        f.close()
        self.recipe_dict = RecipeSerializer.deserialize_dict(json_str)
    ##    with open(persistent_data_path+"/JSONRecipeShelf.json", 'r') as json_str:
    ##        print(json_str)
    ##        self.recipe_dict = RecipeSerializer.deserialize_dict(json_str)

        self.current_recipe = None
        self.recipe_index = None
        self.set_current_recipe('0')

        with shelve.open(path.join(persistent_data_path, "OrderShelf")) as order_shelf:
            self.order = dict(order_shelf)
        
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
        """Write all recipes from the global recipe_dict to file, overwriting previous data"""
        f = open(path.join(persistent_data_path, "JSONRecipeShelf.json"), 'w')
        json_string = RecipeSerializer.serialize_dict(self.recipe_dict)
        f.write(json_string)
        f.close()

    def update_recipe_dict(self):
        for recipe in self.recipe_dict.values():
            recipe.update_core_data(self)
        self.json_write_recipes()
        
    def update_order(self, key):  # Is this used at all?
        with shelve.open(path.join(persistent_data_path, "OrderShelf")) as order_shelf:
            order_shelf[key] = self.order[key]

    def new_ingredient(self):
        ing = Ingredient('', notes='', analysis={}, other_attributes={})
                            # If we just had Ingredient('Ingredient #'+index) above, the default values of the notes, analysis
                            # and other_attributes attributes would change when the last instance of the class defined had those
                            # attributes changed
        self.add_ingredient(ing)
        i = list(self.ingredient_dict.keys())[-1]     # index of new ingredient
        ing.name = 'Ingredient #'+i

        self.json_write_ingredients()  # replace by function that just updates a single ingredient
##        with shelve.open(persistent_data_path+"/IngredientShelf") as ingredient_shelf:
##            ingredient_shelf[i] = self.ingredient_dict[i]

        with shelve.open(path.join(persistent_data_path, "OrderShelf")) as order_shelf:
            temp_list = order_shelf['ingredients']
            temp_list.append(i)
            order_shelf['ingredients'] = temp_list
        self.order['ingredients'] = temp_list
        
        return i, ing
            
    def json_write_ingredients(self):
        """Write all ingredients from self.ingredient_dict to file, overwriting previous data"""
        f = open(path.join(persistent_data_path, "JSONIngredientShelf.json"), 'w')
        json_string = IngredientSerializer.serialize_dict(self.ingredient_dict)
        f.write(json_string)
        f.close()
