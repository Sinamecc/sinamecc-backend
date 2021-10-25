from django.urls import reverse

class ServiceHelper():

    def __init__(self, service=None):
        self.RECORD_DOES_NOT_EXIST_ERROR = '{0} with ID: {1}, does not exist in our database'
        self.NO_EXISTING_RECORDS = 'There are not {0} records in our database'
        self.HAVE_OCCURRED_AN_ERROR = 'Error: {1}'
        self.FUNCTION_INSTANCE_ERROR = 'Error Service does not have {0} function'
        self.ATTRIBUTE_INSTANCE_ERROR = 'Instance Model does not have {0} attribute'
        self._service = service

    # auxiliary functions
    def _create_sub_record(self, data, sub_record_name):
        
        create_function = f'_create_update_{sub_record_name}'

        if hasattr(self._service, create_function):
            function = getattr(self._service, create_function)
            record_status, record_detail = function(data=data)
            result = (record_status, record_detail)
        
        else:
            raise Exception(self.FUNCTION_INSTANCE_ERROR.format(create_function))

        return result


    def _update_sub_record(self, sub_record_name, record_for_updating, data):
        
        update_function = f'_create_update_{sub_record_name}'
        
        if hasattr(self._service, update_function):
          
            function = getattr(self._service, update_function)
        
            record_status, record_detail = function(data, record_for_updating)
          
            result = (record_status, record_detail)
        
        else:
            raise Exception(self.FUNCTION_INSTANCE_ERROR.format(update_function))

        return result


    def _create_or_update_record(self, instance, field, data):

        result = (False, [])
        if hasattr(instance, field):
            if getattr(instance, field) == None:
                record_status, record_data = self._create_sub_record(data, field) ## field = sub_record_name

            else:
                ## change field(string) to object(model instance)
                record_for_updating = getattr(instance, field) 
                record_status, record_data = self._update_sub_record(field, record_for_updating, data)
            
            result = (record_status, record_data)
        else:

            result = (False, self.ATTRIBUTE_INSTANCE_ERROR)

        return result


    def create_or_update_record(self, field_list, data, model_instance=None):
        validation_dict = {}
        for field in field_list:
            if data.get(field, False):
                record_status, record_data = self._create_sub_record(data.get(field), field) if not model_instance else \
                                            self._create_or_update_record(model_instance, field, data.get(field))
                    
                if record_status:
                    data[field] = record_data.id
                dict_data = record_data if isinstance(record_data, list) else [record_data]
                validation_dict.setdefault(record_status,[]).extend(dict_data)
        return validation_dict



    def get_one(self, Instance, record_id, **custom_filter):

        result = (False, self.RECORD_DOES_NOT_EXIST_ERROR.format(Instance._meta.verbose_name, record_id))
        try:
            record = Instance.objects.filter(id=record_id).last() if not custom_filter \
                    else Instance.objects.filter(id=record_id, **custom_filter).last()

            if record:
                result = (True, record)

            else:
                result = (False, self.RECORD_DOES_NOT_EXIST_ERROR.format(Instance._meta.verbose_name, record_id))

        except Instance.DoesNotExist as exc:
            result = (False, self.RECORD_DOES_NOT_EXIST_ERROR.format(Instance._meta.verbose_name, record_id))

        except Exception as exc:
            result = (False, self.RECORD_DOES_NOT_EXIST_ERROR.format(str(exc)))

        finally:

            return result


    def get_all(self, Instance, **custom_filter):

        result = (False, self.NO_EXISTING_RECORDS.format(Instance._meta.verbose_name))

        try:
            record_list = Instance.objects.filter(**custom_filter).all()

            result = (True, record_list)

        except Exception as exc:
            result = (False, self.HAVE_OCCURRED_AN_ERROR.format(str(exc)))

        finally:

            return result

    
    def get_download_endpoint(self, view_name,  *args, **kwargs):
 
        url = reverse(view_name, args=args, kwargs=kwargs)

        return url
