# pylint: skip-file
# flake8: noqa
"""Config file for nox."""
import re
import sys

from typing import Any, Callable, Dict, List, Mapping, Optional, Set

import nox
import nox.command

from nox.sessions import Session as _Session


#: -- MONKEYPATCH SESSION --------------------------------------------------------------
class Session(_Session):  # noqa: R0903
    """Subclass of nox's Session class to add `poetry_install` method."""

    def __init__(self, runner: nox.sessions.SessionRunner) -> None:
        """Overwrite method to add passenv attribute."""
        super().__init__(runner)
        self.passenv: List[str] = []

    def setenv(self, env_vars: Dict[str, str]) -> None:
        """Set given envvars and add them to passenv."""
        for envvar in env_vars:
            self.passenv.append(envvar)
            self.env[envvar] = env_vars[envvar]

    def _run(
        self,
        *args: str,
        env: Mapping[str, str] = None,
        **kwargs: Any,
    ) -> Any:
        """Overwrite method to add env filter functionallity.

        Additional kwargs:
        :param filter_env: bool if env should be filtered
        :param passenv: list of envvars to not filter out
        """
        # Legacy support - run a function given.
        if callable(args[0]):
            return self._run_func(args[0], args[1:], kwargs)

        # Combine the env argument with our virtualenv's env vars.
        run_env = self.env.copy()
        if env is not None:
            run_env.update(env)

        # Filter env
        if kwargs.pop("filter_env", False):
            run_env = self._filter_env(run_env, env, kwargs.pop("passenv", None))

        # If --error-on-external-run is specified, error on external programs.
        if self._runner.global_config.error_on_external_run:
            kwargs.setdefault("external", "error")

        # Allow all external programs when running outside a sandbox.
        if not self.virtualenv.is_sandboxed:
            kwargs["external"] = True

        if args[0] in self.virtualenv.allowed_globals:
            kwargs["external"] = True

        # Run a shell command.
        return nox.command.run(args, env=run_env, paths=self.bin_paths, **kwargs)

    def _filter_env(
        self,
        run_env: Dict[str, str],
        env: Optional[Mapping[str, str]] = None,
        kwargs_passenv: Optional[List[str]] = None,
    ) -> Dict[str, str]:
        """Filter given environment.

        :param run_env: Environment to filter
        :param env: Env added for single command; defaults to None
        :param kwargs_passenv: Passenv added for single command; defaults to None
        :return: Filtered environment
        """
        kwargs_passenv_wo_asterisk = set("")
        kwargs_passenv_regex = set("")
        if kwargs_passenv:
            kwargs_passenv_wo_asterisk = {v for v in kwargs_passenv if "*" not in v}
            kwargs_passenv_regex = {v for v in kwargs_passenv if "*" in v}

        self_passenv_wo_asterisk = set("")
        self_passenv_regex = set("")
        if self.passenv:
            self_passenv_wo_asterisk = {v for v in self.passenv if "*" not in v}
            self_passenv_regex = {v for v in self.passenv if "*" in v}

        passenv_regex = re.compile(
            "|".join(
                v.replace("*", ".*")
                for v in (kwargs_passenv_regex | self_passenv_regex)
            )
        )

        return {
            var: run_env[var]
            for var in run_env
            if var
            in self._create_envvar_whitelist(
                set(env or "") | kwargs_passenv_wo_asterisk | self_passenv_wo_asterisk
            )
            or passenv_regex.fullmatch(var)
        }

    @staticmethod
    def _create_envvar_whitelist(whitelist: Optional[Set[str]] = None) -> Set[str]:
        """Merge ENVVAR whitelists.

        Based on ``tox.config.__init__.tox_addoption.passenv()``.
        """
        nox_whitelist = {"_"}

        tox_whitelist = {
            "CURL_CA_BUNDLE",
            "LANG",
            "LANGUAGE",
            "LD_LIBRARY_PATH",
            "PATH",
            "PIP_INDEX_URL",
            "PIP_EXTRA_INDEX_URL",
            "REQUESTS_CA_BUNDLE",
            "SSL_CERT_FILE",
            "HTTP_PROXY",
            "HTTPS_PROXY",
            "NO_PROXY",
        }

        if sys.platform == "win32":
            os_whitelist = {
                "SYSTEMDRIVE",  # needed for pip6
                "SYSTEMROOT",  # needed for python's crypto module
                "PATHEXT",  # needed for discovering executables
                "COMSPEC",  # needed for distutils cygwincompiler
                "TEMP",
                "TMP",
                # for `multiprocessing.cpu_count()` on Windows (prior to Python 3.4).
                "NUMBER_OF_PROCESSORS",
                "PROCESSOR_ARCHITECTURE",  # platform.machine()
                "USERPROFILE",  # needed for `os.path.expanduser()`
                "MSYSTEM",  # fixes tox#429
            }
        else:
            os_whitelist = {"TMPDIR"}

        custom_whitelist = set() if whitelist is None else whitelist

        return nox_whitelist | tox_whitelist | os_whitelist | custom_whitelist

    def poetry_install(
        self,
        extras: Optional[str] = None,
        no_dev: bool = True,
        no_root: bool = False,
        **kwargs: Any,
    ) -> None:
        """Wrap `poetry install` for nox sessions.

        :param extras: string of space separated extras to install
        :param no_dev: if `--no-dev` should be set; defaults to: True
        :param no_root: if `--no-root` should be set; defaults to: False
        """
        #: Safety hurdle copied from nox.sessions.Session.install()
        if not isinstance(
            self._runner.venv,
            (
                nox.sessions.CondaEnv,
                nox.sessions.VirtualEnv,
                nox.sessions.PassthroughEnv,
            ),
        ):
            raise ValueError(
                "A session without a virtualenv can not install dependencies."
            )

        self.install("poetry>=1", env={"PIP_DISABLE_VERSION_CHECK": "1"})

        extra_deps = []
        if extras:
            extra_deps = ["--extras", extras]

        no_dev_flag = []
        if no_dev:
            no_dev_flag = ["--no-dev"]

        no_root_flag = []
        if no_root:
            no_root_flag = ["--no-root"]

        self._run(
            "poetry", "install", *no_root_flag, *no_dev_flag, *extra_deps, **kwargs
        )


def monkeypatch_session(session_func: Callable) -> Callable:
    """Decorate nox session functions to add `poetry_install` method.

    :param session_func: decorated function with commands for nox session
    """

    def switch_session_class(session: Session, **kwargs: Dict[str, Any]) -> None:
        """Call session function with session object overwritten by custom one.

        :param session: nox session object
        :param kwargs: keyword arguments from e.g. parametrize
        """
        session = Session(session._runner)  # noqa: W0212
        session_func(session=session, **kwargs)

    #: Overwrite name and docstring to imitate decorated function for nox
    switch_session_class.__name__ = session_func.__name__
    switch_session_class.__doc__ = session_func.__doc__
    return switch_session_class
