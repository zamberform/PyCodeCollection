# -*- coding: utf-8 -*-
# coding=utf-8
import codecs
import logging
import multiprocessing
import time
from queue import Queue, Empty
from .helper import safe_queue_get
from .wrapper import Wrapper
from .gc import GC
from .factory import employer as employer_func
from .factory import worker as worker_func

class MultiWorker():
    workers = []
    wrapper = Wrapper()

    def __init__(self, career_id_list):
        self.career_id_list = career_id_list

    def start(self, customer_func, worker_count=2, queue_size=10):
        result_queue = multiprocessing.Queue(queue_size)
        task_queue = multiprocessing.Queue(queue_size)
        employer_process = multiprocessing.Process(name='employer', target=employer_func, args=(self.career_id_list, task_queue, worker_count, self.wrapper))
        for process_id in range(0, worker_count):
            process_name = 'worker_%s' % (process_id)
            worker_process = multiprocessing.Process(name=process_name, target=worker_func, args=(task_queue, result_queue, self.wrapper, customer_func))
            self.workers.append(worker_process)
        employer_process.start()
        self.wrapper.set_works(self.workers[:])
        self.wrapper.add_works(employer_process)
        for worker in self.workers:
            worker.start()
        with GC(self.wrapper.stop):
            count = 0
            while not self.should_stop():
                try:
                    data = safe_queue_get(result_queue, self.should_stop)
                    if data is Empty:
                        count += 1
                        if count == worker_count:
                            break
                        continue
                except Exception:
                    break
                yield data

    def should_stop(self):
        if not any([r for r in self.workers if r.is_alive()]):
            return True
        return self.wrapper.is_stop()
