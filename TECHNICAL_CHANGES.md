# Технические изменения проекта

Дата: 2026-05-05

База сравнения: `upstream/main` оригинального проекта `moodee`.
Рабочая ветка: `codex-improvements`.

## Сводка diff

```text
27 files changed, 2058 insertions(+), 179 deletions(-)
```

Измененные и добавленные файлы:

```text
M .env.example
M .gitignore
A PROJECT_BEFORE_AFTER.md
A README.md
A TECHNICAL_CHANGES.md
A ai_reports/services.py
M ai_reports/tests.py
M ai_reports/views.py
M analytics/views.py
M config/settings.py
M docker-compose.yml
M mood/forms.py
M mood/management/commands/seed_demo_data.py
A mood/migrations/0002_extend_mood_entry.py
A mood/migrations/0003_limit_note_and_edit_window.py
M mood/models.py
M mood/tests.py
M mood/urls.py
M mood/views.py
M static/css/main.css
M templates/accounts/profile.html
M templates/ai_reports/ai_report.html
M templates/analytics/statistics.html
M templates/mood/dashboard.html
M templates/mood/entry_form.html
M templates/mood/entry_list.html
M templates/practices/practices.html
```

## Зависимости

`requirements.txt` не изменялся.

Новые backend-библиотеки не добавлялись. Проект продолжает использовать существующий стек:

- Django 6.0.4;
- PostgreSQL через `psycopg`;
- `python-dotenv`;
- `django-widget-tweaks`;
- стандартные Django apps.

Новые frontend-пакеты не добавлялись. Chart.js уже был подключен через CDN в шаблоне статистики.

Не добавлялись:

- npm/yarn/pnpm;
- package.json;
- сборщик frontend;
- React/Vue/Tailwind;
- Django REST Framework;
- Celery/RQ;
- внешний AI SDK/API.

## Изменения по каждому файлу

### `.env.example`

Было:

- `SECRET_KEY` и параметры БД были пустыми;
- не было `ALLOWED_HOSTS`;
- не было `CSRF_TRUSTED_ORIGINS`;
- defaults БД не были согласованы с новым `docker-compose.yml`.

Стало:

- `SECRET_KEY=replace-me`;
- `ALLOWED_HOSTS=localhost,127.0.0.1`;
- `CSRF_TRUSTED_ORIGINS=`;
- `DB_NAME=ladno_db`;
- `DB_USER=ladno_user`;
- `DB_PASSWORD=ladno_password`;
- `DB_HOST=localhost`;
- `DB_PORT=5433`.

Технический эффект: локальный запуск проще, env-файл отражает текущие defaults проекта.

### `.gitignore`

Было:

- базовые игноры Python, virtualenv, Django media/staticfiles, `.env`, IDE и macOS.

Стало:

