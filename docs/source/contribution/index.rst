Contribution guidelines
=======================

+-------------------+---------------------------------------------------------------------------------------------+
| **Dev tools**     | |pre-commit| |black| |isort| |mypy|                                                         |
|                   +---------------------------------------------------------------------------------------------+
|                   | |bandit| |flake8| |pylint| |pyenchant|                                                      |
|                   +---------------------------------------------------------------------------------------------+
|                   | |nox| |tox| |pytest| |sphinx|                                                               |
|                   +---------------------------------------------------------------------------------------------+
|                   | |conventional_commits| |poetry|                                                             |
+-------------------+---------------------------------------------------------------------------------------------+


.. Dev tools

.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=flat-square&logo=pre-commit&logoColor=yellow
    :target: https://pre-commit.com
    :alt: pre-commit - enabled

.. |black| image:: https://img.shields.io/badge/Code%20Style-black-000000.svg?style=flat-square
    :target: https://black.readthedocs.io
    :alt: Code Style - black

.. |isort| image:: https://img.shields.io/badge/Imports-isort-%231674b1?style=flat-square&labelColor=ef8336&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAZCAMAAADzN3VRAAAAsVBMVEUVdbQWdLEXdLAXdLEYdLAYdLEada4bdLEcdLEddK8ddaweeaAfdqkfeaAgdqknda8pdK8rdawuda8veJ8yeJ48dqc/da1FdqdRd6BYd59adqRleZRxeJ15ttaIe4OPvNqYe3+lfXCmfnC2fmfDgj/DgkDIf17LgkbRgkPTgkbU8/jXgkPZgF3fgU3fgkPigFfkgznl+fzqgk/rgzrsgzztgjjtgzbtgzjugzbvgzb///+RcCogAAAAxklEQVQoz3WSBQ7DMAxF420dMzMz8+re/2ALOm22fqmR/Z+cNHYYxImZIDVHrnvXJXkkrSPkgGGFyBujyhmyRVeaNMnwTdBTRGc1ubsfqinTBkEgnPaDx31BVhLUuXcL6DIoiD1zNBHrgH8LSz7C28uaAuITMWvIyxImjeqfmpI0MpFzFNnonMESseJ5liCRIo71r0pyleCoeuDBmSctsBWoutOgnPp2ovnE9Bpg6ICknekubqYAaetP3beTmAn70vl9VT/6AiI3Qb9AnYdrAAAAAElFTkSuQmCC
    :target: https://pycqa.github.io/isort
    :alt: Imports - isort

.. |mypy| image:: https://img.shields.io/badge/-checked-blue?style=flat-square&labelColor=white&logoWidth=70&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHcAAAAYCAMAAAD3RZI3AAABJlBMVEUAAAAAAP8A//8AgIBVVVVAgL8zZswqgKpVVVUkbbZVVVVNTU0udLkqaqorcaokbaoqarUpcK0xbLEsarBPT08ubLIoa7Unb7FOTk4mbLMrbbArbbYsb7EqarUpb7EqbrMtbbRPT08rbLApbrAoa7Iob7IqbrIrbrEobbIqbrNPT08pbbFRUVFPT08qa7EpbLErbbIqbrEqbbIrbLEqbLEqbLFRUVEqbLErb7IrbrEqbrMrbbIrbrJPT08qbLIqbrIqbbIrbbIrbrMqbbIqbbJRUVErbrIqbbIrbbIqbbIpbrJQUFAqbbIqbbIqbrMqbbIqbbIrbbIrbbIqbbIqbbEqbbIqbbIqbLIqbbIqbrIrbbJQUFAqbbJQUFAqbbNQUFAqbbJQUFBpO8x3AAAAYHRSTlMAAQECAwQFBgYHCQoLDBIVGBkaHR0hJicnKCoqLjA+Q0RER0pMTE9YWWFkaW5xcnZ3eXp9f4CBhoiJjY+Vl5men6iur7e3ub2/wNjb4OLm5+np7/Lz8/X3+Pn8/P39/v4p8tJ3AAAByUlEQVRIx72WZ3+DIBDGSWdau3dr99473TPdO90rbR++/5eoIioompDkl+cFB+eFP/E4hBCuVzDtkbKqCZ6Kmoda2s8jhvK+hasoBZhSw0jmiDEMQ+R2lYarFwaU5kXrctuZcnBNk5AM0Gb3M8hW27bXbBae+hPao0d8spha9shWt9nic1chq95Pu7x8IM1Xds3ME8+QlyrpBZ77/0KO4WGAgkvVXKwwM4UJbxJ3qi+sBRJ3b5kPPFjtHbaZs1Pgtqq5N0rulm2mgVHbpvFstf18LseIXMEtDZywEBY9YoHJXJV12j78BrgstaQB42yUyMl16jp/7i1mfJ9YmLyT9YYvOIjk7pAqTa5jorkIxojcMTJPZelx37Eey73CImlUcAmlBXMTVmrFAglwj9yxcDK43OWfIriWrVNwT5l982Nl7qDNHQhhN5R1pLaXEDeqVEc1wvvGiXROqrlEg0vUXOBYOHWlA5iFKbhnRJO7GeYS+bDfDXG9bzHtYNL/CkkbNejyHJWR3MgdFa8hkcvvGwqu6r7hMhdIAVxpo0ZwgeE4bpL8aXIPrSRexK6F77KYyxbTiB53MjWncqdS0mgpEfX7WYf6XaYL7D/7oSPH9BHEpQAAAABJRU5ErkJggg==
    :target: http://www.mypy-lang.org
    :alt: mypy - checked

