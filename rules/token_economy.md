# Rule Context: Token Economy

Single reference for context-window economics. Consolidates the token-saving mandates previously scattered across `agents.md §2`, `token-saver-auditor`, `omni-context-minimizer`, and `graphify`. The `Token-Saver Auditor` skill enforces this rule when reviewing plans.

## 1. The Decision Ladder (cheapest first)
Before touching any source file, descend this ladder and stop at the first rung that answers the question:

| Rung | Tool | When | Approx. cost |
| :--- | :--- | :--- | :--- |
| **1. Graph query** | `graphify query "<question>"` / MCP `query_graph` | Architecture, relationships, "where is X used" | Scoped subgraph, smallest |
| **2. AST skeleton** | `omni_minimizer.py <file>` | Structure of one large file (classes, signatures) | ~10% of the file |
| **3. Targeted partial read** | `Read` with offset/limit, or `ripgrep` on the symbol | Inspecting one known function/range | Only the affected lines |
| **4. Full read** | `Read` entire file | Files **<200 lines only** | Full file |

Full-dumping a file >200 lines is PROHIBITED (`agents.md §2 token_saver`). Skipping rungs is only justified when a prior rung already returned the exact line range.

**Scope limit — the ladder governs discovery, never editing.** Rungs 1-3 answer *where* something is. They are not a substitute for reading the range you are about to modify: **the lines being edited are read first, every time**, and a graph query or a symbol grep does not discharge that. Without this limit the rule reads as licence to edit code nobody looked at, which is the most expensive kind of cheap.

## 2. Plan-level Economics (enforced by Token-Saver Auditor)
- **1-Agent : 1-File**: subagent prompts receive the exact filename and line range — never "review the whole system".
- **No raw data dumps**: CSV/JSON datasets are summarized via a throwaway script (`.head()`, `.info()`), never pasted into context.
- **Delegate search to heuristics**: `ripgrep`/graph queries over manual directory crawling; recursive `list_dir` over an indexed tree is rejected (`topology_map.md` Discovery Lock).

## 3. Session-level Economics
- **Constitution loads once**: `agents.md` auto-loads via the host `CLAUDE.md` import; re-read it only after context compaction (`agents.md §2 anti_amnesia`), not per execution step.
- **State over rediscovery**: `docs/active_state.json` and `graphify-out/graph.json` are the memory — re-deriving what they already record is a violation, not diligence.
- **Workflows are lazy-loaded**: protocols live behind `/agents:*` commands and are only pulled into context when invoked.

### 3.1 The session bound — binding, and measured per context cycle

**Unit: the ratio of a turn's `cache_read` against the first turn of the current context cycle**, never of the session. Self-calibrating per project — a large repository starts with more base context, but "10× your first turn" means the same everywhere, and nothing is configured per host.

| Threshold | Trigger | Action |
| :--- | :--- | :--- |
| **Soft** | turn > **5×** the cycle's first | Declare remaining cost in the plan's **Cost** section (work units left, delegation mode). `session_probe.py` surfaces the breach at the next start. Calibration may still record-only while the baseline builds |
| **Hard** | turn > **15×** the cycle's first | No new work starts. Sprint complete → close it; sprint open → **suspend** (`session_state.py suspend`) and continue in a fresh session. Declare Cost before the next claim |

**Portable Cost half (Cursor and Claude).** Every Implementation Plan from Sprint
030 onward carries a **Cost** section: work-unit count, `delegation_mode`, and —
when a Claude transcript exists for this tool — the prior cycle ratio from
`python3 scripts/session_cost.py --from-anchor`. Cursor sessions must not invent
`cache_read` from Claude jsonl files; the plan Cost section is the half that
always runs. Structural plan wastes are rejected by
`skills/token-saver-auditor/scripts/audit_plan.py` (exit `2`).

**Why the cycle and not the session.** A session is a **sawtooth**: compaction rebuilds the window from a summary and `cache_read` collapses back to the start-up cost. Measured over one full session of this repository — four cycles, peaks of 849K, 995K, 361K and 631K against reset points of **22,174 tokens, identical three times** — a ratio taken against the session's first turn would collapse at the first reset and never fire again.

**Compaction is not a cost control, and this rule exists because of that.** Those four resets happened and the session still spent 423M `cache_read`. Cycle 2 is the proof: **113 messages cost 99.5M**, nearly matching a 414-message cycle, because it climbed to 995K. **Cost tracks peak height, not message count** — cost is the area under the sawtooth, and compaction only resets the x axis.

**Break-even is an observed constant, not an estimate.** Restarting costs ~22K, measured identically three times. The hard threshold would have fired in **3 of those 4 cycles**.

**Calibration that does not destroy its own data.** A binding hard threshold means the sprint always closes at the bound and the natural close is never observed. So the soft threshold **records and does not act** while the distribution builds, and the hard one records `forced: true` plus whether `task_scope.md` still held unfinished work. A forced close with pending work is the "too tight" signal; one on a complete sprint is not.

**Provenance: n=1**, and of one kind — intensive planning, many reads, little code execution. A file-editing sprint will have a different curve. `scripts/session_cost.py --json` is the reproducing command; a figure without it is memory, not evidence.

## 4. Tool-Result Economics

`§3` forbids re-deriving state that is already recorded. This section is about the other accumulation: tool call/response pairs piling up across a long session.

**The finding that reframes this whole rule.** Retaining full history is not expensive-but-safe; it is expensive **and less accurate**. Measured on a 50-task tool-using benchmark (*"Less Context, Better Agents"*, arXiv 2606.10209): full history completed **71.0%** of tasks using 1.48M tokens; pruning to the last 5 tool calls reached **79.0%** with 535K; pruning plus summarisation reached **91.6%** with 553K. Roughly **−63% tokens and +20 points of task completion**. Old tool results describe superseded states, and an agent reading them assigns values to fields that have already changed.

So token economy is not only about cost. It preserves accuracy, and that is the stronger argument for it.

**What is actually controllable here**, stated plainly because the alternative is a rule the framework cannot execute: Claude Code manages its own context window and compaction — this rule cannot prune it. It governs what the agent *adds back*:
- **Do not re-emit a tool result already in the session.** Re-running a command to re-read its output is re-derivation (`§3`).
- **Do not re-read a file already read this session** unless it changed.
- **What crosses a compaction boundary is the state anchor plus `task_scope.md`, never the raw log.** Those two are the summary; reconstructing from transcript is what the anchor exists to prevent.

## 5. Output Economics
- Markdown tables over prose for data (`agents.md §1 technical_clarity`); no redundant greetings; Mermaid/ASCII restricted to where a diagram genuinely replaces more text than it costs.