- добавлены `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, coverage-файлы, `*.log`, `local_settings.py`;
- добавлены `env/`, `ENV/`;
- добавлен игнор `.env.*`, но `!.env.example` оставлен в git;
- добавлены Windows файлы `Thumbs.db`, `Desktop.ini`.

Технический эффект: меньше случайного мусора и локальных секретов в git, `.env.example` остается коммитабельным.

### `PROJECT_BEFORE_AFTER.md`

Было: файла не было.

Стало: добавлен документ сравнения продукта до и после изменений, включая таблицу по каждому измененному файлу.

### `README.md`

Было: файла не было.

Стало: добавлен полный README с описанием возможностей, маршрутов, запуска на Linux/Windows, env, Docker, тестов и ограничений.

### `TECHNICAL_CHANGES.md`

Было: файла не было.

Стало: добавлен этот технический документ со сводкой diff, изменениями по файлам, проверками и ограничениями.

### `ai_reports/services.py`

Было: файла не было.

Стало: добавлен сервис персональных инсайтов.

Основные функции:

- `extract_keywords(notes)` - извлекает частые слова из заметок с фильтрацией stop words;
- `build_factor_insights(entries)` - собирает факторы, чаще связанные с хорошими и сложными днями;
- `build_weekly_report(entries)` - считает средние значения, формирует insights, recommendation, keywords.

Технический эффект: бизнес-логика отчета отделена от HTTP view и стала тестируемой.

### `ai_reports/tests.py`

Было: пустой scaffold с `TestCase`.

Стало: добавлен `WeeklyReportTests`.

Проверяется:

- низкий сон попадает в текст инсайтов;
- фактор `недосып` попадает в текст инсайтов;
- рекомендация не пустая.

### `ai_reports/views.py`

Было:

- во view находились `STOP_WORDS`, `extract_keywords`, агрегации и правила рекомендаций;
- отчет учитывал настроение, самочувствие и активность.

Стало:

- view импортирует `build_weekly_report` из `services.py`;
- view отвечает только за выбор entries, вызов сервиса и сбор context;
- в context добавлены `average_stress`, `average_anxiety`, `average_sleep`.

Технический эффект: view стал тоньше, отчет проще расширять и тестировать.

### `analytics/views.py`

Было:

- средние значения по `mood_score`, `wellbeing_score`, `activity_score`;
- данные графика только для этих трех метрик;
- распределение настроения, лучший и худший день.

Стало:

- добавлены средние `stress_score`, `anxiety_score`, `sleep_hours`;
- добавлены массивы для графика stress/anxiety/sleep;
- добавлен `Counter` факторов;
- считаются `top_factors`, `positive_factors`, `low_mood_factors`.

Технический эффект: analytics view теперь поддерживает расширенную модель дневника и факторный анализ.

### `config/settings.py`

Было:

- `ALLOWED_HOSTS = []`;
- не было `CSRF_TRUSTED_ORIGINS` из env;
- defaults БД были `moodee_db`, `moodee_user`, `moodee_password`;
- не было `STATIC_ROOT`;
- email backend и `DEFAULT_FROM_EMAIL` были статичными.

Стало:

- `ALLOWED_HOSTS` читается из env-строки;
- `CSRF_TRUSTED_ORIGINS` читается из env-строки;
- defaults БД обновлены на `ladno_db`, `ladno_user`, `ladno_password`;
- добавлен `STATIC_ROOT = BASE_DIR / "staticfiles"`;
- добавлен `DEFAULT_AUTO_FIELD`;
- `EMAIL_BACKEND`, `DEFAULT_FROM_EMAIL`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` читаются из env;
- default sender сохранен как `Ладно <noreply@ladno.local>`.

Технический эффект: настройки стали пригоднее для локального запуска и деплоя без изменения кода.

### `docker-compose.yml`

Было:

- `container_name: moodee_postgres`;
- `POSTGRES_DB: moodee_db`;
- `POSTGRES_USER: moodee_user`;
- `POSTGRES_PASSWORD: moodee_password`;
- порт `5432:5432`;
- volume `moodee_postgres_data`.

Стало:

- `container_name: ladno_postgres`;
- `POSTGRES_DB: ladno_db`;
- `POSTGRES_USER: ladno_user`;
- `POSTGRES_PASSWORD: ladno_password`;
- порт `5433:5432`;
- volume `ladno_postgres_data`.

Технический эффект: docker defaults согласованы с новым названием `Ладно` и не конфликтуют с локальным PostgreSQL на `5432`.

### `mood/forms.py`

Было:

- форма включала `date`, `mood_score`, `wellbeing_score`, `activity_score`, `note`;
- form validation не знала о пользователе;
- дубликат даты ловился только базой или не ловился на уровне формы.

Стало:

- добавлены поля `stress_score`, `anxiety_score`, `sleep_hours`, `factors`, `gratitude`;
- добавлены widgets, min/max/step, placeholders;
- `note` получает `maxlength=400`;
- `__init__` принимает `user`;
- `clean_date` проверяет, что у пользователя нет другой записи на эту дату.

Технический эффект: пользователь получает понятную ошибку до записи в БД; форма соответствует расширенной модели.

### `mood/management/commands/seed_demo_data.py`

Было:

- demo entries содержали только базовые значения настроения, самочувствия, активности и заметку;
- практики создавались без инструкции.

Стало:

- demo entries заполняют stress/anxiety/sleep/factors/gratitude;
- практикам добавляется `instruction`.

