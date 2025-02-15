from datetime import datetime
from typing import List, Dict, Optional
import uuid

class Task:
    def __init__(self, title: str, description: str, category: str, priority: int, 
                 scheduled_date: str = None, id: str = None, created_at: str = None, 
                 completed: bool = False, completed_at: str = None):
        self.id = id if id else str(uuid.uuid4())
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.completed = completed
        self.created_at = created_at if created_at else datetime.now().isoformat()
        self.completed_at = completed_at
        self.scheduled_date = scheduled_date

    def complete(self):
        """Marca la tarea como completada"""
        self.completed = True
        self.completed_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """Convierte la tarea a un diccionario para almacenamiento"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'priority': self.priority,
            'scheduled_date': self.scheduled_date,
            'created_at': self.created_at,
            'completed': self.completed,
            'completed_at': self.completed_at
        }

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self.undo_stack: List[List[Task]] = []
        self.redo_stack: List[List[Task]] = []

    def add_task(self, title: str, description: str, category: str, 
                priority: int, scheduled_date: str = None) -> Task:
        """Añade una nueva tarea"""
        self._save_state()
        task = Task(title, description, category, priority, scheduled_date)
        self.tasks.append(task)
        return task

    def complete_task(self, task_id: str) -> Optional[Task]:
        """Marca una tarea como completada"""
        self._save_state()
        task = self.get_task_by_id(task_id)
        if task:
            task.complete()
        return task

    def delete_task(self, task_id: str) -> bool:
        """Elimina una tarea"""
        self._save_state()
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Obtiene una tarea por su ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_all_tasks(self) -> List[Task]:
        return self.tasks

    def get_tasks_by_category(self, category: str) -> List[Task]:
        return [task for task in self.tasks if task.category == category]

    def get_tasks_for_date(self, date_str: str) -> List[Task]:
        """Obtiene las tareas programadas para una fecha específica"""
        return [task for task in self.tasks if task.scheduled_date == date_str]

    def undo(self) -> bool:
        """Deshace la última acción"""
        if not self.undo_stack:
            return False
        self.redo_stack.append([Task(**task.to_dict()) for task in self.tasks])
        self.tasks = self.undo_stack.pop()
        return True

    def redo(self) -> bool:
        """Rehace la última acción deshecha"""
        if not self.redo_stack:
            return False
        self.undo_stack.append([Task(**task.to_dict()) for task in self.tasks])
        self.tasks = self.redo_stack.pop()
        return True

    def edit_task(self, task_id: str, title: str, description: str, 
                 category: str, priority: int) -> Optional[Task]:
        """Edita una tarea existente"""
        self._save_state()
        task = self.get_task_by_id(task_id)
        if task:
            task.title = title
            task.description = description
            task.category = category
            task.priority = priority
        return task

    def get_tasks_by_dates(self) -> Dict[str, List[Task]]:
        """Agrupa las tareas por fecha"""
        tasks_by_date = {}
        for task in self.tasks:
            date = task.scheduled_date
            if date:
                if date not in tasks_by_date:
                    tasks_by_date[date] = []
                tasks_by_date[date].append(task)
        return tasks_by_date

    def _save_state(self) -> None:
        """Guarda el estado actual para deshacer/rehacer"""
        tasks_copy = [Task(**task.to_dict()) for task in self.tasks]
        self.undo_stack.append(tasks_copy)
        self.redo_stack.clear()
