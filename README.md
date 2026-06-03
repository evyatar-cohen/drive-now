# DriveNow

A car rental management REST API built with FastAPI and SQLAlchemy.

## Architecture

The codebase is organized into distinct layers. Each layer has a single responsibility and communicates only with the layer directly below it.

```
HTTP Request
     │
     ▼
┌─────────────┐
│  API Layer  │  api/routes/
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Service Layer  │  services/
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│  Repository Layer    │  repositories/
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      Database        │
└──────────────────────┘
```

### Layers

**API** (`api/routes/`)
Receives HTTP requests, validates input via Pydantic schemas, delegates to the service layer. No business logic, no DB access.

**Service** (`services/`)
Contains all business logic. Validates rules, handles status transitions, orchestrates operations. Talks only to the repository interface, never to the DB directly.

**Repository** (`repositories/`)
The only layer that touches the DB. Abstracts all data access behind a clean interface. The service doesn't know or care if it's SQLite, PostgreSQL, or MongoDB.

**Models** (`models/`)
SQLAlchemy ORM definitions. Represent the DB tables as Python classes.

**Schemas** (`schemas/`)
Pydantic models. Define the shape of data coming in from requests and going out in responses.

**Core** (`core/`)
Infrastructure setup — DB engine, session, config, logging. Used by all layers but belongs to none.

## Stack

- [FastAPI](https://fastapi.tiangolo.com/) — web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
- [Pydantic](https://docs.pydantic.dev/) — data validation
- [SQLite](https://www.sqlite.org/) — database. Zero-config and easy to bootstrap, which fits the scope of this project. In a production system this should be replaced with PostgreSQL or MySQL.