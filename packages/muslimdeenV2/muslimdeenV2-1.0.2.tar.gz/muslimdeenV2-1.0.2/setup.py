from setuptools import setup, find_packages

# Lire les dépendances depuis requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='muslimdeenV2',
    version='1.0.2',
    packages=find_packages(),
    install_requires=required,
    description='MuslimDeen: Package pour gérer les sourates, noms d\'Allah, ablutions et salat',
    author="personne monsieur",
    author_email="monsieurnobody01@gmail.com",
    url='https://gitlab.com/misternobody01/muslimdeen#',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
