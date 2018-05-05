import json
try:
    from lipgloss.core_data import Other
except:
    from ..lipgloss.core_data import Other

class OtherSerializer(object):
    """A class to support serializing/deserializing of a single other restriction instance and dictionaries of such.
       Needs improvement"""

    @staticmethod
    def get_serializable_other(other):
        """A serializable other is one that can be serialized to JSON using the python json encoder."""
        serializable_other = {}
        serializable_other["name"] = other.name
        serializable_other["numerator coefs"] = other.numerator_coefs
        serializable_other["normalization"] = other.normalization
        serializable_other["def low"] = other.def_low
        serializable_other["def upp"] = other.def_upp
        serializable_other["dec pt"] = other.dec_pt
        return serializable_other

    @staticmethod
    def serialize(other):
        """Serialize a single Other object to JSON."""
        return json.dumps(OtherSerializer.get_serializable_other(other), indent=4)

    @staticmethod
    def serialize_dict(other_dict):
        """Convert a dictionary of Other objects to serializable dictionary.
           Use json.dump(output, file, indent=4) to save output to file"""
        serializable_dict = {};
        for index, other in other_dict.items():
            serializable_dict[index] = OtherSerializer.get_serializable_other(other)
        return serializable_dict
        

    @staticmethod
    def get_other(serialized_other):
        """Convert a serialized other (a dict) returned by the JSON decoder into an Other object."""
        other = Other(serialized_other["name"],
                      serialized_other["numerator coefs"],
                      serialized_other["normalization"],
                      serialized_other["def low"],
                      serialized_other["def upp"],
                      serialized_other["dec pt"]) 
        return other
        
    @staticmethod
    def deserialize(json_str):
        """Deserialize a single other from JSON to an Other object."""
        serialized_other_dict = json.loads(json_str)
        return OtherSerializer.get_other(serialized_other_dict)

    @staticmethod
    def deserialize_dict(serialized_other_dict):
        """Deserialize a number of others from JSON to a dict containing Other objects, indexed by Other ID."""
        other_dict = {}
        for i, serialized_other in serialized_other_dict.items():
            other_dict[i] = OtherSerializer.get_other(serialized_other)                           
        return other_dict

