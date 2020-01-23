python_test
===========

.. start badges

.. list-table::
    :stub-columns: 1

    * - info
      - |license| |black|
    * - tests
      - |travis| |appveyor| |codecov| |docs| |reqs|
    * - package
      - |py_versions| |pypi| |format| |downloads|
    * - Github stats
      - |release| |last_commit| |stars| |forks| |contributors|

+---------+--------------------------------+
| info    | |license| |black|              |
+---------+--------------------------------+
| tests   | |travis| |appveyor| |codecov|  |
|         | |docs| |reqs|                  |
+---------+--------------------------------+
| package | |py_versions| |implementations||
|         | |pypi| |pypi2|                 |
|         | |wheel| |downloads|            |
+---------+--------------------------------+
| Github  | |release| |last_commit|        |
|         | |stars| |forks| |contributors| |
+---------+--------------------------------+

.. |license| image:: https://img.shields.io/github/license/Cielquan/python_test
    :target: https://github.com/Cielquan/python_test/blob/master/LICENSE.rst
    :alt: License

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black


.. |travis| image:: https://travis-ci.com/Cielquan/python_test.svg?branch=master
    :target: https://travis-ci.com/Cielquan/python_test
    :alt: Travis Build Status

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/Cielquan/python_test?branch=master&svg=true
    :target: https://ci.appveyor.com/project/Cielquan/pytest-cov
    :alt: AppVeyor Build Status

.. |codecov| image:: https://codecov.io/gh/Cielquan/python_test/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Cielquan/python_test
    :alt: Codecov Test Coverage

.. |docs| image:: https://readthedocs.org/projects/python-test-cielquan/badge/?version=latest
    :target: https://python-test-cielquan.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |reqs| image:: https://requires.io/github/Cielquan/python_test/requirements.svg?branch=master
    :target: https://requires.io/github/Cielquan/python_test/requirements/?branch=master
    :alt: Requirements status


.. |py_versions| image:: https://img.shields.io/pypi/pyversions/python_test_cielquan.svg?logo=python&logoColor=FBE072
    :target: https://pypi.org/project/python_test_cielquan/
    :alt: Python versions supported

.. |implementations| image:: https://img.shields.io/pypi/implementation/python_test_cielquan.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/python_test_cielquan

.. |pypi| image:: https://badge.fury.io/py/python_test_cielquan.svg
    :target: https://pypi.org/project/python_test_cielquan/
    :alt: PyPI status
.. |pypi2| image:: https://img.shields.io/pypi/v/python_test_cielquan.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/python_test_cielquan

.. |wheel| image:: https://img.shields.io/pypi/format/python_test_cielquan.svg
    :target: https://pypi.org/project/python_test_cielquan/
    :alt: PyPI Wheel

.. |downloads| image:: https://img.shields.io/pypi/dw/python_test_cielquan.svg
    :target: https://pypi.org/project/python_test_cielquan/
    :alt: Weekly PyPI downloads

.. |repos| image:: https://repology.org/badge/tiny-repos/python:python_test_cielquan.svg
    :target: https://repology.org/metapackage/python:python_test_cielquan/versions
    :alt: Packaging status

.. |status| image:: https://img.shields.io/pypi/status/python_test_cielquan.svg
    :target: https://pypi.org/project/python_test_cielquan/
    :alt: Package stability


.. |release| image:: https://img.shields.io/github/v/release/Cielquan/python_test
    :target: https://github.com/Cielquan/python_test/releases/latest
    :alt: Latest Release

.. |last_commit| image:: https://img.shields.io/github/last-commit/Cielquan/python_test
    :alt: GitHub last commit
.. |commits-since| image:: https://img.shields.io/github/commits-since/pytest-dev/pytest-cov/v2.8.1.svg
    :alt: Commits since latest release
    :target: https://github.com/pytest-dev/pytest-cov/compare/v2.8.1...master

.. |stars| image:: https://img.shields.io/github/stars/Cielquan/python_test.svg?logo=github
    :target: https://github.com/Cielquan/python_test/stargazers
    :alt: Github stars

.. |forks| image:: https://img.shields.io/github/forks/Cielquan/python_test.svg?logo=github
    :target: https://github.com/Cielquan/python_test/network/members
    :alt: Github forks

.. |contributors| image:: https://img.shields.io/github/contributors/Cielquan/python_test.svg?logo=github
    :target: https://github.com/Cielquan/python_test/graphs/contributors
    :alt: Contributors













.. other badges:
    https://github.com/pytest-dev/pytest-cov/blob/master/README.rst
    https://github.com/nedbat/coveragepy/blob/master/README.rst

.. finish badges

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