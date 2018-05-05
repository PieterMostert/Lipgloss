import json
try:
    from lipgloss.restrictions import Restriction
except:
    from ..lipgloss.restrictions import Restriction

class RestrictionSerializer(object):
    """A class to support serializing/deserializing of a single restriction and dictionaries of restrictions.  Needs improvement"""

    @staticmethod
    def get_serializable_restriction(restriction):
        """A serializable restriction is one that can be serialized to JSON using the python json encoder."""
        serializable_restriction = {}
        serializable_restriction["index"] = restriction.index
        serializable_restriction["name"] = restriction.name
        serializable_restriction["objective_func"] = restriction.objective_func
        serializable_restriction["normalization"] = restriction.normalization
        serializable_restriction["default_low"] = restriction.default_low
        serializable_restriction["default_upp"] = restriction.default_upp
        serializable_restriction["dec_pt"] = restriction.dec_pt
        return serializable_restriction

    @staticmethod
    def serialize(restriction):
        """Serialize a single Restriction object to JSON."""
        return json.dumps(RestrictionSerializer.get_serializable_restriction(restriction), indent=4)

    @staticmethod
    def serialize_dict(restriction_dict):
        """Convert a dictionary of Restriction objects to serializable dictionary.
           Use json.dump(output, file) to save output to file"""
        serializable_dict = {};
        for index, restriction in restriction_dict.items():
            serializable_dict[index] = RestrictionSerializer.get_serializable_restriction(restriction)
        return serializable_dict
        

    @staticmethod
    def get_restriction(serialized_restriction):
        """Convert a serialized restriction (a dict) returned by the JSON decoder into a Restriction object."""
        restriction = Restriction(serialized_restriction["index"],
                      serialized_restriction["name"],
                      serialized_restriction["objective_func"],
                      serialized_restriction["normalization"],
                      serialized_restriction["default_low"],
                      serialized_restriction["default_upp"],
                      dec_pt=serialized_restriction["dec_pt"]) 
        return restriction
        
    @staticmethod
    def deserialize(json_str):
        """Deserialize a single restriction from JSON to a Restriction object."""
        serialized_restriction_dict = json.loads(json_str)
        return RestrictionSerializer.get_restriction(serialized_restriction_dict)

    @staticmethod
    def deserialize_dict(serialized_restriction_dict):
        """Deserialize a number of restrictions from JSON to a dict containing Restriction objects, indexed by Restriction name."""
        restriction_dict = {}
        for i, serialized_restriction in serialized_restriction_dict.items():
            restriction_dict[i] = RestrictionSerializer.get_restriction(serialized_restriction)                           
        return restriction_dict

