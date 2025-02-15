from datetime import datetime, date
from typing import Dict, Any, Optional

class StatsManager:
    def __init__(self):
        self._initialize_stats()

    def _initialize_stats(self):
        """Inicializa o reinicia las estadísticas con valores por defecto"""
        self.stats: Dict[str, Any] = {
            "total_points": 0,
            "daily_points": {},
            "category_points": {},
            "tasks_completed": 0,
            "tasks_by_category": {},
            "current_streak": 0,
            "best_streak": 0,
            "last_completion_date": None,
            "total_tasks_completed": 0,
            "completed_by_date": {},  # Aseguramos que este campo siempre existe
            "last_streak_date": None  # También agregamos este campo que faltaba
        }

    def update_task_completion(self, task) -> None:
        """Actualiza las estadísticas cuando se completa una tarea"""
        completion_date = task.scheduled_date or date.today().isoformat()
        points = self._calculate_task_points(task)

        # Actualizar puntos y contadores básicos
        self.stats["total_points"] += points
        self.stats["tasks_completed"] += 1
        self.stats["total_tasks_completed"] += 1

        # Actualizar puntos por fecha
        if completion_date not in self.stats["daily_points"]:
            self.stats["daily_points"][completion_date] = 0
        self.stats["daily_points"][completion_date] += points

        # Actualizar completadas por fecha
        if completion_date not in self.stats["completed_by_date"]:
            self.stats["completed_by_date"][completion_date] = 0
        self.stats["completed_by_date"][completion_date] += 1

        # Actualizar categorías
        if task.category not in self.stats["category_points"]:
            self.stats["category_points"][task.category] = 0
            self.stats["tasks_by_category"][task.category] = 0
        self.stats["category_points"][task.category] += points
        self.stats["tasks_by_category"][task.category] += 1

        # Actualizar racha solo si es un nuevo día
        today = date.today().isoformat()
        if self.stats["last_completion_date"] != today:
            self._update_streak(today)

    def _update_streak(self, completion_date: str) -> None:
        """Actualiza la racha de tareas completadas"""
        if not self.stats["last_completion_date"]:
            # Primera tarea completada
            self.stats["current_streak"] = 1
        else:
            last_date = datetime.strptime(self.stats["last_completion_date"], "%Y-%m-%d").date()
            current_date = datetime.strptime(completion_date, "%Y-%m-%d").date()
            days_diff = (current_date - last_date).days

            if days_diff == 1:
                # Día consecutivo
                self.stats["current_streak"] += 1
            elif days_diff == 0:
                pass  # Mismo día, no afecta la racha
            else:
                self.stats["current_streak"] = 1

        self.stats["last_completion_date"] = completion_date
        if self.stats["current_streak"] > self.stats["best_streak"]:
            self.stats["best_streak"] = self.stats["current_streak"]

    def _calculate_task_points(self, task) -> int:
        """Calcula los puntos para una tarea basado en sus características"""
        points = task.priority * 10
        if task.description and len(task.description.strip()) > 0:
            points += 5
        return points

    def remove_task_points(self, task) -> None:
        """Elimina los puntos asociados a una tarea"""
        if not task.completed:
            return

        points = self._calculate_task_points(task)
        completion_date = task.scheduled_date or task.completed_at.split('T')[0]

        # Actualizar contadores generales
        self.stats["total_points"] = max(0, self.stats["total_points"] - points)
        self.stats["tasks_completed"] = max(0, self.stats["tasks_completed"] - 1)
        self.stats["total_tasks_completed"] = max(0, self.stats["total_tasks_completed"] - 1)

        # Actualizar puntos por fecha
        if completion_date in self.stats["daily_points"]:
            self.stats["daily_points"][completion_date] = max(0, 
                self.stats["daily_points"][completion_date] - points)

        # Actualizar completadas por fecha
        if completion_date in self.stats["completed_by_date"]:
            self.stats["completed_by_date"][completion_date] = max(0,
                self.stats["completed_by_date"][completion_date] - 1)

        # Actualizar categorías
        if task.category in self.stats["category_points"]:
            self.stats["category_points"][task.category] = max(0,
                self.stats["category_points"][task.category] - points)
            self.stats["tasks_by_category"][task.category] = max(0,
                self.stats["tasks_by_category"][task.category] - 1)

    def get_stats(self) -> Dict[str, Any]:
        """Retorna las estadísticas actuales"""
        return self.stats

    def get_tasks_completed_for_date(self, date_str: str) -> int:
        """Retorna el número de tareas completadas para una fecha específica"""
        return self.stats["completed_by_date"].get(date_str, 0)
