====================================
Things to do after using as template
====================================


Github repo
===========

#. Add description

#. Add issue labels:
    - bug
    - documentation
    - feature
    - triage
    - security
    - pinned
    - stale

#. Activate stale bot

#. Activate dependabot

#. Activate RTD

#. Activate code-climate
    - Add CC_TEST_REPORTER_ID secret var

#. Add PyPI credentials as secret var

#. Add protection rule for ``master``
    - Require checks
    - Require up to date branch
    - Require signed commits ??
    - No force push
    - No deletion

#. Add branch ``release-DO-NOT-PUSH-HERE`` and protection rules
    - Require checks
    - Require up to date branch
    - Require signed commits
    - Require linear history
    - Include admins
    - No force push
    - No deletion


Code base
=========

#. Update issue templates with repo name and links

#. Update workflow

#. Update pyproject.toml
    - metadata (desc: same as repo (see above))
    - deps
    - coverage config: [plugins and plugin-conf, combine paths]

#. Update tox.ini
    - Repo name
    - Build setting
    - Remove confluence builder?

#. Update docs
    - conf
    - source

#. Update LICENSE

#. Update README
