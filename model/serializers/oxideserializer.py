import json
try:
    from lipgloss.core_data import Oxide
except:
    from ..lipgloss.core_data import Oxide

class OxideSerializer(object):
    """A class to support serializing/deserializing of a single oxide and dictionaries of oxides.  Needs improvement"""

    @staticmethod
    def get_serializable_oxide(oxide):
        """A serializable oxide is one that can be serialized to JSON using the python json encoder."""
        serializable_oxide = {}
        serializable_oxide["molar_mass"] = oxide.molar_mass
        serializable_oxide["flux"] = oxide.flux
        serializable_oxide["min_threshhold"] = oxide.min_threshhold
        return serializable_oxide

    @staticmethod
    def serialize(oxide):
        """Serialize a single Oxide object to JSON."""
        return json.dumps(OxideSerializer.get_serializable_oxide(oxide), indent=4)

    @staticmethod
    def serialize_dict(oxide_dict):
        """Convert a dictionary of Oxide objects to serializable dictionary.
           Use json.dump(output, file) to save output to file"""
        serializable_dict = {};
        for index, oxide in oxide_dict.items():
            serializable_dict[index] = OxideSerializer.get_serializable_oxide(oxide)
        return serializable_dict
        

    @staticmethod
    def get_oxide(serialized_oxide):
        """Convert a serialized oxide (a dict) returned by the JSON decoder into a Oxide object."""
        oxide = Oxide(serialized_oxide["molar_mass"],
                      serialized_oxide["flux"],
                      serialized_oxide["min_threshhold"]) 
        return oxide
        
    @staticmethod
    def deserialize(json_str):
        """Deserialize a single oxide from JSON to a Oxide object."""
        serialized_oxide_dict = json.loads(json_str)
        return OxideSerializer.get_oxide(serialized_oxide_dict)

    @staticmethod
    def deserialize_dict(serialized_oxide_dict):
        """Deserialize a number of oxides from JSON to a dict containing Oxide objects, indexed by Oxide name."""
        oxide_dict = {}
        for i, serialized_oxide in serialized_oxide_dict.items():
            oxide_dict[i] = OxideSerializer.get_oxide(serialized_oxide)                           
        return oxide_dict

