from rest_framework import exceptions, status


class MitigationActionNotFound(exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Mitigation action not found.'
    default_code = 'mitigation_action_not_found'