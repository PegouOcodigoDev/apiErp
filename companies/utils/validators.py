import datetime
from rest_framework.exceptions import APIException

def convert_date_format(date_str):
    input_format = "%d/%m/%Y %H:%M"
    output_format = "%Y-%m-%d %H:%M"

    date_obj = datetime.datetime.strptime(date_str, input_format)
    formatted_date = date_obj.strftime(output_format)
    
    return formatted_date

class Validate:


    def validate_data(**kwargs):
        try:
            if 'due_date' in kwargs:
                new_date = datetime.datetime.strftime(datetime.datetime.strptime(kwargs['due_date'], "%d/%m/%Y %H:%M"), "%d/%m/%Y %H:%M")
                kwargs['due_date'] = convert_date_format(new_date)
        except ValueError:
            raise APIException("A data deve ter o padrão: d/m/Y H:M", "date_invalid")

        for key, value in kwargs.items():
            if value is None:
                raise APIException(f"O campo '{key}' não pode ser nulo", "null_field")
                
        return kwargs
    
    def validate_updated_data(obj, **kwargs):
        for field in obj._meta.fields:
            field_name = field.name
            if field_name in kwargs:
                current_value = getattr(obj, field_name)
                new_value = kwargs[field_name]
                if current_value != new_value:
                    setattr(obj, field_name, new_value)
        return obj
        
                        

                
