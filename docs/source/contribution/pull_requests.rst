Contribution through `Github Pull Requests <https://github.com/cielquan/python_test-cielquan/pulls>`__
======================================================================================================


Table of contents:
    - `Contribution to the Documentation`_
    - `Contribution to Code`_
    - `Git(hub) Workflow`_


Contribution to the Documentation
---------------------------------

Contribution to the documentation is the easiest way to get started to contribute to
``python_test-cielquan``. You can look in the
`Github issue tracker <https://github.com/cielquan/python_test-cielquan/issues>`__
for issues with the ``Documentation`` label and try to solve them.

For creating your local development environment please see below:
`Set up Local Development Environment`_


Contribution to Code
--------------------

Contribution to Code is a bit more complex as some standards have been set and you must
follow these rules to get your contribution accepted. But this sounds scarier than it
is.

First you need an issue to work on. Just pick an issue from the
`Github issue tracker <https://github.com/cielquan/python_test-cielquan/issues>`__
and get started.

    **Note:** If you find are a first time contributor issues with the
    ``Good First Issue`` label are good ones to get started with.


Set up Local Development Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The setup of a local development environment is pretty easy. The only tool you need to
have installed is `poetry <https://python-poetry.org/docs/>`__. You can install it
via the `recommended way <https://python-poetry.org/docs/#installation>`__, which
installs it globally or you can install it via ``pip`` in a selfcreated virtualenv:
`manual here <https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/>`__.

With ``poetry`` set up and ready we can create our development environment in just two
steps::

    $ poetry install
    $ poetry run nox -s dev

This will create a virtualenv (if you did not create and activate one yourself),
install the project plus its dependencies and then install all specified extras so that
you have all development dependencies installed. Next it will create a ``.spellignore``
file, which is just a copy of the ``.gitignore`` file. At last it will create a ``tox``
environment for ``pre-commit``, install ``pre-commit`` as a ``git`` hook and run all
hooks once.


Working with the Local Development Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section will explain how to work with the above created local development
environment. For development we use the following tools:

- `poetry <https://python-poetry.org/docs/>`__:
    for dependency management and package building
- `nox <https://nox.thea.codes/>`__:
    for running standardized tests or automated dev-tasks in an existing virtualenv
- `tox <https://tox.readthedocs.io/>`__:
    as virtualenv backend for ``nox`` to create isolated test virtualenvs
- `pre-commit <https://pre-commit.com/>`__:
    for automated linting and quality checking before commiting


Testing
~~~~~~~

To test the code you can run::

    $ nox -s tox_lint

    $ nox -s tox_code

    $ nox -s tox_docs

to lint, test the code or test the docs respectively.

For more specific testing and development environment setup we have several different
``nox`` sessions available. You can invoke them with ``nox -s <session>``. Some take
additional arguments which need to be added at the end after a double dash and separated
by a space like so: ``nox -s <session> -- arg1 arg2``. For local development and testing
``nox`` sessions are meant to be called from the development virtualenv. If a testing
``nox`` session is invoked without an active virtualenv ``tox`` is automatically invoked
as a *virtualenv backend* to create a virtualenv for the given task specificly and the
session is then run inside it. You can force this behavior also by giving ``tox`` as an
additional argument. If you want to give arguments to ``tox`` you need to specify them
as a comma separated list like this: ``TOX_ARGS=<tox-args>``. For normal development you
should not need it but the same applies for ``nox`` called by ``tox`` with:
``NOX_ARGS=<nox-args>``.

``nox`` testing sessions:

- ``package``:
    Build a package with ``poetry`` from the current source and test it with ``twine``.

- ``test_code``:
    This session will run all tests with the python version used by the virtualenv from
    where it's invoked. If ``tox`` is used as virtualenv backend the tests are run with
    all specified and available python versions.

    **Addtional arguments**:

    * Any argument understood by ``pytest``. Defaults to ``tests`` (tests directory)

- ``coverage_merge``:
    Merge existing ``.coverage.*`` artifacts into one ``.coverage`` file and create XML
    (*coverage.xml*) and HTML (*/htmlcov*) reports.

