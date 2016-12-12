import uuid


class Task(object):

    STATUS_QUEUED = 'queued'
    STATUS_EXECUTING = 'executing'
    STATUS_FAILED = 'failed'
    STATUS_SKIPPED = 'skipped'
    STATUS_COMPLETED = 'completed'

    def __init__(self, job):
        self.id = None
        self.status = self.STATUS_QUEUED
        self.type = None
        self.start_ts = None
        self.finish_ts = None
        self.attempts = 0
        self.error_msg = []
        self.parent_job = job

    def on_exec_start(self, processor):
        """
        Called every time task changes status from 'queued' to 'executing'
        """
        pass

    def on_exec_stop(self, processor):
        """
        Called every time task changes status from 'executing' to anything else
        """
        pass

    @classmethod
    def new(cls, job, **kwargs):
        task = cls(job)
        task.id = uuid.uuid4().hex
        for param in cls.PARAMS:
            setattr(task, param, kwargs.get(param))
        return task

    @classmethod
    def from_data(cls, data, job):
        task = cls(job)
        task.load(data)
        return task

    def load(self, data):
        self.id = data['id']
        self.status = data['status']
        self.type = data['type']
        self.start_ts = data['start_ts']
        self.finish_ts = data['finish_ts']
        self.error_msg = data['error_msg']
        self.attempts = data.get('attempts', 0)

        for param in self.PARAMS:
            val = data.get(param)
            if isinstance(val, unicode):
                val = val.encode('utf-8')
            setattr(self, param, val)

    def dump(self):
        res = {'status': self.status,
               'id': self.id,
               'type': self.type,
               'start_ts': self.start_ts,
               'finish_ts': self.finish_ts,
               'error_msg': self.error_msg,
               'attempts': self.attempts}
        res.update({
            k: getattr(self, k)
            for k in self.PARAMS
        })
        return res

    def human_dump(self):
        return self.dump()

    def __str__(self):
        raise RuntimeError('__str__ method should be implemented in '
            'derived class')
