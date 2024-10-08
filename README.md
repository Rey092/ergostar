# TODO:

- [x] Добавить общие интерфейсы для загрузчиков фикстур (рефакторинг)
- [x] Переделать авторизацию по апи-ключу на хеши. Сделать хранение на Vault
- [x] логирование
- [x] uow vault
- [x] пересмотреть настройки лишние
- [x] рефактор конфигов и коммон
- [x] рефакторинг зависимостей
- [ ] Переписать архитектуру
- [ ] Переписать ентити
- [ ] Переписать Vault UOW
- [ ] Добавить плейграунд для sqlalchemy
- [ ] Написать тесты для сервисов
- [ ] pycharm testrun with coverage

# Отмененные задачи:
- [ ] ~~Переводы~~
- [ ] ~~Загружать фикстуры из любых путей~~
- [ ] ~~Вынести логику криптографии апи-ключей.~~
- [ ] ~~Покрасивее сделать передачу ключа для таблиц с криптографией ?~~
- [ ] ~~infisical docker~~

# Docker Installation

## 1. Copy .env.example.docker to .env.docker

```bash
cp .env.example.docker .env.docker
```

## 2. Start the app

```bash
docker compose up --build
```

# Local Installation

## 1. Install dependencies

```bash
poetry install
```

## 2. Export litestar app path

```bash
export LITESTAR_APP=src.main.api:create_app
```

## 3. Install pre-commit hooks

```bash
pre-commit install
```

## 4. Copy .env.example to .env

```bash
cp .env.example .env
```

Remember to fill the .env file with your own values.
You need two postgres databases, one for the app and another for the admin.

## 5. Migrate the databases

```bash
make migrate
make unfold-migrate
```

## 6. Seed the databases

```bash
make seed
make unfold-seed
```

## 7. Run the app

```bash
make run
```
