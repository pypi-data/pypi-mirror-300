# __init__.py

from .correlation_analysis import (
    analyze_correlation,
    analyze_multiple_correlations
)
from .utils import (
    test_normality,
    test_linearity,
    test_non_linearity,
    desequilibre_outliers,
    choisir_correlation_auto,
    calculer_correlation,
    visualiser_relation,
    obtenir_significativite
)
