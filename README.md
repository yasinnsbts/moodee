# Ладно

**Ладно** — веб-дневник настроения на Django. Проект помогает пользователю ежедневно фиксировать настроение, самочувствие, активность, стресс, тревожность, сон и факторы дня, а затем смотреть статистику, историю записей и персональные инсайты.

Проект задуман как self-care инструмент для наблюдения за состоянием и паттернами поведения.

> Ладно не является медицинским продуктом, не ставит диагнозы и не заменяет врача или психотерапевта.

## Что умеет проект

### Аккаунт пользователя

- регистрация;
- вход;
- выход через POST-форму с CSRF-защитой;
- профиль пользователя;
- настройки пользователя;
- смена пароля;
- удаление аккаунта.

### Дневник настроения

Пользователь может:

- создать запись настроения;
- посмотреть последние записи на главной странице;
- открыть историю всех записей;
- фильтровать записи по датам и настроению;
- удалить свою запись;
- экспортировать записи в CSV с именем вида `пользователь_дата_время_ладно_отчет.csv`;
- редактировать запись только в течение 24 часов после создания.

Одна запись содержит:

- дату;
- настроение по шкале 1-5;
- самочувствие по шкале 1-5;
- активность по шкале 1-5;
- стресс по шкале 1-5;
- тревожность по шкале 1-5;
- сон в часах от 0 до 24;
- факторы дня;
- благодарность;
- заметку до 400 символов.

Правила:

- у одного пользователя может быть только одна запись на одну дату;
- заметка ограничена 400 символами;
- редактирование доступно только первые 24 часа после создания записи;
- если запись старше 24 часов, ссылка редактирования скрывается;
- прямой переход на `/entries/<id>/edit/` для старой записи блокируется на backend-уровне.

### Главная страница после входа

Dashboard показывает:

- сегодняшнее состояние записи;
- серию дней с записями;
- последние записи;
- среднее настроение за 7 дней;
- средний стресс за 7 дней;
- средний сон за 7 дней.

Маршрут:

```text
/dashboard/
```

### История записей

История доступна по маршруту:

```text
/entries/
```

На странице есть:

- список записей;
- фильтр по начальной дате;
- фильтр по конечной дате;
- фильтр по настроению;
- кнопка добавления записи;
- CSV-экспорт;
- имя CSV-файла формируется автоматически: пользователь, дата, время, `ладно_отчет`;
- скрытие редактирования для записей старше 24 часов.

### Статистика

Статистика доступна по маршрутам:

```text
/statistics/?period=week
/statistics/?period=month
/statistics/?period=year
```

Страница статистики показывает:

- среднее настроение;
- среднее самочувствие;
- среднюю активность;
- средний стресс;
- среднюю тревожность;
- средний сон;
- распределение настроений;
- лучший день;
- самый сложный день;
- частые факторы;
- факторы, которые чаще встречаются в хорошие дни;
- факторы, которые чаще встречаются в сложные дни;
- график динамики через Chart.js.

### Персональные инсайты

Маршрут:

```text
/ai-report/
```

Сейчас отчет реализован как rule-based сервис, а не как внешний AI API.

Он анализирует:

- среднее настроение;
- самочувствие;
- активность;
- стресс;
- тревожность;
- сон;
- низкие дни;
- факторы дня;
- частые слова в заметках.

Логика вынесена в:

```text
ai_reports/services.py
```

Такую архитектуру проще тестировать и позже можно заменить на настоящий LLM-сервис без переписывания view.

### Практики

Маршрут:

```text
/practices/
```

В проекте есть дыхательные практики:

- название;
- описание;
- количество циклов;
- длительность;
- инструкция.

### Напоминания

В проекте есть demo-команда для email-напоминаний:

```bash
python manage.py send_mood_reminders
```

По умолчанию письма выводятся в консоль, потому что используется локальный email backend.

## Технологии

- Python;
- Django 6.0.4;
- PostgreSQL;
- psycopg;
- python-dotenv;
- Django templates;
- CSS;
- Chart.js через CDN;
- Docker Compose для локальной базы данных.

Что не используется:

- React;
- Vue;
- Tailwind;
- npm/yarn/pnpm;
- Django REST Framework;
- Celery;
- внешний AI SDK;
- внешний AI API.

## Структура проекта

```text
ladno/
├── accounts/              # регистрация, профиль, настройки пользователя
├── ai_reports/            # персональные инсайты и сервис отчета
├── analytics/             # статистика
├── config/                # настройки Django и основные URL
├── core/                  # landing page
├── mood/                  # дневник настроения, формы, dashboard, история, экспорт
├── notifications/         # команда email-напоминаний
├── practices/             # дыхательные практики
├── static/                # CSS и JS
├── templates/             # HTML-шаблоны
├── docker-compose.yml     # PostgreSQL для локального запуска
├── manage.py
├── requirements.txt
├── PROJECT_BEFORE_AFTER.md
└── TECHNICAL_CHANGES.md
```

