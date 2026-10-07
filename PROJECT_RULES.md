NEXUSCORE — PROJECT CONTEXT & ARCHITECTURAL RULES (UPDATED v1.5)
1. IDENTITY & MISSION
Project Name: NexusCore

Architecture: Production-grade modular framework (Bot / OSINT Engine / Adaptive RAG Memory / IoT Controller).

Core Principle: Security by Design, Scalability & Zero-Trust Architecture.

2. TECH STACK & DEPENDENCIES
Language: Python 3.11+

Database Layer: SQLite + SQLAlchemy 2.0 (AsyncIO + aiosqlite)

Vector Store (RAG): ChromaDB (Local persistent vector database)

Framework: Aiogram 3.x (AsyncIO)

Testing Framework: pytest, pytest-asyncio

Logging: Centralized core/logger.py + RotatingFileHandler (app.log, errors.log, security.log)

Configuration: pydantic-settings / python-dotenv with strict .env validation

Code Quality & Security Gates: pre-commit, gitleaks (secrets scanning), ruff (linter/formatter), pytest (unit testing), GPG commit signing

3. STRICT ARCHITECTURAL & SECURITY RULES
Zero Raw SQL (SQLi Prevention):

Всі запити до реляційної БД виконуються ВИКЛЮЧНО через SQLAlchemy 2.0 ORM / Expression Language.

Сирі SQL-строки (execute("SELECT...")) суворо заборонені.

Data Integrity & Soft Delete:

Сутності в БД не видаляються фізично без крайньої потреби.

Використовувати SoftDeleteMixin із прапорцем is_active / deleted_at. Всі нові моделі даних мають покриватися відповідними юніт-тестами.

Memory & Context Protection (RAG Safety):

Розмежовувати векторний контекст за тенантами/користувачами (Tenant Isolation in ChromaDB).

Обов'язкова санітизація системних промптів для запобігання Prompt Injection та витоку системних даних (Prompt Leaking Defense).

Testing Architecture & Quality Gates:

Централізовані фікстури (tests/conftest.py): Всі асинхронні фікстури бази даних (in-memory SQLite sqlite+aiosqlite:///:memory:) та тестових сесій зберігаються в conftest.py.

Строгий поділ тестів (Test Categorization):

Швидкі тести (Unit Tests): Модульні тести бізнес-логіки, валідаторів, ORM-моделей та міксинів (SoftDeleteMixin). Працюють у пам'яті за мілісекунди.

Повільні тести (@pytest.mark.slow): Інтеграційні тести, що звертаються до зовнішніх API (Gemini, Telegram), ChromaDB або важких ML-моделей.

Двоетапний регламент розробки та комітів:

Етап Агента (Aider): Генерація коду/тестів та фіксація чернетки у робочій гілці.

Етап Tech Lead (Quality Gate): Перевірка коду розробником, запуск pre-commit hooks. У pre-commit hook підключено автоматичний прогон швидких тестів (pytest -m "not slow"). Якщо хоча б один юніт-тест падає — коміт блокується.

Обов'язкове покриття: Будь-який новий міксин, сервіс чи модуль має супроводжуватися відповідним тестом у директорії tests/.

Git Security & Commit Integrity:

Усі підсумкові коміти в репозиторій повинні бути підписані GPG-ключем (статус Verified).

Перед кожним комітом обов'язкове проходження hooks: gitleaks (перевірка на злив ключів), ruff (чистота коду) та pytest -m "not slow" (швидкі автотести).

Log Hygiene:

Використовувати тільки core/logger.py (ніколи не використовувати print()).

Заборонено логувати чутливі дані (паролі, токени, персональні дані, векторні ембединги з PII).

Secret Isolation:

Жодних хардкоджених секретів. Всі ключі беруться з config/settings.py.

Файл .env обов'язково в .gitignore. У репозиторії зберігається тільки .env.example.

Modular Structure & RBAC:

Дотримуватися чіткого розмежування: config/, core/, adapters/, modules/, tests/.

Будь-яка дія обмежується через Role-Based Access Control (RBAC).

4. DIRECTORY STRUCTURE
Plaintext
nexus_core/
├── config/             # Settings & Environment Validation
├── core/               # Database, Logger, Security, Memory (ChromaDB), Base Logic
│   └── memory/         # Vector Store, Embeddings & RAG Engine
├── adapters/           # Transport Layer (Telegram, Webhooks, API)
├── modules/            # Business Logic Modules (Quiz, OSINT, Reports, RAG)
├── tests/              # Test Suite & Pytest Infrastructure
│   ├── conftest.py     # Global async fixtures (In-Memory DB, AsyncSession)
│   ├── test_soft_delete.py # Unit tests for SoftDeleteMixin
│   └── pytest.ini      # Test configuration & custom markers (e.g. slow)
├── data/               # Local Databases, Vector Store & Persistent Files (GitIgnored)
└── logs/               # Application & Security Logs (GitIgnored)
