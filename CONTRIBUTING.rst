.. TODO: change CONTRI: no conventional commits needed b/c squash commit ?

================================================
Contribution Guidelines for python_test-cielquan
================================================

At first thanks for taking the time to contribute!

In the following you will find a bunch of guidelines/rules for contributing to
``python_test-cielquan``.
For the guidelines use your best judgement to follow them. Rules only apply to
Pull Requests and must be followed as otherwise the contribution cannot be included.

If you have ideas for improvement of this paper feel free to submit them in an issue or
even a Pull Request.

Table of contents:

- Contribution through `Github issues <https://github.com/cielquan/python_test-cielquan/issues>`__:
    - `Bug reports`_
    - `Suggestion for improvements`_
    - `Documentation changes`_
- Contribution through `Github Pull Requests <https://github.com/cielquan/python_test-cielquan/pulls>`__:
    - `Contribution to the Documentation`_
    - `Contribution to Code`_
    - `Git(hub) Workflow`_


Contribution through `Github issues <https://github.com/cielquan/python_test-cielquan/issues>`__
================================================================================================


Bug reports
-----------

Before submitting your bug report please check the
`Github issue tracker <https://github.com/cielquan/python_test-cielquan/issues>`__
to avoid multiple instances of the same issue.

    **Note:** If you find a *closed* issue covering your topic and you think that the
    issue is not fully solved/covered yet, please open a new issue and reference the
    closed one.


How to submit a bug report
~~~~~~~~~~~~~~~~~~~~~~~~~~

This section will guide you through the process of submitting a bug report, which helps
others to understand your report, reproduce the problem and eventually find related
issues.

Bugs are tracked at the aforementioned
`Github issue tracker <https://github.com/cielquan/python_test-cielquan/issues>`__
where you can create a new issue and choose the ``Bug Report`` option. Through the
option your issue's body is automatically filled with the
`Bug Report template <https://github.com/Cielquan/python_test-cielquan/blob/master/.github/ISSUE_TEMPLATE/.bug-report.md>`__.
By filling this template you make it easier for others to understand and help with or
fix the problem.

Explain your topic as detailed as possible to help others reproduce the problem:

- The more details the better.
- Use a clear, concise and descriptive title.
- Describe the exact steps to take to reproduce the problem.
- Describe the behavior you observed following the steps above.
- Describe the behavior you expected instead while following the steps above.

If:

- you have specific examples to reproduce the problem like config/code snippets, files
  or links to a Github project

- the problem is an error which unexpectedly occurs and you ran the command again with
  the ``--debug`` option to get a more information

please include them or make a `Gist <https://gist.github.com/>`__ and include its link.

You can also provide more context by asking yourself these questions:

- Did the problem just start happening recently after an update or something?
- If so can you reproduce the problem with older versions?
- Does the problem occur with older or new python versions also?
- Does the problem occur every time and is reliably reproducible?
- If not how often does it occur? Please provide as many details as possible.

The template also asks for some info about your environment:

- What **version** of ``python_test-cielquan`` do you use?
- Which **OS** are you using and which **version**?
- Which **python version** are you using?


Suggestion for improvements
---------------------------

Before submitting your feature request please check the
`Github issue tracker <https://github.com/cielquan/python_test-cielquan/issues>`__
to avoid multiple instances of the same issue.

    **Note:** If you find a *closed* issue covering your topic and you think that the
    issue is not fully solved/covered yet, please open a new issue and reference the
    closed one.


How to submit a feature request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section will guide you through the process of submitting an feature request
which helps others to understand your suggestion and eventually find related issues.
You can suggest enhancements to existing functionality or completely new features.
Your ideas are welcome.

Feature requests are tracked at the aforementioned
`Github issue tracker <https://github.com/cielquan/python_test-cielquan/issues>`__
where you can create a new issue and choose the ``Feature Request`` option. Through the
option your issue's body is automatically filled with the
`Feature Request template <https://github.com/Cielquan/python_test-cielquan/blob/master/.github/ISSUE_TEMPLATE/.feature-request.md>`__.
By filling this template you make it easier for others to understand your suggestions.

Explain your topic as detailed as possible to help others understand your ideas:

- The more details the better.
- Use a clear, concise and descriptive title.
- What behavior do you want to be changed?
- How is the behavior currently?
- How do you want it do be changed and why?
- What new feature to do want to be added and why?
- How should it work and why should it work this way?

Maybe you have an idea how your request can be implemented. If so please describe it as
detailed as possible. Maybe even with code snippets. You can include them directly or
make a `Gist <https://gist.github.com/>`__ and include its link.


Documentation changes
---------------------

If you have errors or enhancement ideas for the documentation please follow the steps
above accordingly but use the ``Documentation`` issue option to get the
`Documentation template <https://github.com/Cielquan/python_test-cielquan/blob/master/.github/ISSUE_TEMPLATE/.documentation.md>`__.


Contribution through `Github Pull Requests <https://github.com/cielquan/python_test-cielquan/pulls>`__
======================================================================================================


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
you have all development dependencies installed. At last it will create a ``tox``
environment for ``pre-commit``, install ``pre-commit`` as ``git`` hook and run all
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
    for the creation of isolated test virtualenvs and running tests inside via ``nox``
- `pre-commit <https://pre-commit.com/>`__:
    for automated linting and quality checking before commiting


