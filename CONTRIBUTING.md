# Contributing

Harper uses Python 3.9 and JavaScript ES8.

## Server

The server is built with:

-   [SQLAlchemy][sqlalchemy] for persistence
-   [FastAPI][fastapi] to implement a REST API

We also use:

-   [Black][black], [Flake8][flake8], [isort][isort], and [pycodestyle][pycodestyle]
    to check our Python
-   [pytest][pytest] to test the server

## Interface

The interface is built with:

-   [React][react] for web pages

We also use:

-   [Cypress][cypress] to test the interface

## Support

We use:

-   [GNU Make][make] as a general-purpose task runner
-   [MkDocs][mkdocs] for documentation

[black]: https://black.readthedocs.io/
[cypress]: https://www.cypress.io/
[fastapi]: https://fastapi.tiangolo.com/
[flake8]: https://flake8.pycqa.org/
[isort]: https://pycqa.github.io/
[make]: https://www.gnu.org/software/make/
[mkdocs]: https://www.mkdocs.org/
[pycodestyle]: https://pycodestyle.pycqa.org/
[pytest]: https://docs.pytest.org/
[react]: https://reactjs.org/
[sqlalchemy]: https://www.sqlalchemy.org/
