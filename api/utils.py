import re

def parse_data(request):
  return request.get_json() if request.is_json else request.form.to_dict()
  
def parse_dict_by_keys(dict, allowed_keys):
  return {key: value for key, value in dict.items() if key in allowed_keys}
  
def snake_to_camel(snake_str):
    components = snake_str.split('_')
    # Capitalize the first letter of each component except the first one
    return components[0] + ''.join(x.title() for x in components[1:])
  

def camel_to_snake(camel_str):
    # Insert an underscore before each uppercase letter, then convert to lowercase
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()
    
def check_empty_field(**kwargs):
  for key, value in kwargs.items():
    if not value or value is None:
      return False
  
  return True