Технический эффект: после seed пользователь сразу видит новые поля, аналитику факторов и инструкции практик.

### `mood/migrations/0002_extend_mood_entry.py`

Было: миграции не было.

Стало: добавлена миграция, которая расширяет `MoodEntry`.

Добавляет поля:

- `anxiety_score`;
- `factors`;
- `gratitude`;
- `sleep_hours`;
- `stress_score`.

Добавляет constraint:

```python
UniqueConstraint(fields=("user", "date"), name="unique_mood_entry_per_user_date")
```

Технический эффект: схема БД соответствует новой бизнес-логике дневника.

### `mood/migrations/0003_limit_note_and_edit_window.py`

Было: миграции не было.

Стало: добавлена миграция, которая меняет поле `note`.

Изменение:

- `MaxLengthValidator(400)`;
- `help_text="До 400 символов"`.

Важно: окно редактирования 24 часа не требует миграции, потому что вычисляется через существующий `created_at`.

### `mood/models.py`

Было:

- `MoodEntry` хранил дату, mood/wellbeing/activity, note, timestamps;
- не было уникальности `user + date`;
- не было helper-свойств для факторов и окна редактирования.

Стало:

- добавлены `stress_score`, `anxiety_score`, `sleep_hours`, `factors`, `gratitude`;
- `note` ограничен `MaxLengthValidator(400)`;
- добавлен `UniqueConstraint` на `user + date`;
- добавлен `factor_list`, который разбивает comma-separated строку факторов;
- добавлен `can_edit`, который разрешает edit только в первые 24 часа после `created_at`.

Технический эффект: модель стала источником правил данных для форм, views, аналитики и отчетов.

### `mood/tests.py`

Было: пустой scaffold с `TestCase`.

Стало: добавлены тесты.

Проверяется:

- `factor_list` корректно разбивает строку факторов;
- БД запрещает вторую запись того же пользователя на ту же дату;
- форма отклоняет дубликат даты;
- форма отклоняет заметку длиннее 400 символов;
- свежая запись открывается для редактирования;
- запись старше 24 часов редиректит с edit page на `/entries/`.

### `mood/urls.py`

Было:

- dashboard;
- entries list;
- create;
- update;
- delete.

Стало:

- добавлен маршрут CSV-экспорта:

```python
path("entries/export/", views.entry_export_view, name="entry_export")
```

### `mood/views.py`

Было:

- dashboard показывал последние записи и среднее настроение за неделю;
- list view сам обрабатывал фильтры;
- create/update не передавали `user` в форму;
- edit был доступен без ограничения по времени;
- CSV-экспорта не было.

Стало:

- добавлен `get_current_streak(user, today)`;
- добавлен `get_filtered_entries(request)`;
- dashboard считает today's entry, streak, weekly mood/stress/sleep/count;
- create/update передают `user` в `MoodEntryForm`;
- update блокирует редактирование после 24 часов;
- добавлен `entry_export_view`;
- CSV использует UTF-8 BOM, `filename*` с русским именем и ASCII fallback;
- CSV экспортирует date, mood, wellbeing, activity, stress, anxiety, sleep, factors, gratitude, note.

Технический эффект: mood app получил основные продуктовые workflows: check-in, history, export, ограничения редактирования.

### `static/css/main.css`

Было:

- базовые стили экранов, карточек, кнопок, форм и bottom nav;
- `.card` имел `border-radius: 20px`;
- не было layout для metric grid, field errors и inline logout form.

Стало:

- `.card` получил `border-radius: 14px`;
- добавлены `.highlight`, `.metric-grid`, `.metric`, `.actions-row`, `.inline-form`;
- добавлены стили `.field`, radio list, `.error`, `.danger-message`;
- добавлен mobile breakpoint для узких экранов.

Технический эффект: новые формы и метрики отображаются компактнее и понятнее.

### `templates/accounts/profile.html`

Было:

- logout был ссылкой.

Стало:

- logout стал POST-формой с `{% csrf_token %}`.

Технический эффект: logout соответствует Django 6 `LogoutView`, который не должен выполнять выход через GET.

