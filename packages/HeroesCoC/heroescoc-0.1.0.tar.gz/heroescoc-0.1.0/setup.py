#!/usr/bin/python3

from setuptools import setup, find_packages

# Leer el archivo README para la descripción larga
with open("README.MD", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Configuración del paquete
setup(
    name="HeroesCoC",  # Nombre del paquete
    version="0.1.0",  # Versión del paquete
    packages=find_packages(),  # Busca automáticamente todos los paquetes
    install_requires=[],  # Dependencias externas del paquete (puedes añadir si tienes)
    author="Luis Lopez",  # Tu nombre como autor
    description="Muestra los niveles actuales de los héroes",  # Descripción corta
    long_description=long_description,  # Descripción larga desde el README
    long_description_content_type="text/markdown",  # Formato de la descripción larga
    url="https://www.clashofstats.com/players/sade-8RC0PLRJQ/army#tabs",  # URL del proyecto (opcional)
    classifiers=[  # Clasificadores opcionales para más información sobre tu paquete
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Versión mínima de Python requerida
)

