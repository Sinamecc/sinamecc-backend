from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from general.helpers.views import ViewHelper
from general.services import GeneralService


@api_view(['GET', 'PATCH', 'POST', 'DELETE', 'PUT'])
def handler404(request):
    result = { "error_code": 404, "error_message": "Page not found" }
    raise NotFound(detail=result, code=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_post_province(request, province_id=False):

    service = GeneralService()
    view_helper = ViewHelper(service)

    if request.method == 'GET' and not province_id:
        result = view_helper.get_all(request)        
    
    elif request.method == 'GET' and province_id:
        result = view_helper.get_one(request, province_id)
        
    return result

@api_view(['GET', 'POST'])
def get_post_canton(request, canton_id=False):

    service = GeneralService()
    view_helper = ViewHelper(service)
    if request.method == 'GET' and not canton_id:
        result = view_helper.execute_by_name("get_all_canton", request)
    
    elif request.method == 'GET' and canton_id:
        result = view_helper.execute_by_name("get_canton_by_id", request, canton_id)
    
    elif request.method == 'POST' and not canton_id:
        result = view_helper.execute_by_name("get_canton_list", request)
        
    return result

@api_view(['GET', 'POST'])
def get_post_district(request, district_id=False):

    service = GeneralService()
    view_helper = ViewHelper(service)
    if request.method == 'GET' and not district_id:
        result = view_helper.execute_by_name("get_all_district", request)
    
    elif request.method == 'GET' and district_id:
        result = view_helper.execute_by_name("get_district_by_id", request, district_id)
    
    elif request.method == 'POST' and not district_id:
        result = view_helper.execute_by_name("get_district_list", request)
        
    return result

@api_view(['GET'])
def get_dimension(request, dimension_id=False):

    service = GeneralService()
    view_helper = ViewHelper(service)
    
    if request.method == 'GET' and not dimension_id:
        result = view_helper.execute_by_name("get_all_dimension", request)
    
    
    return result

@api_view(['GET', 'POST'])
def get_category_group(request, category_group_id=False):

    service = GeneralService()
    view_helper = ViewHelper(service)
    
    if request.method == 'GET' and not category_group_id:
        result = view_helper.execute_by_name("get_all_category_group", request)

    elif request.method == 'POST' and not category_group_id:
        result = view_helper.execute_by_name("get_category_group_list", request)

    return result

@api_view(['GET', 'POST'])
def get_category(request, category_id=False):

    service = GeneralService()
    view_helper = ViewHelper(service)
    
    if request.method == 'GET' and not category_id:
        result = view_helper.execute_by_name("get_all_category", request)

    elif request.method == 'POST' and not category_id:
        result = view_helper.execute_by_name("get_category_list", request)

    return result

@api_view(['GET'])
def get_category_ct(request, category_ct_id=False):

    service = GeneralService()
    view_helper = ViewHelper(service)

    if request.method == 'GET' and not category_ct_id:
        result = view_helper.execute_by_name("get_all_category_ct", request)

    return result

@api_view(['GET', 'POST'])
def get_characteristic(request, characteristic_id=False):

    service = GeneralService()
    view_helper = ViewHelper(service)

    if request.method == 'GET' and not characteristic_id:
        result = view_helper.execute_by_name("get_all_characteristic", request)

    if request.method == 'POST' and not characteristic_id:
        result = view_helper.execute_by_name("get_characteristic_list", request)

    return result