import time
from functools import wraps

def retry(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    time.sleep(delay)
                    retries += 1
            raise Exception(f"Failed after {max_retries} retries")

        return wrapper

    return decorator
