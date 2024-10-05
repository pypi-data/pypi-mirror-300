from setuptools import setup, find_packages

setup(
    name='correlationinspector',
    version='0.1.0',
    description='Un package Python pour analyser la corrélation, incluant des tests de normalité, de linéarité, et des visualisations pour évaluer les relations entre variables.',
    author='CHABI ADJOBO AYEDESSO',
    author_email='aurelus.chabi@gmail.com',
    url='https://github.com/chabiadjobo/correlationinspector',
    project_urls={
        "Documentation": "https://medium.com/@chamaurele/analysez-les-corrélations-facilement-avec-correlationinspector-un-package-python-9037c664dffb",
        "Source Code": "https://github.com/chabiadjobo/correlationinspector",
    },
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scipy',
        'matplotlib',
        'seaborn',
        'statsmodels',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
