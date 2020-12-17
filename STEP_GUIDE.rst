====================================
Things to do after using as template
====================================


Github repo
===========

#. Add description

#. Add issue labels:
    - Bug
    - Documentation
    - Feature
    - Triage
    - Security
    - Pinned
    - Stale
    - Good First Issue

#. Activate stale bot

#. Activate dependabot

#. Activate RTD

#. Activate code-climate
    - Add CC_TEST_REPORTER_ID secret var

#. Add PyPI credentials as secret var

#. Add protection rule for ``master``
    - Require checks
    - Require up to date branch
    - Include admins
    - No force push
    - No deletion


Code base
=========

#. Update .github/ISSUE_TEMPLATES/*
    - Repo name
    - links
    - if not cli remove part from bug report
    - CHANGE ME in publish.yml

#. Update docs:
    - badges.rst
    - index.rst: rm badges from toxtree
    - installation.rst: links && rm pypi if not there
    - usage.rst

#. Update src
    - init: docstr

#. Update tests
    - conftest: docstr

#. Update pyproject.toml
    - _testing: config
    - _metadata: first_release_year
    - poetry:
        * metadata (desc: same as repo (see above))
        * deps / extras
    - pytest.ini_options: rm mock_use_standalone_module if not needed
    - coverage config: [plugins and plugin-conf, combine paths]
    - coverage-conditional-plugin rm if not used

#. Create/Update LICENSE.txt

#. Create/Update README.rst

#. Update CONTRIBUTION.rst:
    - Change links
    - If not CLI remove this part
