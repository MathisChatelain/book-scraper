# Utilisez les bases de Python pour l'analyse de marché.
## Projet n° 2 formation développeur d'applications Python OC.

### Présentation:
Le but de ce projet est la mise en place d'un processus ETL (Extraction-Transformation-Chargement) visant à récupérer
des données sur [le site de vente de livres en ligne BookToScrape](http://books.toscrape.com/).

*Comme indiqué sur le site : ce site est une page de démonstration utilisé pour de l'entrainement au web scraping, les prix et les notes sont assignées aléatoirement et n'ont pas de sens réel.*

### Installation:

1. Vérifiez que python et son outil d'installation de paquets pip sont bien installés sur votre machine:

```
python3 -V
pip3 -V
```

2. Mise en place de votre environement virtuel:

```
python3 -m venv /path/to/new/virtual/environment
```

3. Activation de votre environement:

Veillez à remplacer path/to/env par le chemin d'accés à otre environement:

Sous Unix ou MacOS avec bash par défaut: 
```
source /path/to/venv/bin/activate
```

Sous windows par défaut:
```
path\to\venv\Scripts\activate
```

4. Installation des paquets:

```
pip install -r requirements.txt
```

5. Execution du script de book-scrapper

```
main.py
```