import multiprocessing


def safe_queue_get(queue, is_stop_func=None, timeout=2):
    while True:
        if is_stop_func is not None and is_stop_func():
            raise Exception
        try:
            data = queue.get(timeout=timeout)
            return data
        except:
            continue

def safe_queue_put(queue, item, is_stop_func=None, timeout=2):
    while True:
        if is_stop_func is not None and is_stop_func():
            raise Exception
        try:
            queue.put(item, timeout=timeout)
            return item
        except:
            continue
