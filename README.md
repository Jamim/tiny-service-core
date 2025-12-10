# 🪐 Tiny Service Core

[![CI][ci-badge]][ci]
[![Coverage][cov-badge]][cov]
[![License][license-badge]][license]
[![Version][ver-badge]][pypi]
[![Python][py-badge]][pypi]

This library implements common functions that allows
you to build tiny microservices with less boilerplate.

[ci-badge]: https://img.shields.io/github/actions/workflow/status/Jamim/tiny-service-core/ci.yml.svg
[ci]: https://github.com/Jamim/tiny-service-core/actions/workflows/ci.yml
[cov-badge]: https://codecov.io/github/Jamim/tiny-service-core/graph/badge.svg
[cov]: https://app.codecov.io/github/Jamim/tiny-service-core
[license-badge]: https://img.shields.io/github/license/Jamim/tiny-service-core
[ver-badge]: https://img.shields.io/pypi/v/tiny-service-core
[pypi]: https://pypi.org/project/tiny-service-core/
[py-badge]: https://img.shields.io/pypi/pyversions/tiny-service-core
[license]: https://github.com/Jamim/tiny-service-core/blob/main/LICENSE

## Installation

Install with `pip`, including optional dependencies:

```shell
pip install tiny-service-core[cache,db,http-client]
```

Clearly, you can use any other Python package manager instead.  
I personally prefer using [uv][uv] nowadays.

```shell
uv add tiny-service-core --extra cache --extra db --extra http-client
```

[uv]: https://docs.astral.sh/uv/

## Dependencies

Tiny Service Core is highly opinionated.  
Current version glues together these components:
  - [FastAPI][fastapi]
  - [pydantic-settings][pydantic-settings]
  - [Sentry][sentry]
  - with `cache` [extra][installing-extras]
    * [Redis][redis]
  - `db`
    * [SQLModel][sqlmodel]
    * [asyncpg][asyncpg]
    * [Alembic][alembic]
  - `http-client`
    * [HTTPX][httpx]

[fastapi]: https://fastapi.tiangolo.com
[pydantic-settings]: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
[sentry]: https://docs.sentry.io/platforms/python/
[redis]: https://github.com/redis/redis-py
[sqlmodel]: https://sqlmodel.tiangolo.com
[asyncpg]: https://github.com/MagicStack/asyncpg
[alembic]: https://alembic.sqlalchemy.org
[httpx]: https://www.python-httpx.org

[installing-extras]: https://packaging.python.org/en/latest/tutorials/installing-packages/#installing-extras
