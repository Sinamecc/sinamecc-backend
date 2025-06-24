from enum import Enum
from typing import Callable

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import models


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
    INDICATOR_SUSTAINABILITY = 'indicator-sustainability'
    INDICATOR_METHODOLOGICAL_DETAIL = 'indicator-methodological-detail'
    MONITORING_REPORT_LINE_TEXT = 'monitoring-report-line-text'
    MONITORING_UPDATED_DATA = 'monitoring-updated-data'
    MONITORING_WEB_SERVICE_CONNECTION = 'monitoring-web-service-connection'

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
   
        labels = {
            cls.INITIATIVE: 'Initiative',
            cls.GEOGRAPHIC_LOCATION: 'Geographic Location',
            cls.GHG_INFORMATION: 'GHG Information',
            cls.IMPACT_DOCUMENTATION: 'Impact Documentation',
            cls.INDICATOR_SUSTAINABILITY: 'Indicator Sustainability',
            cls.INDICATOR_METHODOLOGICAL_DETAIL: 'Indicator Methodological Detail',
            cls.MONITORING_REPORT_LINE_TEXT: 'Monitoring Report Line Text',
            cls.MONITORING_UPDATED_DATA: 'Monitoring Updated Data',
            cls.MONITORING_WEB_SERVICE_CONNECTION: 'Monitoring Web Service Connection',
        }

        return [(key.value, labels[key]) for key in cls]
    
    @classmethod
    def values(cls) -> list[str]:
        
        return [key.value for key in cls]
    
    @classmethod
    def get_models(cls) -> dict[str, Callable[..., models.Model]]:

        ## Lazy loading of content types
        ## This way, we avoid circular imports and ensure that the models are loaded when needed.
        return {
            cls.INITIATIVE: lambda: apps.get_model('mitigation_action.MitigationAction'),
            cls.GEOGRAPHIC_LOCATION: lambda: apps.get_model('mitigation_action.MitigationAction'),
            cls.GHG_INFORMATION: lambda: apps.get_model('mitigation_action.MitigationAction'),
            cls.IMPACT_DOCUMENTATION: lambda: apps.get_model('mitigation_action.MitigationAction'),
            cls.INDICATOR_SUSTAINABILITY: lambda: apps.get_model('mitigation_action.Indicator'),
            cls.INDICATOR_METHODOLOGICAL_DETAIL: lambda: apps.get_model('mitigation_action.Indicator'),
            cls.MONITORING_REPORT_LINE_TEXT: lambda: apps.get_model('mitigation_action.MonitoringIndicator'),
            cls.MONITORING_UPDATED_DATA: lambda: apps.get_model('mitigation_action.MonitoringIndicator'),
            cls.MONITORING_WEB_SERVICE_CONNECTION: lambda: apps.get_model('mitigation_action.MonitoringIndicator'),
        }
    @classmethod
    def get_entity_types(cls) -> list[str]:
        """
        Returns a list of entity types that can be used to filter files.
        """
        return {
            'indicator': 'Indicator',
            'monitoring-indicator': 'Monitoring Indicator',
        }
    
    @classmethod
    def get_entity_types_from_value(cls, value: str) -> str | None:
        """
        Returns the entity type for a given value.
        """
        options = {
            cls.INITIATIVE: 'mitigation-action',
            cls.GEOGRAPHIC_LOCATION: 'mitigation-action',
            cls.GHG_INFORMATION: 'mitigation-action',
            cls.IMPACT_DOCUMENTATION: 'mitigation-action',
            cls.INDICATOR_SUSTAINABILITY: 'indicator',
            cls.INDICATOR_METHODOLOGICAL_DETAIL: 'indicator',
            cls.MONITORING_REPORT_LINE_TEXT: 'monitoring-indicator',
            cls.MONITORING_UPDATED_DATA: 'monitoring-indicator',
            cls.MONITORING_WEB_SERVICE_CONNECTION: 'monitoring-indicator',
        }

        return options.get(value, None)