# Local Installation

## 1. Install dependencies

```bash
poetry install
```

## 2. Export litestar app path

```bash
export LITESTAR_APP=src.apps.api:create_app
```

## 3. Install pre-commit hooks

```bash
pre-commit install
```

## 4. Seed the database

```bash
make seed
```

## 5. Seed admin database

```bash
make unfold-seed
```
