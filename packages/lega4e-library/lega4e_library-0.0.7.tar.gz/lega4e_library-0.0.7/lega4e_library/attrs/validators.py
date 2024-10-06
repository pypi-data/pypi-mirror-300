def list_validator(type):

  def validate(_, __, value):
    if not isinstance(value, list):
      raise ValueError(f'Expected a list of {type.__name__}')
    for item in value:
      if not isinstance(item, type):
        raise ValueError(f'Expected a list of {type.__name__}')
    return value

  return validate


def list_list_validator(type):

  def validate(_, __, value):
    if not isinstance(value, list):
      raise ValueError(f'Expected a list of lists of {type.__name__}')

    for row in value:
      if not isinstance(row, list):
        raise ValueError(f'Expected a list of lists of {type.__name__}')
      for item in row:
        if not isinstance(item, type):
          raise ValueError(f'Expected a list of lists of {type.__name__}')

  return validate
