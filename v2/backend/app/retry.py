import time


def retry(operation, attempts: int = 3, base_delay: float = 1.0, sleep=time.sleep):
    for attempt in range(1, attempts + 1):
        try:
            return operation()
        except Exception:
            if attempt == attempts:
                raise
            sleep(base_delay * attempt)
