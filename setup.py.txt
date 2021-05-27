  
from setuptools import setup, find_packages

setup(
    name='smart_energy_API',
    version='0.1',
    description=(
        'Implementation of the Smart Energy project'
    ),
    author='Hamid Malik',
    license='APL 2.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'requests',
        'schedule',
        'PyMySQL',
        'solaredge'
    ],
    zip_safe=False
)