# engine/task_manager.py

# Global list to store tasks
task_list = []

def add_task(task_name):
    """
    Add a task to the task list.
    """
    task_list.append(task_name)

def remove_task(task_name):
    """
    Remove a task from the task list.
    """
    if task_name in task_list:
        task_list.remove(task_name)
    else:
        raise ValueError(f"Task '{task_name}' not found.")

def get_task_list():
    """
    Retrieve the list of tasks.
    """
    return task_list

def list_tasks():
    """
    Retrieve and format the list of tasks.
    """
    if not task_list:
        return "You have no tasks."
    elif len(task_list) == 1:
        return f"You have 1 task: {task_list[0]}"
    else:
        return "Your tasks are: " + ", ".join(task_list)