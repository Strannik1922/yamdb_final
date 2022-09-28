# REST API Yamdb – база отзывов пользователей о произведениях.
![Build Status](https://github.com/Strannik1922/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
## Технологический стек
![Django-app workflow](https://github.com/needred/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=008080)](https://jwt.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)

## Workflow
* tests - Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest. Дальнейшие шаги выполнятся только если push был в ветку master или main.
* build_and_push_to_docker_hub - Сборка и доставка докер-образов на Docker Hub
* deploy - Автоматический деплой проекта на боевой сервер. Выполняется копирование файлов из репозитория на сервер:
* send_message - Отправка уведомления в Telegram

### Подготовка для запуска workflow
Создайте и активируйте виртуальное окружение, обновите pip:
```
python3 -m venv venv
source venv/Scripts/activate
python3 -m pip install --upgrade pip
```
Запустите автотесты:
```
pytest
```
Скопируйте подготовленные файлы `docker-compose.yaml` и `nginx/default.conf` из вашего проекта на сервер:
```
scp docker-compose.yaml <username>@<host>/home/<username>/docker-compose.yaml
sudo mkdir nginx
scp default.conf <username>@<host>/home/<username>/nginx/default.conf
```
В репозитории на Гитхабе добавьте данные в `Settings - Secrets - Actions secrets`:
```
DOCKER_USERNAME - имя пользователя в DockerHub
DOCKER_PASSWORD - пароль пользователя в DockerHub
HOST - ip-адрес сервера
USER - пользователь
SSH_KEY - приватный ssh-ключ (публичный должен быть на сервере)
PASSPHRASE - кодовая фраза для ssh-ключа
DB_ENGINE - django.db.backends.postgresql
DB_NAME - postgres (по умолчанию)
POSTGRES_USER - postgres (по умолчанию)
POSTGRES_PASSWORD - postgres (по умолчанию)
DB_HOST - db
DB_PORT - 5432
SECRET_KEY - секретный ключ приложения django (необходимо чтобы были экранированы или отсутствовали скобки)
ALLOWED_HOSTS - список разрешённых адресов
TELEGRAM_TO - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
TELEGRAM_TOKEN - токен бота (получить токен можно у @BotFather, /token, имя бота)
```
При внесении любых изменений в проект, после коммита и пуша
```
git add .
git commit -m "..."
git push
```
запускается набор блоков команд jobs (см. файл yamdb_workflow.yaml), т.к. команда `git push` является триггером workflow проекта.

## Описание:
Реализован пользовательский функционал дающий возможность пользоваться приложением не посещая сайт:
1.	Пользовательские роли:
   * Аноним — может просматривать описания произведений, читать отзывы и комментарии.
   * Аутентифицированный пользователь (user)— может читать всё, как и Аноним, дополнительно может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять свои отзывы и комментарии.
   * Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять и редактировать любые отзывы и комментарии.
   * Администратор (admin) — полные права на управление проектом и всем его содержимым. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
   * Администратор Django — те же права, что и у роли Администратор.
2.	Система регистрации пользователей:
   * Пользователь отправляет POST-запрос с параметром email на /api/v1/auth/email/.
   * YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
   * Пользователь отправляет POST-запрос с параметрами email и confirmation_code на /api/v1/auth/token/, в ответе на запрос ему приходит token(JWT-токен).
   * После регистрации и получения токена пользователь может отправить PATCH-запрос на /api/v1/users/me/ и заполнить поля в своём профайле.
3.	Ресурсы API YaMDb:
   * Ресурс AUTH: аутентификация.
   * Ресурс USERS: пользователи.
   * Ресурс TITLES: произведения, к которым можно написать отзыв.
   * Ресурс CATEGORIES: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
   * Ресурс GENRES: жанры произведений.
   * Ресурс REVIEWS: отзывы на произведения.
   * Ресурс COMMENTS: комментарии к отзывам.
4.  Передача токена в контейнер.
   * Создать файл .env.
   * Указываем, что работаем с postgresql:
      `DB_ENGINE=django.db.backends.postgresql`
   * Имя базы данных:
      `DB_NAME=postgres`
   * логин для подключения к базе данных:
      `POSTGRES_USER=postgres`
   * пароль для подключения к БД (установите свой):
      `POSTGRES_PASSWORD=postgres`
   * название сервиса (контейнера):
      `DB_HOST=db`
   * порт для подключения к БД:
      `DB_PORT=5432`

## Как развернуть проект локально:

Клонируйте репозиторий и перейдите в него в командной строке:
```
git clone https://github.com/needred/yamdb_final.git
cd yamdb_final
```
Создайте файл .env командой `touch .env` и добавьте в него переменные окружения для работы с базой данных:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```
В папке проекта создайте образ:
```
docker build -t username/imagename:version api_yamdb/.
```
Соберите контейнеры:
```
docker-compose -f infra/docker-compose.yaml up -d --build
```
или пересоберите:
```
docker-compose up -d --build
```
Выполните миграции:
```
(опционально) docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```
Для входа внутрь контейнера используйте команду `exec`:
```
docker-compose exec web bash
```

## Как развернуть проект на сервере:
Установите соединение с сервером:
```
ssh username@server_address
```
Проверьте статус nginx:
```
sudo service nginx status
```
Установите Docker и Docker-compose:
```
sudo apt install docker.io
sudo apt-get update
sudo apt-get install docker-compose-plugin
sudo apt install docker-compose
docker-compose version
```
Проверьте корректность установки Docker-compose:
```
sudo  docker-compose --version
```
Создайте `nginx` на сервере ubuntu:
```
scp -r nginx username@51.250.110.135:/home/username/
```
Создайте файл `docker-compose.yaml` на сервере ubuntu:
```
scp docker-compose.yaml username@51.250.110.135:/home/username/
```

### После успешного деплоя:
Соберите статические файлы (статику):
```
docker-compose exec web python manage.py collectstatic --no-input
```
Примените миграции:
```
(опционально) docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate --noinput
```
Создайте суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
собираем статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```
Отобразите список работающих контейнеров:
```
sudo docker container ls -a
```
В списке контейнеров копируйте CONTAINER ID контейнера username/api_yamdb:latest (username - имя пользователя на DockerHub).   
Выполните вход в контейнер:
```
sudo docker exec -it <CONTAINER_ID> bash
```
Внутри контейнера выполните миграции:
```
python manage.py migrate
Документация к API доступна по адресу http://ip_adress/redoc/

API доступен по адресу [http://ip_adress/api/v1/]