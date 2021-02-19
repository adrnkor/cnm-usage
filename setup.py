from setuptools import setup, find_packages

setup(
    name='cnm_usage',
    version='0.1',
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

    author='Sal Koritz',
    description='cli app to pull usage data from cnMaestro API'
)
