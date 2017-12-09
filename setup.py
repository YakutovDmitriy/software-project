from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='thesongclash-bot',
    version='0.1.0',
    description='Bot for thesongclash.com',
    long_description=readme,
    author='Yakutov Dmitry',
    author_email='yakutov@rain.ifmo.ru',
    url='https://github.com/YakutovDmitriy/software-project',
    license=license,
    packages=find_packages(exclude=('bbox', 'dbs', 'pics'))
)
