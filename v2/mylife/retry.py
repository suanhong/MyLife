import time


def retry(operation, attempts: int = 5, base_delay: float = 1.0, sleep=time.sleep):
    last = None
    for attempt in range(1, attempts + 1):
        try:
            return operation()
        except Exception as exc:
            last = exc
            if attempt == attempts:
                raise
            sleep(base_delay * attempt)
    raise last
