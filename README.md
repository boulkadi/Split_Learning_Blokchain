# 🚀 Split Learning & Blockchain Registry

Ce projet implémente une architecture de **Split Learning** (Apprentissage Divisé) sécurisée par une **Blockchain Ethereum (Ganache)**.  
Il permet à plusieurs hôpitaux (clients) d'entraîner un modèle d'IA de manière collaborative sans partager leurs données brutes, tout en enregistrant les preuves d'entraînement sur un registre immuable.

---

## 🧠 1. Concept du Projet

### Le Split Learning
Le modèle est divisé en deux parties pour protéger la vie privée :

- **Client (Partie basse)**  
  Reçoit les images MNIST, extrait les caractéristiques initiales et génère des *Smashed Data*.

- **Serveur (Partie haute)**  
  Reçoit ces données compressées, termine l'inférence, calcule la perte (*Loss*) et renvoie les gradients pour la mise à jour locale du client.

---

### L’Intégration Blockchain
La Blockchain sert de couche de confiance. À chaque round :

1. Chaque client génère un **Hash SHA-256** de ses poids locaux.
2. Les métriques (**Accuracy** et **Loss**) sont envoyées vers un **Smart Contract Solidity**.
3. Ces données sont gravées sur **Ganache**, rendant l'historique **infalsifiable**.

---

## 🛠️ 2. Prérequis

- **Python 3.10+**
- **Ganache GUI** : https://trufflesuite.com/ganache/
- **uv** : Gestionnaire de paquets Python ultra-rapide

---

## ⚙️ 3. Installation et Configuration

### Installation de `uv` (Windows – PowerShell)

    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

### Setup de l’environnement

Depuis la racine du projet **split-learning-blockchain** :

    # Créer l’environnement virtuel
    uv venv

    # Activer l’environnement
    # Windows
    .venv\Scripts\activate

    # Mac / Linux
    source .venv/bin/activate

    # Installer les dépendances
    uv pip install torch torchvision web3 py-solc-x matplotlib

---

## 🏦 4. Configuration de Ganache

1. Lancer **Ganache GUI**
2. Créer un nouveau **Workspace Ethereum**
3. Vérifier l’URL RPC (par défaut) :  
   http://127.0.0.1:7545
4. Copier les **clés privées** des 4 premiers comptes Ganache
5. Les coller dans `scripts/train.py` dans la liste `all_private_keys`

---

## 🚀 5. Exécution du Projet

### Étape 1 : Entraînement et Enregistrement Blockchain

Cette commande compile le contrat, le déploie, télécharge MNIST et lance les rounds d’entraînement :

    python -m scripts.train

### Étape 2 : Visualisation Blockchain

Extraction des données directement depuis le smart contract :

    python -m scripts.visualize_results

Les graphiques sont automatiquement sauvegardés dans `data/images/`.

---

## 📂 6. Structure du Dossier

    split-learning-blockchain/
    ├── data/
    │   ├── datasets/          # Cache MNIST (ignoré par Git)
    │   └── images/            # Graphiques générés
    │
    ├── scripts/
    │   ├── train.py           # Orchestrateur (Déploiement + Entraînement)
    │   └── visualize_results.py
    │
    ├── src/
    │   └── split_learning_blockchain/
    │       ├── blockchain/    # Smart Contract et Web3 Manager
    │       ├── core/          # Client, Server, Coordinator
    │       ├── models/        # Réseaux de neurones (Split Learning)
    │       ├── data/          # MNIST Loader sécurisé
    │       └── utils/         # Logger, crypto, métriques
    │
    ├── contract_info.json     # Adresse et ABI du contrat (auto-généré)
    ├── pyproject.toml
    ├── README.md
    └── .gitignore

---

## 📊 7. Visualisation Attendue

Le script de visualisation génère deux graphiques **certifiés par la blockchain** :

- **Évolution de la Précision (Accuracy)**  
  Convergence du modèle global

- **Évolution de la Perte (Loss)**  
  Diminution de l’erreur au fil des transactions

---

## ✅ Résumé

- ✔️ Apprentissage collaboratif sans partage de données
- ✔️ Traçabilité et immuabilité via blockchain
- ✔️ Architecture modulaire propre et extensible
- ✔️ Projet prêt pour recherche ou démonstration académique
