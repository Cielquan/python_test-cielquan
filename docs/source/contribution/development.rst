Development
===========


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


Commit message rules
~~~~~~~~~~~~~~~~~~~~

We use `Conventional Commits <https://www.conventionalcommits.org/en/v1.0.0/>`__ as
standard for our commit messages. With this standard commit messages are human **and**
machine readable so that the changelog creation and versioning can be automated based
on keywords. Commit messages will be checked in the CI pipeline.

If you submit noncompliant commit messages we will need to ask you to fix them. So we
highly recommend you to set ``pre-commit`` up.

If you set up ``pre-commit`` as described above you already have the ``commit-msg`` hook
installed which will check your commit message for compliance else you can run::

    $ nox -s setup_pre_commit


Development workflow
~~~~~~~~~~~~~~~~~~~~

We have no dedicated development branch so all changes are expected to be submitted and
merged into ``master``. Merging into ``master`` is only allowed after all CI tests
**succeeded**. Pull requests must be merged with a merge commit.

Bugfixes are also expected to be merged into ``master``. Buf if they are
critical the next release will be much sooner.

If the pull request has many small commits the maintainer may use a *squash merge* to
keep the changelog cleaner. Of cause the squash commit-message must follow the
aforementioned commit message rules!


Release workflow
~~~~~~~~~~~~~~~~

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
