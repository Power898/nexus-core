# NexusCore — Project Rules & Architectural Specifications

## 1. Core Principles & Philosophy
* **Security by Design:** Secrets management via `.env` and `.env.example`. Never commit credentials.
* **Cost efficiency:** 100% Open Source / Free Tier stack (Local Python, SQLite, Docker, AWS Free Tier).
* **Isolation:** Strict role-based access control (RBAC).

## 2. Tech Stack
* **Language:** Python 3.11+
* **Core:** Asyncio, Pydantic, SQLAlchemy / SQLite
* **Bot Framework:** Aiogram 3.x
* **Monitoring:** psutil, prometheus_client, Grafana
* **DevOps:** Docker, Docker Compose, GitHub Actions, Terraform (AWS t3.micro)

## 3. Project Structure
nexus_core/
├── .env.example
├── .gitignore
├── PROJECT_RULES.md
├── requirements.txt
├── config/
│   └── settings.py
├── core/
│   ├── logger.py
│   ├── database.py
│   └── health_checker.py
├── adapters/
│   ├── base_adapter.py
│   └── telegram_adapter.py
├── modules/
│   ├── content_module.py
│   ├── quiz_module.py
│   └── reporting_module.py
└── main.py

## 4. Git & Security Rules
* All secrets must be loaded from `config/settings.py`.
* `.env` is ignored by Git. `.env.example` must contain placeholder keys.
* Commits should follow Conventional Commits standard (`feat:`, `fix:`, `docs:`, `refactor:`).