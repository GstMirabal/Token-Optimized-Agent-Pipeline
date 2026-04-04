# 🧠 KI-002: Ingestion Resilience with Circuit Breakers

**Domain**: `architecture/ingestion`
**Version**: 1.0.0
**Status**: `CERTIFIED`
**Tag**: `resilience`, `circuit-breaker`, `external-service-error`, `api-stability`

---

## 🏛️ Context & Rationale
External data providers (CMC, Exchanges, Macro APIs) are inherently unreliable. Repeated failures can lead to (1) IP/API Key bans, (2) Corrupted partial data, and (3) System-wide resource exhaustion from timing out.

## 🛠️ Implementation Pattern: Persistent Circuit Breaker
Use a database-backed `IngestionMonitor` to track the state of each provider:

### 1. The Monitor Model
- `provider_name` (Unique)
- `status` (Operational, Decoupled/Paused)
- `failure_count` (Track consecutive errors)
- `retry_after` (Duration of the cooling period)

### 2. The Decorator Mechanism
Wrap ingestion methods with a `resilience_circuit_breaker(provider_name)` decorator:
- **Pre-Check:** If `monitor.is_available()` is False, skip the call immediately and return an empty result.
- **On Failure:** Increment `failure_count`. If `count >= 3`, set status to `DECOUPLED` and define a cooling period (e.g., 1 hour / institutional standard).
- **On Success:** Reset `failure_count` and `status` to `OPERATIONAL` (Full Recovery policy).

## 🛡️ Safeguards
- The decorator MUST use `objects.get_or_create` to ensure new providers are initialized safely.
- A manual `reset` command should be provided to force restoration during maintenance cycles.

---
*Certified under Roadmap 008 - Matrix Strategic Intelligence*
