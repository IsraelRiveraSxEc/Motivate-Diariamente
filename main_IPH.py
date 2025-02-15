import customtkinter as ctk
from task_manager_IPH import TaskManager, Task  # Importar Task explícitamente
from ui_manager_IPH import UIManager
from data_manager_IPH import DataManager
from stats_manager_IPH import StatsManager

class MotivateApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Motívate Diariamente")
        
        # Inicializar managers
        self.data_manager = DataManager()
        self.task_manager = TaskManager()
        self.stats_manager = StatsManager()
        
        # Cargar datos guardados
        saved_data = self.data_manager.load_data()
        
        # Inicializar UI Manager con las dependencias necesarias
        self.ui_manager = UIManager(
            root=self.root,
            task_manager=self.task_manager,
            stats_manager=self.stats_manager
        )
        
        # Verificar si es la primera ejecución
        is_first_run = not saved_data or "username" not in saved_data
        
        if saved_data:
            # Cargar tareas
            for task_data in saved_data.get("tasks", []):
                self.task_manager.tasks.append(Task(**task_data))
            
            # Cargar estadísticas
            saved_stats = saved_data.get("stats", {})
            default_stats = self.stats_manager.stats.copy()
            default_stats.update(saved_stats)
            self.stats_manager.stats = default_stats
            
            # Cargar username si existe
            if "username" in saved_data:
                self.ui_manager.set_username(saved_data["username"])
        
        # Mostrar diálogo de nombre SOLO si es la primera ejecución
        if is_first_run:
            self.ui_manager.show_name_dialog()
            self.save_all_data()  # Guardar inmediatamente después de obtener el nombre
        
        # Configurar el guardado automático al cerrar
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Configurar el callback de guardado
        self.ui_manager.set_save_callback(self.save_all_data)
    
    def setup_theme(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    
    def save_all_data(self):
        """Guarda todos los datos de la aplicación"""
        data_to_save = {
            "tasks": [task.to_dict() for task in self.task_manager.tasks],
            "stats": self.stats_manager.stats,
            "username": self.ui_manager.username
        }
        self.data_manager.save_data(data_to_save)
    
    def on_closing(self):
        """Método llamado cuando se cierra la aplicación"""
        self.save_all_data()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MotivateApp()
    app.run()
