import inspect
import types
from typing import Dict, Any, Callable, Optional


class Storage(Dict):

  def __call__(self, providerFun: Any, *args, **kwargs) -> Any:
    if inspect.isclass(providerFun):
      return providerFun.provider(self, *args, **kwargs)
    return providerFun(self, *args, **kwargs)


_storage: Optional[Storage] = None


def storage() -> Storage:
  global _storage  # pylint: disable=W0603
  if _storage is None:
    _storage = Storage()
  return _storage


# decorator
def provider(fun_or_class: Any):
  if isinstance(fun_or_class, types.FunctionType):

    def wrapper(ref: Optional[Storage] = None, *args, **kwargs) -> Any:
      ref = ref or storage()
      key = _calculate_key(fun_or_class, *args, **kwargs)

      value = ref.get(key)
      if value is None:
        value = fun_or_class(ref, *args, **kwargs)
        ref[key] = value
      return value

    return wrapper

  else:

    @provider
    def fun(ref: Storage, **kwargs):
      return fun_or_class(ref, **kwargs)

    fun_or_class.provider = fun
    return fun_or_class


def _calculate_key(fun: Callable, *args, **kwargs) -> str:
  key = str(hash(fun))
  for arg in args:
    key += f'_{hash(arg)}'
  for k, v in kwargs.items():
    key += f'_{k}={hash(v)}'
  return key
