import inspect


async def maybeAwait(result):
  if inspect.isawaitable(result):
    return await result
  return result
