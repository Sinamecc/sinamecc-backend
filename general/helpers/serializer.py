class SerializersHelper():

    def get_serialized_record(self, Serializer, data, record = False, partial = False, many = False):

        record_data = self._get_serialized_record_list(Serializer, data) if isinstance(data, list) else \
                        self._get_serialized_record(Serializer, data)
  
        if record:
            serializer = Serializer(record, data = record_data, partial = partial)

        else:
            serializer = Serializer(data = record_data, partial = partial,  many=many)
        
        return serializer
    
    def _get_serialized_record(self, Serializer, data):

        record_data = {}
        for field in Serializer.Meta.fields:
            if field in data:
                record_data[field] = data.get(field)
        
        return record_data
    
    def _get_serialized_record_list(self, Serializer, data):
        record_data = {}
        record_data_list = []
        for record in data:
            
            for field in Serializer.Meta.fields:
                if field in record:
                    record_data[field] = record.get(field)
            record_data_list.append(record_data.copy())
            record_data.clear()

        return record_data_list
    