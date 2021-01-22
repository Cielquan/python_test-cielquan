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

The first command will create a virtualenv (if you did not create and activate one
yourself) and install the project plus its dependencies.

The second command will run some ``nox`` sessions inside the virtualenv to set up
development tools. First it will install all extras so that you have all
development/additional dependencies available. Next it will create a ``.spellignore``
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
~~~~~~~

To run the full test suit you can run::

    $ nox

or you can run the following commands to lint/format, test the code or test the docs
respectively::

    $ nox -s full_lint

    $ nox -s full_test_code

    $ nox -s full_test_docs


For more specific testing and development environment setup we have several different
more specific ``nox`` sessions available. The above ones are only wrapper around
multiple of the smaller ones. You can invoke them the same way with
``nox -s <session>``. Some take additional arguments which need to be added at the end
after a double dash and separated by a space like so: ``nox -s <session> -- arg1 arg2``.

``nox`` sessions work in one of two ways here:

1) You call ``nox`` from a virtualenv and ``nox`` runs its commands inside it.
2) You call ``nox`` without a virtualenv and ``nox`` will instead of running the
   commands call ``tox`` as a *virtualenv back-end*. ``tox`` then will create a
   virtualenv and call ``nox`` the same way you did. The inner ``nox`` then will run
   the commands. You can force this behavior also by giving ``tox`` as an additional
   argument after the double dash.

For local development and testing ``nox`` sessions are meant to be called from the
development virtualenv (option 1) for better performance.

Option 2 is used for the above mentioned ``full_*`` sessions, testing the code against
different python versions and in CI pipelines. If you want to give arguments to ``tox``
you need to specify them as a comma separated list after the double dash like this:
``nox -s <session> -- TOX_ARGS=<tox-args>``. The same way you can also specify
additional arguments for the inner ``nox`` with:
``nox -s <session> -- NOX_ARGS=<nox-args>``.


``nox`` testing sessions:
~~~~~~~~~~~~~~~~~~~~~~~~~

- ``package``:
    Build a package with ``poetry`` from the current source and test it with ``twine``.
    Only the package and **not** the code is tested here!

- ``test_code``:
    This session will run all tests with the python version used by the virtualenv from
    where it's invoked. If ``tox`` is used as virtualenv back-end the tests are run with
    all specified (*pyproject.toml*) and available (*locally installed*) python
    versions. Will also save coverage data in ``.coverage_cache``.

    **Addtional arguments**:

    * Any argument understood by ``pytest``. Defaults to ``tests`` (tests directory)

- ``coverage_merge``:
    Merge existing ``.coverage.*`` artifacts into one ``.coverage`` file and create XML
    (*coverage.xml*) and HTML (*/htmlcov*) reports in ``.coverage_cache``.

- ``coverage_report``:
    Report the total coverage and diff coverage against origin/main or DIFF_AGAINST.

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
    * ``SKIP=<hook-id>`` Specify hooks (separated by comma) to skip. Overshadows
      ``HOOKS=<hook-id>``.
    * ``diff``: Print the diff when a hook fails. Recommended to only set when one or
      no hook is specified as the diff will be printed on every failing hook otherwise.
    * Any argument understood by ``pre-commit``.

- ``docs``:
    Build the docs as HTML in *docs/build/html*.

    **Addtional arguments**:

    * ``autobuild`` / ``ab``: Build the docs and open them automatically in your browser
      after starting a development web-server via ``sphinx-autobuild``.
    * Any argument understood by ``sphinx`` or ``sphinx-autobuild``.

- ``"test_docs(builder='html')"``:
    Build the docs with the **html** builder in *docs/build/test/html*
    under nit-picky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.

- ``"test_docs(builder='linkcheck')"``:
    Build the docs with the **linkcheck** builder in *docs/build/test/linkcheck*
    under nit-picky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.

- ``"test_docs(builder='coverage')"``:
    Build the docs with the **coverage** builder in *docs/build/test/coverage*
    under nit-picky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.

- ``"test_docs(builder='doctest')"``:
    Build the docs with the **doctest** builder in *docs/build/test/doctest*
    under nit-picky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.

- ``"test_docs(builder='spelling')"``:
    Build the docs with the **spelling** builder in *docs/build/test/spelling*
    under nit-picky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.

- ``test_docs``:
    Run all ``test_docs`` sessions from above. Same as ``full_test_docs`` but runs in
    the virtualenv where its invoked from.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.


``nox`` dev setup sessions:
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``install_extras``:
    Install all extras (*pyproject.toml*) into the active venv.

- ``setup_pre_commit``:
    Create ``pre_commit`` ``tox`` environment, install *pre-commit* hooks and run the
    prior created environment once with all *pre-commit* hooks.

- ``create_spellignore``:
    Create ``.spellignore`` file at project root if non exists. The content is a copy of
    the ``.gitignore`` file.

- ``dev``:
    Run ``install_extras``, ``setup_pre_commit`` and ``create_spellignore`` ``nox``
    sessions.
