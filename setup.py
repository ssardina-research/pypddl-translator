"""A setuptools based setup module.

See:
      https://packaging.python.org/guides/distributing-packages-using-setuptools/
      https://github.com/pypa/sampleproject
      https://github.com/pypa/sampleproject/blob/main/setup.py
"""
from setuptools import setup, find_packages

import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# from example in https://github.com/pypa/sampleproject
setup(name='pypddl',
      version='1.5',
      description="A parser and translator of PDDL files",  # Optional
      long_description=long_description,  # Optional
      url="https://github.com/ssardina-planning/pypddl-translator",
      author="Sebastian Sardina",
      author_email="ssardina@gmail.com",  # Optional
      license_files=('LICENSE',),
      classifiers=[  # Optional
          "License :: GNU Lesser General Public License"
      ],
      project_urls={  # Optional
          "Original repo": "https://github.com/thiagopbueno/pypddl-parser"
      },
      ####################################################
      install_requires=["ply"],
      packages=find_packages(where="src"),
      package_dir={"": "src"},
      # For example, the following would provide a command called `sample` which 
      # executes the function `main` from this package when invoked:
      entry_points={  # Optional
          "console_scripts": [
              "pypddl=pypddl:main",
          ],
      },
      )
