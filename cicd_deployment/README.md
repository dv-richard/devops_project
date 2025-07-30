# 📦 Projet CI/CD & GitOps – `Appliquer les bonnes pratiques GitOps dans l'intégration et déploiement continu d'applications`

## 🎯 Objectif du projet

Mettre en œuvre un environnement d’intégration et de déploiement continu (CI/CD) en appliquant les bonnes pratiques **GitOps**.  
Le tout basé sur une application Python containerisée, avec des tests unitaires et un pipeline automatisé conditionnant les merges à la réussite des tests.

---

## 🛠️ Environnement utilisé

| Élément                   | Détail                                                                 |
|---------------------------|------------------------------------------------------------------------|
| 🧰 Plateforme CI/CD       | GitLab CE auto-hébergé sur Azure                                      |
| 🖥️ Infrastructure         | 2 VMs Azure déployées via Terraform (1 GitLab + 1 GitLab Runner)      |
| ⚙️ Provisionning          | Ansible (Docker, GitLab Runner, NGINX, Certbot...)                    |
| 📦 Déploiement            | Docker / Shell / FastAPI (Uvicorn)                                                       |
| 🔍 Supervision (optionnel)| Docker logs (local)                                                    |

---

## 🧱 Architecture déployée

```
[ Dev ]
   │
   ├──> GitLab CE (CI/CD + Git)
   │     └──> GitLab Runner (Shell + Docker)
   │            └──> Build + Test + Deploy
   │
   └──> VM Azure exposée via HTTPS (Nginx + Certbot)
```

---

## 📂 Fichiers clés

- [`hexencoder.py`](hexencoder.py) : code principal FastAPI
- [`test_hexencoder.py`](test_hexencoder.py) : tests unitaires Pytest
- [`Dockerfile`](Dockerfile) : création de l’image
- [`requirements.txt`](requirements.txt) : dépendances
- [`.gitlab-ci.yml`](.gitlab-ci.yml) : pipeline GitLab CI/CD

---

## 🧪 Phase de test en local

1. Créer et activer un environnement virtuel
```bash 
python3 -m venv .venv
source .venv/bin/activate
```
2. Installer les dépendances 
```bash 
pip install -r requirements.txt
```
Si tu n’as pas encore de requirements.txt, tu peux le créer avec ce contenu :
```
pytest
flask
fastapi
uvicorn
```
3. Lancer les tests unitaires avec `pytest`
```bash 
pytest
```

Tu dois voir une sortie comme :
```
==================== test session starts ====================
collected 2 items

test_hexencoder.py ..                                      [100%]

===================== 2 passed in 0.05s =====================
```
![Uvicorn Host](images/pytest_and_uvicorn_host.png)

4. Lancer le serveur en local (FastAPI)
```bash 
uvicorn hexencoder:app --host 0.0.0.0 --port 8000
```

Puis aller sur : 
- Swagger UI → http://127.0.0.1:8000/docs
- Test via `curl` :
```bash 
curl http://127.0.0.1:8000/encode/Héllo
→ "48c3a96c6c6f"

curl http://127.0.0.1:8000/decode/48c3a96c6c6f
→ "Héllo"
```

![Fast API Access](images/fat_api_access.png)
![Encode Hello Local](images/encode_hello.png)
![Hello Local](images/hello.png)

---

## ⚙️ Pipeline `.gitlab-ci.yml`

```yaml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  image: python:3.10
  tags: [auto]
  script:
    - pip install -r requirements.txt
    - python3 -m pytest
  only: [main, merge_requests]

build:
  stage: build
  tags: [auto]
  script:
    - docker build -t rda-devops-app .
  only: [main]

deploy:
  stage: deploy
  tags: [auto]
  script:
    - docker stop rda-devops-app || true
    - docker rm rda-devops-app || true
    - docker run -d --name rda-devops-app -p 5000:5000 rda-devops-app
  only: [main]
```

[Pipeline fonctionnel](images/stages%20build%20&%20deploy.png)

---

## 🔬 Tests unitaires

Les tests sont déclenchés automatiquement via `pytest`.  
> 📌 Si un test échoue, le pipeline échoue et la merge request est bloquée (simulation réalisée sur GitLab CE).

Extrait du test :

```python
from hexencoder import hex_encode_text, hex_decode_text
def test_encode():
     assert hex_encode_text('Héllo') == '48c3a96c6c6f'
def test_decode():
     assert hex_decode_text('48c3a96c6c6f') == "Héllo"
```

![Tests unitaires](images/curl.png)

---

## 🧪 Simulation de test cassé

Une branche `test-fail` a été créée avec un test volontairement erroné.  
Le pipeline échoue correctement et empêche le merge (du point de vue des développeurs sans rôle admin).

![MR ALLOWED](images/mr_allowed.png)
![Pipeline FAIL](images/merge%20request%20failed%201.png)
![All pipelines](images/all_pipelines_failed.png)

---

## 🚀 Déploiement final

Une fois l’image Docker construite, elle est automatiquement lancée sur la VM Runner.

> Accès public : `http://<rda-runner-vm>:5000/docs`  
 Exemple d’appel API :
 ```bash
 curl http://<runner-vm>:5000/encode/Héllo
 → "48c3a96c6c6f"

 curl http://<runner-vm>:5000/decode/48c3a96c6c6f
 → "Héllo"
 ```
![Application Dockeurisé](images/Docker%20ps%20&%20curl.png)

---

## 🧠 Conclusion

Ce projet m’a permis de :
- Mettre en place une chaîne CI/CD complète sur GitLab auto-hébergé
- Appliquer des pratiques GitOps : merge via pipeline, tests automatisés, infrastructure versionnée
- Maîtriser les outils : Terraform, Ansible, GitLab CI/CD, Docker, Flask, Pytest

L’environnement est **fonctionnel, reproductible et démontrable** à tout moment.

---

## 👨‍💻 Crédits

![License](https://img.shields.io/badge/auteur-Richard%20DEVA-blue)   
Formation **DevOps** – Simplon.co, Montpellier  
Brief : _CICD & GitOps_  
© 2025