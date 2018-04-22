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

import pulp
import shelve
import lipgloss as lg
from serializers.recipeserializer import RecipeSerializer
from inspect import getsourcefile
import os
from os.path import abspath, dirname
import sys

persistent_data_path = dirname(abspath(getsourcefile(lambda:0)))+'\persistent_data'  # please tell me there's an easier way to import stuff in Python
#print(persistent_data_path)
sys.path.append(persistent_data_path)

import copy


# initialize oxides, ingredients, recipe_dict, etc.
##lg.core_data.OxideData.set_default_oxides()
##cd = lg.core_data.CoreData()
##cd.set_default_data()
#CoreData.load_ingredients(path)

class Model:
    "A partial model for the GUI. The full model consists of this together the CoreData class."

    def __init__(self):
        
        f = open(persistent_data_path+"/JSONRecipeShelf.json", 'r')
        json_str = f.read()
        f.close()
        self.recipe_dict = RecipeSerializer.deserialize_dict(json_str)
    ##    with open(persistent_data_path+"/JSONRecipeShelf.json", 'r') as json_str:
    ##        print(json_str)
    ##        self.recipe_dict = RecipeSerializer.deserialize_dict(json_str)

        self.current_recipe = None
        self.recipe_index = None
        self.set_current_recipe('0')

        with shelve.open(persistent_data_path+"/OrderShelf") as order_shelf:
            self.order = dict(order_shelf)
        
    def set_current_recipe(self, index):
        self.current_recipe = copy.deepcopy(self.recipe_dict[index])
        self.recipe_index = index

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
        f = open(persistent_data_path+"/JSONRecipeShelf.json", 'w')
        json_string = RecipeSerializer.serialize_dict(self.recipe_dict)
        f.write(json_string)
        f.close()

    def update_recipe_dict(self, core_data):
        for recipe in self.recipe_dict.values():
            recipe.update_core_data(core_data)
        self.json_write_recipes()
        
    def update_order(self, key):  # Is this used at all?
        with shelve.open(persistent_data_path+"/OrderShelf") as order_shelf:
            order_shelf[key] = self.order[key]
            
