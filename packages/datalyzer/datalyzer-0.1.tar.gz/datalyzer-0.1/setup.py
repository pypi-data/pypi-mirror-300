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
    long_description=open('README.txt').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/TwojeImie/datalyzer',  # Link do repozytorium
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
