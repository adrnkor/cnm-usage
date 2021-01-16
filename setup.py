''' instructs setup.py to create a
    script named get_usage that will invoke the main
    method in the module cnm-usage.cnm-usage '''

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name="cnm-usage",
    version='0.1',
    #py_modules=['hello'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'get_usage = cnm-usage.cli:main'
        ],
    },
    author="Sal Koritz",
    description='cli app to pull usage data from cnMaestro API',
    long_description=readme,
)
