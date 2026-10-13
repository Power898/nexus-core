Специфікація вимог до системи: NexusCore (v1.7 MVP)
Розділ 1. Візія та межі проєкту (Vision & Scope)
1.1. Мета проєкту (Project Purpose)
Створення універсальної, модульної, високопродуктивної та захищеної за принципом Security by Design серверної платформи (NexusCore Engine) на мові Python 3.14+. Платформа слугує єдиним централізованим вузлом управління для інтерактивних Telegram-ботів, OSINT-інструментів, адаптивної векторної пам'яті (RAG), аналітики дезінформації, AI-агентів та IoT-інфраструктури.

1.2. Межі версії 1.7 (MVP Scope Boundaries)
Що ВХОДИТЬ у версію 1.7 (In-Scope):
Асинхронне ядро та база даних: Асинхронна робота на базі Aiogram 3.x та SQLAlchemy 2.0 (AsyncIO + aiosqlite).

Adaptive Memory Engine (RAG): Інтеграція ChromaDB для збереження та пошуку контексту, запікання короткочасної пам’яті в довготривалу та санітизація промптів (Prompt Leaking Defense).

Модульна архітектура: Динамічне підключення та вимкнення незалежних бізнес-модулів без зміни коду ядра (main.py).

Рольова модель (RBAC): Розділення прав доступу за допомогою декораторів між System Admin, Tenant Admin та User.

Динамічний контент-менеджмент: Завантаження, оновлення та м'яке видалення (Soft Delete, SoftDeleteMixin, is_active = False, deleted_at) матеріалів/тестів через файли .json, .csv чи .xlsx (Pandas / OpenPyXL).

Бізнес-модулі автоматизації: Інтеграція спеціалізованих модулів OSINT Engine (modules/osint_module.py) для збору відкритих даних та Job Hunter (modules/job_hunter.py) для пошуку й фільтрації вакансій із залученням RAG-матчингу.

Модуль звітності (Reporting Engine): Генерація текстових дашбордів та вивантаження статистики тестування у форматі .csv / .xlsx.

Моніторинг та метрики (Observability): Контроль системних ресурсів через modules/health.py з використанням psutil та неблокуючого виконання через asyncio.to_thread, сповіщення про перевантаження (>85%) та експорт метрик для Prometheus & Grafana (порт 8000).

Інфраструктура автоматизованого тестування (Pytest Infrastructure):

