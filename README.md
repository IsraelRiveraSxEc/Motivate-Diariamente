# 🚀 Motívate Diariamente

Una aplicación de gestión de tareas gamificada diseñada para mantener a los usuarios motivados mediante un sistema de recompensas y seguimiento visual del progreso.

## ✨ Características Principales

### 📋 Sistema de Tareas
- Creación de tareas con título, descripción, categoría y nivel de importancia (1-5 estrellas)
- Edición y eliminación de tareas
- Sistema de deshacer cambios
- Marcado de tareas como completadas
- Mensajes motivacionales personalizados al completar tareas

### 🎯 Categorías
- Personal 👤
- Trabajo 💼
- Estudio 📚
- Salud ❤️
- Ejercicio 🏃
- Hogar 🏠
- Proyectos 🎯
- Otros 📌

### 🏆 Sistema de Logros y Motivación
- Mensajes motivacionales contextualizados
- Sistema de rachas diarias con contador 🔥
- Logros desbloqueables basados en el progreso
- Retroalimentación visual inmediata

### 📊 Seguimiento y Estadísticas
- Calendario interactivo con código de colores
- Estadísticas en tiempo real
- Sistema de rachas diarias
- Seguimiento de puntos por categoría
- Historial de actividad

## 🛠️ Características Técnicas

### Arquitectura del Proyecto
- Diseño modular con separación de responsabilidades
- Managers especializados:
  - `TaskManager`: Gestión de tareas
  - `UIManager`: Interfaz de usuario
  - `DataManager`: Persistencia de datos
  - `StatsManager`: Estadísticas y seguimiento

### Persistencia de Datos
- Guardado automático en formato JSON
- Sistema de respaldo automático
- Recuperación de estados anteriores
- Estructura de datos organizada

### Interfaz de Usuario
- Diseño moderno con CustomTkinter
- Soporte para emojis en diferentes sistemas operativos
- Interfaz responsive y adaptable
- Temas claro/oscuro
- Botones y elementos UI optimizados

## 🚀 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tuusuario/motivate-diariamente.git
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:
```bash
python main_IPH.py
```

### Creación del Ejecutable

Puedes crear un ejecutable standalone usando PyInstaller:

```bash
pyinstaller --name="Motivate Diariamente" --icon=icon.ico --windowed --onefile main_IPH.py
```

## 📦 Dependencias

-# GUI y Widgets
customtkinter>=5.2.0
tkcalendar>=1.6.1
Pillow>=10.0.0

# Procesamiento de datos
numpy>=1.24.0  # Requerido por algunas dependencias internas

# Utilidades del sistema
darkdetect>=0.7.1  # Para detección del tema del sistema
babel>=2.12.1      # Para localización y formateo de fechas

# Dependencias de desarrollo
pyinstaller>=6.2.0  # Para crear ejecutables
setuptools>=68.0.0  # Para empaquetado
wheel>=0.41.0      # Para distribución

## 💾 Estructura de Datos

Los datos se almacenan en `motivate_diariamente_data.json`:

```json
{
  "tasks": [],
  "stats": {
    "total_points": 0,
    "daily_points": {},
    "category_points": {},
    "tasks_by_category": {},
    "tasks_completed": 0,
    "current_streak": 0,
    "best_streak": 0,
    "last_completion_date": null,
    "total_tasks_completed": 0
  }
}
```

## 🔄 Sistema de Respaldo

- Backups automáticos en la carpeta `backups`
- Formato de nombre: `backup_YYYYMMDD.json`
- Sistema de recuperación integrado

## 🤝 Contribuir

1. Haz fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
