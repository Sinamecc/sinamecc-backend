import random, string
from django.utils.translation import get_language

def unique_field_value_generator(instance, size, field_name,set_of_symbols=string.ascii_letters):

    generator = lambda size, chars: ''.join(random.choice(chars) for _ in range(size))
    field_value = generator(size, set_of_symbols)

    instance_class_model= instance.__class__
    record_exists = instance_class_model.objects.filter(**{field_name: field_value}).exists()

    if record_exists:
        return unique_field_value_generator(instance, size, field_name, set_of_symbols)

    return field_value

def get_translation_from_database(instance, field_name):
    lan = get_language()[:2]
    
    if lan in ['en', 'es']:
        if isinstance(instance, dict):
            return instance[f'{field_name}_{lan}']
        
        return getattr(instance, f'{field_name}_{lan}')
    else:
        raise Exception(f'Language {lan} is not supported')
