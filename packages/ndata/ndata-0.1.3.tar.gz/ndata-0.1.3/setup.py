from setuptools import setup, find_packages
import pathlib

# Get the long description from the README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='ndata',  # Name of the package
    version='0.1.3',
    description='Automated Data Preprocessing Library',
    long_description=long_description,  # Use the README as long description
    long_description_content_type='text/markdown',  # Tell PyPI the format of the README
    author='Leandre',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'scipy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
