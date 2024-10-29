import time
from functools import wraps


class RateLimit:
    def __init__(self, calls_per_second=1):
        self.calls_per_second = calls_per_second
        self.last_call = 0

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Simple rate limiting
            current_time = time.time()
            time_since_last = current_time - self.last_call
            sleep_time = (1.0 / self.calls_per_second) - time_since_last

            if sleep_time > 0:
                time.sleep(sleep_time)

            self.last_call = time.time()
            return await func(*args, **kwargs)

        return wrapper
