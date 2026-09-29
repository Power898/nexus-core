# NEXUSCORE — PROJECT CONTEXT & ARCHITECTURAL RULES (UPDATED v1.4)

## 1. IDENTITY & MISSION
- **Project Name:** NexusCore
- **Architecture:** Production-grade modular framework (Bot / OSINT Engine / Adaptive RAG Memory / IoT Controller).
- **Core Principle:** Security by Design, Scalability & Zero-Trust Architecture.

## 2. TECH STACK & DEPENDENCIES
- **Language:** Python 3.11+
- **Database Layer:** SQLite + SQLAlchemy 2.0 (AsyncIO + aiosqlite)
- **Vector Store (RAG):** ChromaDB (Local persistent vector database)
- **Framework:** Aiogram 3.x (AsyncIO)
- **Logging:** Centralized `core/logger.py` + RotatingFileHandler (`app.log`, `errors.log`, `security.log`)
- **Configuration:** `pydantic-settings` / `python-dotenv` with strict `.env` validation
- **Code Quality & Security Gates:** `pre-commit`, `gitleaks` (secrets scanning), `ruff` (linter/formatter), GPG commit signing

## 3. STRICT ARCHITECTURAL & SECURITY RULES
1. **Zero Raw SQL (SQLi Prevention):** 
   - Всі запити до реляційної БД виконуються ВИКЛЮЧНО через SQLAlchemy 2.0 ORM / Expression Language. 
   - Сирі SQL-строки (`execute("SELECT...")`) суворо заборонені.

2. **Data Integrity & Soft Delete:**
   - Сутності в БД не видаляються фізично без крайньої потреби. 
   - Використовувати прапорець `is_active = Column(Boolean, default=True)` (Soft Delete).

3. **Memory & Context Protection (RAG Safety):**
   - Розмежовувати векторний контекст за тенантами/користувачами (Tenant Isolation in ChromaDB).
   - Обов'язкова санітизація системних промптів для запобігання Prompt Injection та витоку системних даних (Prompt Leaking Defense).

4. **Git Security & Commit Integrity:**
   - Усі коміти в репозиторій повинні бути підписані GPG-ключем (статус `Verified`).
   - Перед кожним комітом обов'язкове проходження hooks: `gitleaks` (перевірка на злив ключів) та `ruff` (чистота коду).

5. **Log Hygiene:**
   - Використовувати тільки `core/logger.py` (ніколи не використовувати `print()`).
   - Заборонено логувати чутливі дані (паролі, токени, персональні дані, векторні ембединги з PII).

6. **Secret Isolation:**
   - Жодних хардкоджених секретів. Всі ключі беруться з `config/settings.py`.
   - Файл `.env` обов'язково в `.gitignore`. У репозиторії зберігається тільки `.env.example`.

7. **Modular Structure & RBAC:**
   - Дотримуватися чіткого розмежування: `config/`, `core/`, `adapters/`, `modules/`.
   - Будь-яка дія обмежується через Role-Based Access Control (RBAC).

## 4. DIRECTORY STRUCTURE

nexus_core/
├── config/             # Settings & Environment Validation
├── core/               # Database, Logger, Security, Memory (ChromaDB), Base Logic
│   └── memory/         # Vector Store, Embeddings & RAG Engine
├── adapters/           # Transport Layer (Telegram, Webhooks, API)
├── modules/            # Business Logic Modules (Quiz, OSINT, Reports, RAG)
├── data/               # Local Databases, Vector Store & Persistent Files (GitIgnored)
└── logs/               # Application & Security Logs (GitIgnored)