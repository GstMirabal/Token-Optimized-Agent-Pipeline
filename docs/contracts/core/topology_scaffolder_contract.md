# 📄 Contract: Topology Scaffolder Skill Interface (v1.0.0)

This contract defines the logic-level interface for the **Topology Scaffolder** local skill. It standardizes the physical injection of the Matrix hierarchy.

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `target_root` | Path | Yes | N/A | Destination directory for the /docs/ tree. |
| `layer` | String | Yes | `unassigned` | Layer tag for hierarchy pathing. |
| `app` | String | Yes | `global` | App tag for hierarchy pathing. |
| `homologate` | Boolean | No | `false` | If true, migrates legacy MD files to /docs/. |

## 1. Directory Tree Protocol
The skill MUST instantiate the following physical paths:
1. `/docs/roadmaps/{layer}/{app}/`
2. `/docs/sprints/{layer}/{app}/`
3. `/docs/architecture/`
4. `/docs/contracts/`

## 2. Integrity Signatures
The skill is responsible for injecting the **Sync-Lock** verification signature.
- **Trigger**: Successful tree injection.
- **Action**: Update `docs/architecture/matrix_topology_map.md`.
