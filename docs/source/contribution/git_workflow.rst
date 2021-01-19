.. spelling::

    Bugfixes
    bugfixes

Git(hub) Workflow
=================

This section will explain the specifics regarding to ``git`` and ``github``.


Development workflow
--------------------

We have no dedicated development branch so all changes are expected to be submitted and
merged into ``main``. Merging into ``main`` is only allowed after all CI tests
**succeeded**. Pull requests must be merged with a merge commit.

Bugfixes are also expected to be merged into ``main``.


Release workflow
----------------

When enough changes and additions or time important fixes have accumulated on the
``main`` branch its time for a new release. The exact time is subject to the
judgment of the maintainer(s).

To trigger a new release you have to manually start the ``Release new version`` workflow
for the ``main`` branch form the ``Actions`` tab of the Github repository. To start the
workflow you must specify the kind of version bump you want to make:




The workflow then will:

1) check if all CI pipelines ran successfully on the latest commit (you can start them
   manually if they did not run)
2) run the full test suit of the previous release
3) check if *BREAKING CHANGES* are declared in the ``CHANGELOG.md``, when the old test
   suit fails
4) bump the version, commit the update, tag the commit and push them
5) build (sdist + wheel) and publish the code on PyPI and Github

    **Note**: As all changes are merged into ``main`` only the current released
    version is supported and will receive bugfixes. Bugfixes for older versions are not
    planned.
