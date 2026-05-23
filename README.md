### Hexlet tests and linter status:

[![Actions Status](https://github.com/Irina-Grebennikova/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Irina-Grebennikova/python-project-83/actions)

<hr>

[![CI](https://github.com/Irina-Grebennikova/python-project-83/actions/workflows/ci.yml/badge.svg)](https://github.com/Irina-Grebennikova/python-project-83/actions/workflows/ci.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Irina-Grebennikova_python-project-83&metric=alert_status&token=8702750feb174092b2ebb7d7dd3ddbfb1c04b9b6)](https://sonarcloud.io/summary/new_code?id=Irina-Grebennikova_python-project-83)

### About

Page Analyzer is a Flask-based web application that helps inspect websites and track important SEO metrics.

### Links

**App link**: https://page-analyzer-seven.vercel.app

#### Tooling

| Tool                                 | Description                                                           |
| ------------------------------------ | --------------------------------------------------------------------- |
| [uv](https://docs.astral.sh/uv/)     | An extremely fast Python package and project manager, written in Rust |
| [ruff](https://docs.astral.sh/ruff/) | An extremely fast Python linter and code formatter, written in Rust   |

#### Runtime

| Tool                                        | Description                                |
| ------------------------------------------- | ------------------------------------------ |
| [Flask](https://flask.palletsprojects.com/) | Lightweight WSGI web application framework |
| [Gunicorn](https://gunicorn.org/)           | Python WSGI HTTP server                    |
| [PostgreSQL](https://www.postgresql.org/)   | Relational database                        |

---

## Requirements

- Python 3.11+
- uv
- PostgreSQL

### Installation

```bash
make install
```

### Environment variables

Create `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/page_analyzer
SECRET_KEY=your_secret_key
```

### Database setup

Create PostgreSQL database:

```bash
createdb page_analyzer
```

Apply database schema:

```bash
psql -d page_analyzer -f database.sql
```

### Run locally

```bash
make dev
```
