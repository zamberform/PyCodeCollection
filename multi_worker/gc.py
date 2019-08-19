class GC(object):
    def __init__(self, dispose):
        self.dispose = dispose

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()
