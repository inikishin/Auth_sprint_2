# Проектная работа 6 спринта

[Ссылка на репозиторий](https://github.com/inikishin/Auth_sprint_2).

### !!! "Не нашел реализации задания про лимитирование запросов."
Было реализовано через декоратор `limit_leaky_bucket` в файле `auth/utils/rate_limits.py`

## Описание сервисов

Для запуска всех сервисов в корневой директории проекта необходимо ввести команду:

```shell
docker-compose up -d
```

После запуска docker-compose на локальной машине, cервисы доступны по следующим url:
* [http://admin.local](http://admin.local) Admin Service
* [http://api.local](http://api.local) (а также по умолчанию на 80 порту) Movies API
* [http://auth.local](http://auth.local) Auth Service

## Описание сервисов

### Movies API

Основное API на FastAPI, предоставляющее информацию о фильмах.

### Auth Service

Сервис предоставляет возможность работы пользователю с личным кабинетом. Для реализиации аутентификации используется jwt подход.

После запуска docker-compose методы API становятся доступны по базовому url `http://auth.local/`. Описание API в формате OpenAPI 2.0 можно найти по ссылке `http://auth.local/apidocs/`

Сервис использует базу данных PostgreSQL из сервиса `auth_postgres` для хранения данных о пользователях, а также отдельную базу redis в сервисе `redis`, используюмую для хранения просроченных access_tokens.

Для создания суперпользователя можно воспользоваться командой `flask command createsuperuser`.

### Admin Service

Django админ панель для работы с базой данных фильмов PostgreSQL.

### Тесты

Для запуска тестов необходимо из корневой директории перейти в папку `cd tests/functional` и запустить скрипт `./run.sh`