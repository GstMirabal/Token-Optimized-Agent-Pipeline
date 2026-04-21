# KI-027: Lazy Signal Paradigm (Django Resilience)

## 📌 Identification
- **ID**: KI-027
- **Project**: CryptoBot
- **Sprint**: 028 (Identity Hardening)
- **Problem**: Circular dependencies occurring when Django `signals.py` imports models from the same app, especially when using the `@receiver` decorator with the actual model class.

## 🛠️ Resolution Strategy
To prevent architectural lockup during application initialization, follow the **Lazy Signal Paradigm**:

### 1. Lazy Sender Reference
Never use the model class directly in the decorator. Use the string-based reference.
```python
# ❌ INCORRECT (Triggers early import)
from .models import User
@receiver(post_save, sender=User)

# ✅ CORRECT (Lazy resolution)
@receiver(post_save, sender='users.User')
```

### 2. Localized Model Imports
Perform model imports INSIDE the receiver function to ensure the app registry is fully loaded when the logic executes.
```python
@receiver(post_save, sender='users.User')
def my_handler(sender, instance, **kwargs):
    # 🏛️ Local import
    from .models import Profile
    # Logic...
```

## ⚖️ Governance Impact
- **Stability**: Eliminates `ImportError` or `AppRegistryNotReady` during `makemigrations` and `runserver`.
- **Decoupling**: Allows models to trigger signals that interact with other related models without creating rigid module-level links.

---
*Certified under Protocol: extract_workflow.md*
