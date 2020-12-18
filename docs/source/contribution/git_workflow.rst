Git(hub) Workflow
=================

This section will explain the specifics regarding to ``git`` and ``github``.


Commit message rules
--------------------

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
--------------------

We have no dedicated development branch so all changes are expected to be submitted and
merged into ``master``. Merging into ``master`` is only allowed after all CI tests
**succeeded**. Pull requests must be merged with a merge commit.

Bugfixes are also expected to be merged into ``master``. Buf if they are
critical the next release will be much sooner.

If the pull request has many small commits the maintainer may use a *squash merge* to
keep the changelog cleaner. Of cause the squash commit-message must follow the
aforementioned commit message rules!


Release workflow
----------------

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
