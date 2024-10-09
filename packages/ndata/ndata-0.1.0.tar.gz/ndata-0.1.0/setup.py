from setuptools import setup, find_packages

setup(
    name='ndata',
    version='0.1.0',
    description='Automated Data Preprocessing Library',
    author='Le Andre Nash',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'scipy',
    ],
)
