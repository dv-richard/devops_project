# 🚀 DevOps Project

Ce repository regroupe deux projets DevOps développés dans le cadre de ma formation DevOps Cloud Engineer chez Simplon.co. Il met en œuvre des pratiques modernes de CI/CD, monitoring, sécurité, et déploiement cloud sur Microsoft Azure.

---

## ✅ Projet 1 – `checkup_django`

### 🎯 Objectif

Développement d'une application web en Django permettant aux administrateurs système de réaliser une **checklist journalière** pour la supervision et le bon fonctionnement de l'infrastructure.

### ⚙️ Fonctionnalités

- Saisie des tâches système quotidiennes
- Suivi de l’historique des checklists
- Affichage ergonomique avec Bootstrap
- Interface sécurisée et authentifiée (facultatif)
- Base de données SQLite locale

### 🚀 Technologies

- Python 3.10+
- Django 4.x
- Bootstrap 5
- GitLab CI/CD (Docker)

### 📂 Dossier :
```bash
cd checkup_django/
```
[README checkup_django](checkup_django/README.md)

---

## ✅ Projet 2 – `azure_monitoring_deployment`

### 🎯 Objectif

Développement et déploiement d’une **API sécurisée de gestion de paiements**, avec hébergement sur **Azure App Service**, base de données **Azure SQL**, cache **Redis**, supervision via **Application Insights** et alertes métiers critiques.

### ⚙️ Fonctionnalités

- Endpoint **/api/payments** pour enregistrer un paiement
- Endpoint **/health** pour l’intégrité de l’app, SQL & Redis
- Monitoring 24/7 avec App Insights
- Alertes automatisées (erreurs et lenteurs)
- Tests de montée en charge

### 🧱 Stack technique

- Node.js / Express
- Azure SQL Database
- Azure Redis Cache
- Azure Application Insights
- Azure App Service (déploiement via **az webapp**)
- CI/CD manuelle avec **.zip** + **az cli**

### 🔐 Sécurité

- Helmet + Rate Limit sur les endpoints
- **.env** pour les secrets (non versionné)
- Application Insights pour audit et journalisation
- Option : Key Vault pour secrets (à implémenter)

### 📂 Dossier
```bash
cd azure_monitoring_deployment/
```
[README azure_monitoring_deployment](azure_monitoring_deployment/README.md)
### 🧪 Tests & Observabilité

- Tests manuels via **curl** pour injecter du trafic
- Visualisation live dans Azure App Insights
- Logs d’erreurs accessibles via Kudu
- Alerte critiques sur :
- Temps de réponse > 2s
- Échecs de paiements > 5/5min

---

## ✅ Projet 3 – `gitops_rda_microservice`

### 🎯 Objectif

Mise en place d’un pipeline CI/CD GitOps pour un microservice Python hexencoder, développé avec FastAPI.
Ce projet démontre une chaîne complète d’intégration et de déploiement continu, incluant :

- Tests unitaires automatisés
- Build Docker
- Déploiement sur une VM Azure via GitLab Runner
- Détection et blocage des erreurs en PR

### 🧰 Fonctionnalités du microservice

- **/encode/{text}** : encode un texte en hexadécimal
- **/decode/{hex}** : décode une chaîne hexadécimale en texte
- **Interface Swagger** : `http://<ip>:5000/docs`

### 🔁 CI/CD GitLab

| Étape    | Description                                                            |
| -------- | ---------------------------------------------------------------------- |
| `test`   | Lance `pytest` à chaque commit et sur chaque merge request             |
| `build`  | Construit une image Docker avec `Dockerfile`                           |
| `deploy` | Déploie l’image sur la **VM GitLab Runner** avec `docker run`          |
| 💥 PR KO | Si les tests échouent, la **MR est bloquée** (manuellement, GitLab CE) |

💡 L’option de blocage automatique des MR en cas de test échoué n’est pas native en **GitLab CE**, mais un contournement a été mis en place par vérification manuelle.

### 🖼️ Architecture

```
Terraform + Ansible
        │
        └──> Déploiement VMs Azure
                 ├── GitLab CE (Docker)
                 └── GitLab Runner (Docker)
                          └──> CI/CD (Test > Build > Deploy)
                                   └──> Service Python (Docker, FastAPI, port 5000)
```

### 🐳 Stack technique

- Python 3.10 + FastAPI
- Pytest
- Docker
- GitLab CI/CD (Runner Shell)
- Terraform & Ansible (infra as code)
- Azure VMs (GitLab + Runner)

### 🔬 Tests
```bash
curl http://<ip>:5000/encode/Hello
# "48656c6c6f"

curl http://<ip>:5000/decode/48656c6c6f
# "Hello"
```
### 📂 Dossier
```bash
cd cicd_deployment/
```

### 🤝 Auteur
Ingénieur DevOps  
Nom : Richard Deva  
Année : 2024 - 2025  
LinkedIn : Richard DEVA 