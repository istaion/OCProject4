# OCProject4

Logiciel de gestion de tournoi d'échec. Le programme permet d'ajouter des joueurs, de créer des tournois à 8 joueurs et de gérer les résultats de ce tournoi.

## utilisation

Dans votre terminal placez-vous à la racine du projet puis :

### Créer votre environnement virtuel :


```bash
python3 -m venv env
```

### Activer votre environnement :

linux ou mac :
```bash
source env/bin/activate
```

windows :

```bash
env\\Scripts\\activate.bat
```

### Installer les packages :

```bash
pip install -r requirements.txt
```

### Executer le programme :

```bash
python3 main.py
```

## Fonctionnement

Les informations obtenues lors de l'execution du programme sont stockés dans un fichier db.json à la racine du fichier.

### menu joueur

Permet d'ajouter de nouveaux joueurs, changer les classements et de modifier les informations d'un joueur.

### menu tournoi

Permet de créer un tournoi et de continuer un tournoi.

### menu rapport

Permet d'afficher sur la console les différents rapports

### Flake8

Pour réaliser un rapport flake8-html exécuter dans la console :

```bash
flake8 --format=html --htmldir=flake-report --max-line-length=119 --exclude ./env
```

Vous devez éventuellement changer env par le nom que vous avez donné à votre environment virtuel
