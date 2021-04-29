from django.urls import reverse

class ServiceHelper():

    def __init__(self):
        self.RECORD_DOES_NOT_EXIST_ERROR = '{0} with ID: {1}, does not exist in our database'
        self.NO_EXISTING_RECORDS = 'There are not {0} records in our database'
        self.HAVE_OCCURRED_AN_ERROR = 'Error: {1}'

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
