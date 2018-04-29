import json
try:
    from lipgloss.ingredients import ingredient
except:
    from ..lipgloss.ingredients import ingredient
#import lipgloss
##from ..lipgloss.core_data import CoreData

class IngredientSerializer(object):
    """A class to support serializing/deserializing of a single ingredient and dictionaries of ingredients.  Needs improvement"""

    @staticmethod
    def get_serializable_ingredient(ingredient):
        """A serializable ingredient is one that can be serialized to JSON using the python json encoder."""
        serializable_ingredient = {}
        serializable_ingredient["name"] = ingredient.name
        serializable_ingredient["notes"] = ingredient.notes
        serializable_ingredient["oxide_comp"] = ingredient.oxide_comp
        serializable_ingredient["other_attributes"] = ingredient.other_attributes
        serializable_ingredient["glaze_calculator_ids"] = ingredient.glaze_calculator_ids
        return serializable_ingredient

    @staticmethod
    def serialize(ingredient):
        """Serialize a single ingredient object to JSON."""
        return json.dumps(ingredientSerializer.get_serializable_ingredient(ingredient), indent=4)

    @staticmethod
    def serialize_dict(ingredient_dict):
        """Serialize a dict containing ingredient objects indexed by ID keys to JSON."""
        serializable_dict = {};
        for index in ingredient_dict:
            serializable_dict[index] = ingredientSerializer.get_serializable_ingredient(ingredient_dict[index])
        return json.dumps(serializable_dict, indent=4)

    @staticmethod
    def get_ingredient(serialized_ingredient_dict):
        """Convert a dict returned by the JSON decoder into a ingredient object."""
        ingredient = Ingredient(serialized_ingredient_dict["name"], 
                            serialized_ingredient_dict["notes"],
                            serialized_ingredient_dict["oxide_comp"],
                            serialized_ingredient_dict["ingredients"],
                            serialized_ingredient_dict["other_attributes"],
                            serialized_ingredient_dict["glaze_calculator_ids"]) 
        return ingredient
        
    @staticmethod
    def deserialize(json_str):
        """Deserialize a single ingredient from JSON to a ingredient object."""
        serialized_ingredient_dict = json.loads(json_str)
        return ingredientSerializer.get_ingredient(serialized_ingredient_dict)

    @staticmethod
    def deserialize_dict(json_str):
        """Deserialize a number of ingredients from JSON to a dict containing ingredient objects, indexed by ingredient ID."""
        ingredient_dict = {}
        serialized_ingredients = json.loads(json_str)
        for index in serialized_ingredients:
            serialized_ingredient_dict = serialized_ingredients[index]
            ingredient = ingredientSerializer.get_ingredient(serialized_ingredient_dict)                           
            ingredient_dict[index] = ingredient
        return ingredient_dict

