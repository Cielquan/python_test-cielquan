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

- ``patch``/``bugfix``: for changes that **do not** add new functionallity and are backwards compatible
- ``minor``/``feature``: for changes that **do** add new functionallity and are backwards compatible
- ``major``/``breaking``: for changes that are **not** backwards compatible

The workflow then will:

#) check if all CI pipelines ran successfully on the latest commit (you can start them
   manually if they did not run)
#) run the full test suit of the previous release
#) check if *BREAKING CHANGES* are declared in the ``CHANGELOG.md``, when the old test
   suit fails
#) bump the version, commit the update, tag the commit and push them
#) build (sdist + wheel) and publish the code on PyPI and Github

    **Note**: As all changes are merged into ``main`` only the current released
    version is supported and will receive bugfixes. Bugfixes for older versions are not
    planned.
