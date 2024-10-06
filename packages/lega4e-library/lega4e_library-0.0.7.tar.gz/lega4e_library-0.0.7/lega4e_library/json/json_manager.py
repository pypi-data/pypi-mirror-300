import json

from datetime import datetime
from enum import StrEnum, IntEnum
from typing import Dict, Any

from lega4e_library.attrs.jsonkin import Jsonkin


class JsonEncoder(json.JSONEncoder):

  def default(self, o: Any):
    if isinstance(o, StrEnum) or isinstance(o, IntEnum):
      return o.value
    elif isinstance(o, datetime):
      return o.strftime('%Y.%m.%d %H:%M:%S.%f')
    elif isinstance(o, Jsonkin):
      return o.toJson()
    return super().default(o)


class JsonManager:

  def __init__(self, encoder=None):
    self.encoder = encoder or JsonEncoder

  def loads(self, s: str) -> Dict[str, Any]:
    return json.loads(s)

  def load(self, filename: str) -> Dict[str, Any]:
    return self.loads(open(filename, 'r', encoding='utf-8').read())

  def dumps(self, d: Dict[str, Any], sortKeys: bool = False) -> str:
    return json.dumps(
      d,
      cls=self.encoder,
      separators=(',', ':'),
      ensure_ascii=False,
      sort_keys=sortKeys,
    )

  def pretty(self, d: Dict[str, Any]) -> str:
    return json.dumps(
      d,
      cls=self.encoder,
      indent=2,
      ensure_ascii=False,
    )