### `templates/ai_reports/ai_report.html`

Было:

- показывались базовые средние значения;
- блок назывался `Рекомендация`;
- дисклеймер был коротким.

Стало:

- добавлены средний стресс, тревожность, сон;
- `Рекомендация` заменена на `Следующий шаг`;
- дисклеймер явно говорит, что это не диагноз и не медицинская рекомендация, и предлагает обратиться за помощью при риске вреда.

### `templates/analytics/statistics.html`

Было:

- три карточки средних значений;
- график mood/wellbeing/activity;
- блок распределения и best/worst day;
- кнопка `Экспорт данных - позже`.

Стало:

- metric grid для настроения, самочувствия, активности, стресса, тревожности, сна;
- добавлен блок факторов;
- график дополнен stress/anxiety/sleep;
- сон отображается на отдельной правой оси;
- заглушка экспорта заменена ссылкой на `entry_export`.

### `templates/mood/dashboard.html`

Было:

- приветствие;
- среднее настроение за 7 дней;
- кнопки добавления записи и истории;
- последние записи с базовыми полями;
- edit-ссылка всегда видима.

Стало:

- показывается streak;
- добавлен highlight-блок сегодняшней записи или быстрый check-in;
- weekly metric grid: настроение, стресс, сон;
- actions row: история, аналитика, инсайты;
- последние записи показывают stress/anxiety/sleep/factors/gratitude;
- edit-ссылка показывается только если `entry.can_edit`.

### `templates/mood/entry_form.html`

Было:

- форма выводилась через `{{ form.as_p }}`.

Стало:

- ручной рендер каждого поля;
- вывод `non_field_errors`;
- вывод label, field, help text и field errors;
- кнопки save/cancel сохранены.

Технический эффект: расширенная форма стала читаемой и показывает validation feedback рядом с полями.

### `templates/mood/entry_list.html`

Было:

- фильтры по дате и настроению;
- кнопка добавления записи;
- карточки с базовыми полями;
- edit-ссылка всегда видима.

Стало:

- добавлена кнопка `Экспорт CSV`, которая сохраняет текущие query filters;
- карточки показывают stress/anxiety/sleep/factors/gratitude;
- edit-ссылка скрывается, если запись старше 24 часов.

### `templates/practices/practices.html`

Было:

- практика показывала title, cycles, duration, description;
- блок назывался `Рекомендация от нейросети`.

Стало:

- если у практики есть `instruction`, она отображается;
- блок переименован в `Персональные инсайты`;
- текст объясняет, что `Ладно` сравнит настроение, сон, активность, стресс и факторы дня.

## Проверки

Фактически выполнено после rebase на `upstream/main`:

```bash
.venv/bin/python manage.py test
```

Результат:

```text
Found 7 test(s).
System check identified no issues (0 silenced).
Ran 7 tests in 8.292s
OK
```

Также выполнены проверки git:

```bash
git diff --check upstream/main...HEAD
git merge-base --is-ancestor upstream/main HEAD
rg -n "Moodee|moodee"
```

Результат:

- conflict markers и whitespace-ошибок в diff нет;
- `upstream/main` является предком текущей ветки;
- старое видимое имя `Moodee/moodee` в проект не вернулось.

## Merge-состояние

Ветка `codex-improvements` перебазирована поверх `upstream/main`.

Конфликт был в `config/settings.py`: `upstream/main` зафиксировала sender `Ладно <noreply@ladno.local>`, а ветка добавляла env-настройки email. Итоговое состояние объединяет оба изменения: email читается из env, default sender остается `Ладно <noreply@ladno.local>`.

Для публикации переписанной истории ветки нужен:

```bash
git push --force-with-lease origin codex-improvements
```

## Что не менялось

- `requirements.txt`;
- app structure Django monolith;
- база PostgreSQL;
- внешний AI API;
- scheduler/queue для напоминаний;
- REST API;
- frontend stack.

## Важное ограничение

Текущий AI-отчет остается rule-based сервисом. Он не вызывает LLM, не ставит диагнозы и не должен восприниматься как медицинская рекомендация.