Testing
~~~~~~~

To test the code you can run::

    $ nox -s tox_lint

    $ nox -s tox_code

    $ nox -s tox_docs

to lint, test the code or test the docs respectively.

For more specific testing we have several different ``tox``/``nox``
environment/sessions available. You can invoke them with ``tox -e <environment>`` or
``nox -s <session>``. Some take additional arguments which need to be added at the end
after a double dash and separated by a space like so: ``nox -s session -- arg1 arg2``.
All ``nox`` sessions skip the install steps when invoked by ``tox`` as ``tox`` manages
the dependencies itself.

``tox`` / ``nox``:

- ``safety`` / ``safety``:
    Run ``safety`` over all specified dependencies to check for dependency versions that
    are known to be vulnerable.

- ``pre_commit`` / ``pre_commit``:
    Run ``pre-commit`` over all project files to lint, format and check them.

    **Addtional arguments**:

    * ``<hook-id>``: Specify a hook to run. Can be specified multiple times.
    * ``SKIP=<hook-id>`` Specify hooks (seperated by comma) to skip.
    * ``diff``: Print the diff when a hook fails. Recommended to only set when one or
      no hook is specified as the diff will be printed on every failing hook otherwise.

- ``package`` / ``package``:
    Build a package with ``poetry`` from the current source and test it with ``twine``.

- ``py<PYTHON-VERSION>`` / ``test_code``:
    *PYTHON-VERSION* can by either e.g. *py3* for *pypy3* or e.g. *310* for *python3.10*.
    The ``nox`` session ``test_code`` will run the tests with the python version used by
    the virtualenv from where its invoked.

    **Addtional arguments**:

    * Any argument understood by ``pytest``. Defaults to ``tests`` (for the tests
      directory)

- ``coverage-merge`` / ``coverage -- merge``:
    Merge existing ``.coverage.*`` artifacts into one ``.coverage`` file and create XML
    (*coverage.xml*) and HTML (*/htmlcov*) reports.

- ``coverage-report`` / ``coverage -- report``:
    Report the total coverage and diff coverage against origin/master.

- ``coverage-all`` / ``coverage``:
    Merge and report the coverage. (runs both coverage sessions above)

- ``docs`` / ``docs``:
    Build the docs as HTML in */docs/build/html*.

    **Addtional arguments**:

    * ``autobuild`` / ``ab``: Build the docs and open them automatically in your browser
      after starting a development webserver via ``sphinx-autobuild``.
    * Any argument understood by ``sphinx`` or ``sphinx-autobuild``.

- ``test_docs-html`` / ``"test_docs(builder='html')"``:
    Build the docs with the **html** builder in */docs/build/test/html*
    under nitpicky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.

- ``test_docs-linkcheck`` / ``"test_docs(builder='linkcheck')"``:
    Build the docs with the **linkcheck** builder in */docs/build/test/linkcheck*
    under nitpicky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.

- ``test_docs-coverage`` / ``"test_docs(builder='coverage')"``:
    Build the docs with the **coverage** builder in */docs/build/test/coverage*
    under nitpicky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.

- ``test_docs-doctest`` / ``"test_docs(builder='doctest')"``:
    Build the docs with the **doctest** builder in */docs/build/test/doctest*
    under nitpicky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.

- ``test_docs-spelling`` / ``"test_docs(builder='spelling')"``:
    Build the docs with the **spelling** builder in */docs/build/test/spelling*
    under nitpicky test conditions.

    **Addtional arguments**:

    * Any argument understood by ``sphinx``.


Git(hub) Workflow
-----------------

This section will explain the specifics regarding to ``git`` and ``github``.


Commit messages
~~~~~~~~~~~~~~~

We use `Conventional Commits <https://www.conventionalcommits.org/en/v1.0.0/>`__ as
standard for our commit messages. With this standard commit messages are human **and**
machine readable so that the changelog creation and versioning can be automated based
on keywords. Commit messages will be checked in the CI pipeline.

If you set up ``pre-commit`` as described above you already have the ``commit-msg``
hook installed which will check your commit message for compliance.

For small changes (like fixing a typo) with one commit and for larger changes (like
feature additions) with multiple commits alike we will ask you fix you commit messages
if they are not compliant. So we highly recommend you to set ``pre-commit`` up as it is
very easy.


Development
~~~~~~~~~~~

The ``master`` branch is the development branch and so all changes are expected to be
submitted and merged there. Merging into ``master`` is only allowed after all CI tests
succeeded. Pull requests must be merged with a merge commit.

Bugfixes are also expected to be merged into ``master``. Buf if they are
critical the next release will be much sooner.

    **Note**: As all changes are merged into ``master`` only the current released
    version is supported and will receive bugfixes. Bugfixes for older versions are not
    planned.


Releases
~~~~~~~~

When enough changes and additions or time important fixes have accumulated on the
``master`` branch its time for a new release. The exact time is subject to the
judgement of the maintainer(s).

To trigger a new release you have to manually start the ``Release new version`` workflow
for the ``master`` branch form the ``Actions`` tab of the Github repository. The
workflow will run the full test suit and after success automatically bump the version
counter based on semantic versioning and conventional commits, update the changelog,
create a new git tag, build the package/wheel and push it to PyPI.
