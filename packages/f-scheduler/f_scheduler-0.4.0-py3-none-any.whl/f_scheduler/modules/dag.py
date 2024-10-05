from graphlib import TopologicalSorter


class DAG:
    def __init__(self, use_graphlib=False):
        self.tasks = {}
        self.graph = TopologicalSorter()
        self.use_graphlib = use_graphlib

    def add_task(self, task):
        self.tasks[task.task_id] = task
        if self.use_graphlib:
            self.graph.add(task.task_id)

    def set_downstream(self, task_id, next_task_id):
        if not self.use_graphlib:
            task = self.tasks[task_id]
            next_task = self.tasks[next_task_id]
            task.next(next_task)
        else:
            self.graph.add(task_id, next_task_id)

    def run(self, start_task_id=None):
        if not self.use_graphlib:
            if start_task_id is None:
                start_task_id = list(self.tasks.keys())[0]
            start_task = self.tasks[start_task_id]
            start_task.run()
        else:
            order = list(self.graph.static_order())
            order.reverse()
            for task_id in order:
                self.tasks[task_id].run()

    def clear(self):
        self.tasks.clear()

    def get_return_value(self, task_id):
        return self.tasks[task_id].return_value

    def get_all_tasks(self):
        return self.tasks

    def update_task(self, task_id, new_param):
        if not self.use_graphlib:
            task = self.tasks[task_id]
        else:
            task = self.tasks.get(task_id)
        if task:
            task.param = new_param
        else:
            print(f"No task found with id: {task_id}")
