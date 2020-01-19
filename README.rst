python_test
===========

Repo for testing different stuff with python repos.

#. create repo and cd into::

    $ git clone xxx
    $ cd xxx

#. add basic files::

    $ touch .gitignore
    $ touch .gitattributes
    $ touch LICENSE.rst
    $ touch README.rst
    $ touch CHANGELOG.rst

#. create venv and activate it::

    $ python3 -m venv venv
    $ . venv/bin/activate

#. update pip, setuptools::

    $ pip install -U pip setuptools

#. open in pycharm and setup venv as interpreter

#. setup docs
    Badges for docs:
      * License
      * Version
      * Travis (https://travis-ci.com/)
      * Coverage (https://coveralls.io/)
      * Docs (RtD)
      * Black

    ::

        $ pip install sphinx
        $ mkdir docs && pushd docs
        $ sphinx-quickstart
        $ make html
        $ popd
        # TODO 19.01.2020: readthedocs.yaml

#. setup tests::

    $ pip install pytest
    $ mkdir tests && pushd tests
    $ touch conftest.py
    $ popd

#. setup tox::

    $ touch tox.ini

#. setup travis-ci::

    $ touch .travis.yaml

#. setup setup::

    $ touch setup.py
    '''add stuff to setup.py'''
    $ pip install -e .




TODO:

* pre-commit
* tox:

  - flake8
  - black
  - coverage
  - docs
  - test