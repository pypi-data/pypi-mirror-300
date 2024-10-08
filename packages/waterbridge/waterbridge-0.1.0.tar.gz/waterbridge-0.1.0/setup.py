from setuptools import setup, find_packages


setup(
    name='waterbridge',  # Package name
    version='0.1.0',      # Version
    packages=find_packages(),  # Automatically find packages
    install_requires=[],   # List of dependencies (if any)
    description='Identification of water bridges in RNA:protein complexes',
    long_description=open('README.md').read(),  # Read the README file
    long_description_content_type='text/markdown',
    author='Raman Jangra',
    author_email='raman.compchem@gmail.com',
    url='https://github.com/RamanCompChem/waterbridges',  # Link to the project repository
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
