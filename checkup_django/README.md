# CheckUP — Application de checklist quotidienne

Une application Django légère pour gérer des checklists opérationnelles quotidiennes, avec SSO OIDC, suivi historique et tableau de bord interactif.

---

## 📋 Table des matières

1. [Présentation](#présentation)  
2. [Fonctionnalités](#fonctionnalités)  
3. [Technologies](#technologies)  
4. [Prérequis](#prérequis)  
5. [Installation & Configuration locale](#installation--configuration-locale)  
6. [Variables d’environnement](#variables-denvironnement)  
7. [Démarrage de l’application](#démarrage-de-lapplication)  
8. [Routes & Vues](#routes--vues)  
9. [Modèles & Administration](#modèles--administration)  
10. [CI/CD & Déploiement](#cicd--déploiement)  
11. [Extension & Personnalisation](#extension--personnalisation)  
12. [Crédits](#crédits)  

---

## Présentation

**CheckUP** permet à votre équipe de :

- Remplir chaque jour une **checklist** de tâches opérationnelles  
- Consulter l’**historique** des checklists avec filtres par date  
- Plonger dans l’**historique par tâche** (qui a modifié quoi et quand)  
- Visualiser un **dashboard interactif** des pourcentages OK/KO/etc. sur une période  
- S’authentifier via le **SSO OIDC** de votre collectivité  

Chaque tâche est définie dans le **TaskTemplate** (nom, section, aide contextuelle, lien vers la doc).

---

## Fonctionnalités

- **SSO OIDC** pour l’authentification centralisée  
- **Checklist du jour** auto-synchronisée avec les templates  
- **Champ “Vérifié par”** pré-rempli avec l’utilisateur connecté (non modifiable)  
- **Historique des modifications** par tâche (django-simple-history)  
- **Vue historique** des checklists, filtres par date  
- **Dashboard** Chart.js avec filtres de période  
- **Interface Admin** pour gérer sections et tâches (description & URL doc)  
- UI responsive avec **Bootstrap 5**  

---

## Technologies

- **Python 3.12**  
- **Django 5.2**  
- **Django REST Framework** (endpoint token mobile/JS)  
- **django-simple-history**  
- **Bootstrap 5** + **Chart.js**  
- **GitLab CI/CD** + Docker + Traefik  

---

## Prérequis

- Python ≥ 3.10  
- pip (ou pipenv / poetry)  
- Docker & Docker Compose (pour CI/CD)  
- Un fournisseur OIDC (client_id, secret, redirect URI)  

---

## Installation & Configuration locale

1. **Cloner** le dépôt et se positionner :
```bash
git clone git@gitlab.example.com:mon-groupe/checkup.git
cd checkup
```

2. Créer & activer un virtuel : 
```bash
pythhon -m venv .venv
source .venv/bin/activate
```

3. Installer les dépendances : 
```bash
pip install -r requirements.txt
```

4. Duppliquer `.env example` -> `.env` et remplir (voir ci-dessous).

5. Migrer & collectstatic : 
```bash
python manage.py migrate
python manage.py collectstatic --no-input
```

## Variables d'environnement

Copiez `.env example` -> `.env` puis complétez : 

```bash
# DEBUG & Sécurité
DEBUG=True
SECRET_KEY=une-cle-secrete
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,checkup.local
CSRF_TRUSTED_ORIGINS=https://checkup.local

# OIDC SSO
OIDC_CLIENT_ID=…
OIDC_CLIENT_SECRET=…
OIDC_RP_CALLBACK_URI=http://127.0.0.1:8000/oidc/callback/
OIDC_OP_AUTHORIZATION_ENDPOINT=https://mon-oidc/oauth2/authorize
OIDC_TOKEN_ENDPOINT=https://mon-oidc/oauth2/token
OIDC_USER_ENDPOINT=https://mon-oidc/oauth2/userinfo
OIDC_OP_SSL=False

# CORS (si besoin)
CORS_ALLOWED_ORIGINS=http://localhost:8000
```

## Démarrage de l'application

```bash
python manage.py runserver
```

- /redirive vers /checklist/
- /oidc/ -> SSO -> /oidc/callback/

## Route & Vues 

| URL                                  | Vue                              | Authentification        |
| ------------------------------------ | -------------------------------- | ----------------------- |
| `/`                                  | Redirection vers `/checklist/`   | Aucune                  |
| `/oidc/login/`                       | Déclenchement du flux OIDC       | Aucune                  |
| `/oidc/callback/`                    | Échange code → token → login     | Aucune                  |
| `/api/auth/oidc/`                    | Endpoint DRF pour apps JS/mobile | Aucune                  |
| `/checklist/`                        | Checklist du jour (formulaire)   | Login requis            |
| `/checklist/historique/?start=&end=` | Historique filtrable             | Login requis            |
| `/checklist/<YYYY-MM-DD>/`           | Détail + historique par tâche    | Login requis            |
| `/dashboard/?start=&end=`            | Dashboard interactif             | Login requis            |
| `/admin/`                            | Interface d’administration       | Login staff (is\_staff) |

## Modèle & Administration 

- **Section** : catégories de tâches
- **TaskTemplate** : 
    - `nom`, `section`, `ordre`
    - `description` -> infobulle d'aide
    - `doc_url` ->  lien “📖 Documentation complète”
- **Checklist** : une instance par date (unique)
- **CheckItem** : copie d'un template pour la date :
    - `statut`, `commentaire`, `verifie_par`
    - historiqiue automatique (`django-simple-history`)

Dans l'admin, gérez l'ordre, le texte d'aide et les URL de documentation.

## CI/CD & Déploiement

Déployé via GitLab CI : 
- `gitlab-ci.yml` : 
    - Construction Docker -> push image staging/production
    - Déploiement via Portainer & Traefik

Point clés : 
- Variable d'environnement injectées depuis GitLab
- `ALLOWED_HOSTS`et `CSRF_TRUSTED_ORIGIN` configurés dynamiquement
- Base SQLite en volume Docker
- Serveur ASGI (Daphne) derrière Traefik

## Extension & Personnalisation 
- **Ajouter une section** : Admin > Sections
- **Créer / éditer un template** : nom, section, description, doc_url
- **Personnaliser les styles** : `checklist/static/checklist/css/checklist.css`
- **Ajouter des champs** : étendre `CheckItem` + `forms.py`

## Crédits

MIT © 2025 Montpellier Métropole

_Conçu avec ❤️ par Richard DEVA votre stagiaire DevOps._  