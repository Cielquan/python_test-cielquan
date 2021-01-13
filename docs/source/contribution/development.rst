.. spelling::

    virtualenvs

Development
===========


Set up Local Development Environment
------------------------------------

The setup of a local development environment is pretty easy. The only tool you need is
`poetry <https://python-poetry.org/docs/>`__. You can install it via the
`recommended way <https://python-poetry.org/docs/#installation>`__, which installs it
globally on your system or you can install it via ``pip`` in a self-created virtualenv
(`virtualenv manual <https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/>`__).

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
----------------------------------------------

This section will explain how to work with the above created local development
environment. For development we use the following tools:

    - `poetry <https://python-poetry.org/docs/>`__:
      for dependency management and package building
    - `nox <https://nox.thea.codes/>`__:
      for running standardized tests or automated dev-tasks in an existing virtualenv
    - `tox <https://tox.readthedocs.io/>`__:
      as virtualenv back-end for ``nox`` to create isolated test virtualenvs
    - `pre-commit <https://pre-commit.com/>`__:
      for automated linting and quality checking before committing


Testing
-------

To test the code you can run::

    $ nox

to run all tests or::

    $ nox -s full_lint

    $ nox -s full_test_code

    $ nox -s full_test_docs

to lint, test the code or test the docs respectively.

For more specific testing and development environment setup we have several different
``nox`` sessions available. You can invoke them with ``nox -s <session>``. Some take
additional arguments which need to be added at the end after a double dash and separated
by a space like so: ``nox -s <session> -- arg1 arg2``. For local development and testing
``nox`` sessions are meant to be called from the development virtualenv. If a testing
``nox`` session is invoked without an active virtualenv ``tox`` is automatically invoked
as a *virtualenv back-end* to create a virtualenv for the given task specifically and the
session is then run inside it. You can force this behavior also by giving ``tox`` as an
additional argument. If you want to give arguments to ``tox`` you need to specify them
as a comma separated list like this: ``TOX_ARGS=<tox-args>``. For normal development you
should not need it but the same applies for ``nox`` called by ``tox`` with:
``NOX_ARGS=<nox-args>``.

``nox`` testing sessions:
~~~~~~~~~~~~~~~~~~~~~~~~~

- ``package``:
    Build a package with ``poetry`` from the current source and test it with ``twine``.

- ``test_code``:
    This session will run all tests with the python version used by the virtualenv from
    where it's invoked. If ``tox`` is used as virtualenv back-end the tests are run with
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

    * ``HOOKS=<hook-id>``: Specify hooks (separated by comma) to run. If you want to run
      a single hook just add its name without the ``HOOKS=`` prefix.
    * ``SKIP=<hook-id>`` Specify hooks (separated by comma) to skip.
    * ``diff``: Print the diff when a hook fails. Recommended to only set when one or
      no hook is specified as the diff will be printed on every failing hook otherwise.
    * Any argument understood by ``pre-commit``.

- ``docs``:
    Build the docs as HTML in */docs/build/html*.

    **Addtional arguments**:

    * ``autobuild`` / ``ab``: Build the docs and open them automatically in your browser
      after starting a development web-server via ``sphinx-autobuild``.
    * Any argument understood by ``sphinx`` or ``sphinx-autobuild``.

- ``"test_docs(builder='html')"``:
    Build the docs with the **html** builder in */docs/build/test/html*
    under nit-picky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.

- ``"test_docs(builder='linkcheck')"``:
    Build the docs with the **linkcheck** builder in */docs/build/test/linkcheck*
    under nit-picky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.

- ``"test_docs(builder='coverage')"``:
    Build the docs with the **coverage** builder in */docs/build/test/coverage*
    under nit-picky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.

- ``"test_docs(builder='doctest')"``:
    Build the docs with the **doctest** builder in */docs/build/test/doctest*
    under nit-picky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.

- ``"test_docs(builder='spelling')"``:
    Build the docs with the **spelling** builder in */docs/build/test/spelling*
    under nit-picky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.

- ``test_docs``:
    Run all ``test_code`` sessions from above.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.


``nox`` dev setup sessions:
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``install_extras``:
    Install all specified extras into the active venv.

- ``setup_pre_commit``:
    Create ``pre_commit`` ``tox`` environment, install *pre-commit* and *commit-msg*
    hooks and run the prior created environment once with all *pre-commit* hooks.

- ``create_spellignore``:
    Create ``.spellignore`` file at project root if non exists. The content is a copy of
    the ``.gitignore`` file.

- ``dev``:
    Run ``install_extras``, ``setup_pre_commit`` and ``create_spellignore`` ``nox``
    sessions.
