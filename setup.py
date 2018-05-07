from distutils.core import setup
from setuptools import find_packages

package_names = find_packages()

setup(name='ropeclient',
        version='0.0.4',
        description='Access to autorope api.',
        author='Will Roscoe',
        author_email='wroscoe@gmail.com',
        url='',
        install_requires=[],
        packages=package_names,
        )