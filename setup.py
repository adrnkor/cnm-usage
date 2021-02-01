''' instructs setup.py to create a
    script named get_usage that will invoke the main
    method in the module cnm_usage.cnm_usage '''

from distutils.core import setup
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name="cnm_usage",
    version='0.1',
    #py_modules=['hello'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'Requests',
    ],
    entry_points='''
        [console_scripts]
        get_usage=cnm_usage.cli:main
    ''',

    author="Sal Koritz",
    description='cli app to pull usage data from cnMaestro API',
    long_description=readme,
)
