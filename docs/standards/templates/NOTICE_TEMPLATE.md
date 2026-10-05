# NOTICE — Third-Party Licenses
**File**: `NOTICE.md` (repository root)
**Template**: `docs/standards/templates/NOTICE_TEMPLATE.md`
**Last reviewed**: {{ISO_DATE}} at sprint {{SPRINT_ID}}

> [!IMPORTANT]
> The attribution text in this file is a **legal statement** and is authored by a human. An agent MUST NOT generate, infer, or "complete" a license name, a copyright holder, or an upstream URL from memory or from a similar-looking component. Every value in the tables below is copied from the upstream license file or the upstream repository by a human who then verifies it. A value that is not verified stays in the "Unverified" section (Section 4), never in a component table.

---

## 1. When this file is required

| Situation | `NOTICE.md` | Recorded answer at close (`close_workflow.md` `repo_docs_check`) |
| :--- | :--- | :--- |
| The repository vendors third-party content under a license other than its own: copied source files, skills, assets, fonts, datasets, or templates placed in the tree | **Required** | `present` and reviewed at this sprint |
| The only third-party code is declared in a package-manager lockfile (`pnpm-lock.yaml`, `requirements*.txt`, `poetry.lock`, `package-lock.json`) and nothing from it is copied into the tree | **Not required** | `not applicable` |
| The repository vendors third-party content, and this sprint added, removed, or re-versioned a component | **Required, and updated in this sprint** | `present` and `updated` |

"Not applicable" is a recorded answer, not an omission: the close records it explicitly so a later reader can tell a reviewed "no" from a forgotten check. Do not create an empty `NOTICE.md` to satisfy a presence check.

---

## 2. Preamble

This repository is distributed under {{OWN_LICENSE}} (`{{OWN_LICENSE_FILE}}`), except for the vendored components listed below, which retain their own original license. Each component carries its own license file or attribution inside its directory where the upstream license requires it; this file discloses the mixed licensing at the top level as well.

---

## 3. Vendored components

One row per component. A component is a directory or file set that came from one upstream source at one upstream version. Two components from the same upstream repository at different versions are two rows.

| Component | Path in this repository | Upstream source (URL) | Upstream commit or version | License (SPDX id) | Copyright holder | Local modifications |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| {{COMPONENT_NAME}} | `{{PATH_IN_REPOSITORY}}` | {{UPSTREAM_URL}} | `{{UPSTREAM_COMMIT_OR_VERSION}}` | {{SPDX_LICENSE_ID}} | {{COPYRIGHT_HOLDER}} | {{NONE_OR_ONE_LINE_DESCRIPTION_AND_COMMIT}} |

Column rules:

| Column | Constraint |
| :--- | :--- |
| Path in this repository | Relative path, no absolute paths (`agents.md` §1 `path_type`). It must exist: a row pointing at a deleted path is stale and is removed in the same change that deleted the path |
| Upstream source (URL) | The repository or package page the content was copied from, not a mirror or a search result |
| Upstream commit or version | A full commit SHA or a release tag. `latest` and `main` are not acceptable: they name no fixed content |
| License (SPDX id) | The identifier from the upstream license file (for example `MIT`, `Apache-2.0`), copied by a human from that file |
| Copyright holder | The name in the upstream copyright line, copied verbatim |
| Local modifications | `None`, or one line stating what was changed and the commit that changed it. Apache-2.0 and similar licenses require modified files to carry notice of the change |

---

## 4. Unverified components

Components whose license or provenance has not been confirmed against the upstream source. They are tracked here, are not covered by this notice, and each one names who verifies it.

| Component | Path in this repository | What is unverified | Verifier |
| :--- | :--- | :--- | :--- |
| {{COMPONENT_NAME}} | `{{PATH_IN_REPOSITORY}}` | {{LICENSE_OR_PROVENANCE_OR_BOTH}} | {{HUMAN_NAME}} |

If there are none, replace the table with the single line `None.`

---

## 5. Worked example

The nucleus's own `NOTICE.md` (repository root of `.agents`) is the worked example of this template: one table of vendored skills, each with its license and origin, plus a pointer to the audit file that tracks unverified provenance. Read it before filling this template for the first time.

## 6. Maintenance

- [ ] Every row's path in Section 3 exists in the tree (`ls {{PATH_IN_REPOSITORY}}`).
- [ ] Every license and copyright holder was copied by a human from the upstream license file, not generated.
- [ ] A component added, removed, or re-versioned in this sprint is reflected above (`close_workflow.md` `repo_docs_check`).
- [ ] If the repository vendors nothing, this file does not exist and the close recorded `not applicable`.
