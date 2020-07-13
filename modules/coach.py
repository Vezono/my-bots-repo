from timeit import default_timer as timer


class Coach:
    def __init__(self):
        self.start_time = timer()

    def time(self):
        return timer() - self.start_time
