import asyncio

from typing import Any, Tuple, Optional, Callable, Dict


class CompleterCanceledException(Exception):

  def __init__(self):
    Exception.__init__(self, 'AsyncCompleter canceled')


_tokens: Dict[str, Callable] = {}


class AsyncCompleter:

  def __init__(
    self,
    pollingInterval: float = 0.05,  # seconds
    cancelToken: Optional[str] = None,
  ):
    self.pollingInterval = pollingInterval
    self._calculated = False
    self._result: Any = None
    self._canceled: bool = False
    self._cancelToken = cancelToken

    if cancelToken is not None:
      _tokens[cancelToken] = self.cancel

  def haveResult(self) -> bool:
    return self._calculated

  async def result(self) -> Any:
    """
    Ожидает до тех пор, пока кто-то не положит результат с помощью функции
    putResult().
    
    Может выкинуть исключение CompleterCanceledException, если вычисление
    результата отменено (функция cancel или cancelByToken)
    """
    while not self._calculated:
      await asyncio.sleep(self.pollingInterval)
      if self._canceled:
        raise CompleterCanceledException()
    return self._result

  def tryGetResult(self) -> Tuple[Any, bool]:
    if self._canceled:
      raise CompleterCanceledException()
    if self.haveResult():
      return self._result, True
    else:
      return None, False

  def putResult(self, result: Any):
    if self._cancelToken is not None:
      try:
        _tokens.pop(self._cancelToken)
      except:
        pass
    self._result = result
    self._calculated = True

  def cancel(self):
    self._canceled = True

  @staticmethod
  def cancelByToken(token: str) -> bool:
    cancel = _tokens.get(token)
    if cancel is None:
      return False
    _tokens.pop(token)
    cancel()
    return True
