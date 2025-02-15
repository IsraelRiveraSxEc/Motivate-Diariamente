from datetime import datetime

class StatsManager:
    def __init__(self):
        self.stats = {
            'total_points': 0,
            'current_streak': 0,
            'last_streak_date': None,
            'completed_tasks': 0,
            'tasks_by_category': {}
        }
        self.load_stats()

    def update_task_completion(self, task):
        today = datetime.now().date()
        today_str = today.strftime('%Y-%m-%d')
        
        # Actualizar puntos
        points = self.calculate_points(task)
        self.stats['total_points'] += points
        self.stats['completed_tasks'] += 1
        
        # Actualizar estadísticas por categoría
        if task.category not in self.stats['tasks_by_category']:
            self.stats['tasks_by_category'][task.category] = 0
        self.stats['tasks_by_category'][task.category] += 1
        
        # Actualizar racha solo si es un nuevo día
        if self.stats['last_streak_date'] != today_str:
            self.stats['current_streak'] += 1
            self.stats['last_streak_date'] = today_str
        
        self.save_stats()
