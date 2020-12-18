Add this to ``conf.py``:

.. code-block:: python

    from formelsammlung.envvar import getenv_typed

    #: -- CONFLUENCE BUILDER ---------------------------------------------------------------
    #: needs install: "sphinxcontrib-confluencebuilder"
    if tags.has("builder_confluence"):  # type:ignore[name-defined]
        extensions.remove("sphinx.ext.viewcode")
        extensions.append("sphinxcontrib.confluencebuilder")
    confluence_publish = True
    confluence_server_url = getenv_typed("CONFLUENCE_SERVER_URL")
    confluence_server_user = getenv_typed("CONFLUENCE_SERVER_USER")
    confluence_server_pass = getenv_typed("CONFLUENCE_SERVER_PASS")
    confluence_space_name = "SWFPTOOL"
    confluence_parent_page = "SPHINXTEST"
    confluence_page_hierarchy = True
    confluence_prev_next_buttons_location = "bottom"
    confluence_timeout = 30
    confluence_purge = True


Add this to ``extlinks =`` in ``conf.py``:

.. code-block:: python

    from formelsammlung.envvar import getenv_typed

    extlinks = {
        "jira_issue": (f"{getenv_typed('JIRA_LINK')}%s", ""),
    }


Add this to ``setup()`` in ``conf.py``:

.. code-block:: python

    from typing import Any

    from sphinx.directives.other import SeeAlso

    def setup():
        if not tags.has("builder_confluence"):  # type:ignore[name-defined]

            class _SeeAlso(SeeAlso):
                def run(self) -> Any:
                    self.content[0] = "JIRA issue: " + f":jira_issue:`{self.content[0]}`"
                    return super().run()

            app.add_directive("jira_issue", _SeeAlso)


#####

Add dependency to ``pyproject.toml`` **and to ``docs`` extras! Add also** ``formelsammlung``:

.. code-block:: toml

    [tool.poetry.dependencies]
        sphinxcontrib-confluencebuilder = {version = "^1.2.0", optional = true}
        # sphinxcontrib-confluencebuilder = {git = "https://github.com/sphinx-contrib/confluencebuilder.git", rev = "6e6edbb64260ea09858eb844dd46c79c7697267e", optional = true}


#####

Add test to ``tox.ini``:

.. code-block:: ini

    [testenv:test_docs-{confluence}]
    commands =
        confluence: nox {env:_TOX_FORCE_NOX_COLOR:} --session "test_docs(builder='confluence')" {posargs}


#####


Add this to ``test_docs()`` in ``noxfile.py``:

.. code-block:: python

    def test_docs():
        ...
        add_args = ["-t", "builder_confluence"] if builder == "confluence" else []
        ...
        session.run("sphinx-build", "-b", builder, *color, *std_args, *add_args, *session.posargs)
