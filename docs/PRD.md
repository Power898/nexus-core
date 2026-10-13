# Product Requirements Document (PRD): NexusCore

## 1. Product Overview & Vision
* **Product Name:** NexusCore
* **Vision:** A sustainable, open-core micro-SaaS and automation platform designed to provide modular, highly secure, and asynchronous tools for developers and business workflows.
* **Core Philosophy:** "Keep It Simple, Stupid" (KISS) — reliable, production-ready core components over bloated, unfinished features. High code quality and thorough test coverage serve as our foundational standards.
* **Business Model:** Hybrid Open-Core. The core platform, database abstractions, and system monitors are open-source, while specialized automation modules and advanced analytics are monetized.

---

## 2. Target Audience
* **Developers & DevOps Engineers:** Seeking clean, async-first Python components, lightweight monitoring, and robust database management tools.
* **Solo Entrepreneurs & Micro-SaaS Builders:** Looking for a reliable, low-cost architectural foundation to launch targeted automation solutions quickly.

---

## 3. Technical Stack & Architecture
* **Language:** Python 3.14+ (Async-first design leveraging modern standard libraries and `asyncio`).
* **Database & ORM:** SQLite with asynchronous support (`aiosqlite`) via SQLAlchemy 2.0.
* **System Monitoring:** `psutil` (7.2.2+) integrated with non-blocking thread execution (`asyncio.to_thread`).
* **Testing Framework:** `pytest`, `pytest-asyncio` with 100% passing test suites.
* **Code Standards:** Type hinting, timezone-aware datetimes (`datetime.now(timezone.utc)`), modular architecture with strict separation of concerns.

---

## 4. Implemented Scope (Current Status)
* [x] **Async Database Layer:** Session management and async database operations configured.
* [x] **Soft Delete Mechanism:** Secure record lifecycle management ensuring data integrity and recovery options.
* [x] **System Health Checker (Task 1.9):**
  * Real-time synchronous and asynchronous metrics collection for CPU, RAM (`virtual_memory`), and Disk usage (`disk_usage`).
  * Non-blocking architecture using `asyncio.to_thread` to protect the event loop.
  * ISO-compliant UTC timestamps with timezone awareness.
* [x] **Test Suite:** Comprehensive unit tests covering database managers, soft delete logic, and system health checks (9/9 passing tests).

---

## 5. Future Scope & Roadmap
* **Phase 2: Bot Interface & Commands**
  * Integration with Telegram/Async bots (`aiogram`).
  * Implementation of user-facing status commands (e.g., `/health`, `/status`) leveraging the `HealthChecker` module.
* **Phase 3: Per-User Resource Tracking**
  * Granular tracking of CPU/Memory allocation per user session or background task.
  * Load management hooks to support future resource limits and pay-as-you-go logic.
* **Phase 4: Business Modules (Open-Core Expansion)**
  * Development of specialized automation modules (e.g., Job Hunter / Auto-Recruiter).

---

## 6. Non-Functional Requirements
* **Performance:** Zero-lag event loop execution; heavy system diagnostics offloaded to thread pools.
* **Maintainability:** Modular directory structure (`modules/`, `tests/`) ensuring independent scaling of components.
* **Security:** Security-by-Design principles, secure environment variable handling, and robust database constraint management.