- ``coverage_report``:
    Report the total coverage and diff coverage against origin/master or DIFF_AGAINST.

- ``coverage``:
    Merge and report the coverage. (runs both coverage sessions above)

- ``safety``:
    Run ``safety`` over all specified dependencies to check for dependency versions that
    are known to be vulnerable.

- ``pre_commit``:
    Run ``pre-commit`` over all project files to lint, format and check them.

    **Addtional arguments**:

    * ``HOOKS=<hook-id>``: Specify hooks (seperated by comma) to run. If you want to run
      a single hook just add its name without the ``HOOKS=`` prefix.
    * ``SKIP=<hook-id>`` Specify hooks (seperated by comma) to skip.
    * ``diff``: Print the diff when a hook fails. Recommended to only set when one or
      no hook is specified as the diff will be printed on every failing hook otherwise.
    * Any argument understood by ``pre-commit``.

- ``docs``:
    Build the docs as HTML in */docs/build/html*.

    **Addtional arguments**:

    * ``autobuild`` / ``ab``: Build the docs and open them automatically in your browser
      after starting a development webserver via ``sphinx-autobuild``.
    * Any argument understood by ``sphinx`` or ``sphinx-autobuild``.

- ``"test_docs(builder='html')"``:
    Build the docs with the **html** builder in */docs/build/test/html*
    under nitpicky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.

- ``"test_docs(builder='linkcheck')"``:
    Build the docs with the **linkcheck** builder in */docs/build/test/linkcheck*
    under nitpicky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.

- ``"test_docs(builder='coverage')"``:
    Build the docs with the **coverage** builder in */docs/build/test/coverage*
    under nitpicky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.

- ``"test_docs(builder='doctest')"``:
    Build the docs with the **doctest** builder in */docs/build/test/doctest*
    under nitpicky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.

- ``"test_docs(builder='spelling')"``:
    Build the docs with the **spelling** builder in */docs/build/test/spelling*
    under nitpicky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.

- ``test_docs``:
    Run all ``test_code`` sessions from above.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.


``nox`` dev setup sessions:

- ``install_extras``:
    Install all specified extras into the active venv.

- ``setup_pre_commit``:
    Create ``pre_commit`` ``tox`` environment, install *pre-commit* and *commit-msg*
    hooks and run the prior created environment once with all *pre-commit* hooks.

- ``debug_import``:
    Add/Install files to active virtualenv's site-packages directory which add
    ``devtools.debug()`` as ``debug`` to python builtins. ``devtools`` gets installed
    as dev-dependency by ``poetry``.

- ``create_pdbrc``:
    Create ``.pdbrc`` file at project root if non exists.

- ``create_spellignore``:
    Create ``.spellignore`` file at project root if non exists. The content is a copy of
    the ``.gitignore`` file.

- ``dev``:
    Run ``install_extras``, ``setup_pre_commit`` and ``create_spellignore`` ``nox``
    sessions.

- ``dev2``:
    Run all other dev setup ``nox`` sessions.


Git(hub) Workflow
-----------------

This section will explain the specifics regarding to ``git`` and ``github``.


Commit messages
~~~~~~~~~~~~~~~

We use `Conventional Commits <https://www.conventionalcommits.org/en/v1.0.0/>`__ as
standard for our commit messages. With this standard commit messages are human **and**
machine readable so that the changelog creation and versioning can be automated based
on keywords. Commit messages will be checked in the CI pipeline.

If you submit noncompliant commit messages we will need to ask you to fix them. So we
highly recommend you to set ``pre-commit`` up.

If you set up ``pre-commit`` as described above you already have the ``commit-msg`` hook
installed which will check your commit message for compliance else you can run::

    $ nox -s setup_pre_commit


Development
~~~~~~~~~~~

We have no dedicated development branch so all changes are expected to be submitted and
merged into ``master``. Merging into ``master`` is only allowed after all CI tests
**succeeded**. Pull requests must be merged with a merge commit.