.. |bandit| image:: https://img.shields.io/badge/Security-bandit-yellow.svg?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAAUCAMAAAC3SZ14AAAAilBMVEUAAAAYGBgXFxf50DX72mD51E361kz50DT50jn72mHcvEz711UXFxd/fHyKeEXcukXcukfcu0ncvE3dvlTev1rjwUjjw0jlxVj50Db50Tn50Tv50j/500H600T61Ef61Ej61Er61k361lD711P711X72Fn72Fv72Vz72V772mH72mP822b822f///+Yj+WZAAAADHRSTlMAKu/39/v8/f39/v731TR1AAAAnklEQVQY013QSQKCMBBE0XbE4SviyChIjCKQ+1/PRUADtXyb6mqRLgCIE2ib+uOaleqt/0bbADu9VQzEGKPKHzW1JR70TfUawEABWJtXGAMUub1kouClAcgzS3CGvSqvRQ4+UxERbvoEAAc/7ip5qnJx3ARpEvcDgGVxz9LEmQlAmsRR6NJlKCIEVtz3kMRR6I0etgpnAxEBbyQi0ssXVHoQyCIgOjIAAAAASUVORK5CYII=
    :target: https://bandit.readthedocs.io
    :alt: Security - bandit

.. |flake8| image:: https://img.shields.io/badge/Linting-flake8-blue.svg?style=flat-square
    :target: https://flake8.pycqa.org
    :alt: Linting - flake8

.. |pylint| image:: https://img.shields.io/badge/Linting-pylint-blue.svg?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAXCAYAAADpwXTaAAADAklEQVQ4T42USWgUQRSG/4pgZPAST4o3EUSNghcPylzUiAvBkwsIirtBjBIHlLgwuIREJhjbDfHkRVAvyihBYpJDEpfBQIKjIARUJKCiUYlGp6vee1LV3TOTYQLTl6K76n38739/tcIUz/pUjydGg4lhjIaIXQlijPS3bj1SrkyV+7gx1eORrweJaZ4Q15AYsCEYMhAmsDF40b6jsbS2LGx9a5fXeaLOHV6VfOARC1j7cKsxYCJkOnZWBlvX0ukZEnCoxIQAsqsEyl55eyqDlcqPJ+4sJeG9JgQJEQav7S8Pq2/vvWQ0TxMOWjBsYAucInGmwxCDWUMMwxBh6Prno/gy3gERAD7UnKuNKplMVr2MxTtsgS20AAknyMKQ0HjmCEpOuIN9/tkB1gD7QEwuqg1tTy8zkZoEshMr8cupsyqYA9ip7F2AtsJopwyioda1PvFKsxSBrNF2EGJ8sAg4BA3fONgon/Z5YHIQp4w11NoLnZ7N0KQskehnF7cdK5dBGW3YBaOXBWrIQWB8ABpqzblHnlUSZMgHkWCgKfMGohbnYa49W5ADTLGaECZWWQ5qdTKdYjbToyxB9LX+pqFDBZAtyAUKLDBS41qz4HCPfHI3IN5837ORsCbrv7olcybbHI08aEMXvAGF74FPtj0YA7VkoNHB6pPp2Pc/v1ptluQftWRODzfnldgCZ3Jk9GTTw+mm1ZKBrrJ3U0YbvOKRF9SFrVmzF/ZWdp3k426veOQOVhQBq8a2VdFfQz5s94pHHrUZqZHXK73KYe83z4b2mxGOPPArSL57RN1WS/sHK1KWr3mzaDq4JpUvGufjasXzv1P9ncsOAMB8ACNRkQK6BVhdBJm0X3QOGGrD2LdxYM15zLIb2RS6l5/E24kcDgOYkU3hcW0CGwH8i1XjSuYCFtUm8vC5AL7awDll2RTG7FqbcLCZ2RQe9r0DN9xCXU0MN/vOYn78DEZ+TODAjX3oii9AVW0CmwD8Lm65bJuxatRP5JCODp7bgu7T9wptlu5H5/4D001rKLIpQrgAAAAASUVORK5CYII=
    :target: https://pylint.pycqa.org
    :alt: Linting - pylint

.. |pyenchant| image:: https://img.shields.io/badge/Spelling-pyenchant-blue.svg?style=flat-square
    :target: https://pyenchant.github.io/pyenchant
    :alt: Spelling - pyenchant

.. |nox| image:: https://img.shields.io/badge/Test%20automation-nox-brightgreen.svg?style=flat-square
    :target: https://nox.thea.codes
    :alt: nox

.. |tox| image:: https://img.shields.io/badge/Venv%20backend-tox-brightgreen.svg?style=flat-square
    :target: https://tox.readthedocs.io
    :alt: tox

.. |pytest| image:: https://img.shields.io/badge/Test%20framework-pytest-brightgreen.svg?style=flat-square
    :target: https://docs.pytest.org
    :alt: Pytest

.. |sphinx| image:: https://img.shields.io/badge/Doc%20builder-sphinx-brightgreen.svg?style=flat-square
    :target: https://www.sphinx-doc.org/
    :alt: Sphinx

.. |conventional_commits| image:: https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square
    :target: https://conventionalcommits.org
    :alt: Conventional Commits - 1.0.0

.. |poetry| image:: https://img.shields.io/badge/Packaging-poetry-brightgreen.svg?style=flat-square
    :target: https://python-poetry.org/
    :alt: Poetry
