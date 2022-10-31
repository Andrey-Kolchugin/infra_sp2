# api_yamdb

## Описание

Проект **YaMDb** собирает отзывы (Review) пользователей на произведения (Titles).
Произведения делятся на категории:

- "Книги"
- "Фильмы"
- "Музыка"
  Список категорий (Category) может быть расширен администратором (например, можно добавить категорию "Ювелирка").
  Сами произведения в **YaMDb** не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число).
На одно произведение пользователь может оставить только один отзыв.
Подробная документация доступна по адресу http://127.0.0.1:8000/redoc/ после запуска проекта. Процедура запуска проекта представлена ниже.

---

## Техническое описание


### Пользовательские роли

- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь** (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- **Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- **Администратор (admin)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- **Суперюзер Django** — обладает правами администратора (admin).

### Алгоритм регистрации пользователей

Для добавления нового пользователя нужно отправить POST-запрос с параметрами email и username на эндпоинт /api/v1/auth/signup/.
Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.
После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт /api/v1/users/me/ и заполнить поля в своём профайле (описание полей — в документации).
Если пользователя создаёт администратор, например, через POST-запрос на эндпоинт api/v1/users/ — письмо с кодом отправлять не нужно (описание полей запроса для этого случая — в документации).

---

## Технологии в проекте
- **Python 3.7.9**
- **Django Framework**
- **Django Rest Framework**
- **Django Rest Framework Simplejwt**
- **Docker**

---

## Процедура запуска проекта

Клонировать репозиторий и перейти в него в командной строке и перейти в директорию проекта  
```
git clone https://github.com/Andrey-Kolchugin/infra_sp2.git
cd infra_sp2
```
Переходим в папку infra_sp2/infra и создаем в ней файл .env с переменными окружения, необходимыми для работы приложения.
```
cd infra
```
```
# Пример заполнения .env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=key
``` 
Запускаем docker compose

```
docker-compose up -d
```
Будут созданы и развернуты контейнеры:
db - база данных,
web - приложения проекта,
nginx - хранение и раздача медиа и статики.

Далее нужно последовательно выполнить команды миграции, создания суперюзера и сбора статики
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
Проект будет доступен по адресу http://localhost/

### Заполнение базы данных
Авторизоваться по адресу http://localhost/admin/, внести записи в базу данных через админку.

### Создание резервной копии
Бекап можно создать командой
```
docker-compose exec web python manage.py dumpdata > fixtures.json
```
### Остановка работы
Оставить работы можно командой
```
docker-compose stop
```
Либо использовать нажатие клавишь  Ctrl+C в терминале, из которого запускались контейнеры 

### Последующие запуски
В дальнейшем использовать команду запуска контейнеров
```
docker-compose start 
```



## Исполнители проекта

Студенты курса "Яндекс. Практикум", когорта 38

Андрей Кольчугин (тимлид проекта)
https://github.com/Andrey-Kolchugin/

Иван Гоцецура
https://github.com/storm4724

Юлия Шаталина
https://github.com/fromufawithlove