Bugfixes are also expected to be merged into ``master``. Buf if they are
critical the next release will be much sooner.

If the pull request has many small commits the maintainer may use a *squash merge* to
keep the changelog cleaner. Of cause the squash commit-message must follow the
aforementioned commit message rules!


Releases
~~~~~~~~

When enough changes and additions or time important fixes have accumulated on the
``master`` branch its time for a new release. The exact time is subject to the
judgement of the maintainer(s).

To trigger a new release you have to manually start the ``Release new version`` workflow
for the ``master`` branch form the ``Actions`` tab of the Github repository. The
workflow will run the full current test suit first. After that it will also run the full
test suit of the previous version and when the test suit fails it will look for a commit
declaring *BREAKING CHANGES*. If none is found the worklow will fail. After success the
workflow will automatically bump the version counter based on semantic versioning and
conventional commits, update the changelog, create a new git tag, build the
package + wheel and push them to PyPI. At last a Github release is created with the built
source as assets.

    **Note**: As all changes are merged into ``master`` only the current released
    version is supported and will receive bugfixes. Bugfixes for older versions are not
    planned.



+-------------------+---------------------------------------------------------------------------------------------+
| **Dev tools**     | |pre-commit| |black| |isort| |mypy|                                                         |
|                   +---------------------------------------------------------------------------------------------+
|                   | |bandit| |flake8| |pylint| |pyenchant|                                                      |
|                   +---------------------------------------------------------------------------------------------+
|                   | |nox| |tox| |pytest| |sphinx|                                                               |
|                   +---------------------------------------------------------------------------------------------+
|                   | |conventional_commits| |poetry|                                                             |
+-------------------+---------------------------------------------------------------------------------------------+


.. Dev tools

.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=flat-square&logo=pre-commit&logoColor=yellow
    :target: https://pre-commit.com
    :alt: pre-commit - enabled

.. |black| image:: https://img.shields.io/badge/Code%20Style-black-000000.svg?style=flat-square
    :target: https://black.readthedocs.io
    :alt: Code Style - black

.. |isort| image:: https://img.shields.io/badge/Imports-isort-%231674b1?style=flat-square&labelColor=ef8336&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAZCAMAAADzN3VRAAAAsVBMVEUVdbQWdLEXdLAXdLEYdLAYdLEada4bdLEcdLEddK8ddaweeaAfdqkfeaAgdqknda8pdK8rdawuda8veJ8yeJ48dqc/da1FdqdRd6BYd59adqRleZRxeJ15ttaIe4OPvNqYe3+lfXCmfnC2fmfDgj/DgkDIf17LgkbRgkPTgkbU8/jXgkPZgF3fgU3fgkPigFfkgznl+fzqgk/rgzrsgzztgjjtgzbtgzjugzbvgzb///+RcCogAAAAxklEQVQoz3WSBQ7DMAxF420dMzMz8+re/2ALOm22fqmR/Z+cNHYYxImZIDVHrnvXJXkkrSPkgGGFyBujyhmyRVeaNMnwTdBTRGc1ubsfqinTBkEgnPaDx31BVhLUuXcL6DIoiD1zNBHrgH8LSz7C28uaAuITMWvIyxImjeqfmpI0MpFzFNnonMESseJ5liCRIo71r0pyleCoeuDBmSctsBWoutOgnPp2ovnE9Bpg6ICknekubqYAaetP3beTmAn70vl9VT/6AiI3Qb9AnYdrAAAAAElFTkSuQmCC
    :target: https://pycqa.github.io/isort
    :alt: Imports - isort

