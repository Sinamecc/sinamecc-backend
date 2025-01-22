from rest_framework import serializers

"""
This document contains the serializers for the responses of the API

Classes:
    SuccessResponseSerializers: Serializer for the success response of the API.
    ErrorResponseSerializers: Serializer for the error response of the API.
    ErrorSerializer: Serializer for the error object of the error response.

Examples:

    SuccessResponseSerializers:
        data = {
            'key': 'value'
        }
        code = 0

    ErrorResponseSerializers:
        code = -1
        error = {
            'code': 'error_code',
            'error': 'error_message'
        }

    ErrorSerializer:
        code = 'error_code'
        error = 'error_message'

code = 0: Success
code = -1: Error Handling
code = -2: Internal Server Error

"""


class SuccessResponseSerializers(serializers.Serializer):
    data = serializers.JSONField()
    code = serializers.IntegerField(default=0)

class ErrorSerializer(serializers.Serializer):
    code = serializers.CharField()
    error = serializers.CharField()

class ErrorResponseSerializers(serializers.Serializer):
    code = serializers.IntegerField(default=-1)
    error = ErrorSerializer()

