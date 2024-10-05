# utils.py

import numpy as np
import statsmodels.api as sm
from statsmodels.stats.diagnostic import linear_reset
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Test de normalité
def test_normality(df, column):
    stat, p = stats.shapiro(df[column].dropna())
    return p > 0.05

# 2. Test de linéarité : Durbin-Watson
def test_linearity(df, var1, var2):
    X = sm.add_constant(df[var1])
    model = sm.OLS(df[var2], X).fit()
    dw_stat = sm.stats.durbin_watson(model.resid)
    return 1.5 <= dw_stat <= 2.5

# 3. Test de non-linéarité : RESET de Ramsey
def test_non_linearity(df, var1, var2):
    X = sm.add_constant(df[var1])
    model = sm.OLS(df[var2], X).fit()
    ramsey_test = linear_reset(model, power=2)
    return ramsey_test.pvalue < 0.05

# 4. Détection de déséquilibres et valeurs aberrantes
def desequilibre_outliers(var_des):
    if var_des.isnull().all():
        return {"is_balanced": False, "skewness": np.nan, "num_outliers": 0}

    value_counts = var_des.value_counts()
    max_frequency = value_counts.max()
    min_frequency = value_counts.min()
    skewness = stats.skew(var_des.dropna())

    Q1, Q3 = np.percentile(var_des.dropna(), [25, 75])
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = var_des[(var_des < lower_bound) | (var_des > upper_bound)]

    return {
        "is_balanced": (max_frequency / min_frequency) < 10,
        "skewness": skewness,
        "num_outliers": len(outliers)
    }

# 5. Choisir la méthode de corrélation
def choisir_correlation_auto(df, var1, var2, normal_var1, normal_var2):
    if normal_var1 and normal_var2:
        return "pearson" if test_linearity(df, var1, var2) else "spearman"
    if test_non_linearity(df, var1, var2):
        if desequilibre_outliers(df[var1])['is_balanced'] or desequilibre_outliers(df[var2])['is_balanced']:
            return "kendall"
    return "spearman"

# 6. Calculer la corrélation
def calculer_correlation(method, df, var1, var2):
    corr, p_value = stats.pearsonr(df[var1], df[var2]) if method == "pearson" else \
                    stats.spearmanr(df[var1], df[var2]) if method == "spearman" else \
                    stats.kendalltau(df[var1], df[var2])
    return corr, p_value


# 7. Visualiser la relation
def visualiser_relation(df, var1, var2):
    
    # Création des sous-figures pour le nuage de points et les boxplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # Nuage de points entre var1 et var2
    sns.scatterplot(x=df[var1], y=df[var2], ax=axes[0, 0])
    axes[0, 0].set_title(f"Nuage de points : {var1} vs {var2}")
    axes[0, 0].set_xlabel(var1)
    axes[0, 0].set_ylabel(var2)

    # Boxplot pour var1
    sns.boxplot(y=df[var1], ax=axes[0, 1])
    axes[0, 1].set_title(f"Boxplot : {var1}")
    
    # Boxplot pour var2
    sns.boxplot(y=df[var2], ax=axes[1, 1])
    axes[1, 1].set_title(f"Boxplot : {var2}")
    
    # Ajustement du layout
    plt.tight_layout()

    # Affichage des résultats statistiques pour var1
    print(f"### Statistiques pour '{var1}' ###")
    print(f"- Normalité (Shapiro): {'Normale' if test_normality(df, var1) else 'Non normale'}")
    print(f"- Déséquilibre et Outliers : {desequilibre_outliers(df[var1])}")
    
    # Affichage des résultats statistiques pour var2
    print(f"\n### Statistiques pour '{var2}' ###")
    print(f"- Normalité (Shapiro): {'Normale' if test_normality(df, var2) else 'Non normale'}")
    print(f"- Déséquilibre et Outliers : {desequilibre_outliers(df[var2])}")
    
    # Test de linéarité entre les deux variables
    print(f"\n### Test de linéarité entre '{var1}' et '{var2}' ###")
    print(f"- Linéarité (Durbin-Watson) : {'Linéaire' if test_linearity(df, var1, var2) else 'Non linéaire'}")

    # Affichage des graphiques
    plt.show()

    # Interaction avec l'utilisateur pour choisir la méthode de corrélation
    choix = input("Choisissez la méthode de corrélation (1 : Pearson, 2 : Spearman, 3 : Kendall) : ")

    # Retourner la méthode choisie en fonction de l'input utilisateur
    if choix == '1':
        return "pearson"  # Méthode Pearson pour la corrélation linéaire
    elif choix == '2':
        return "spearman"  # Méthode Spearman pour les relations non-linéaires
    elif choix == '3':
        return "kendall"  # Méthode Kendall pour les relations ordinales ou avec déséquilibres
    else:
        print("Choix non valide, la méthode par défaut sera 'spearman'.")
        return "spearman"


# 8. Obtenir la significativité
def obtenir_significativite(p_value):
    if p_value < 0.001: return '***'
    if p_value < 0.01: return '**'
    if p_value < 0.05: return '*'
    return ''
