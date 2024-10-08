from setuptools import setup, find_packages

setup(
    name='pwes',
    version='0.1.2',
    description='A brief description of your package',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scikit-learn',
        'seaborn',
        'matplotlib',
        'scipy',
        'numpy',
        'biopython'
    ],
)