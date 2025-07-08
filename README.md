# TechMart Payment API – Déploiement Azure & Monitoring

## 🔍 Objectif
Mettre en place une infrastructure Azure robuste pour une API de paiement avec monitoring avancé et bonnes pratiques DevOps.

## 🔄 Architecture

```
[ Utilisateur ]
     |
[ App Service (Node.js) ]
     |
+----+------------------+
|                     |
[ Azure SQL ]       [ Redis Cache ]
     |
[ Application Insights ]
     |
[ Azure Monitor (Alertes) ]
```

## 📈 Choix techniques et justification

### Pourquoi choisir **Azure SQL niveau S0** ?
- 💲 **Coût optimisé** : Idéal pour un usage startup avec charges modérées.
- 🔄 **Montée en charge facile** : Possibilité d'évoluer vers S1/S2 ou vCore.
- 🔢 **Haute disponibilité native (99,99%)**.
- 🔹 Utilisation pour environnements **DEV, TEST** ou faible volumétrie.

### Quand migrer vers un niveau supérieur ?
- 🔹 Volume de données important (plusieurs millions d'enregistrements)
- 🔹 Temps de réponse insuffisant
- 🔹 Pic de charge ou augmentation du trafic
- 🔹 Besoins en réplication géographique ou résilience accrue

### Pourquoi utiliser **Redis Cache** ?
- 💡 Accélérer les temps de réponse
- 💲 Décharger la base de données principale
- 🔑 Gestion des sessions utilisateurs, files d'attente, cache temporaire

### Quand Redis est-il indispensable ?
| Cas d'usage                               | Redis ? |
|-------------------------------------------|---------|
| Données fréquemment lues (mais peu modifiées) | Oui     |
| Sessions utilisateur / Token              | Oui     |
| Faible trafic                             | Non     |
| Données critiques, sensibles              | Non (à éviter sans sécurité) |

## 🚧 Déploiement Azure CLI

### Groupe de ressource
```bash
az group create --name rg-techmart-lab --location "West Europe"
```

### Serveur SQL + Base de données
```bash
az sql server create \
  --name techmart-sql-$(whoami) \
  --resource-group rg-techmart-lab \
  --location "West Europe" \
  --admin-user techmartadmin \
  --admin-password "DevOps@2024!"

az sql db create \
  --resource-group rg-techmart-lab \
  --server techmart-sql-$(whoami) \
  --name paymentsdb \
  --service-objective S0
```

### Redis Cache
```bash
az redis create \
  --name techmart-cache-$(whoami) \
  --resource-group rg-techmart-lab \
  --location "West Europe" \
  --sku Basic \
  --vm-size c0
```

### App Service & déploiement de l'API
```bash
az appservice plan create \
  --name techmart-plan \
  --resource-group rg-techmart-lab \
  --sku S1 \
  --is-linux

az webapp create \
  --name techmart-payments-$(whoami) \
  --plan techmart-plan \
  --resource-group rg-techmart-lab \
  --runtime "NODE|18-lts"
```

## 🔍 Monitoring & Application Insights
```bash
az monitor app-insights component create \
  --app techmart-insights \
  --location "West Europe" \
  --resource-group rg-techmart-lab \
  --application-type web
```

### Alertes sur les erreurs de paiement
```bash
az monitor metrics alert create \
  --name "Payment Failures Critical" \
  --resource-group rg-techmart-lab \
  --scopes /subscriptions/$(az account show --query id -o tsv)/resourceGroups/rg-techmart-lab/providers/Microsoft.Insights/components/techmart-insights \
  --condition "count exceptions/count > 5" \
  --description "Plus de 5 erreurs de paiement en 5 minutes" \
  --evaluation-frequency 1m \
  --window-size 5m \
  --severity 0
```
### Alerte sur la performance
```bash
az monitor metrics alert create \
  --name "Payment Response Time" \
  --resource-group rg-techmart-lab-rda \
  --scopes /subscriptions/<subscription-id>/resourceGroups/rg-techmart-lab-rda/providers/Microsoft.Insights/components/techmart-insights \
  --condition "avg requests/duration > 2000" \
  --description "Temps de réponse des paiements > 2s" \
  --evaluation-frequency 1m \
  --window-size 5m \
  --severity 2
```

## Variables d'environnement 

```bash
DB_USER
DB_PASSWORD
DB_NAME
DB_SERVER
REDIS_HOST
REDIS_PASSWORD
APPINSIGHTS_INSTRUMENTATIONKEY
```

## Création de la table SQL : 
```bash
CREATE TABLE Payments (
    PaymentId int IDENTITY(1,1) PRIMARY KEY,
    Amount decimal(10,2) NOT NULL,
    Currency nvarchar(3) NOT NULL,
    MerchantId nvarchar(50) NOT NULL,
    Status nvarchar(20) NOT NULL,
    CreatedAt datetime2 NOT NULL DEFAULT GETDATE()
);

CREATE INDEX IX_Payments_MerchantId_CreatedAt ON Payments(MerchantId, CreatedAt);
```
## Préparation du package de déploiement (ZIP) et déploiement sur Azure

### Préparation du projet

1. Assurez-vous d'avoir dans votre dossier projet : 
```bash
index.js
package.json
.deployment
```
2. Le fichier `.deployment` contient :
```bash
[config]
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```
3. Ne pas inclure : 
  - `.env` (les variables sont configurées dans Azure App Service)
  - `node_modules` (Azure les installera automatiquement)

### Génération du fichier ZIP

1. Dans votre terminal local :
```bash
npm install --production
zip -r app.zip index.js package.json .deployment
```
2. Le fichier ZIP doit contenir uniquement : 
```bash
index.js
package.json
.deployment
```

### Déploiement du ZIP sur Azure

1. Dans PowerShell Windows (⚠️Pas WSL Ni Cloud Shell⚠️):
```bash
az login
az webapp deploy `
  --resource-group rg-techmart-lab-rda `
  --name techmart-payments-rda `
  --src-path "C:\Users\utilisateur\Desktop\VOTRECHEMIN\app.zip"
```
2. Résultat attendu :
  - L'application est déployé avec succès.
  - Vous pouvez accéder à :
  ```https://techmart-payments-rda.azurewebsites.net/health```
  et
  ```https://techmart-payments-rda.azurewebsites.net/api/payments```

## 🛠️ Tests & Simulation de Charge
```bash
for i in {1..50}; do
  curl -X POST https://techmart-payments-$(whoami).azurewebsites.net/api/payments \
    -H "Content-Type: application/json" \
    -d '{"amount":100,"currency":"EUR","merchantId":"MERCHANT_$i"}' &
done
wait
```

## 🛡️ Nettoyage
```bash
az group delete --name rg-techmart-lab --yes --no-wait
```
## Session Débrief

### Exercice d'Observation

1. Dans les métriques Application Insights et Azure Monitor, on observe que : 
  - Les appels `/health` sont réguliers grâce à la sonde d’intégrité d’Azure (fréquence stable).
  -  Les appels `/api/payments` génèrent des événements et des métriques de performance (durée d’exécution, nombre de succès).

2. Les pattern qui émergent :
  - Un comportement prévisible et linéaire sous faible charge.
  - Des points de rupture poteniels qui pourraient apparaître sous une charge beaucoup plus élevée.

### Réflexion stratégique

1. Architecture - Composant que j'ajouterais pour une montée en charge x10 :
  - 

## 📌 Auteurs
Richard DEVA Cloud DevOps