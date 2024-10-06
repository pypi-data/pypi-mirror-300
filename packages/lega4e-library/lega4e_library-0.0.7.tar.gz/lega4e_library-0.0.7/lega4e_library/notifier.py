from copy import copy
from typing import Callable, Any, Dict


class Notifier:
  """
  Базовый класс для тех классов, которые могут производить события
  """

  def __init__(self):
    self._listeners: Dict[int, (Any, Callable)] = {}
    self._counter = 0

  def addListener(self, callback: Callable, event=None) -> Callable:
    """
    Добавить слушателя на событие (по умолчанию основное "None"-событие)

    :param callback: функцию, которую нужно вызывать при возникновении события

    :param event: событие, которые нужно слушать у данного объекта

    :return: функцию, вызов которой прервёт отслеживание события
    """
    if not isinstance(event, list):
      self._counter += 1
      self._listeners[self._counter] = (event, callback)
      counter = copy(self._counter)
      return lambda: self._listeners.pop(counter)
    dispose_funs = [self.addListener(callback, e) for e in event]

    def dispose():
      for d in dispose_funs:
        d()

    return dispose

  def notify(self, *args, event=None, **kwargs):
    """
    Требуется вызвать, при наступлении события.
    :param event: Какое именно сыбите произошло
           (по умолчанию основное "None"-событие).
    :param args: Аргументы, которые нужно передать в коллбэк функции.
    :param kwargs: Аргументы, которые нужно передать в коллбэк функции.
    """
    for e, callback in copy(list(self._listeners.values())):
      if e == event:
        callback(self, *args, **kwargs)
    return self
