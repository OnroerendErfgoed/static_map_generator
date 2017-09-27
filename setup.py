import os

from setuptools import setup, find_packages
from codecs import open

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt'), encoding='utf-8') as f:
    CHANGES = f.read()

requires = [
      'pyramid',
      'tempdir',
      'Wand',
      'argparse',
      'requests',
      'colander',
      'rfc3987'
      ]

setup(name='static_map_generator',
      version='0.1.0',
      description='static_map_generator',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid"
        ],
      author='Flanders Heritage Agency',
      author_email='ict@onroerenderfgoed.be',
      url='https://github.com/OnroerendErfgoed/static_map_generator',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='static_map_generator',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = static_map_generator:main
      [console_scripts]
      """,
      )