.. |mypy| image:: https://img.shields.io/badge/-checked-blue?style=flat-square&labelColor=white&logoWidth=70&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHcAAAAYCAMAAAD3RZI3AAABJlBMVEUAAAAAAP8A//8AgIBVVVVAgL8zZswqgKpVVVUkbbZVVVVNTU0udLkqaqorcaokbaoqarUpcK0xbLEsarBPT08ubLIoa7Unb7FOTk4mbLMrbbArbbYsb7EqarUpb7EqbrMtbbRPT08rbLApbrAoa7Iob7IqbrIrbrEobbIqbrNPT08pbbFRUVFPT08qa7EpbLErbbIqbrEqbbIrbLEqbLEqbLFRUVEqbLErb7IrbrEqbrMrbbIrbrJPT08qbLIqbrIqbbIrbbIrbrMqbbIqbbJRUVErbrIqbbIrbbIqbbIpbrJQUFAqbbIqbbIqbrMqbbIqbbIrbbIrbbIqbbIqbbEqbbIqbbIqbLIqbbIqbrIrbbJQUFAqbbJQUFAqbbNQUFAqbbJQUFBpO8x3AAAAYHRSTlMAAQECAwQFBgYHCQoLDBIVGBkaHR0hJicnKCoqLjA+Q0RER0pMTE9YWWFkaW5xcnZ3eXp9f4CBhoiJjY+Vl5men6iur7e3ub2/wNjb4OLm5+np7/Lz8/X3+Pn8/P39/v4p8tJ3AAAByUlEQVRIx72WZ3+DIBDGSWdau3dr99473TPdO90rbR++/5eoIioompDkl+cFB+eFP/E4hBCuVzDtkbKqCZ6Kmoda2s8jhvK+hasoBZhSw0jmiDEMQ+R2lYarFwaU5kXrctuZcnBNk5AM0Gb3M8hW27bXbBae+hPao0d8spha9shWt9nic1chq95Pu7x8IM1Xds3ME8+QlyrpBZ77/0KO4WGAgkvVXKwwM4UJbxJ3qi+sBRJ3b5kPPFjtHbaZs1Pgtqq5N0rulm2mgVHbpvFstf18LseIXMEtDZywEBY9YoHJXJV12j78BrgstaQB42yUyMl16jp/7i1mfJ9YmLyT9YYvOIjk7pAqTa5jorkIxojcMTJPZelx37Eey73CImlUcAmlBXMTVmrFAglwj9yxcDK43OWfIriWrVNwT5l982Nl7qDNHQhhN5R1pLaXEDeqVEc1wvvGiXROqrlEg0vUXOBYOHWlA5iFKbhnRJO7GeYS+bDfDXG9bzHtYNL/CkkbNejyHJWR3MgdFa8hkcvvGwqu6r7hMhdIAVxpo0ZwgeE4bpL8aXIPrSRexK6F77KYyxbTiB53MjWncqdS0mgpEfX7WYf6XaYL7D/7oSPH9BHEpQAAAABJRU5ErkJggg==
    :target: http://www.mypy-lang.org
    :alt: mypy - checked

.. |bandit| image:: https://img.shields.io/badge/Security-bandit-yellow.svg?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAAUCAMAAAC3SZ14AAAAilBMVEUAAAAYGBgXFxf50DX72mD51E361kz50DT50jn72mHcvEz711UXFxd/fHyKeEXcukXcukfcu0ncvE3dvlTev1rjwUjjw0jlxVj50Db50Tn50Tv50j/500H600T61Ef61Ej61Er61k361lD711P711X72Fn72Fv72Vz72V772mH72mP822b822f///+Yj+WZAAAADHRSTlMAKu/39/v8/f39/v731TR1AAAAnklEQVQY013QSQKCMBBE0XbE4SviyChIjCKQ+1/PRUADtXyb6mqRLgCIE2ib+uOaleqt/0bbADu9VQzEGKPKHzW1JR70TfUawEABWJtXGAMUub1kouClAcgzS3CGvSqvRQ4+UxERbvoEAAc/7ip5qnJx3ARpEvcDgGVxz9LEmQlAmsRR6NJlKCIEVtz3kMRR6I0etgpnAxEBbyQi0ssXVHoQyCIgOjIAAAAASUVORK5CYII=
    :target: https://bandit.readthedocs.io
    :alt: Security - bandit

.. |flake8| image:: https://img.shields.io/badge/Linting-flake8-blue.svg?style=flat-square
    :target: https://flake8.pycqa.org
    :alt: Linting - flake8

