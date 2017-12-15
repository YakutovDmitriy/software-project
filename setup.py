from setuptools import setup
import os


def main():
  with open('README.md') as f:
    readme = f.read()
  with open('LICENSE') as f:
    license = f.read()
  with open('requirements.txt') as f:
    requires = list(map(str.strip, f.readlines()))
  temp_dir = os.path.join('sample', 'files', 'temp')
  if not os.path.exists(temp_dir):
    os.mkdir(temp_dir)

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
    install_requires=requires,
    include_package_data=True,
    zip_safe=False,
    entry_points={
      'console_scripts': [
        '_dbg_mainloop_lover=sample.lover:main_loop',
        '_dbg_config_bbox_lover=sample.config_bbox:main',
        'lover=sample.app:main',
        '_dbg_getdb_lover=sample.getdb:main'
      ]
    }
  )


if __name__ == '__main__':
  main()
