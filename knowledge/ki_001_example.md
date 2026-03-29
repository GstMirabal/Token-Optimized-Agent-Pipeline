# Handling Docker Compose timeouts in dev

**Context:** During the testing of the local backend, the Orchestrator received recurring connection timeout errors from `psycopg2` or equivalent drivers.

**The Bug/Issue:** The PostgreSQL container takes a few seconds to initialize its internal socket on a cold start. If the application matrix immediately tries to run migrations or tests, it crashes.

**The Solution:**
Do not modify the business logic or tests to add `time.sleep()`. Instead, rely on Docker's native `healthcheck` and `depends_on`.
Ensure the target container uses:
```yaml
depends_on:
  db:
    condition: service_healthy
```

**Lesson for future Subagents:** 
Whenever instructed to configure Docker databases, NEVER assume the database is instantly ready. ALWAYS use `service_healthy` conditions for any backend consumer.
