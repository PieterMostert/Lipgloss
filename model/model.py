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


# initialize oxides, ingredients, recipe_dict, etc.
##lg.core_data.OxideData.set_default_oxides()
##cd = lg.core_data.CoreData()
##cd.set_default_data()
#CoreData.load_ingredients(path)

class Model:

    def __init__(self, core_data):

        self.current_recipe = None
        self.recipe_dict = None
        self.order = {"oxides":[], "ingredients":[], "other":[]}

    def set_recipe_dict(self):
    ##    with open(persistent_data_path+"/JSONRecipeShelf.json", 'r') as json_str:
    ##        print(json_str)
    ##        self.recipe_dict = RecipeSerializer.deserialize_dict(json_str)

        f = open(persistent_data_path+"/JSONRecipeShelf.json", 'r')
        json_str = f.read()
        f.close()
        self.recipe_dict = RecipeSerializer.deserialize_dict(json_str)
        
    def set_current_recipe(self, index):
        self.current_recipe = self.recipe_dict[index]

    def set_order(self):
        with shelve.open(persistent_data_path+"/OrderShelf") as order_shelf:
            self.order = dict(order_shelf)
