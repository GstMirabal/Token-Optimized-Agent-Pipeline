# 🧠 Knowledge Item: Prioritized Asynchronous Communications

## 🚦 Context: Alert Overload & Critical Path
In trading bots, notification storms (e.g., connection lost) can block the execution of critical alerts (e.g., Kill-switch or OTP).

## ⚠️ The Blockage: Shared Queues
Using a single Celery queue for all notifications leads to high-priority alerts waiting behind informational reports.

## ✅ The Solution: Async Routing (Sprint 004)
1.  **Queue Segregation**: Configured `critical_alert` vs. `info_report` queues in Celery.
2.  **BaseNotifier Interface**: Abstracted the notification transport (`BaseNotifier`) to allow switching from Email to Telegram/Push without changing business logic.
3.  **Anti-Spam Squelching**: Implemented logic placeholders for batching identical alerts to protect SMTP quotas and prevent administrative fatigue.

---
`Governance Standard: Phase 3 Operational Infrastructure`
