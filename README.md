# 🐂 Bovin Market

Application web de vente de bœufs en ligne développée avec Django.

## Description

Bovin Market est une plateforme qui permet à des vendeurs de publier des bœufs à vendre et à des clients de passer des commandes en ligne. Les bœufs peuvent être vendus par kilogramme ou par lot.

## Fonctionnalités

- Authentification en plusieurs étapes (inscription + connexion)
- Gestion des sessions et cookies
- Publication de bœufs avec formulaire multi-étapes
- Catalogue des bœufs disponibles
- Système de commande en ligne
- Dashboard vendeur pour gérer les commandes
- Page "Mes commandes" pour les clients
- Gestion automatique du stock

## Technologies utilisées

- **Backend** : Django 6.0
- **Base de données** : SQLite
- **Frontend** : HTML, CSS, Bootstrap 5
- **Langage** : Python 3.13

## Installation

### Prérequis
- Python 3.8 ou supérieur
- pip

### Étapes

**1. Cloner le projet**
```bash
git clone <url_du_projet>
cd boeuf_project
```

**2. Créer et activer l'environnement virtuel**
```bash
python -m venv env

# Windows
env\Scripts\activate

# Mac/Linux
source env/bin/activate
```

**3. Installer les dépendances**
```bash
pip install django pillow
```

**4. Appliquer les migrations**
```bash
cd boeuf_project
python manage.py makemigrations
python manage.py migrate
```

**5. Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

**6. Lancer le serveur**
```bash
python manage.py runserver
```

**7. Ouvrir dans le navigateur**
```
http://127.0.0.1:8000/
```

## Structure du projet
```
boeuf_project/
├── boeuf_project/          → Configuration du projet
│   ├── settings.py         → Paramètres Django
│   ├── urls.py             → URLs principales
│   └── wsgi.py
│
├── bovin_market/           → Application principale
│   ├── models.py           → Modèles (Bovin, Commande, Profil)
│   ├── views.py            → Vues
│   ├── forms.py            → Formulaires
│   ├── urls.py             → URLs de l'application
│   └── templates/          → Templates HTML
│       └── bovin_market/
│           ├── base.html
│           ├── connexion_etape1.html
│           ├── connexion_etape2.html
│           ├── inscription.html
│           ├── catalogue.html
│           ├── detail_boeuf.html
│           ├── publier_etape1.html
│           ├── publier_etape2.html
│           ├── dashboard_vendeur.html
│           └── mes_commandes.html
│
├── media/                  → Photos uploadées
├── db.sqlite3              → Base de données
└── manage.py
```

## Utilisation

### Compte Vendeur
1. S'inscrire en choisissant le rôle **Vendeur**
2. Se connecter
3. Cliquer sur **"+ Publier un bœuf"** dans le catalogue
4. Remplir le formulaire en 2 étapes
5. Gérer les commandes depuis le **Dashboard**

### Compte Client
1. S'inscrire en choisissant le rôle **Client**
2. Se connecter
3. Parcourir le **Catalogue**
4. Cliquer sur un bœuf pour voir le détail
5. Passer une commande
6. Suivre ses commandes dans **"Mes Commandes"**

## Auteur

- **Nom** : Aichatou Mamadou Kebe
- **Projet** : Projet de classe
- **Framework** : Django