NEXUSCORE — FULL ROADMAP & SPRINTS (UPDATED v1.5)
⚽ Спринт 1: Базовий каркас, Безпека та Context Engineering (Поточний)
[x] Task 1.1: Ініціалізація проєкту, venv, requirements.txt, .gitignore.

[x] Task 1.2: Налаштування змінних оточення .env та модуля config/settings.py.

[x] Task 1.3: Реалізація централізованого модуля логування core/logger.py (app.log, errors.log, security.log).

[x] Task 1.4 (Context Engineering): Створення специфікації проєкту PROJECT_RULES.md, SPECIFICATION.md та ROADMAP.md.

[ ] Task 1.5 (Database Setup): Модуль core/database.py та ORM-моделі (core/models.py) на SQLAlchemy 2.0 AsyncIO.

[ ] Task 1.6 (Soft Delete & Parametrized Queries): Захист від SQLi та реалізація SoftDeleteMixin з прапорцями is_active / deleted_at.

[ ] Task 1.7 (Testing Infrastructure Setup): Створення папки tests/, настройка pytest.ini (з маркером slow) та глобальних асинхронних фікстур у tests/conftest.py (in-memory SQLite sqlite+aiosqlite:///:memory:).

[ ] Task 1.8 (Unit Test Verification): Написання швидкого тесту tests/test_soft_delete.py для перевірки роботи м'якого видалення.

[ ] Task 1.9 (Git Security & Quality Gate): Налаштування GPG-підписів комітів (Verified badge), конфігурація .pre-commit-config.yaml (gitleaks, ruff, trailing-whitespace та прогон швидких тестів pytest -m "not slow").

[ ] Task 1.10 (Entrypoint): Створення головної точки входу main.py та ініціалізація бота (Aiogram 3.x).

[ ] Task 1.11 (Health Check): Модуль core/health_checker.py — контроль RAM/CPU через psutil (>85%).

🤖 Спринт 2: Транспортний адаптер, RBAC та Telegram-бот
[ ] Task 2.1: Модуль adapters/base_adapter.py — абстракція транспортного рівня (Messenger Agnostic).

[ ] Task 2.2: Модуль adapters/telegram_adapter.py — підключення Telegram API (Aiogram 3.x).

[ ] Task 2.3: Реалізація Rate Limiting (захист від DoS/Spam) та фіксація порушень у security.log.

[ ] Task 2.4: Декоратор перевірки ролей @require_role (System Admin vs Tenant Admin vs User) — RBAC Middleware.

[ ] Task 2.5: Реалізація обробників базових команд (/start, /health, /help).

[ ] Task 2.6 (Unit Tests): Написання швидких тестів для перевірки RBAC-декораторів та валідації ролей.

📊 Спринт 3: Контент-менеджмент, Обробка даних та Звітність
[ ] Task 3.1: Модуль modules/content_module.py — валідація та завантаження .json / .csv / .xlsx файлів (pandas / openpyxl).

[ ] Task 3.2: Команда /my_tests з підтримкою Soft Delete (is_active = False).

[ ] Task 3.3: Модуль modules/quiz_module.py — проходження тесту та фіксація результатів у БД.

[ ] Task 3.4: Модуль modules/reporting_module.py — вивантаження результатів у .csv / .xlsx та команда /admin_report.

[ ] Task 3.5 (Unit Tests): Написання тестів для перевірки валідації контенту та фільтрації м'яко видалених записів у звітах.

📈 Спринт 4: Інтеграція метрик Prometheus & Grafana
[ ] Task 4.1: Модуль core/metrics_exporter.py — підняття HTTP-сервера метрик на порту 8000 (prometheus_client).

[ ] Task 4.2: Експорт системних метрик (RAM, CPU, Uptime) та бізнес-метрики (nexus_quizzes_passed_total).

[ ] Task 4.3: Конфігурація scrape_config для Prometheus та створення дашборду в Grafana.

🧠 Спринт 5: Adaptive Memory Engine (RAG & Memory Management)
[ ] Task 5.1 (Vector Store Setup): Модуль core/memory/vector_db.py — інтеграція локальної ChromaDB для векторного збереження знань і контексту.

[ ] Task 5.2 (Embeddings & Ingestion): Модуль core/memory/embeddings.py — векторатизація текстів/документів та створення індексів за тенантами.

[ ] Task 5.3 (Short & Long-term Memory): Реалізація алгоритму сесійного контексту (Short-term buffer) та його періодичного запікання у Long-term Vector Memory.

[ ] Task 5.4 (Context Pruning & Leaking Defense): Механізм очищення застарілого контексту, санітизація системних промптів та захист від витоку персональних/системних даних у відповідях.

[ ] Task 5.5 (Integration Tests - Slow): Повільні тести з міткою @pytest.mark.slow для перевірки ізоляції тенантів у ChromaDB та RAG-пошуку.

🧪 Спринт 6: Розширене Тестування, Pentest (Ethical Hacking) та Security Validation
[ ] Task 6.1 (Full Test Suite Audit): Ревізія покриття коду юніт-тестами (pytest -m "not slow") та повільними інтеграційними тестами (pytest -m slow).

[ ] Task 6.2 (Pentesting & Security Validation):

Симуляція DoS/Spam атаки для перевірки спрацьовування Rate Limiter.

Перевірка коректності запису спроб несанкціонованого доступу та витоку даних у security.log.

Тестування валідатора контенту на стійкість до завантаження шкідливих чи некоректних файлів.

Тест на Prompt Injection та спроби обходу RBAC.

[ ] Task 6.3 (Two-step Commit Workflow Check): Фінальне шліфування взаємодії: Aider генерує тести/код → Tech Lead перевіряє та проганяє Quality Gates через pre-commit.

🐳 Спринт 7: Контейнеризація (Docker, Proxmox Alpine) & CI/CD
[ ] Task 7.1: Написання легковажного Dockerfile (python:3.11-slim / alpine).

[ ] Task 7.2: Конфігурація docker-compose.yml із підключенням Docker Volumes (/data, /logs, /chromadb).

[ ] Task 7.3: Налаштування .github/workflows/ci-cd.yml — автоматичний запуск лінтерів (ruff), перевірка на секрети (gitleaks), запуск швидких/повільних тестів (pytest) та збірка Docker-образу при git push.

☁️ Спринт 8: Cloud Infrastructure (AWS & Terraform) & E2E Валідація
[ ] Task 8.1: Написання Terraform-скриптів (main.tf, variables.tf) для створення AWS EC2 (t3.micro Free Tier), Security Group та S3 Bucket.

[ ] Task 8.2: Налаштування AWS Budget Alert ($0.01) для захисту від незапланованих витрат.

[ ] Task 8.3: Тестовий деплой в AWS та перевірка авто-видалення ресурсів (terraform destroy).

[ ] Task 8.4: E2E-тестування за сценаріями всіх ролей.

[ ] Task 8.5: Фіналізація README.md на GitHub із детальною архітектурною діаграмою та інструкціями з розгортання.