.. |pylint| image:: https://img.shields.io/badge/Linting-pylint-blue.svg?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAXCAYAAADpwXTaAAADAklEQVQ4T42USWgUQRSG/4pgZPAST4o3EUSNghcPylzUiAvBkwsIirtBjBIHlLgwuIREJhjbDfHkRVAvyihBYpJDEpfBQIKjIARUJKCiUYlGp6vee1LV3TOTYQLTl6K76n38739/tcIUz/pUjydGg4lhjIaIXQlijPS3bj1SrkyV+7gx1eORrweJaZ4Q15AYsCEYMhAmsDF40b6jsbS2LGx9a5fXeaLOHV6VfOARC1j7cKsxYCJkOnZWBlvX0ukZEnCoxIQAsqsEyl55eyqDlcqPJ+4sJeG9JgQJEQav7S8Pq2/vvWQ0TxMOWjBsYAucInGmwxCDWUMMwxBh6Prno/gy3gERAD7UnKuNKplMVr2MxTtsgS20AAknyMKQ0HjmCEpOuIN9/tkB1gD7QEwuqg1tTy8zkZoEshMr8cupsyqYA9ip7F2AtsJopwyioda1PvFKsxSBrNF2EGJ8sAg4BA3fONgon/Z5YHIQp4w11NoLnZ7N0KQskehnF7cdK5dBGW3YBaOXBWrIQWB8ABpqzblHnlUSZMgHkWCgKfMGohbnYa49W5ADTLGaECZWWQ5qdTKdYjbToyxB9LX+pqFDBZAtyAUKLDBS41qz4HCPfHI3IN5837ORsCbrv7olcybbHI08aEMXvAGF74FPtj0YA7VkoNHB6pPp2Pc/v1ptluQftWRODzfnldgCZ3Jk9GTTw+mm1ZKBrrJ3U0YbvOKRF9SFrVmzF/ZWdp3k426veOQOVhQBq8a2VdFfQz5s94pHHrUZqZHXK73KYe83z4b2mxGOPPArSL57RN1WS/sHK1KWr3mzaDq4JpUvGufjasXzv1P9ncsOAMB8ACNRkQK6BVhdBJm0X3QOGGrD2LdxYM15zLIb2RS6l5/E24kcDgOYkU3hcW0CGwH8i1XjSuYCFtUm8vC5AL7awDll2RTG7FqbcLCZ2RQe9r0DN9xCXU0MN/vOYn78DEZ+TODAjX3oii9AVW0CmwD8Lm65bJuxatRP5JCODp7bgu7T9wptlu5H5/4D001rKLIpQrgAAAAASUVORK5CYII=
    :target: https://pylint.pycqa.org
    :alt: Linting - pylint

.. |pyenchant| image:: https://img.shields.io/badge/Spelling-pyenchant-blue.svg?style=flat-square
    :target: https://pyenchant.github.io/pyenchant
    :alt: Spelling - pyenchant

.. |nox| image:: https://img.shields.io/badge/Test%20automation-nox-brightgreen.svg?style=flat-square
    :target: https://nox.thea.codes
    :alt: nox

.. |tox| image:: https://img.shields.io/badge/Venv%20backend-tox-brightgreen.svg?style=flat-square
    :target: https://tox.readthedocs.io
    :alt: tox

.. |pytest| image:: https://img.shields.io/badge/Test%20framework-pytest-brightgreen.svg?style=flat-square
    :target: https://docs.pytest.org
    :alt: Pytest

.. |sphinx| image:: https://img.shields.io/badge/Doc%20builder-sphinx-brightgreen.svg?style=flat-square
    :target: https://www.sphinx-doc.org/
    :alt: Sphinx

.. |conventional_commits| image:: https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square
    :target: https://conventionalcommits.org
    :alt: Conventional Commits - 1.0.0

.. |poetry| image:: https://img.shields.io/badge/Packaging-poetry-brightgreen.svg?style=flat-square
    :target: https://python-poetry.org/
    :alt: Poetry