Централізовані асинхронні фікстури в tests/conftest.py (in-memory SQLite sqlite+aiosqlite:///:memory:).

Строгий поділ тестів на швидкі (unit, зокрема test_soft_delete.py, test_health.py) та повільні (@pytest.mark.slow) (інтеграційні/AI/RAG).

Двоетапний регламент контролю якості: розробка/генерація тесту (Aider) → верифікація та прогон Quality Gates через pre-commit (Tech Lead).

Практичний пентестінг та валідація безпеки (Ethical Hacking): Симуляція DoS/Spam атак, тестування Rate Limiter, валідація завантажуваних файлів та перевірка реакції журналу security.log.

Розширений захист (Security by Design): Повна відсутність сирого SQL, Rate Limiting, поділ секретів через .env, журнал дій security.log, GPG-підписи комітів та Pre-commit hooks (gitleaks, ruff, автоматизований прогон швидких тестів pytest -m "not slow").

Абстракція транспорту (Messenger Agnostic): Ізоляція бізнес-логіки від Telegram API для легкого переносу на інші месенджери чи REST API.

Контейнеризація та Cloud CI/CD: Повна підготовка Docker/Docker Compose (з волюмами під ChromaDB, logs, data) та Terraform-скриптів для деплою в AWS (EC2 Free Tier, S3, Budget Alert).

Що НЕ ВХОДИТЬ у версію 1.7 (Out-of-Scope — відкладено на наступні фази):
Пряме стикування з фізичним залізом (ESP32) та розгортання локальних MQTT-брокерів.

Складні автономні мультиагентні системи ройового типу (LangChain / LangGraph / AutoGen).

Повне шифрування всієї реляційної бази даних на рівні диска (SQLCipher) — реалізується на етапі розширення після MVP.

Графічна веб-панель адміністрування (все управління реалізовано через Telegram-інтерфейс, метрики Grafana та файли).

Розділ 2. Вимоги користувача (User Requirements & Use Cases)
2.1. Актори та їхні ролі (Actors & Roles)
System Administrator (Інженер / DevSecOps / Tech Lead): Відповідає за інфраструктуру, сервери, моніторинг ресурсів (Prometheus/Grafana), логування, CI/CD-пайплайни, деплой нових модулів, підтвердження комітів через Quality Gates (pre-commit, pytest), проведення внутрішніх пентестів та налаштування кібербезпеки.

Tenant Admin (Адміністратор на стороні замовника): Власник бізнес-контенту. Завантажує й коригує тести/матеріали, керує векторними знаннями тенанта, вивантажує аналітичні звіти.

End User (Кінцевий користувач / Студент / Аналітик): Взаємодіє з ботом: проходить профілювання/тестування, запускає кар'єрний пошук чи OSINT-перевірки, запитує інформацію з RAG-бази знань, отримує результати чи сповіщення.

2.2. Прецеденти використання (Use Cases)
UC-1: Ініціалізація та запуск ядра (System Startup)
Актор: System Admin / Система.

Передумова: Заповнено файл .env, наявні необхідні API-токени, створено каталоги /data, /logs, /chromadb, пройдено автотести.

Основний сценарій:

System Admin запускає main.py (або запуск через Docker Container).

NexusCore зчитує та валідує конфігурацію (config/settings.py), ініціалізує асинхронну базу даних (core/database.py), векторну БД ChromaDB (core/memory/vector_db.py) та створює відсутні таблиці/індекси.

Ядро реєструє всі активні модулі та надсилає сповіщення System Admin-у в Telegram: «NexusCore v1.7 успішно запущено».

Обробка помилок: При відсутності токена чи збої БД ядро записує помилку в errors.log і безпечно зупиняється.

UC-2: Управління контентом та Soft Delete
Актор: Tenant Admin.

Передумова: Авторизація за роллю через RBAC Middleware.

Основний сценарій:

Tenant Admin надсилає боту файл із тестами (.json, .csv чи .xlsx).

Модуль modules/content_module.py валідує структуру файла на відповідність схемі.

При видаленні тесту Tenant Admin викликає команду /my_tests та обирає [🗑 Видалити]. Запис отримує статус is_active = False та фіксується часова мітка deleted_at (Soft Delete), зберігаючи цілісність аналітики.

UC-3: Пошук знань та генерація відповідей (RAG Querying)
Актор: End User.

Основний сценарій:

Користувач ставить текстове питання боту.

RAG Engine (core/memory/) шукає релевантні контексти у ChromaDB з урахуванням ізоляції тенанта (Tenant Isolation).

Система очищує контекст від потенційних Prompt Injection та видає відповідь, фіксуючи сесію у Short-Term Memory.

UC-4: Проходження тестування та фіксація результатів
Актор: End User.

Основний сценарій:

Користувач викликає команду /start або обирає доступну тему.

Модуль modules/quiz_module.py послідовно видає питання, фіксує відповіді та обчислює бал.

Результат фіксується в таблиці results асинхронним записом ORM.

UC-5: OSINT та Job Hunter Автоматизація
Актор: End User.

Основний сценарій:

Користувач викликає команди /hunt або /osint_check через Telegram-бот.

Модулі modules/job_hunter.py або modules/osint_module.py здійснюють паралельний збір або парсинг даних.

За допомогою локального RAG та LLM результати фільтруються відповідно до профілю користувача та видаються у вигляді структурованого звіту в чат.

UC-6: Моніторинг та бізнес-звітність
Актор: System Admin / Tenant Admin.

Основний сценарій:

System Admin переглядає системні метрики (CPU, RAM через HealthChecker, Uptime) та бізнес-метрики (nexus_quizzes_passed_total) на дашборді Grafana (порт 8000).

Tenant Admin викликає команду /admin_report у боті та отримує текстовий дашборд і файл .csv/.xlsx із результатами.

UC-7: Автоматизоване тестування та Quality Gates (Test Execution)
Актор: System Admin (Tech Lead).

Передумова: Наявність тестового середовища tests/ з conftest.py.

Основний сценарій:

При створенні нових модулів чи міксинів генеруються відповідні unit-тести у tests/.

Під час виконання git commit розробником (Tech Lead), pre-commit hook автоматично викликає pytest -m "not slow".

Швидкі тести проганяються на ізольованій in-memory SQLite за лічені мілісекунди. При успішному проходженні коміт дозволяється; при падінні тесту — коміт заблоковано до усунення помилки.

Повільні тести з міткою @pytest.mark.slow виконуються окремо або перед вивантаженням на CI/CD (GitHub Actions / Cloud).

UC-8: Аудит безпеки та Пентестінг (Pentesting Execution)
Актор: System Admin (Ethical Hacker).

Основний сценарій:

System Admin проводить контрольовані випробування стійкості ядра (симуляція атак DoS/Spam, некоректні запити, підробка файлів, спроби обходу RBAC та SQLi).

Система автоматично відсікає аномальні запити через Rate Limiter, відхиляє некоректні структури файлів та записує інциденти в logs/security.log.

Інженер аналізує логи та підтверджує захищеність платформи.

Розділ 3. Функціональні вимоги (Functional Requirements)
3.1. Файлова структура проєкту (Project Architecture)
Plaintext
nexus_core/
├── config/                 # Конфігурація та Pydantic-валідація .env
│   ├── __init__.py
│   └── settings.py
│
├── core/                   # Ядро системи (Core Engine)
│   ├── __init__.py
│   ├── database.py         # SQLAlchemy 2.0 AsyncIO підключення
│   ├── models.py           # ORM Моделі (User, QuizQuestion, Result) & SoftDeleteMixin
│   ├── logger.py           # Централізоване логування (app, errors, security)
│   ├── metrics_exporter.py # Prometheus metrics HTTP server (port 8000)
│   └── memory/             # Adaptive Memory Engine (RAG)
│       ├── __init__.py
│       ├── vector_db.py    # Інтеграція з ChromaDB
│       ├── embeddings.py   # Векторатизація контенту
│       └── manager.py      # Керування Short/Long-term пам'яттю
│
├── adapters/               # Транспортний шар (Messenger Agnostic)
│   ├── __init__.py
│   ├── base_adapter.py     # Абстрактний інтерфейс адаптера
│   └── telegram_adapter.py # Адаптер під Telegram API (Aiogram 3.x)
│
├── modules/                # Бізнес-модулі
│   ├── __init__.py
│   ├── base_module.py      # Базовий клас для модулів
│   ├── health.py           # Моніторинг RAM/CPU/Disk через psutil + asyncio.to_thread
│   ├── quiz_module.py      # Модуль проведення тестування
│   ├── content_module.py   # Валідація та завантаження JSON/CSV/XLSX
│   ├── reporting_module.py # Генерація CSV/Excel звітів
│   ├── osint_module.py     # Модуль збору та перевірки відкритих даних
│   └── job_hunter.py       # Автоматизований агент пошуку вакансій
│
├── tests/                  # Інфраструктура автоматизованого тестування
│   ├── conftest.py         # Глобальні асинхронні фікстури (in-memory SQLite, sessions)
│   ├── test_soft_delete.py # Юніт-тести для SoftDeleteMixin
│   ├── test_health.py      # Юніт-тести для HealthChecker
│   └── pytest.ini          # Кастомні маркери (наприклад, @pytest.mark.slow) та конфігурація
│
├── data/                   # Локальні бази даних, векторне сховище (в .gitignore)
│   ├── nexus.db            # Файл бази даних SQLite
│   └── chromadb/           # Локальні векторні індекси ChromaDB
│
├── logs/                   # Журнали подій та безпеки (в .gitignore)
│   ├── app.log
│   ├── errors.log
│   └── security.log
│
├── .github/workflows/      # CI/CD автоматизація (GitHub Actions)
│   └── ci-cd.yml
│
├── .pre-commit-config.yaml # Хуки якості, безпеки та автоматичного прогону тестів
├── .env                    # Секретні ключі (в .gitignore)
├── .env.example            # Безпечний шаблон конфігурації
├── .gitignore              # Виключення секретів і даних з Git
├── PROJECT_RULES.md        # Архітектурні правила та кодинг-стандарти
├── SPECIFICATION.md        # Повна специфікація вимог
├── ROADMAP.md              # Повний роадмап і статус тасок
├── Dockerfile              # Легковажний контейнер Python 3.14-slim
├── docker-compose.yml      # Конфігурація контейнерів та волюмів
├── requirements.txt        # Залежності проєкту (включно з psutil 7.2.2+)
└── main.py                 # Головна точка входу
