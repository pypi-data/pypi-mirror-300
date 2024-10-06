from typing import Optional

from attr import asdict, field
from attr.validators import instance_of

from .validators import list_validator, list_list_validator


class Jsonkin:

  def toJson(self):
    pass

  @staticmethod
  def fromJson(json):
    pass

  @staticmethod
  def jsonConverter(json):
    pass

  @staticmethod
  def listJsonConverter(json):
    pass

  @staticmethod
  def listListJsonConverter(json):
    pass

  @staticmethod
  def attrField(**kwargs):
    pass

  @staticmethod
  def attrOptionalField(**kwargs):
    pass

  @staticmethod
  def attrListField(**kwargs):
    pass

  @staticmethod
  def attrListListField(**kwargs):
    pass


def jsonkin(cls):

  def toJson(self):

    def serialize(_, __, value):
      if isinstance(value, Jsonkin):
        return value.toJson()
      elif isinstance(value, list):
        return [serialize(None, None, v) for v in value]
      elif isinstance(value, set):
        return {serialize(None, None, v) for v in value}
      elif isinstance(value, dict):
        return {
          serialize(None, None, k): serialize(None, None, v)
          for k, v in value.items()
        }
      return value

    return asdict(self, value_serializer=serialize)

  def fromJson(json):
    filtered = {
      attribute.name: json[attribute.name]
      for attribute in cls.__attrs_attrs__
      if attribute.name in json
    }
    return cls(**filtered)

  def jsonConverter(json):
    if json is None:
      return None
    elif isinstance(json, cls):
      return json
    else:
      return cls.fromJson(json)

  def listJsonConverter(jsons):
    try:
      list_validator(cls)(None, None, jsons)
      return jsons
    except ValueError:
      return [cls.jsonConverter(json) for json in jsons]

  def listListJsonConverter(jsons):
    try:
      list_list_validator(cls)(None, None, jsons)
      return jsons
    except ValueError:
      return [cls.listJsonConverter(json) for json in jsons]

  def attrField(**kwargs):
    return field(
      validator=instance_of(cls),
      converter=cls.jsonConverter,
      **kwargs,
    )

  def attrOptionalField(**kwargs):
    return field(
      validator=instance_of(Optional[cls]),
      converter=cls.jsonConverter,
      **kwargs,
    )

  def attrListField(**kwargs):
    return field(
      validator=list_validator(cls),
      converter=cls.listJsonConverter,
      **kwargs,
    )

  def attrListListField(**kwargs):
    return field(
      validator=list_list_validator(cls),
      converter=cls.listListJsonConverter,
      **kwargs,
    )

  cls.fromJson = fromJson
  cls.toJson = toJson
  cls.jsonConverter = jsonConverter
  cls.listJsonConverter = listJsonConverter
  cls.listListJsonConverter = listListJsonConverter
  cls.attrField = attrField
  cls.attrOptionalField = attrOptionalField
  cls.attrListField = attrListField
  cls.attrListListField = attrListListField
  return cls


def jsonkinEnum(cls):

  def toJson(self):
    return self.value

  def fromJson(json):
    return cls(json)

  def jsonConverter(json):
    if json is None:
      return None
    if isinstance(json, cls):
      return json
    return fromJson(json)

  def listJsonConverter(jsons):
    return [jsonConverter(json) for json in jsons]

  def listListJsonConverter(jsons):
    return [listJsonConverter(json) for json in jsons]

  def attrField(**kwargs):
    return field(
      validator=instance_of(cls),
      converter=jsonConverter,
      **kwargs,
    )

  def attrOptionalField(**kwargs):
    return field(
      validator=instance_of(Optional[cls]),
      converter=jsonConverter,
      **kwargs,
    )

  def attrListField(**kwargs):
    return field(
      validator=list_validator(cls),
      converter=cls.listJsonConverter,
      **kwargs,
    )

  def attrListListField(**kwargs):
    return field(
      validator=list_list_validator(cls),
      converter=cls.listJsonConverter,
      **kwargs,
    )

  cls.fromJson = fromJson
  cls.toJson = toJson
  cls.jsonConverter = jsonConverter
  cls.listJsonConverter = listJsonConverter
  cls.listListJsonConverter = listListJsonConverter
  cls.attrField = attrField
  cls.attrOptionalField = attrOptionalField
  cls.attrListField = attrListField
  cls.attrListListField = attrListListField
  return cls
