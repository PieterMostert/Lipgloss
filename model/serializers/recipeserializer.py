import json
from ..recipes import Recipe
from ..core_data import CoreData
from inspect import getsourcefile
import os
from os.path import abspath, dirname
import sys

persistent_data_path = dirname(dirname(abspath(getsourcefile(lambda:0))))+'/persistent_data'  # please tell me there's an easier way to import stuff in Python
sys.path.append(persistent_data_path)

class RecipeSerializer(object):
    """A class to support serializing/deserializing of a single recipes and dictionaries of recipe.  Needs improvement"""

    @staticmethod
    def get_serializable_recipe(recipe):
        """A serializable recipe is one that can be serialized to JSON using the python json encoder."""
        serializable_recipe = {}
        serializable_recipe["name"] = recipe.name
        serializable_recipe["entry_type"] = recipe.entry_type
        serializable_recipe["ingredients"] = recipe.ingredients
        serializable_recipe["other"] = recipe.other
        # oxides must be converted from a set to a list
        serializable_recipe["oxides"] = list(recipe.oxides)
        serializable_recipe["lower_bounds"] = recipe.lower_bounds
        serializable_recipe["upper_bounds"] = recipe.upper_bounds
        serializable_recipe["pos"] = recipe.pos
        serializable_recipe["variables"] = recipe.variables
        return serializable_recipe

    @staticmethod
    def serialize(recipe):
        """Serialize a single Recipe object to JSON."""
        return json.dumps(RecipeSerializer.get_serializable_recipe(recipe), indent=4)

    @staticmethod
    def serialize_dict(recipe_dict):
        """Serialize a dict containing Recipe objects indexed by ID keys to JSON."""
        serializable_dict = {};
        for index in recipe_dict:
            serializable_dict[index] = RecipeSerializer.get_serializable_recipe(recipe_dict[index])
        return json.dumps(serializable_dict, indent=4)

    @staticmethod
    def get_recipe(serialized_recipe_dict):
        """Convert a dict returned by the JSON decoder into a Recipe object."""
        recipe = Recipe(serialized_recipe_dict["name"], 
                            serialized_recipe_dict["pos"], 
                            serialized_recipe_dict["ingredients"],
                            serialized_recipe_dict["other"],
                            serialized_recipe_dict["lower_bounds"],
                            serialized_recipe_dict["upper_bounds"],
                            serialized_recipe_dict["entry_type"],
                            serialized_recipe_dict["variables"]) 
        return recipe
        
    @staticmethod
    def deserialize(json_str):
        """Deserialize a single recipe from JSON to a Recipe object."""
        serialized_recipe_dict = json.loads(json_str)
        return RecipeSerializer.get_recipe(serialized_recipe_dict)

    @staticmethod
    def deserialize_dict(json_str):
        """Deserialize a number of recipes from JSON to a dict containing Recipe objects, indexed by Recipe ID."""
        recipe_dict = {}
        serialized_recipes = json.loads(json_str)
        for index in serialized_recipes:
            serialized_recipe_dict = serialized_recipes[index]
            recipe = RecipeSerializer.get_recipe(serialized_recipe_dict)                           
            recipe_dict[index] = recipe
        return recipe_dict

# Add a method to CoreData that initializes the recipe_dict from the JSON file
# This isn't done in core_data to avoid circular imports
def set_recipe_dict(self):
##    with open(persistent_data_path+"/JSONRecipeShelf.json", 'r') as json_str:
##        print(json_str)
##        self.recipe_dict = RecipeSerializer.deserialize_dict(json_str)

    f = open(persistent_data_path+"/JSONRecipeShelf.json", 'r')
    json_str = f.read()
    f.close()
    self.recipe_dict = RecipeSerializer.deserialize_dict(json_str)

CoreData.set_recipe_dict = classmethod(set_recipe_dict)

