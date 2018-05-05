import json
try:
    from lipgloss.recipes import Recipe
except:
    from ..lipgloss.recipes import Recipe
#import lipgloss
##from ..lipgloss.core_data import CoreData

class RecipeSerializer(object):
    """A class to support serializing/deserializing of a single recipe and dictionaries of recipes.  Needs improvement"""

    @staticmethod
    def get_serializable_recipe(recipe):
        """A serializable recipe is one that can be serialized to JSON using the python json encoder."""
        serializable_recipe = {}
        serializable_recipe["name"] = recipe.name
        serializable_recipe["pos"] = recipe.pos
        serializable_recipe["ingredients"] = recipe.ingredients
        serializable_recipe["other"] = recipe.other
        # oxides must be converted from a set to a list
        serializable_recipe["oxides"] = list(recipe.oxides)
        serializable_recipe["lower_bounds"] = recipe.lower_bounds
        serializable_recipe["upper_bounds"] = recipe.upper_bounds
        serializable_recipe["entry_type"] = recipe.entry_type
        serializable_recipe["variables"] = recipe.variables
        return serializable_recipe

    @staticmethod
    def serialize(recipe):
        """Serialize a single Recipe object to JSON."""
        return json.dumps(RecipeSerializer.get_serializable_recipe(recipe), indent=4)

    @staticmethod
    def serialize_dict(recipe_dict):
        """Convert a dictionary of Recipe objects to serializable dictionary.
           Use json.dump(output, file) to save output to file"""
        #"""Serialize a dict containing Recipe objects indexed by ID keys to JSON."""
        serializable_dict = {};
        for index, recipe in recipe_dict.items():
            serializable_dict[index] = RecipeSerializer.get_serializable_recipe(recipe)
        #return json.dumps(serializable_dict, indent=4)
        return serializable_dict
        

    @staticmethod
    def get_recipe(serialized_recipe):
        """Convert a serialized recipe (a dict) returned by the JSON decoder into a Recipe object."""
        recipe = Recipe(serialized_recipe["name"], 
                            serialized_recipe["pos"],
                            # oxides must be converted from a list to a set
                            set(serialized_recipe["oxides"]),
                            serialized_recipe["ingredients"],
                            serialized_recipe["other"],
                            serialized_recipe["lower_bounds"],
                            serialized_recipe["upper_bounds"],
                            serialized_recipe["entry_type"],
                            serialized_recipe["variables"]) 
        return recipe
        
    @staticmethod
    def deserialize(json_str):
        """Deserialize a single recipe from JSON to a Recipe object."""
        serialized_recipe_dict = json.loads(json_str)
        return RecipeSerializer.get_recipe(serialized_recipe_dict)

    @staticmethod
    #def deserialize_dict(json_str):
    def deserialize_dict(serialized_recipe_dict):
        """Deserialize a number of recipes from JSON to a dict containing Recipe objects, indexed by Recipe ID."""
        recipe_dict = {}
##        serialized_recipes = json.loads(json_str)
##        for index in serialized_recipes:
##            serialized_recipe_dict = serialized_recipes[index]
##            recipe = RecipeSerializer.get_recipe(serialized_recipe_dict)                           
##            recipe_dict[index] = recipe
        for i, serialized_recipe in serialized_recipe_dict.items():
            recipe_dict[i] = RecipeSerializer.get_recipe(serialized_recipe)                           
        return recipe_dict

