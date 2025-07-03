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

### Alertes critiques
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

---

🔧 Ce README peut être enrichi avec des parties CI/CD si besoin. Dis-moi si tu veux que je le génère aussi !
