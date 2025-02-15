from setuptools import setup, find_packages

setup(
    name="motivate-diariamente",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'customtkinter',
        'tkcalendar',
        'pillow',
    ],
    author="Tu Nombre",
    author_email="tu@email.com",
    description="Una aplicación de gestión de tareas gamificada para mantener la motivación",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tuusuario/motivate-diariamente",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Scheduling",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'motivate-diariamente=src.main_IPH:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['resources/*'],
    },
)