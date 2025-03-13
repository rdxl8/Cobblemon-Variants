# Ajout de variantes aux datapacks Cobblemon

## Description
Ce script Python permet d'ajouter facilement des variantes (« aspects ») aux Pokémon dans un datapack Cobblemon. Il génère automatiquement les fichiers nécessaires pour la gestion des espèces, des textures et des résolutions d'aspect.

---

## Prérequis
Avant d'exécuter ce script, assurez-vous d'avoir :
- Python installé sur votre machine (version 3.x recommandée).
- Les fichiers de textures dans un dossier `textures/` correspondant aux Pokémon.
- Un environnement compatible avec les datapacks Cobblemon.

---

## Installation
1. Téléchargez ou clonez ce projet dans un répertoire local.
2. Assurez-vous que le script `variant.py` est dans le répertoire principal du projet.
3. Préparez un dossier `textures/` contenant les textures des Pokémon concernés.
   - Les textures doivent être rangées dans des sous-dossiers correspondant à leur aspect (exemple : `textures/cyber/dragonite.png`).
   - Le nom des textures doit uniquement contenir le nom du Pokémon sans numéro ni caractères additionnels.

---

## Utilisation
1. Ouvrez un terminal ou une invite de commande.
2. Placez-vous dans le répertoire du script en utilisant la commande :
   ```sh
   cd /chemin/vers/le/script
   ```
3. Exécutez le script avec la commande :
   ```sh
   python variant.py
   ```
4. Renseignez les informations demandées :
   - **Nom de l'aspect** : (exemple : "shiny", "shadow", etc.).
   - **Liste des Pokémon** sous le format `id_nom` (exemple : `25_Pikachu, 6_Charizard`).
     - Vous pouvez obtenir l'ID des Pokémon à cette URL : [Liste des IDs Cobblemon](https://gitlab.com/cable-mc/cobblemon/-/tree/main/common/src/main/resources/assets/cobblemon/bedrock/pokemon/resolvers?ref_type=heads)
   - **Informations sur le spawn** : Le script vous demandera plusieurs détails sur le spawn de chaque Pokémon. Les valeurs correspondantes peuvent être trouvées à cette URL : [Spawn Pool World](https://wiki.cobblemon.com/index.php/Spawn_Pool_World)

Le script va alors :
- Générer un fichier de définition d'aspect dans `output/data/cobblemon/species_features/`.
- Créer un fichier d'assignation des aspects dans `output/data/cobblemon/species_feature_assignments/`.
- Produire des fichiers de résolution de texture dans `output/assets/cobblemon/bedrock/pokemon/resolvers/`.
- Copier les textures associées dans `output/assets/cobblemon/textures/pokemon/`.
- Générer des fichiers de taux d'apparition dans `output/data/cobblemon/spawn_pool_world/`, qui doivent être ajoutés au JSON du même nom déjà présent sur le serveur.

---

## Organisation des fichiers
- **species_features/** : Contient les fichiers JSON définissant les nouveaux aspects.
- **species_feature_assignments/** : Contient les fichiers assignant les aspects aux Pokémon.
- **resolvers/** : Contient les fichiers JSON liant les aspects aux textures.
- **spawn_pool_world/** : Contient les fichiers JSON déterminant les taux d'apparition des Pokémon.
- **textures/** : Dossier source contenant les textures à copier.

Les dossiers dans `output/data` doivent être placés sur le serveur, tandis que les dossiers dans `output/assets` doivent être ajoutés au texture pack.

---

## Exemple
Si vous entrez :
```
Nom de l'aspect : ghost
Liste des Pokémon : 25_Pikachu, 6_Charizard
```
Le script va générer les fichiers suivants :
```
output/data/cobblemon/species_features/ghost.json
output/data/cobblemon/species_feature_assignments/ghost_assignment.json
output/assets/cobblemon/bedrock/pokemon/resolvers/25_pikachu/<RANDOM>_pikachu_ghost.json
output/assets/cobblemon/bedrock/pokemon/resolvers/6_charizard/<RANDOM>_charizard_ghost.json
output/assets/cobblemon/textures/pokemon/25_pikachu/pikachu_ghost.png
output/assets/cobblemon/textures/pokemon/6_charizard/charizard_ghost.png
output/data/cobblemon/spawn_pool_world/25_pikachu.json
output/data/cobblemon/spawn_pool_world/6_charizard.json
```

---

## Remarques
- Assurez-vous que les textures sont nommées correctement et placées dans `textures/<aspect>/`.
- Les fichiers dans `spawn_pool_world/` doivent être fusionnés avec ceux déjà présents sur le serveur.

---