## Переменные окружения

Создайте `.env` из `.env.example`.

Linux/macOS:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Пример:

```env
SECRET_KEY=replace-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,.app.github.dev,.githubpreview.dev
CSRF_TRUSTED_ORIGINS=https://*.app.github.dev,https://*.githubpreview.dev

DB_NAME=ladno_db
DB_USER=ladno_user
DB_PASSWORD=ladno_password
DB_HOST=localhost
DB_PORT=5433

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=Ладно <noreply@ladno.local>
```

Файл `.env` не должен попадать в git.

Если `.env` был создан до переименования проекта, проверьте, что в нем нет старых
значений `moodee_db`, `moodee_user`, `moodee_password`. После смены данных
PostgreSQL для существующего Docker volume может потребоваться пересоздать volume.

## Запуск на Linux

```bash
cd moodee

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

cp .env.example .env

docker compose up -d db

python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

Открыть:

```text
http://127.0.0.1:8000/
```

## Запуск на Windows

Установите:

- Python 3.12 или новее;
- Git for Windows;
- Docker Desktop.

Команды в PowerShell:

```powershell
cd C:\Projects
git clone <url-репозитория>
cd moodee

Copy-Item .env.example .env

py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

docker compose up -d db

python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

Открыть:

```text
http://127.0.0.1:8000/
```

Если PowerShell не дает активировать `.venv`:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## Демо-пользователь

После команды:

```bash
python manage.py seed_demo_data
```

можно войти под демо-аккаунтом:

```text
Email: irina@example.com
Password: test12345
```

## База данных

PostgreSQL запускается через Docker Compose:

```bash
docker compose up -d db
```

В текущей конфигурации порт проброшен так:

```yaml
5433:5432
```

Поэтому в `.env` должен быть:

```env
DB_PORT=5433
```

Если порт `5433` занят, поменяйте `DB_PORT` в `.env`; Docker Compose использует это
значение автоматически.

## Полезные команды

Применить миграции:

```bash
python manage.py migrate
```

Создать демо-данные:

```bash
python manage.py seed_demo_data
```

Запустить сервер:

```bash
python manage.py runserver
```

Проверить настройки Django:

```bash
python manage.py check
```

Запустить тесты:

```bash
python manage.py test mood ai_reports
```

Отправить demo-напоминания:

```bash
python manage.py send_mood_reminders
```

## Тесты

Сейчас тестами покрыто:

- разбор факторов записи;
- запрет второй записи на одну дату для одного пользователя;
- проверка дубликата даты на уровне формы;
- ограничение заметки до 400 символов;
- доступность редактирования свежей записи;
- запрет редактирования записи старше 24 часов;
- генерация недельного отчета.

Ожидаемый результат:

```text
Ran 7 tests
OK
```

Последняя полная проверка:

```text
Django check — OK
Тесты mood + ai_reports — 7 tests OK
Миграции — применены
Основные URL — 200
POST-сценарии — работают
CSV export — 200
Заметка 401 символ — запись не создается
Старая запись /edit/ — backend redirect
```

## Smoke test после изменений

После изменений в моделях, формах, views, URL или шаблонах нельзя проверять только главную страницу.

Минимально нужно проверить:

```text
/
/register/
/login/
/dashboard/
/entries/
/entries/new/
/statistics/?period=week
/statistics/?period=month
/statistics/?period=year
/ai-report/
/practices/
/profile/
/entries/export/
```

Также нужно проверить:

- регистрацию через POST;
- вход через POST;
- выход через POST;
- создание записи через POST;
- удаление записи через POST;
- прямой переход на edit старой записи;
- скрытие ссылки редактирования для старой записи.

## Документация

В проекте также есть:

- `PROJECT_BEFORE_AFTER.md` — что было и что стало;
- `TECHNICAL_CHANGES.md` — техническое описание изменений, зависимостей и проверок.

## Ограничения текущей версии

- Персональный отчет пока rule-based, без внешнего AI API.
- Нет мобильного приложения.
- Нет REST API.
- Нет Celery или production scheduler для напоминаний.
- Настройка темы есть в модели, но полноценная темная тема еще не реализована.
- Продукт не является медицинским сервисом.

## Что можно улучшить дальше

1. Добавить полноценный onboarding.
2. Заменить свободную строку факторов на пользовательские теги.
3. Добавить более глубокий анализ корреляций.
4. Добавить PDF-экспорт отчета.
5. Подключить реальные push/email/Telegram-напоминания.
6. Добавить политику приватности и страницу управления данными.
7. Добавить REST API для мобильного приложения.
8. Подключить настоящий LLM-отчет с guardrails и безопасными ограничениями.
