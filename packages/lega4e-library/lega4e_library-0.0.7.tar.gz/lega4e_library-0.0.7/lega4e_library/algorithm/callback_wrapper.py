from typing import Callable


class CallbackWrapper:

  def __init__(self, callback: Callable, *args, **kwargs):
    self.args = args
    self.kwargs = kwargs
    self.callback = callback

  def __call__(self, *args, **kwargs):
    for key, value in self.kwargs.items():
      kwargs[key] = value
    return self.callback(*self.args, *args, **kwargs)
