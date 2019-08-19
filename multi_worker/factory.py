import time
from .helper import (
    safe_queue_get,
    safe_queue_put
)
from queue import Empty


def employer(task_generator, task_queue, worker_count, wrapper):
    try:
        for task in task_generator:
            safe_queue_put(task_queue, task, wrapper.is_stop)
    except Exception:
        print('employer is stop with exception')
        return
    for i in range(worker_count):
        task_queue.put(Empty)
    print('worker employer finished')

def worker(task_queue, result_queue, wrapper, gene_func):
    while not wrapper.is_stop():
        if task_queue.empty():
                # リソース解放時間を与えた方がスムーズにタスクを閉じれる
            time.sleep(0.01)
            continue
        try:
            task = safe_queue_get(task_queue, wrapper.is_stop)
            if task == Empty:
                result_queue.put(Empty)
                break
            for item in gene_func(task):
                safe_queue_put(result_queue, item, wrapper.is_stop)
        except Exception:
            print('worker is stop with exception')
            break
        