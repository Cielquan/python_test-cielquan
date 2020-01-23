python_test
===========

.. include:: docs/source/badges.rst

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
        $ touch .readthedocs.yaml

#. setup tests::

    $ pip install pytest
    $ mkdir tests && pushd tests
    $ touch conftest.py
    $ popd
    $ touch pytest.ini

#. setup tox
    tox:
      - flake8
      - pylint
      - black
      - isort
      - coverage
      - docs
      - pytest

::

    $ touch tox.ini

#. setup travis-ci::

    $ touch .travis.yml

#. setup setup::

    $ touch setup.py
    '''add stuff to setup.py'''
    $ pip install -e .




TODO:

* badges:

    - https://github.com/nedbat/coveragepy/blob/master/README.rst
    - https://github.com/pytest-dev/pytest-cov/blob/master/README.rst
    - requires.io

* pre-commit
* appveyor a