import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
# with open(os.path.join(here, 'CHANGES.txt')) as f:
#     CHANGES = f.read()
CHANGES = "changes"

requires = [
      'pyramid',
      'tempdir',
      'Wand',
      'argparse',
      'requests',
      'wsgiref']

setup(name='static_map_generator',
      version='0.0.0.dev',
      description='static_map_generator',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        ],
      author='Flanders Heritage Agency',
      author_email='ict@onroerenderfgoed.be',
      url='',
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
