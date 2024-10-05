# Description

correlationinspector est un package Python destiné à l'analyse de corrélations entre variables dans des ensembles de données. Il fournit des outils pour tester la normalité des données, évaluer la linéarité, détecter les déséquilibres et les valeurs aberrantes, ainsi que pour calculer et visualiser les coefficients de corrélation.

# Fonctionnalités

- **Test de normalité** avec la méthode de Shapiro-Wilk.
- **Test de linéarité** à l'aide de Durbin-Watson.
- **Test de non-linéarité** avec le test RESET de Ramsey.
- **Détection de déséquilibres** et de valeurs aberrantes dans les variables.
- **Choix automatique de la méthode de corrélation** (Pearson, Spearman, Kendall) selon la distribution des données.
- **Visualisation des relations entre variables avec des graphiques.**

# Installation

Pour installer le package, utilisez `pip` :

```bash
pip install correlationinspector
```

# Documentation des Fonctions

## 1. `analyze_correlation(df, var1, var2, mode='auto')`

* **Description** : Analyse la corrélation entre deux variables.
* **Arguments** :
  * `df` : DataFrame contenant les variables.
  * `var1` : Première variable pour l'analyse.
  * `var2` : Deuxième variable pour l'analyse.
  * `mode` : Mode d'analyse (`'auto'` ou `'manuel'`).
* **Retourne** : La valeur de la corrélation et la méthode utilisée.

## 2. `analyze_multiple_correlations(df, variables, mode='auto')`

* **Description** : Analyse les corrélations entre plusieurs paires de variables.
* **Arguments** :
  * `df` : DataFrame contenant les variables.
  * `variables` : Liste des variables à analyser.
  * `mode` : Mode d'analyse (`'auto'` ou `'manuel'`).
* **Retourne** : Un DataFrame avec les résultats des corrélations.

## 3. `test_normality(df, column)`

* **Description** : Teste la normalité d'une variable à l'aide du test de Shapiro-Wilk.
* **Arguments** :
  * `df` : DataFrame contenant la variable.
  * `column` : Colonne à tester.
* **Retourne** : `True` si la variable est normalement distribuée, sinon `False`.

## 4. `choisir_correlation_auto(df, var1, var2, normal_var1, normal_var2)`

* **Description** : Choisit automatiquement la meilleure méthode de corrélation (Pearson, Spearman ou Kendall).
* **Arguments** :
  * `df` : DataFrame contenant les variables.
  * `var1` et `var2` : Variables à analyser.
  * `normal_var1` et `normal_var2` : Indique si les variables sont normalement distribuées.
* **Retourne** : La méthode de corrélation recommandée.

## 5. `visualiser_relation(df, var1, var2, mode='manuel')`

* **Description** : Génère une visualisation de la relation entre deux variables.
* **Arguments** :
  * `df` : DataFrame contenant les variables.
  * `var1` et `var2` : Variables à visualiser.
  * `mode` : Mode de visualisation (`'manuel'` ou autre).
* **Retourne** : Une visualisation graphique.

# Dépendance

Les dépendances suivantes seront installées automatiquement avec le package : `numpy, pandas, scipy, statsmodels, matplotlib, seaborn`

# Utilisation


## Préparation des données

Avant d'utiliser ce package pour analyser les corrélations, assurez-vous que vos données sont nettoyées. Cela signifie qu'il ne doit pas y avoir de valeurs manquantes (`NaN`) ou infinies dans les colonnes que vous souhaitez analyser.

## Analyser la corrélation entre deux variables

```
import pandas as pd
from correlationinspector import analyze_correlation

# Chargement d'un DataFrame
df = pd.read_csv('votre_fichier.csv')

# Analyser la corrélation entre deux variables
correlation, method = analyze_correlation(df, 'var1', 'var2')

print(f"Corrélation entre var1 et var2 : {correlation} (Méthode : {method})")

```

## Analyser plusieurs corrélations en même temps

```
import pandas as pd
from correlationinspector import analyze_multiple_correlations

# Chargement d'un DataFrame
df = pd.read_csv('votre_fichier.csv')

# Variables à analyser
variables = ['var1', 'var2',.., 'varn']

# Analyser les corrélations multiples
resultats = analyze_multiple_correlations(df, variables)

# Afficher les résultats
print(resultats)

```

# Contribuer

Les contributions sont les bienvenues ! Veuillez suivre ces étapes :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/YourFeature`)
3. Faites vos modifications et validez (`git commit -m 'Add some feature'`)
4. Poussez vers la branche (`git push origin feature/YourFeature`)
5. Ouvrez une pull request

# License

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

# Auteurs

CHABI ADJOBO AYEDESSO

aurelus.chabi@gmail.com
