from schedulers.scheduler import Scheduler


class NoScheduler(Scheduler):
    TEMPLATE_PATH = None
    SCHEDULER_TYPE = "None"

    @property
    def template_data(self):
        return {}

    def checkqueue(self, _):
        return True
