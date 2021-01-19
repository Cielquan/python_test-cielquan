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

#. Add PyPI token as PYPI_TOKEN secret var

#. Add protection rule for ``master``
    - Require checks
    - Require up to date branch
    - Include admins
    - No force push
    - No deletion


Code base
=========

#. Update docs:
    - installation.rst: rm pypi if not there

#. Update pyproject.toml
    - pytest.ini_options: rm mock_use_standalone_module if not needed
    - coverage config: [plugins and plugin-conf]
    - coverage-conditional-plugin rm if not used

#. Create LICENSE and update license in files if no default one
