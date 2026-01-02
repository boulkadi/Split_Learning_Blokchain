# Split Learning & Blockchain Registry

## Objectif du Projet

Ce Projet vise à démontrer la faisabilité d'une architecture de **Split Learning sécurisée par Blockchain**. Il permet à plusieurs clients (ex : hôpitaux ou institutions) de collaborer pour entraîner un modèle d'IA sans partager leurs données brutes, tout en garantissant la **traçabilité et immuabilité** des preuves d'entraînement grâce à un Smart Contract Ethereum (Ganache).

### Valeur Ajoutée

- **Confidentialité des données** : Les données brutes restent locales sur le client
- **Transparence et confiance** : Chaque round d'entraînement est enregistré sur la blockchain
- **Collaboration multi-parties** : Plusieurs clients peuvent participer simultanément
- **Suivi des performances** : Accuracy et Loss stockés dans la blockchain

## Périmètre Couvert

### Fonctionnalités Implémentées

#### **Split Learning**

- **Client (partie basse du modèle)** : Prétraitement des images (MNIST), génération des *smashed data*
- **Serveur (partie haute du modèle)** : Achève l'inférence, calcule les gradients et renvoie les mises à jour au client
- **Round d'entraînement sécurisé** : Hash SHA-256 des poids locaux avant enregistrement sur blockchain

#### **Blockchain**

- Smart Contract Solidity pour le registre d'entraînement
- Déploiement sur **Ganache GUI**
- Stockage immuable des métriques : Accuracy, Loss, Hash des poids locaux
- Visualisation des résultats via script Python

## Technologies Utilisées

### **Intelligence Artificielle**

- **PyTorch / Torchvision** : Réseaux de neurones pour le split learning
- **Transforms MNIST** : Prétraitement et normalisation des données

### **Blockchain**

- **Web3.py** : Interaction Python avec Ethereum
- **Solidity** : Smart Contract `TrainingRegistry.sol`
- **Ganache** : Blockchain locale pour tests

### **Interface & Scripts**

- Scripts Python pour :
  - Entraînement (`train.py`)
  - Visualisation des métriques (`visualize_results.py`)
    
### **Infrastructure**

- **Python 3.12+**
- **UV** : Gestionnaire de dépendances

## Instructions de Lancement

### **Prérequis**

- Python 3.12+
- Ganache GUI: [Télécharger Ganache](https://trufflesuite.com/ganache/)
- UV (gestionnaire de dépendances Python)

### **Installation Locale**

#### 1. Cloner le projet

```bash
cd split-learning-blockchain
```

#### 2. Installer UV (gestionnaire de dépendances)

```bash
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex
```

#### 3. Créer l'environnement virtuel

```bash
uv venv
```

#### 4. Activer l'environnement

```bash
# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

#### 5. Installer les dépendances

```bash
uv sync
```

### **Configuration Ganache** 
1. Lancer Ganache GUI
2. Créer un nouveau Workspace Ethereum
3. Vérifier l'URL RPC (par défaut `http://127.0.0.1:7545`)
4. Copier les clés privées des 4 premiers comptes Ganache
5. Les ajouter dans `scripts/train.py` dans la liste `private_keys`

### **Exécution du Projet**

#### Étape 1 : Entraînement et enregistrement

```bash
python -m scripts.train
```

#### Étape 2 : Visualisation Blockchain

```bash
python -m scripts.visualize_results
```

Les graphiques sont sauvegardés automatiquement dans `data/images/`.

## Structure du Projet

```
blockchain/
├── data/
│   ├── datasets/        # Cache MNIST (ignoré par Git)
│   └── images/          # Graphiques générés
├── scripts/
│   ├── train.py         # Orchestrateur (Déploiement + Entraînement)
│   ├── visualize_results.py
│  
├── src/
│   └── blockchain/
│       ├── blockchain_code/  # Smart Contract + Web3 Manager
│       ├── core/        # Client, Server, Coordinator
│       ├── models/      # Réseaux de neurones Split
│       ├── data/        # Loader MNIST sécurisé
│       └── utils/       # Logger, crypto, métriques
├── contract_info.json   # Adresse & ABI du contrat
├── pyproject.toml       # Dépendances UV
├── README.md
└── .gitignore
```

## Vision d'Évolution

- Déploiement sur Ethereum Testnet / Mainnet
- Interface web pour suivre les rounds d'entraînement et métriques
- Support multi-client réel pour hôpitaux ou entreprises
- Monitoring et alertes sur la blockchain
- Intégration avec des dashboards (Plotly / Streamlit)

## Métriques de Succès

- Convergence du modèle global (Accuracy)
- Réduction progressive de la Loss
- Traçabilité complète via blockchain
- Confidentialité garantie des données locales
