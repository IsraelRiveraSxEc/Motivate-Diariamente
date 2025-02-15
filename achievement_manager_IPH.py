import random
from typing import List, Dict, Any
from datetime import datetime

class AchievementManager:
    def __init__(self):
        self.unlocked_achievements = set()  # Usar un set para evitar duplicados
        self.achievements = {
            # Logros básicos
            "Primera paso": {"name": "Primer Paso 🌱", "description": "Completa tu primera tarea", "unlocked": False},
            "Maestro de puntos": {"name": "Maestro de Puntos 🏆", "description": "Alcanza 100 puntos totales", "unlocked": False},
            
            # Logros de categorías
            "study_expert": {"name": "Experto en Estudios 📚", "description": "Completa 10 tareas de estudio", "unlocked": False},
            "health_guru": {"name": "Gurú de la Salud ❤️", "description": "Completa 20 tareas de salud", "unlocked": False},
            "exercise_champion": {"name": "Campeón del Ejercicio 🏃", "description": "Completa 15 tareas de ejercicio", "unlocked": False},
            "work_master": {"name": "Maestro del Trabajo 💼", "description": "Completa 25 tareas laborales", "unlocked": False},
            "home_expert": {"name": "Experto del Hogar 🏠", "description": "Completa 30 tareas del hogar", "unlocked": False},
            "project_wizard": {"name": "Mago de Proyectos 🎯", "description": "Completa 20 tareas de proyectos", "unlocked": False},
            
            # Logros de rachas
            "streak_master": {"name": "Maestro de Rachas 🔥", "description": "Mantén una racha de 7 días", "unlocked": False},
            "streak_warrior": {"name": "Guerrero de Rachas ⚔️", "description": "Mantén una racha de 14 días", "unlocked": False},
            "streak_legend": {"name": "Leyenda de Rachas 👑", "description": "Mantén una racha de 30 días", "unlocked": False},
            
            # Logros de cantidad
            "task_centurion": {"name": "Centurión de Tareas ⚔️", "description": "Completa 100 tareas", "unlocked": False},
            "task_master": {"name": "Maestro de Tareas 🎓", "description": "Completa 500 tareas", "unlocked": False},
            "task_legend": {"name": "Leyenda de Tareas 🏅", "description": "Completa 1000 tareas", "unlocked": False},
            
            # Logros de prioridad
            "priority_warrior": {"name": "Guerrero Prioritario ⭐", "description": "Completa 10 tareas de alta prioridad", "unlocked": False},
            "priority_master": {"name": "Maestro de Prioridades 🌟", "description": "Completa 50 tareas de alta prioridad", "unlocked": False},
            
            # Logros de versatilidad
            "category_master": {"name": "Maestro Versátil 🌟", "description": "Completa tareas en todas las categorías", "unlocked": False},
            "daily_champion": {"name": "Campeón Diario 🌞", "description": "Completa 5 tareas en un solo día", "unlocked": False},
            "weekly_legend": {"name": "Leyenda Semanal 📅", "description": "Completa 25 tareas en una semana", "unlocked": False},
            
            # Logros especiales
            "night_owl": {"name": "Búho Nocturno 🦉", "description": "Completa 10 tareas después de las 22:00", "unlocked": False},
            "early_bird": {"name": "Madrugador 🌅", "description": "Completa 10 tareas antes de las 8:00", "unlocked": False},
            "weekend_warrior": {"name": "Guerrero de Fin de Semana 🎮", "description": "Completa 20 tareas en fines de semana", "unlocked": False}
        }
        
        # Mensajes motivacionales categorizados
        self.motivational_messages = {
            "intrinsic": [
                "¡Has dado un paso más hacia tus metas personales! 🎯",
                "Tu dedicación demuestra tu compromiso con el crecimiento personal 🌱",
                "Cada tarea completada te acerca a tu mejor versión 💫",
                "¡Estás construyendo hábitos positivos! 🌟",
                "Tu esfuerzo de hoy construye tu éxito de mañana 🌅",
                "¡Cada pequeño paso cuenta en tu viaje! 👣",
                "Tu determinación es inspiradora 💪",
                "¡Estás creando un futuro mejor para ti! 🌈",
                "Tu compromiso con tus metas es admirable 🎯",
                "¡Sigues avanzando, eso es lo importante! 🚀"
            ],
            "mastery": [
                "¡Excelente trabajo! Dominas cada vez mejor tus responsabilidades 💪",
                "Tu consistencia está creando resultados extraordinarios 🚀",
                "¡Sigues mejorando día a día! 📈",
                "Tu progreso es inspirador 🌈",
                "¡Cada vez eres más eficiente en tus tareas! ⚡",
                "Tu dominio crece con cada tarea completada 📚",
                "¡Estás desarrollando una maestría impresionante! 🎯",
                "Tu experiencia se refleja en tu rendimiento 💫",
                "¡Tus habilidades mejoran constantemente! 🌟",
                "Estás alcanzando nuevos niveles de excelencia 🏆"
            ],
            "achievement": [
                "¡Nueva victoria conseguida! 🏆",
                "¡Otro objetivo alcanzado en tu camino al éxito! ⭐",
                "¡Celebra este logro, te lo has ganado! 🎉",
                "¡Increíble trabajo! Sigue rompiendo tus propios récords 🎯",
                "¡Un logro más en tu colección de éxitos! 🌟",
                "¡Extraordinario! Sigues superando expectativas 🚀",
                "¡Victoria tras victoria, construyes tu legado! 👑",
                "¡Un paso más hacia la grandeza! ⭐",
                "¡Brillante ejecución de tus objetivos! 💫",
                "¡Tu determinación te lleva a nuevas alturas! 🦅"
            ],
            "streak": [
                "¡Tu racha demuestra tu compromiso! 🔥",
                "¡Mantén el impulso, vas por buen camino! ⚡",
                "¡Tu consistencia es tu superpoder! 💫",
                "¡Cada día suma en tu camino hacia el éxito! 📅",
                "¡Tu racha es imparable! 🚀",
                "¡Sigues encendiendo el camino con tu constancia! 🔥",
                "¡Tu dedicación diaria da frutos! 🌱",
                "¡Construyendo éxito, un día a la vez! ⚡",
                "¡Tu persistencia es admirable! 💪",
                "¡Mantén ese fuego encendido! 🔥"
            ],
            "morning": [
                "¡Empezando el día con energía! 🌅",
                "¡Gran manera de comenzar la mañana! ☀️",
                "¡Tu productividad matutina es inspiradora! 🌄",
                "¡Aprovechando las primeras horas del día! 🌞"
            ],
            "evening": [
                "¡Excelente manera de cerrar el día! 🌙",
                "¡Terminando el día con broche de oro! ���",
                "¡Tu dedicación no conoce horarios! 🌠",
                "¡Un día productivo hasta el final! 🌆"
            ],
            "weekend": [
                "¡Aprovechando el fin de semana al máximo! 🎯",
                "¡Tu compromiso no descansa! 💪",
                "¡Haciendo que cada día cuente! 📅",
                "¡El éxito no conoce de días libres! 🌟"
            ]
        }

    def check_achievements(self, stats: Dict[str, Any], task: Any = None) -> List[str]:
        new_achievements = []
        potential_achievements = self._get_potential_achievements(stats, task)
        
        for achievement in potential_achievements:
            if (achievement not in self.unlocked_achievements and 
                self._check_achievement_condition(achievement, stats, task)):
                new_achievements.append(achievement)
                self.unlocked_achievements.add(achievement)
        
        return new_achievements

    def _check_achievement_condition(self, achievement: str, stats: Dict[str, Any], task: Any) -> bool:
        if achievement not in self.unlocked_achievements:
            current_hour = datetime.now().hour
            is_weekend = datetime.now().weekday() >= 5
            
            match achievement:
                # Logros básicos
                case "Primer tarea completada" if stats.get("total_tasks_completed", 0) >= 1:
                    return True
                case "diez_tareas" if stats.get("total_tasks_completed", 0) >= 10:
                    return True
                    
                # Logros de categoría
                case "study_expert" if stats.get("tasks_by_category", {}).get("Estudio", 0) >= 10:
                    return True
                case "health_guru" if stats.get("tasks_by_category", {}).get("Salud", 0) >= 20:
                    return True
                case "exercise_champion" if stats.get("tasks_by_category", {}).get("Ejercicio", 0) >= 15:
                    return True
                case "work_master" if stats.get("tasks_by_category", {}).get("Trabajo", 0) >= 25:
                    return True
                    
                # Logros de racha
                case "streak_master" if stats.get("current_streak", 0) >= 7:
                    return True
                case "streak_warrior" if stats.get("current_streak", 0) >= 14:
                    return True
                case "streak_legend" if stats.get("current_streak", 0) >= 30:
                    return True
                    
                # Logros especiales
                case "night_owl" if current_hour >= 22 and task:
                    return True
                case "early_bird" if current_hour < 8 and task:
                    return True
                case "weekend_warrior" if is_weekend and task:
                    return True
                    
        return False

    def get_random_message(self, task=None, stats=None) -> str:
        current_hour = datetime.now().hour
        is_weekend = datetime.now().weekday() >= 5

        # Priorizar mensajes contextuales
        if current_hour < 8:
            return random.choice(self.motivational_messages["morning"])
        elif current_hour >= 22:
            return random.choice(self.motivational_messages["evening"])
        elif is_weekend:
            return random.choice(self.motivational_messages["weekend"])
        elif stats and stats.get("current_streak", 0) > 3:
            return random.choice(self.motivational_messages["streak"])
        elif task and task.priority >= 4:
            return random.choice(self.motivational_messages["achievement"])
        elif stats and stats.get("total_points", 0) > 50:
            return random.choice(self.motivational_messages["mastery"])
        
        return random.choice(self.motivational_messages["intrinsic"])

    def _get_potential_achievements(self, stats: Dict[str, Any], task: Any = None) -> List[str]:
        """
        Returns a list of achievement IDs that should be checked based on current stats and task.
        """
        potential = []
        
        # Basic achievements
        if stats.get("total_tasks_completed", 0) >= 1:
            potential.append("Primera Tarea Completada")
        if stats.get("total_tasks_completed", 0) >= 10:
            potential.append("Aprendiendo, Maestro De puntos")
        
        # Category achievements
        if stats.get("tasks_by_category", {}).get("Estudio", 0) >= 10:
            potential.append("study_expert")
        if stats.get("tasks_by_category", {}).get("Salud", 0) >= 20:
            potential.append("health_guru")
        if stats.get("tasks_by_category", {}).get("Ejercicio", 0) >= 15:
            potential.append("exercise_champion")
        if stats.get("tasks_by_category", {}).get("Trabajo", 0) >= 25:
            potential.append("work_master")
        
        # Streak achievements
        if stats.get("current_streak", 0) >= 7:
            potential.append("streak_master")
        if stats.get("current_streak", 0) >= 14:
            potential.append("streak_warrior")
        if stats.get("current_streak", 0) >= 30:
            potential.append("streak_legend")
        
        # Special achievements (time-based)
        current_hour = datetime.now().hour
        is_weekend = datetime.now().weekday() >= 5
        
        if current_hour >= 22 and task:
            potential.append("night_owl")
        if current_hour < 8 and task:
            potential.append("early_bird")
        if is_weekend and task:
            potential.append("weekend_warrior")
        
        return potential
