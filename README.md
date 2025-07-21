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

### 🤝 Auteur
Ingénieur DevOps  
Nom : Richard Deva  
Année : 2024 - 2025  
LinkedIn : Richard DEVA 