================================================
Contribution Guidelines for python_test-cielquan
================================================

At first thanks for taking the time to contribute!

In the following you will find a bunch of guidelines/rules for contributing to
python_test-cielquan.
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
    issue is not fully solved yet, please open a new issue and reference the closed one.


How to submit a bug report
~~~~~~~~~~~~~~~~~~~~~~~~~~

This section will guide you through the process of submitting a bug report which helps
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

If you have specific examples to reproduce the problem like config/code snippets, files
or links to a Github project.

If the problem is an error which unexpectedly occurs please run the command again with
the ``--debug`` option to get a more information.

Please include them or make a `Gist <https://gist.github.com/>`__ and include its link.

You can also provide more context by asking yourself these questions:

- Did the problem just start happening recently after an update or something?
- If so can you reproduce the problem with older versions?
- Does the problem occur with older or new python versions also?
- Does the problem occur every time and is reliably reproducible?
- If not how often does it occur? Please provide as many details as possible.

The template also asks for some info about your environment:

- What **version** of python_test-cielquan do you use?
- Which **OS** are you using and which **version**?
- Which **python version** are you using?


Suggestion for improvements
---------------------------

Before submitting your Feature request please check the
`Github issue tracker <https://github.com/cielquan/python_test-cielquan/issues>`__
to avoid multiple instances of the same issue.

    **Note:** If you find a *closed* issue covering your topic and you think that the
    issue is not fully solved yet, please open a new issue and reference the closed one.


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
python_test-cielquan. You can look in the
`Github issue tracker <https://github.com/cielquan/python_test-cielquan/issues>`__
for issues with the ``Documentation`` label and try to solve them.

For creating your local development environment please see: `Setup Local Development Environment`_


Contribution to Code
--------------------

Contribution to Code is a bit more complex as some standards has been set and you must
follow these rules to get your contribution accepted. But this sounds scarier than it
is.


First you need an issue to work on. Just pick an issue from the
`Github issue tracker <https://github.com/cielquan/python_test-cielquan/issues>`__
and get started.

    **Note:** If you find are a first time contributor issues with the
    ``First Good Issue`` label are good ones to get started with.


Setup Local Development Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section will explain how to setup an local development environment with the
tools used for python_test-cielquan. We use:

- `tox <https://tox.readthedocs.io/>`__ for automated creation of virtual environments (venv) and testing
- `poetry <https://python-poetry.org/docs/>`__ for dependency management and package building
- `pre-commit <https://pre-commit.com/>`__ for automated linting and checking before commiting (managed via ``tox``)

The ``dev`` venv is created via ``tox`` and has 2 different versions: with and without
``tox`` + ``poetry`` installed.

If you have **both** tools globally installed and available you can use the ``dev``
environment. If you miss either of them you can either install the missing one on your
system or use the ``devfull`` environment instead. ``devfull`` has both tools installed.

At first you need to clone the repository and have a command prompt ready from within
the local copy of the repository.

If you are missing ``tox`` you need to take the following 3 extra steps to create the
``devfull`` ``tox`` environment from which you then can call/run the other ``tox``
environments:

#. Create a virtual environment (venv) and activate it::

    Unix (bash): $ python3 -m venv .venv && source .venv/bin/activate
    Windows (cmd): > python -m venv .venv && .venv\Scripts\activate

#. Install tox into the venv::

    All: $ python -m venv pip install tox

*If you use ``devfull`` exchange it for ``dev`` in the following examples*.
To create the ``dev`` or ``devfull`` venv just call::

    All: $ tox -e dev

After successful creation, activate it::

    Unix (bash): $ source .tox/dev/bin/activate
    Windows (cmd): > .tox\dev\Scripts\activate

Now you have your development environment active and ready.

We recommend that also setup ``pre-commit`` - which is only two more commands - to ensure
that your commits are okay and the CI pipeline does not complain about linting issues.

You just need to invoke the ``pre-commit`` ``tox`` environment::

    All: $ tox -e pre-commit

and then install the `pre-commit` and `commit-msg` git hooks::

    All: $ pre-commit install -t pre-commit -t commit-msg

Now you are set up and ready to go. If you have questions regarding the aforementioned
tools please see their respective documentation which are linked at this sections
beginning.


Testing
~~~~~~~

We have several different ``tox`` environments configured for all sorts of tests which
you can invoke via ``tox -e <ENVIRONMENT_NAME>``.

The main testing environments are:

- ``code-test``: Run ``pytest`` with available configured python versions and report coverage
- ``docs-test``: Test the current docs

Also available are:

- ``package``: Test if the current package fails to build
- ``docs``: Build the current docs (for reading purpose)
- ``safety``: Lookup all dependencies in vulnerability database
- ``pre-commit``: Run all `pre-commit` hooks over all files

You should run the test environments prior commiting/pushing as those tests are run in
the CI pipeline anyways and will block merging your Pull request in case of failure.


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


Releases
~~~~~~~~

When enough changes and additions or time important fixes have accumulated on the
``master`` branch its time for a new release. The exact time is subject to the
judgement of the maintainer(s).

To trigger a new **major** or **minor** release you have to manually start the
``Release new version`` workflow for the ``master`` branch form the ``Actions`` tab of
the Github repository. The workflow will run the full test suit and after success
automatically bump the version counter based on semantic versioning and conventional
commits, update the changelog, create a new git tag, build the package/wheel and push it
to PyPI. The workflow will also create a branch called ``release/<major>.<minor>``.

To trigger a new **patch** release you have to manually start the
``Release new version`` workflow for the corresponding ``release/<major>.<minor>``
branch form the ``Actions`` tab of the Github repository. The workflow will like above
run the test suit and create a new release. It will also update the changelog on the
``master`` branch to include the **patch** release.
