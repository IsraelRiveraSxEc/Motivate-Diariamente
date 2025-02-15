import json
import os
from datetime import datetime
from typing import Dict, Any

class DataManager:
    def __init__(self):
        self.data_file = "motivate_diariamente_data.json"
        self.backup_dir = "backups"
        self.ensure_backup_dir()

    def ensure_backup_dir(self):
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def datetime_handler(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    def save_data(self, data: Dict[str, Any]):
        try:
            # Guardar datos principales
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=self.datetime_handler)
            
            # Crear backup
            self.create_backup(data)
        except Exception as e:
            print(f"Error al guardar datos: {e}")

    def load_data(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return self.create_empty_data()
        except json.JSONDecodeError:
            # Si el archivo está corrupto, crear uno nuevo
            empty_data = self.create_empty_data()
            self.save_data(empty_data)
            return empty_data
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            return self.create_empty_data()

    def create_backup(self, data: Dict[str, Any]):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.json")
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=self.datetime_handler)
        except Exception as e:
            print(f"Error al crear backup: {e}")

    def create_empty_data(self) -> Dict[str, Any]:
        return {
            "tasks": [],
            "stats": {
                "total_points": 0,
                "daily_points": {},
                "category_points": {},
                "tasks_by_category": {},
                "tasks_completed": 0,
                "current_streak": 0,
                "best_streak": 0,
                "last_completion_date": None,
                "total_tasks_completed": 0
            }
        }

    def restore_backup(self, backup_file: str) -> Dict[str, Any]:
        backup_path = os.path.join(self.backup_dir, backup_file)
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error al restaurar backup: {e}")
            return self.create_empty_data()

    def list_backups(self):
        try:
            return [f for f in os.listdir(self.backup_dir) if f.startswith("backup_") and f.endswith(".json")]
        except Exception as e:
            print(f"Error al listar backups: {e}")
            return []
