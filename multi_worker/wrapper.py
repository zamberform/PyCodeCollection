import multiprocessing


class Wrapper():
    def __init__(self):
        self.stop_flag = False
        self.workers = []

    def set_works(self, work_list):
        self.workers = work_list

    def add_works(self, add_list):
        self.workers.append(add_list)

    def is_stop(self):
        return self.stop_flag

    def stop(self):
        self.stop_flag = True
        for process in self.workers:
            if isinstance(process, multiprocessing.Process):
                process.terminate()