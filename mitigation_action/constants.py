from enum import Enum
# 'initiative': self._upload_file_to_initiative, 
# 'geographic-location': self._upload_file_to_geographic_location,
# 'ghg-information': self._upload_file_to_ghg_information,
# 'impact-documentation': self._upload_file_to_impact_documentation
class MitigationActionFilesType(str, Enum):
    """
    Enum for the type of mitigation action files.
    """
    INITIATIVE = 'initiative'
    GEOGRAPHIC_LOCATION = 'geographic-location'
    GHG_INFORMATION = 'ghg-information'
    IMPACT_DOCUMENTATION = 'impact-documentation'

    @classmethod
    def choices(cls):
        labels = {
            cls.INITIATIVE: 'Initiative',
            cls.GEOGRAPHIC_LOCATION: 'Geographic Location',
            cls.GHG_INFORMATION: 'GHG Information',
            cls.IMPACT_DOCUMENTATION: 'Impact Documentation',
        }

        return [(key.value, labels[key]) for key in cls]