# Datalyzer

Datalyzer to biblioteka do analizy danych w Pythonie. Umożliwia łatwe uzyskanie statystyk opisowych i wykrywanie brakujących wartości.

## Instalacja

Aby zainstalować bibliotekę, użyj:

```bash
pip install datalyzer

Użycie
Oto przykład użycia:

import pandas as pd
from datalyzer.analyzer import DataAnalyzer

data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
analyzer = DataAnalyzer(data)

# Uzyskaj statystyki opisowe
summary = analyzer.summary()
print(summary)

# Sprawdź brakujące wartości
missing = analyzer.missing_values()
print(missing)

Plik setup.py
Upewnij się, że plik setup.py jest poprawny i zawiera poniższy kod. Możesz zmienić author, author_email i url zgodnie z własnymi danymi:

from setuptools import setup, find_packages

setup(
    name='datalyzer',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',  # Wymagana biblioteka
    ],
    author='Twoje Imię',
    author_email='twoj.email@example.com',
    description='Biblioteka do analizy danych.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/TwojeImie/datalyzer',  # Link do repozytorium
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)


Datalyzer (English Version)

Datalyzer is a library for data analysis in Python.
 It allows you to easily obtain descriptive statistics and detect missing values.

Installation
To install the library, use:

pip install datalyzer

Usage
Here is an example of usage:
import pandas as pd
from datalyzer.analyzer import DataAnalyzer

data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
analyzer = DataAnalyzer(data)

# Get descriptive statistics
summary = analyzer.summary()
print(summary)

# Check for missing values
missing = analyzer.missing_values()
print(missing)

setup.py File
Make sure the setup.py file is correct and contains the following code.
 You can change author, author_email, and url according to your own data:

from setuptools import setup, find_packages

setup(
    name='datalyzer',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',  # Required library
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='Library for data analysis.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/YourName/datalyzer',  # Link to repository
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)

