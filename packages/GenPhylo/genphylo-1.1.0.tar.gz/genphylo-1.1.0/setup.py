from setuptools import setup, find_packages

# Ensure the file is read using UTF-8 encoding to avoid encoding issues
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='GenPhylo',  # Package name in lowercase
    version='1.1.0',  # Version
    author='Marta Casanellas, Martí Cortada Garcia, Adrià Diéguez Moscardó',
    author_email='marta.casanellas@upc.edu, marti.cortada@estudiantat.upc.edu, adria.dieguez@estudiantat.upc.edu',
    description='GenPhylo generates synthetic alignments on a phylogenetic tree with given branch lengths.',
    long_description=long_description,  # Ensure README.md exists
    long_description_content_type='text/markdown',  # Ensure this matches the README format
    url='https://github.com/GenPhyloProject/GenPhylo',  # Link to your GitHub repo
    packages=find_packages(),  # Automatically find and include your package
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify Python version support
    install_requires=[
        # List your package dependencies here, e.g., 'numpy>=1.18.0'
    ],
)

