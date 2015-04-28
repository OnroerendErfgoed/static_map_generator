import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'Shapely',
    'Wand',
    'mapnik2',
    'argparse',
    'requests',
    'tempdir'
    ]

setup(name='static_map_generator',
      version='0.0.0-dev',
      description='static_map_generator',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python"
        ],
      author='',
      author_email='',
      url='',
      keywords='python static map generator',
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
