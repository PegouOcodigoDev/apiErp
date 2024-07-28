import datetime
from rest_framework.exceptions import APIException

class Validate:
    def validate_data(**kwargs):
        try:
            if 'due_date' in kwargs:
                kwargs['due_date'] = datetime.datetime.strftime(datetime.datetime.strptime(kwargs['due_date'], "%d/%m/%Y %H:%M"), "%d/%m/%Y %H:%M")
        except ValueError:
            raise APIException("A data deve ter o padrão: d/m/Y H:M", "date_invalid")

        for key, value in kwargs.items():
            if value is None:
                raise APIException(f"O campo '{key}' não pode ser nulo", "null_field")
                
        return kwargs
    
    def validate_updated_data(obj, *args):
        attributes = [attr for attr in dir(obj) if not attr.startswith('__') and not callable(getattr(obj, attr))]
        
        if len(attributes) != len(args):
            raise ValueError("Número de argumentos não corresponde ao número de atributos não-métodos do objeto")
        
        for attr, value in zip(attributes, args):
            current_value = getattr(obj, attr)
            if current_value != value:
                setattr(obj, attr, value)
                
        return obj
        
                        

                
