import customtkinter as ctk
from typing import Dict, Any
from task_manager_IPH import TaskManager
from stats_manager_IPH import StatsManager
import tkcalendar
from datetime import datetime
from achievement_manager_IPH import AchievementManager
from typing import List
import tkinter.ttk as ttk
import random

class UIManager:
    def __init__(self, root: ctk.CTk, task_manager: TaskManager, stats_manager: StatsManager):
        self.root = root
        self.username = "Usuario"  # Valor por defecto fijo
        self.task_manager = task_manager
        self.stats_manager = stats_manager
        self.achievement_manager = AchievementManager()
        
        # Colores modernos para tema claro
        self.light_theme = {
            "bg_color": "#ffffff",
            "fg_color": "#333333",
            "secondary_bg": "#f0f0f0",
            "accent_color": "#4a90e2",
            "success_color": "#2ecc71",
            "danger_color": "#e74c3c",
            "warning_color": "#f1c40f",
            "text_color": "#333333"
        }
        
        # Colores modernos para tema oscuro
        self.dark_theme = {
            "bg_color": "#1a1a1a",
            "fg_color": "#ffffff",
            "secondary_bg": "#2d2d2d",
            "accent_color": "#3498db",
            "success_color": "#27ae60",
            "danger_color": "#c0392b",
            "warning_color": "#f39c12",
            "text_color": "#ff6b6b"
        }
        
        # Configuración inicial
        self.appearance_mode = "dark"
        self.selected_date = datetime.now().strftime('%Y-%m-%d')
        
        self.update_theme()
        self.setup_ui()

        # Agregar referencia al método de guardado
        self.save_callback = None

    def set_save_callback(self, callback):
        """Establece el callback para guardar datos"""
        self.save_callback = callback

    def setup_ui(self):
        self.selected_date = datetime.now().strftime('%Y-%m-%d')
        
        # Configuración inicial del tema
        self.update_theme()
        
        # Centrar la ventana
        window_width = int(self.root.winfo_screenwidth() * 0.8)
        window_height = int(self.root.winfo_screenheight() * 0.8)
        x = (self.root.winfo_screenwidth() - window_width) // 2
        y = (self.root.winfo_screenheight() - window_height) // 2
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Configurar el frame principal solo una vez
        self.setup_main_layout()
        
        # Configurar los componentes de la UI
        self.setup_task_input()
        self.setup_task_list()
        self.setup_stats_panel()
        self.setup_calendar()
        
        # Finalmente, configuramos los colores
        self.update_theme()

    def update_theme(self):
        theme = self.light_theme if self.appearance_mode == "light" else self.dark_theme
        for key, value in theme.items():
            setattr(self, key, value)
        
        # Actualizar el color del texto de bienvenida
        if hasattr(self, 'welcome_label'):
            self.welcome_label.configure(text_color=self.text_color)
        
        self.update_calendar_style()
        if hasattr(self, 'calendar'):
            self.update_calendar_colors()

    def update_all_widgets_colors(self):
        for widget in self.root.winfo_children():
            self._update_widget_colors(widget)

    def _update_widget_colors(self, widget):
        if isinstance(widget, ctk.CTkLabel):
            widget.configure(text_color=self.fg_color)
        elif isinstance(widget, ctk.CTkFrame):
            widget.configure(fg_color=self.bg_color)
        elif isinstance(widget, ctk.CTkEntry):
            widget.configure(
                fg_color=self.entry_bg_color,
                text_color=self.entry_fg_color,
                placeholder_text_color=self.entry_fg_color
            )
        
        # Recursivamente actualizar widgets hijos
        for child in widget.winfo_children():
            self._update_widget_colors(child)

    def toggle_theme(self):
        self.appearance_mode = "dark" if self.appearance_mode == "light" else "light"
        self.update_theme()
        self.refresh_ui()

    def refresh_ui(self):
        """Actualiza todos los elementos de la UI con los colores del tema actual"""
        # Actualizar frames principales
        self.root.configure(fg_color=self.bg_color)
        self.main_frame.configure(fg_color=self.bg_color)
        self.left_frame.configure(fg_color=self.bg_color)
        self.right_frame.configure(fg_color=self.bg_color)
        self.header_frame.configure(fg_color=self.bg_color)
        self.task_list_frame.configure(fg_color=self.bg_color)
        
        # Actualizar panel de estadísticas
        if hasattr(self, 'stats_frame'):
            self.stats_frame.configure(fg_color=self.secondary_bg)
        if hasattr(self, 'stats_title_label'):
            self.stats_title_label.configure(text_color=self.fg_color)
        if hasattr(self, 'points_label'):
            self.points_label.configure(text_color=self.fg_color)
        
        # Actualizar el texto de bienvenida
        self.welcome_label.configure(text_color=self.text_color)
        
        # Actualizar otros elementos
        self.refresh_task_list()
        self.update_calendar_style()

    def setup_main_layout(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Frames izquierdo y derecho
        self.left_frame = ctk.CTkFrame(self.main_frame)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Header del frame izquierdo
        self.header_frame = ctk.CTkFrame(self.left_frame)
        self.header_frame.pack(fill="x", padx=5, pady=5)

        # Label para el nombre de usuario con color inicial
        self.welcome_label = ctk.CTkLabel(
            self.header_frame,
            text="",  # Se actualizará con update_welcome_message
            font=("Segoe UI", 16, "bold"),
            text_color=self.text_color,  # Usar el color de texto del tema
            anchor="w"
        )
        self.welcome_label.pack(side="left", padx=5, fill="x", expand=True)

        # Botón de tema en el header
        self.theme_button = ctk.CTkButton(
            self.header_frame,
            text="🌓",
            command=self.toggle_theme,
            width=40,
            height=40,
            font=("Segoe UI", 16),
            fg_color=self.accent_color,
            hover_color=self.success_color
        )
        self.theme_button.pack(side="right", padx=5)

        self.right_frame = ctk.CTkFrame(self.main_frame)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    def setup_task_input(self):
        # Frame para entrada de tareas
        input_frame = ctk.CTkFrame(self.left_frame)
        input_frame.pack(fill="x", padx=5, pady=5)

        # Título
        self.title_entry = ctk.CTkEntry(input_frame, placeholder_text="Título de la tarea")
        self.title_entry.pack(fill="x", padx=5, pady=5)

        # Descripción
        self.desc_entry = ctk.CTkEntry(input_frame, placeholder_text="Descripción")
        self.desc_entry.pack(fill="x", padx=5, pady=5)

        # Categoría
        self.category_var = ctk.StringVar(value="Personal")
        categories = ["Personal", "Trabajo", "Estudio", "Salud", "Ejercicio", "Hogar", "Proyectos", "Otros"]
        self.category_menu = ctk.CTkOptionMenu(input_frame, values=categories, variable=self.category_var)
        self.category_menu.pack(fill="x", padx=5, pady=5)

        # Prioridad con estrellas
        self.priority_var = ctk.IntVar(value=3)
        self.priority_display = {
            1: "⭐",
            2: "⭐⭐",
            3: "⭐⭐⭐",
            4: "⭐⭐⭐⭐",
            5: "⭐⭐⭐⭐⭐"
        }
        
        priority_container = ctk.CTkFrame(input_frame)
        priority_container.pack(fill="x", padx=5, pady=5)
        
        priority_label = ctk.CTkLabel(
            priority_container,
            text="Nivel de prioridad:",
            font=("Arial", 12)
        )
        priority_label.pack(side="left", padx=5)
        
        self.priority_menu = ctk.CTkOptionMenu(
            priority_container,
            values=[self.priority_display[i] for i in range(1, 6)],
            variable=self.priority_var,
            width=120,
            command=self.on_priority_change
        )
        self.priority_menu.pack(side="left", padx=5)

        # Botón agregar
        self.add_button = ctk.CTkButton(input_frame, text="Agregar Tarea", command=self.add_task)
        self.add_button.pack(fill="x", padx=5, pady=5)

        # Fecha
        self.date_label = ctk.CTkLabel(input_frame, 
            text=f"Fecha seleccionada: {self.selected_date}")
        self.date_label.pack(fill="x", padx=5, pady=5)

    def on_priority_change(self, value):
        # Convertir estrellas a número
        for num, stars in self.priority_display.items():
            if stars == value:
                self.priority_var.set(num)
                break

    def setup_task_list(self):
        # Frame para lista de tareas
        self.task_list_frame = ctk.CTkScrollableFrame(self.left_frame)
        self.task_list_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def setup_stats_panel(self):
        # Frame para estadísticas con color de fondo específico
        self.stats_frame = ctk.CTkFrame(
            self.right_frame,
            fg_color=self.secondary_bg
        )
        self.stats_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Título de estadísticas
        self.stats_title_label = ctk.CTkLabel(
            self.stats_frame,
            text="Estadísticas",
            font=("Arial", 20, "bold"),
            text_color=self.fg_color
        )
        self.stats_title_label.pack(pady=10)

        # Frame para los detalles de estadísticas
        self.stats_details_frame = ctk.CTkFrame(
            self.stats_frame,
            fg_color="transparent"
        )
        self.stats_details_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Puntos totales
        self.points_label = ctk.CTkLabel(
            self.stats_details_frame,
            text="Puntos totales: 0",
            font=("Arial", 14),
            text_color=self.fg_color
        )
        self.points_label.pack(pady=5)

    def setup_calendar(self):
        # Eliminar el streak frame duplicado de arriba y mantener solo el de abajo
        calendar_frame = ctk.CTkFrame(self.right_frame, fg_color=self.secondary_bg)
        calendar_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configurar estilo del calendario
        style = ttk.Style()
        self.update_calendar_style()
        
        self.calendar = tkcalendar.Calendar(
            calendar_frame,
            selectmode='day',
            date_pattern='y-mm-dd',
            style='Custom.Calendar',
            font=('Segoe UI', 10),
            borderwidth=0,
            showweeknumbers=False
        )
        self.calendar.pack(fill="both", expand=True, padx=5, pady=5)
        self.calendar.bind("<<CalendarSelected>>", self.on_date_selected)

        # Streak frame mejorado
        streak_frame = ctk.CTkFrame(self.right_frame, fg_color=self.accent_color)
        streak_frame.pack(fill="x", padx=10, pady=10)
        
        self.streak_label = ctk.CTkLabel(
            streak_frame,
            text="🔥 Racha actual: 0 días",
            font=("Segoe UI", 20, "bold"),
            text_color="white"
        )
        self.streak_label.pack(pady=10)

    def on_date_selected(self, event=None):
        self.selected_date = self.calendar.get_date()
        self.date_label.configure(text=f"Fecha seleccionada: {self.selected_date}")
        self.refresh_task_list()

    def add_task(self):
        title = self.title_entry.get()
        description = self.desc_entry.get()
        category = self.category_var.get()
        priority = self.priority_var.get()

        if title:
            task = self.task_manager.add_task(
                title, description, category, priority, self.selected_date)
            self.create_task_widget(task)
            self.clear_inputs()
            self.update_calendar_colors()  # Actualizar colores inmediatamente

    def create_task_widget(self, task):
        task_frame = ctk.CTkFrame(
            self.task_list_frame,
            fg_color=self.secondary_bg if task.completed else self.bg_color
        )
        task_frame.pack(fill="x", padx=10, pady=5)

        info_frame = ctk.CTkFrame(task_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, padx=5)
        
        title_label = ctk.CTkLabel(
            info_frame,
            text=task.title,
            font=("Segoe UI", 12, "bold"),
            text_color=self.fg_color
        )
        title_label.pack(anchor="w")

        if task.description:
            desc_label = ctk.CTkLabel(
                info_frame,
                text=task.description,
                font=("Segoe UI", 10),
                text_color=self.fg_color
            )
            desc_label.pack(anchor="w")

        meta_text = f"📋 {task.category} | {'⭐' * task.priority}"
        meta_label = ctk.CTkLabel(
            info_frame,
            text=meta_text,
            font=("Segoe UI", 10),
            text_color=self.fg_color
        )
        meta_label.pack(anchor="w")

        button_frame = ctk.CTkFrame(task_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=5)

        if not task.completed:
            complete_btn = ctk.CTkButton(
                button_frame,
                text="✓",
                width=30,
                height=30,
                font=("Segoe UI", 14),  # Ajustado el tamaño de fuente
                command=lambda: self.complete_task(task.id),
                fg_color=self.success_color,
                hover_color=self.success_color
            )
            complete_btn.pack(side="left", padx=2)
            
            edit_btn = ctk.CTkButton(
                button_frame,
                text="✎",
                width=30,
                height=30,
                font=("Segoe UI", 14),  
                command=lambda: self.edit_task_dialog(task),
                fg_color=self.accent_color,
                hover_color=self.accent_color
            )
            edit_btn.pack(side="left", padx=2)

        delete_btn = ctk.CTkButton(
            button_frame,
            text="🗑",  
            width=30,
            height=30,
            font=("Segoe UI", 13),  
            command=lambda: self.delete_task(task.id),
            fg_color=self.danger_color,
            hover_color=self.danger_color
        )
        delete_btn.pack(side="left", padx=2)

    def clear_inputs(self):
        self.title_entry.delete(0, 'end')
        self.desc_entry.delete(0, 'end')
        self.category_var.set("Personal")
        self.priority_var.set(3)

    def complete_task(self, task_id):
        task = self.task_manager.complete_task(task_id)
        if task:
            self.stats_manager.update_task_completion(task)
            
            # Obtener estadísticas actualizadas
            stats = self.stats_manager.get_stats()
            
            # Actualizar la racha en el botón azul
            if hasattr(self, 'streak_label'):
                self.streak_label.configure(
                    text=f"🔥 Racha actual: {stats['current_streak']} días"
                )
            
            # Obtener mensaje motivacional contextualizado
            message = self.achievement_manager.get_random_message(task=task, stats=stats)
            
            # Mostrar mensaje motivacional
            self.show_motivation_popup(message)
            
            # Verificar logros
            unlocked = self.achievement_manager.check_achievements(stats, task)
            if unlocked:
                self.show_achievements_popup(unlocked)
            
            self.update_stats_display()
            self.refresh_task_list()
            self.update_calendar_colors()

    def show_motivation_popup(self, message: str):
        popup = ctk.CTkToplevel(self.root)
        popup.title("¡Motivación!")
        
        # Hacer la ventana modal
        popup.grab_set()
        
        # Frame con scroll
        scroll_frame = ctk.CTkScrollableFrame(
            popup,
            fg_color=self.bg_color,
            width=400
        )
        scroll_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Contenido
        title_label = ctk.CTkLabel(
            scroll_frame,
            text="¡Excelente Trabajo! 🌟",
            font=("Segoe UI", 24, "bold"),
            text_color=self.fg_color
        )
        title_label.pack(pady=(0, 20))
        
        message_label = ctk.CTkLabel(
            scroll_frame,
            text=message,
            font=("Segoe UI", 16),
            wraplength=360,
            text_color=self.fg_color
        )
        message_label.pack(pady=15)
        
        button = ctk.CTkButton(
            scroll_frame,
            text="¡Gracias!",
            command=popup.destroy,
            width=200,
            height=40,
            font=("Segoe UI", 14, "bold"),
            fg_color=self.accent_color,
            hover_color=self.success_color
        )
        button.pack(pady=20)
        
        # Ajustar tamaño y posición
        width = 450
        height = 300
        x = self.root.winfo_x() + (self.root.winfo_width() - width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - height) // 2
        popup.geometry(f'{width}x{height}+{x}+{y}')

    def show_achievements_popup(self, achievements: List[str]):
        popup = ctk.CTkToplevel(self.root)
        popup.title("¡Nuevos Logros Desbloqueados!")
        popup.geometry("600x400")  # Ventana más grande para logros
        
        # Hacer la ventana modal
        popup.grab_set()
        
        # Centrar la ventana
        popup.update_idletasks()
        width = 600  # Ancho fijo
        height = 400  # Alto fijo
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f'{width}x{height}+{x}+{y}')
        
        # Contenedor principal con padding
        frame = ctk.CTkFrame(popup)
        frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        # Título
        title_label = ctk.CTkLabel(
            frame,
            text="🏆 ¡Felicitaciones! 🏆",
            font=("Arial", 28, "bold")
        )
        title_label.pack(pady=(0, 30))
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            frame,
            text="Has desbloqueado los siguientes logros:",
            font=("Arial", 18)
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Frame para los logros
        achievements_frame = ctk.CTkFrame(frame)
        achievements_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Mostrar cada logro con un ícono y formato especial
        for achievement in achievements:
            achievement_label = ctk.CTkLabel(
                achievements_frame,
                text=f"🌟 {achievement}",
                font=("Arial", 16, "bold"),
                pady=10
            )
            achievement_label.pack()
        
        # Mensaje motivacional
        motivation_label = ctk.CTkLabel(
            frame,
            text="¡Sigue así! Cada logro te acerca más a tus metas.",
            font=("Arial", 16),
            text_color="#FFD700"  # Color dorado para el mensaje
        )
        motivation_label.pack(pady=20)
        
        # Botón de cierre
        button = ctk.CTkButton(
            frame,
            text="¡Continuar!",
            command=popup.destroy,
            width=200,
            height=40,
            font=("Arial", 16)
        )
        button.pack(pady=20)
        
        # Auto-cerrar después de 8 segundos para logros
        popup.after(8000, popup.destroy)

    def delete_task(self, task_id):
        task = self.task_manager.get_task_by_id(task_id)
        if task and self.task_manager.delete_task(task_id):
            if task.completed:
                self.stats_manager.remove_task_points(task)
                self.update_stats_display()
            self.refresh_task_list()
            self.update_calendar_colors()

    def refresh_task_list(self):
        """Actualiza la lista de tareas mostrada"""
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()
        
        # Obtener tareas para la fecha seleccionada
        tasks = self.task_manager.get_tasks_for_date(self.selected_date)
        
        # Ordenar tareas: primero no completadas, luego por prioridad
        tasks.sort(key=lambda x: (x.completed, -x.priority))
        
        for task in tasks:
            self.create_task_widget(task)

    def update_stats_display(self):
        """Actualiza la visualización de las estadísticas"""
        stats = self.stats_manager.get_stats()
        
        # Actualizar puntos totales
        if hasattr(self, 'points_label'):
            self.points_label.configure(
                text=f"Puntos totales: {stats['total_points']}",
                text_color=self.fg_color
            )
        
        # Actualizar la racha en el botón azul
        if hasattr(self, 'streak_label'):
            self.streak_label.configure(
                text=f"🔥 Racha actual: {stats['current_streak']} días"
            )

    def edit_task_dialog(self, task):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Editar Tarea")
        dialog.grab_set()
        
        # Crear un frame principal con padding
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Frame scrollable para el contenido
        scroll_frame = ctk.CTkScrollableFrame(main_frame, height=400)  # Altura fija para el contenido
        scroll_frame.pack(fill="both", expand=True)
        
        # Título
        title_label = ctk.CTkLabel(scroll_frame, text="Título:")
        title_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        title_entry = ctk.CTkEntry(scroll_frame, width=300)  # Ancho fijo para entradas
        title_entry.pack(fill="x", padx=10, pady=(0, 15))
        title_entry.insert(0, task.title)
        
        # Descripción
        desc_label = ctk.CTkLabel(scroll_frame, text="Descripción:")
        desc_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        desc_entry = ctk.CTkEntry(scroll_frame, width=300)
        desc_entry.pack(fill="x", padx=10, pady=(0, 15))
        desc_entry.insert(0, task.description)
        
        # Categoría
        category_label = ctk.CTkLabel(scroll_frame, text="Categoría:")
        category_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        category_var = ctk.StringVar(value=task.category)
        category_menu = ctk.CTkOptionMenu(
            scroll_frame,
            values=["Personal", "Trabajo", "Estudio", "Salud", "Ejercicio", "Otro"],
            variable=category_var,
            width=300
        )
        category_menu.pack(fill="x", padx=10, pady=(0, 15))
        
        # Prioridad
        priority_label = ctk.CTkLabel(scroll_frame, text="Prioridad:")
        priority_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        priority_var = ctk.IntVar(value=task.priority)
        priority_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        priority_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        star_buttons = []
        for i in range(1, 6):
            btn = ctk.CTkButton(
                priority_frame,
                text="★" if i <= task.priority else "☆",
                width=30,
                height=30,
                command=lambda x=i: update_priority(x)
            )
            btn.pack(side="left", padx=2)
            star_buttons.append(btn)
        
        def update_priority(value):
            priority_var.set(value)
            for i, btn in enumerate(star_buttons, 1):
                btn.configure(text="★" if i <= value else "☆")
        
        # Frame para botones (fuera del scroll_frame)
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=(15, 0))
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Guardar",
            command=lambda: self.save_task_edit(
                dialog,
                task.id,
                title_entry.get(),
                desc_entry.get(),
                category_var.get(),
                priority_var.get()
            )
        )
        save_btn.pack(side="left", padx=5, expand=True)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            command=dialog.destroy
        )
        cancel_btn.pack(side="right", padx=5, expand=True)
        
        # Ajustar tamaño y posición de la ventana
        dialog.update_idletasks()
        width = 400
        height = 600  # Altura fija más grande
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')

    def on_edit_priority_change(self, value, priority_var):
        # Convertir estrellas a número
        for num, stars in self.priority_display.items():
            if stars == value:
                priority_var.set(num)
            # Obtener mensaje motivacional contextualizado
            stats = self.stats_manager.get_stats()
            message = self.achievement_manager.get_random_message(task=TaskManager)
            
            # Mostrar mensaje motivacional
            self.show_motivation_popup(message)
            
            # Verificar logros
            unlocked = self.achievement_manager.check_achievements(stats, TaskManager)
            if unlocked:
                self.show_achievements_popup(unlocked)
            
            self.update_stats_display()
            self.refresh_task_list()
            self.update_calendar_colors()

    def show_motivation_popup(self, message: str):
        popup = ctk.CTkToplevel(self.root)
        popup.title("¡Motivación!")
        
        # Hacer la ventana modal
        popup.grab_set()
        
        # Frame con scroll
        scroll_frame = ctk.CTkScrollableFrame(
            popup,
            fg_color=self.bg_color,
            width=400
        )
        scroll_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Contenido
        title_label = ctk.CTkLabel(
            scroll_frame,
            text="¡Excelente Trabajo! 🌟",
            font=("Segoe UI", 24, "bold"),
            text_color=self.fg_color
        )
        title_label.pack(pady=(0, 20))
        
        message_label = ctk.CTkLabel(
            scroll_frame,
            text=message,
            font=("Segoe UI", 16),
            wraplength=360,
            text_color=self.fg_color
        )
        message_label.pack(pady=15)
        
        button = ctk.CTkButton(
            scroll_frame,
            text="¡Gracias!",
            command=popup.destroy,
            width=200,
            height=40,
            font=("Segoe UI", 14, "bold"),
            fg_color=self.accent_color,
            hover_color=self.success_color
        )
        button.pack(pady=20)
        
        # Ajustar tamaño y posición
        width = 450
        height = 300
        x = self.root.winfo_x() + (self.root.winfo_width() - width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - height) // 2
        popup.geometry(f'{width}x{height}+{x}+{y}')

    def show_achievements_popup(self, achievements: List[str]):
        popup = ctk.CTkToplevel(self.root)
        popup.title("¡Nuevos Logros Desbloqueados!")
        popup.geometry("600x400")  # Ventana más grande para logros
        
        # Hacer la ventana modal
        popup.grab_set()
        
        # Centrar la ventana
        popup.update_idletasks()
        width = 600  # Ancho fijo
        height = 400  # Alto fijo
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f'{width}x{height}+{x}+{y}')
        
        # Contenedor principal con padding
        frame = ctk.CTkFrame(popup)
        frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        # Título
        title_label = ctk.CTkLabel(
            frame,
            text="🏆 ¡Felicitaciones! 🏆",
            font=("Arial", 28, "bold")
        )
        title_label.pack(pady=(0, 30))
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            frame,
            text="Has desbloqueado los siguientes logros:",
            font=("Arial", 18)
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Frame para los logros
        achievements_frame = ctk.CTkFrame(frame)
        achievements_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Mostrar cada logro con un ícono y formato especial
        for achievement in achievements:
            achievement_label = ctk.CTkLabel(
                achievements_frame,
                text=f"🌟 {achievement}",
                font=("Arial", 16, "bold"),
                pady=10
            )
            achievement_label.pack()
        
        # Mensaje motivacional
        motivation_label = ctk.CTkLabel(
            frame,
            text="¡Sigue así! Cada logro te acerca más a tus metas.",
            font=("Arial", 16),
            text_color="#FFD700"  # Color dorado para el mensaje
        )
        motivation_label.pack(pady=20)
        
        # Botón de cierre
        button = ctk.CTkButton(
            frame,
            text="¡Continuar!",
            command=popup.destroy,
            width=200,
            height=40,
            font=("Arial", 16)
        )
        button.pack(pady=20)
        
        # Auto-cerrar después de 8 segundos para logros
        popup.after(8000, popup.destroy)

    def delete_task(self, task_id):
        task = self.task_manager.get_task_by_id(task_id)
        if task and self.task_manager.delete_task(task_id):
            if task.completed:
                self.stats_manager.remove_task_points(task)
                self.update_stats_display()
            self.refresh_task_list()
            self.update_calendar_colors()

    def refresh_task_list(self):
        """Actualiza la lista de tareas mostrada"""
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()
        
        # Obtener tareas para la fecha seleccionada
        tasks = self.task_manager.get_tasks_for_date(self.selected_date)
        
        # Ordenar tareas: primero no completadas, luego por prioridad
        tasks.sort(key=lambda x: (x.completed, -x.priority))
        
        for task in tasks:
            self.create_task_widget(task)

    def update_stats_display(self):
        """Actualiza la visualización de las estadísticas"""
        stats = self.stats_manager.get_stats()
        if hasattr(self, 'points_label'):
            self.points_label.configure(
                text=f"Puntos totales: {stats['total_points']}",
                text_color=self.fg_color
            )

    def edit_task_dialog(self, task):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Editar Tarea")
        dialog.grab_set()
        
        # Crear un frame principal con padding
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Frame scrollable para el contenido
        scroll_frame = ctk.CTkScrollableFrame(main_frame, height=400)  # Altura fija para el contenido
        scroll_frame.pack(fill="both", expand=True)
        
        # Título
        title_label = ctk.CTkLabel(scroll_frame, text="Título:")
        title_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        title_entry = ctk.CTkEntry(scroll_frame, width=300)  # Ancho fijo para entradas
        title_entry.pack(fill="x", padx=10, pady=(0, 15))
        title_entry.insert(0, task.title)
        
        # Descripción
        desc_label = ctk.CTkLabel(scroll_frame, text="Descripción:")
        desc_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        desc_entry = ctk.CTkEntry(scroll_frame, width=300)
        desc_entry.pack(fill="x", padx=10, pady=(0, 15))
        desc_entry.insert(0, task.description)
        
        # Categoría
        category_label = ctk.CTkLabel(scroll_frame, text="Categoría:")
        category_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        category_var = ctk.StringVar(value=task.category)
        category_menu = ctk.CTkOptionMenu(
            scroll_frame,
            values=["Personal", "Trabajo", "Estudio", "Salud", "Ejercicio", "Otro"],
            variable=category_var,
            width=300
        )
        category_menu.pack(fill="x", padx=10, pady=(0, 15))
        
        # Prioridad
        priority_label = ctk.CTkLabel(scroll_frame, text="Prioridad:")
        priority_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        priority_var = ctk.IntVar(value=task.priority)
        priority_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        priority_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        star_buttons = []
        for i in range(1, 6):
            btn = ctk.CTkButton(
                priority_frame,
                text="★" if i <= task.priority else "☆",
                width=30,
                height=30,
                command=lambda x=i: update_priority(x)
            )
            btn.pack(side="left", padx=2)
            star_buttons.append(btn)
        
        def update_priority(value):
            priority_var.set(value)
            for i, btn in enumerate(star_buttons, 1):
                btn.configure(text="★" if i <= value else "☆")
        
        # Frame para botones (fuera del scroll_frame)
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=(15, 0))
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Guardar",
            command=lambda: self.save_task_edit(
                dialog,
                task.id,
                title_entry.get(),
                desc_entry.get(),
                category_var.get(),
                priority_var.get()
            )
        )
        save_btn.pack(side="left", padx=5, expand=True)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            command=dialog.destroy
        )
        cancel_btn.pack(side="right", padx=5, expand=True)
        
        # Ajustar tamaño y posición de la ventana
        dialog.update_idletasks()
        width = 400
        height = 600  # Altura fija más grande
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')

    def on_edit_priority_change(self, value, priority_var):
        # Convertir estrellas a número
        for num, stars in self.priority_display.items():
            if stars == value:
                priority_var.set(num)
                break

    def refresh_task_list(self):
        # Limpiar lista actual
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()
        
        # Obtener tareas para la fecha seleccionada
        tasks = self.task_manager.get_tasks_for_date(self.selected_date)
        
        # Ordenar tareas: primero no completadas, luego por prioridad
        tasks.sort(key=lambda x: (x.completed, -x.priority))
        
        for task in tasks:
            self.create_task_widget(task)

    def update_calendar_colors(self):
        """Actualiza los colores del calendario basado en las tareas"""
        if not hasattr(self, 'calendar'):
            return
        
        # Limpiar eventos anteriores
        for tag in self.calendar.tag_names():
            self.calendar.tag_delete(tag)

        tasks_by_date = self.task_manager.get_tasks_by_dates()
        
        for date_str, tasks in tasks_by_date.items():
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                
                completed_tasks = sum(1 for task in tasks if task.completed)
                total_tasks = len(tasks)
                high_priority_tasks = sum(1 for task in tasks if task.priority >= 4)
                
                if total_tasks > 0:
                    # Determinar el color basado en el estado de las tareas
                    if completed_tasks == total_tasks:
                        color = self.success_color
                    elif completed_tasks > 0:
                        color = self.warning_color if high_priority_tasks > 0 else "#ffd700"
                    else:
                        color = self.danger_color if high_priority_tasks > 0 else "#ff7f50"
                    
                    # Crear evento en el calendario
                    self.calendar.calevent_create(
                        date=date_obj,
                        text=f"{completed_tasks}/{total_tasks} tareas completadas",
                        tags=[f"tag_{date_str}"]
                    )
                    self.calendar.tag_config(f"tag_{date_str}", background=color)
                    
            except ValueError as e:
                print(f"Error al procesar fecha {date_str}: {e}")

    def update_calendar_style(self):
        style = ttk.Style()
        
        if self.appearance_mode == "dark":
            # Tema oscuro
            style.configure(
                "Custom.Calendar",
                background=self.bg_color,
                foreground=self.fg_color,
                arrowcolor="#ffffff",
                bordercolor=self.accent_color,
                headersbackground=self.accent_color,
                headersforeground="#ffffff",
                selectbackground=self.success_color,
                selectforeground="#ffffff",
                normalbackground=self.secondary_bg,
                normalforeground=self.fg_color,
                weekendbackground=self.secondary_bg,
                weekendforeground=self.accent_color,
                othermonthbackground=self.bg_color,
                othermonthforeground="#666666",
                arrowstyle="custom",  # Estilo personalizado para las flechas
            )
            
            # Personalizar las flechas del calendario
            style.layout('custom.Calendar.leftarrow', [
                ('custom.Calendar.leftarrow.button', {
                    'sticky': 'nswe',
                    'children': [
                        ('custom.Calendar.leftarrow.image', {'sticky': 'nswe'})
                    ]
                })
            ])
            
            style.layout('custom.Calendar.rightarrow', [
                ('custom.Calendar.rightarrow.button', {
                    'sticky': 'nswe',
                    'children': [
                        ('custom.Calendar.rightarrow.image', {'sticky': 'nswe'})
                    ]
                })
            ])
            
        else:
            # Tema claro
            style.configure(
                "Custom.Calendar",
                background="#ffffff",
                foreground="#333333",
                arrowcolor="#333333",
                bordercolor=self.accent_color,
                headersbackground=self.accent_color,
                headersforeground="#ffffff",
                selectbackground=self.success_color,
                selectforeground="#ffffff",
                normalbackground="#ffffff",
                normalforeground="#333333",
                weekendbackground="#f5f5f5",
                weekendforeground=self.accent_color,
                othermonthbackground="#fafafa",
                othermonthforeground="#999999",
                arrowstyle="custom",
            )

    def update_ui_colors(self):
        # Actualizar colores de la interfaz principal
        self.root.configure(fg_color=self.bg_color)
        
        # Actualizar frames principales
        for frame in [self.main_frame, self.left_frame, self.right_frame]:
            frame.configure(fg_color=self.bg_color)
        
        # Actualizar labels y otros widgets
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color=self.fg_color)
            elif isinstance(widget, ctk.CTkFrame):
                widget.configure(fg_color=self.bg_color)
        
        # Actualizar el estilo del calendario
        self.update_calendar_style()

    def save_task_edit(self, dialog, task_id, title, description, category, priority):
        """Guarda los cambios realizados en una tarea editada."""
        if not title:  # Validación básica
            return
        
        task = self.task_manager.edit_task(
            task_id=task_id,
            title=title,
            description=description,
            category=category,
            priority=priority
        )
        
        if task:
            self.refresh_task_list()
            if self.save_callback:
                self.save_callback()  # Guardar después de editar
            dialog.destroy()

    def show_name_dialog(self):
        """Muestra el diálogo de nombre solo en la primera ejecución"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Bienvenido")
        
        # Hacer la ventana modal
        dialog.grab_set()
        dialog.transient(self.root)
        
        # Dimensiones de la ventana
        width = 650
        height = 600
        
        # Obtener dimensiones de la pantalla
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        
        # Calcular posición para centrar
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Configurar geometría centrada
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Prevenir que se cierre con el botón X
        dialog.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Colores personalizados
        primary_color = "#4A90E2"  # Azul principal
        secondary_color = "#2ECC71"  # Verde para el botón
        accent_color = "#F39C12"  # Naranja para acentos
        bg_color = "#F5F6FA"  # Fondo suave
        text_color = "#2C3E50"  # Color de texto principal
        
        frame = ctk.CTkFrame(dialog, fg_color=bg_color)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título principal con diseño especial
        title_frame = ctk.CTkFrame(frame, fg_color=bg_color)
        title_frame.pack(fill="x", pady=(0, 20))
        
        welcome_label = ctk.CTkLabel(
            title_frame,
            text="✨ Bienvenido a Motívate Diariamente ✨",
            font=("Segoe UI", 28, "bold"),
            text_color=primary_color
        )
        welcome_label.pack(pady=(0, 10))
        
        # Subtítulo inspirador
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Tu viaje hacia el éxito comienza aquí",
            font=("Segoe UI", 16, "italic"),
            text_color=accent_color
        )
        subtitle_label.pack()
        
        # Marco decorativo para el mensaje motivacional
        message_frame = ctk.CTkFrame(
            frame,
            fg_color="#FFFFFF",
            corner_radius=15,
            border_width=2,
            border_color=primary_color
        )
        message_frame.pack(fill="x", padx=30, pady=(20, 30))
        
        # Mensaje motivacional principal
        motivational_text = (
            "🌟 ¡Tu Camino Hacia la Excelencia! 🌟\n\n"
            "Cada día es una nueva oportunidad para:\n\n"
            "🎯 Establecer metas inspiradoras\n"
            "📝 Organizar tus tareas eficientemente\n"
            "🌱 Cultivar hábitos positivos\n"
            "⭐ Celebrar tus logros\n"
            "🚀 Alcanzar tu máximo potencial\n\n"
            "¡El éxito es un viaje, y estás a punto de dar el primer paso!"
        )
        
        motivation_label = ctk.CTkLabel(
            message_frame,
            text=motivational_text,
            font=("Segoe UI", 14),
            justify="center",
            wraplength=500,
            text_color=text_color
        )
        motivation_label.pack(pady=20, padx=20)
        
        # Marco para la entrada del nombre
        name_frame = ctk.CTkFrame(frame, fg_color=bg_color)
        name_frame.pack(fill="x", pady=20)
        
        intro_label = ctk.CTkLabel(
            name_frame,
            text="¿Cómo te gustaría que te llamemos?",
            font=("Segoe UI", 16, "bold"),
            text_color=text_color
        )
        intro_label.pack(pady=(0, 15))
        
        name_entry = ctk.CTkEntry(
            name_frame,
            width=300,
            height=45,
            placeholder_text="Ingresa tu nombre...",
            font=("Segoe UI", 14),
            fg_color="#FFFFFF",
            border_color=primary_color,
            text_color=text_color
        )
        name_entry.pack()
        
        def save_name():
            name = name_entry.get().strip()
            if name:  # Solo proceder si hay un nombre
                self.set_username(name)
                dialog.destroy()
                if self.save_callback:
                    self.save_callback()
        
        # Botón ¡Empecemos!
        start_button = ctk.CTkButton(
            name_frame,  # Lo ponemos en name_frame para que esté debajo del entry
            text="¡Empecemos! 🎯",
            command=save_name,
            width=260,  # Más ancho
            height=55,
            font=("Segoe UI", 17),  # Fuente más grande
            fg_color=secondary_color,
            hover_color="#27AE60",
            corner_radius=10  # Radio de esquinas más sutil
        )
        start_button.pack(expand=True)
        
        # Nota final inspiradora
        final_note = ctk.CTkLabel(
            frame,
            text="Tu viaje hacia la productividad y el éxito comienza ahora",
            font=("Segoe UI", 12, "italic"),
            text_color=accent_color
        )
        final_note.pack(pady=20)
        
        # Vincular la tecla Enter al botón de guardar
        name_entry.bind('<Return>', lambda e: start_button.invoke())
        
        # Dar foco al campo de entrada
        name_entry.focus()

    def set_username(self, username: str):
        """Establece el nombre de usuario y actualiza la interfaz"""
        if username and isinstance(username, str):
            self.username = username.strip()
            self.update_welcome_message()

    def update_welcome_message(self):
        current_hour = datetime.now().hour
        greeting = "Buenos días" if 5 <= current_hour < 12 else \
                   "Buenas tardes" if 12 <= current_hour < 20 else \
                   "Buenas noches"
        
        motivational_phrases = [
            "¡hoy es un gran día para alcanzar tus metas!",
            "¡prepárate para conquistar este día!",
            "¡tu determinación te llevará lejos!",
            "¡cada pequeño paso cuenta en tu viaje!",
            "¡tu potencial no tiene límites!",
            "¡hoy es el día perfecto para brillar!"
        ]
        
        phrase = random.choice(motivational_phrases)
        welcome_text = f"{greeting}, {self.username} - {phrase}"
        
        # Actualizar el texto del label con el color del tema actual
        self.welcome_label.configure(
            text=welcome_text,
            text_color=self.text_color
        )
