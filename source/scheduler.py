
class Task(object):
    def __init__(self, name, callback, start_at):
        self.name = name
        self.callback = callback
        self.start_at = start_at
    
    def update(self, dt):
        pass

class Scheduler(object):
    
    def __init__(self):
        self.tasks = {}
    
    def schedule(name, action, requirements, delay):
        pass

