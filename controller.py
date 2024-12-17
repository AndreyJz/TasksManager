from configdb import session
from Task import Task
import json
import os
import datetime

# DB Controllers

def add_task(name, description):
    task = Task(name=name, description=description)
    session.add(task)
    session.commit()

def get_all_tasks():
    return session.query(Task).all()

def get_task_by_id(task_id):
    return session.query(Task).filter(Task.id == task_id).first()

def update_task(task_id, name=None, description=None, completed=None):
    task = get_task_by_id(task_id)
    if task:
        if name is not None:
            task.name = name
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed
        session.commit()
        return task
    return None

def delete_task(task_id):
    task = get_task_by_id(task_id)
    if task:
        session.delete(task)
        session.commit()
        return True
    return False


# Json Controllers

BASE = 'data/'
def checkFile(archivo:str, data=None):
    if data is None:
        if os.path.isfile(BASE + archivo): 
            with open(BASE + archivo, 'r') as br: 
                data = json.load(br)
            return data
        else: 
            return []
    else:
        with open(BASE + archivo, "w") as bw: 
            json.dump(data, bw, indent=4)

def export_tasks_to_json():
    tasks = get_all_tasks()
    tasks_data = [
        {
            'id': task.id,
            'name': task.name,
            'description': task.description,
            'completed': task.completed,
            'date': task.date.isoformat()
        }
        for task in tasks
    ]
    checkFile('tasks.json', tasks_data)

def import_tasks_from_json(file_data):
    tasks = json.loads(file_data)
    for task_data in tasks:
        task = Task(
            name=task_data['name'],
            description=task_data['description'],
            completed=task_data['completed'],
            date=datetime.datetime.fromisoformat(task_data['date'])
        )
        session.add(task)
    session.commit()

