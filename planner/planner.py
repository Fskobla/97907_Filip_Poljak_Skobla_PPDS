"""
Copyright 2022 Filip Poljak Skobla. All Rights Reserved.
Licensed to GPLv2 www.gnu.org/licenses/old-licenses/gpl-2.0.html

Simple planner with three coroutines
"""


class Planner(object):
    """ A class of planner """
    def __init__(self):
        """
        Constructs all the necessary attributes for the planner object.
        Parameters
        ----------
            task_array : array
                array of tasks
            running : None
                value to send
                    """
        self.task_array = []
        self.running = None

    def plan(self, task):
        """
        Method of planner which add coroutine to plan
        """
        self.task_array.append(task)

    def run(self):
        """
        Method of planner which start the coroutine
        """
        while self.task_array:
            # Select first task
            actual_task = self.task_array[0]
            # Remove it from array (insted of using cycle)
            self.task_array.remove(self.task_array[0])
            # Due to yield
            actual_task.send(self.running)
            # Add actual task to the end of array
            self.task_array.append(actual_task)


def first_task():
    """ First task with print
    """
    while True:
        print("FIRST TASK")
        yield


def second_task():
    """ Second task with print
    """
    while True:
        print("SECOND TASK")
        yield


def third_task():
    """ Third task with print
    """
    while True:
        print("THIRD TASK")
        yield

if __name__ == "__main__":
    """ Initialization of class and add tasks to run
    """
    planner = Planner()
    planner.plan(first_task())
    planner.plan(second_task())
    planner.plan(third_task())
    planner.run()
