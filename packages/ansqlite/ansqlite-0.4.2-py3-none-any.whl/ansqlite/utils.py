import traceback


def trace(msg: str, e: Exception) -> str:
    return '\n'.join([msg] +
        traceback.format_exception(e))
