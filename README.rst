python_test
===========

.. image:: https://img.shields.io/github/license/Cielquan/python_test
   :target: https://github.com/Cielquan/python_test/blob/master/LICENSE.rst

.. image:: https://img.shields.io/github/v/release/Cielquan/python_test
   :target: https://github.com/Cielquan/python_test/releases/latest


.. image:: https://travis-ci.com/Cielquan/python_test.svg?branch=master
    :target: https://travis-ci.com/Cielquan/python_test

.. image:: https://readthedocs.org/projects/python-test-cielquan/badge/?version=latest
  :target: https://python-test-cielquan.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black


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