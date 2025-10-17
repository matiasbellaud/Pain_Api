# Pain_Api
Application de recettes proposées par IA (API)
# pAIn — Recettes intelligentes par IA

## Concept
pAIn est une application web qui génère des recettes personnalisées à partir d’une liste d’ingrédients fournie par l’utilisateur. L’objectif est de réduire le gaspillage alimentaire et de simplifier la cuisine quotidienne en proposant des recettes pertinentes basées sur ce qui est disponible chez soi.

---

## Fonctionnement
1. L’utilisateur saisit une liste d’ingrédients (prompt).
2. Le backend (FastAPI) envoie le prompt à un modèle LLaMA3 exécuté localement via Ollama.
3. Le modèle renvoie une ou plusieurs recettes contenant :
   - **Nom de la recette**
   - **Durée estimée**
   - **Difficulté**
   - **Liste d’ingrédients**
   - **Étapes détaillées**
4. Le frontend (React) récupère et affiche les recettes. L’utilisateur peut dérouler les étapes pour suivre la préparation.

---

## Fonctionnalités développées
- Interface utilisateur simple pour saisir des ingrédients.
- Intégration LLaMA3 via Ollama (exécution locale).
- Génération dynamique de recettes selon le prompt.
- Affichage des recettes avec déroulement des étapes.
- Mesure de la consommation des ressources via psutil sur le backend.

---

## Technologies utilisées
- **Frontend** : React.js
- **Backend** : Python (FastAPI) 
- **IA** : LLaMA3 via Ollama (local marche sans connexion internet)
- **Monitoring** : psutil (mesure CPU/mémoire)

Python est aujourd’hui la langue principale de l’écosystème IA, et offre une intégration fluide avec les outils de machine learning.

FrontEnd en react tout les membres de l'équipe avait des compétences techniques sur la technologie.

---

## Lancer l’application

### Prérequis
- **Python 3.10+**
- **Node.js 18+**
- **Ollama installé** et le modèle llama3 téléchargé
- **pipenv ou venv** (gestion d’environnement Python)

### Backend (FastAPI)
Commande : 
- **pip install -r requirements.txt**
- **python -m uvicorn main:app --reload --port 4000**

Assurez-vous qu’Ollama est lancé et que le modèle est chargé : **ollama run llama3**

### Frontend (React)
Commande : 
- **npm install**
- **npm start**

L’application sera disponible sur [http://localhost:3000](http://localhost:3000).

---

## Mesure approximative pour une session de génération (~30s)
- **CPU moyen** : ~65%
- **Mémoire utilisée** : ~2.3 GB
- **Temps d’exécution** : ~10s
- **Consommation estimée** : ~15–20 Wh (pour la génération)

### Comparaison
Microsoft Word (30 minutes d’édition simple) ≈ 5–7 Wh.  

**Conclusion** : l’inférence IA locale consomme significativement plus d’énergie, malgré l’avantage de garder les données en local.

---

## Limites actuelles
- L’IA peut produire des recettes incohérentes ou imprécises.
- Pas de système de feedback utilisateur pour améliorer les résultats.
- Pas d’historique des recettes générées.

---

## Équipe
- Maxence MAHIEU
- Mathéo HAMON
- Matias BELLAUD