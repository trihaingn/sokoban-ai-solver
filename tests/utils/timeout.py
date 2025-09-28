import threading
import functools
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

def timeout(seconds):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    return future.result(timeout=seconds)
                except FutureTimeoutError:
                    raise TimeoutError(f"timed out after {seconds} seconds")
        return wrapper
    return decorator

class TimeoutError(Exception):
    pass