from setuptools import setup, find_packages

setup(
    name="treech",  
    version="0.3.0",  
    author="Yannik Fleischer",
    author_email="yanflei@math.uni-paderborn.de",
    description="with this package you can create data-based decision trees manually, semi-automatically, or automatically",
    long_description=open('README.md').read(),  
    long_description_content_type="text/markdown",
    url="https://github.com/dein_github/my_library",# noch zu ergänzen
    packages=find_packages(),  # Findet und packt alle Module und Pakete in deinem Verzeichnis
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Gebe die Lizenz deines Projekts an
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Gibt die Python-Versionen an, die unterstützt werden
    install_requires=[  # Abhängigkeiten deiner Bibliothek
        'numpy==1.26.4',
        'pandas==2.2.2',
        'python-graphviz==0.20.1',
    ],
)

