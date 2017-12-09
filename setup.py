from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='thesongclash-bot',
    version='0.1.0',
    description='Bot for www.thesongclash.com',
    long_description=readme,
    author='Yakutov Dmitry',
    author_email='yakutov@rain.ifmo.ru',
    url='https://github.com/YakutovDmitriy/software-project',
    license=license,
    packages=['sample'],
    entry_points={
        'console_scripts': [
            'lover=sample.lover:main_loop',
            'config_lover=sample.config_bbox:main'
        ]
    }
)
