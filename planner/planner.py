class Planner(object):
    def __init__(self):
        self.task_array = []
        self.running = None

    def plan(self, task):
        self.task_array.append(task)

    def run(self):
        while self.task_array:
            actual_task = self.task_array[0]
            self.task_array.remove(self.task_array[0])
            actual_task.send(self.running)
            self.task_array.append(actual_task)

def first_task():
    while True:
        print("FIRST TASK")
        yield

def second_task():
    while True:
        print("SECOND TASK")
        yield

def third_task():
    while True:
        print("THIRD TASK")
        yield

if __name__ == "__main__":
    planner = Planner()
    planner.plan(first_task())
    planner.plan(second_task())
    planner.plan(third_task())
    planner.run()
