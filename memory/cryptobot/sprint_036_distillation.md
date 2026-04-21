# Sprint 036 Distillation: Financial Identity (KYC) Implementation

## 🧩 Accomplishments
- **Phase 4 Liquidation**: Deployed the `UserDocument` ledger and ingestion infrastructure.
- **Secure Handling**: Implemented UUID-based path obfuscation and server-side FileField validation (5MB, restricted extensions).
- **KYC Status Life-cycle**: Integrated `kyc_status` across `UserProfile`, `UserDocument`, and the `AdminDashboard`.
- **Identity Nodes**: Verified 100% parity between backend model states and frontend verification badges.

## 🛠️ Design Patterns & Lessons
- **Secure File Serving**: Avoided using `MEDIA_URL` directly for sensitive nodes. Created a `serve_document` action in `UserViewSet` protected by `RequiresStepUp`.
- **Step-Up Ingestion**: Forcing a re-authentication handshake BEFORE allowing an upload prevents session hijacking from submitting fraudulent nodes.
- **Certification Logic**: Decoupled profile `kyc_status` from individual document statuses to allow multi-document flows where one document rejection doesn't necessarily block the entire node (though currently, any certification updates the profile).

## ⚠️ Potential Gotchas
- **Migrations vs Tests**: Always run `makemigrations` before running tests that introduce new fields to existing relations (like `UserProfile.kyc_status`), as Django's test setup relies on migration resolution.
- **Audit Name Redundancy**: Avoid confusion between `UserLoginAudit` and generic `AuditLog` names. Stick to the model's institutional name.

## 🧪 Verification Coverage
- Backend: `apps.users.tests.test_kyc_flow` Certified (Upload, Step-Up Gate, Admin Certification).
- UI: Manual verification of drag-and-drop ingestion and sidebar certified node viewing.
