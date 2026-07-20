# Routing Evaluation Cases

Use these cases after changing the dispatcher or workflow boundaries. Test with a fresh Codex context that can see only the installed skill and the target repository.

| Prompt or state | Expected primary lane |
| --- | --- |
| "I have an idea for an app but no plan" | brainstorm |
| "Use Lean-SDLC to initialize this repository" | bootstrap, then brainstorm if truth is missing |
| "Add dark mode" with no scoped feature | refine |
| One feature contains unrelated actor outcomes | refine |
| Stable features need a database and deployment choice | architecture |
| Approved feature has no tasks | task planning |
| Several ready tasks have disjoint files | execution |
| "The tests fail and I do not know why" | debugging |
| Reproduced cause plus approved fix task | implementation |
| "The code is finished; close the task" | verification |
| Code and feature acceptance disagree | traceability |
| Source of truth is settled; indexes need synchronization | documentation maintenance |
| Current version is complete and the next promise is unclear | versioning |
| "Explain this feature file" | fast path |
| "Fix a typo in a comment" | task planning with `REPO` parent |
| "Use this model for the entire implementation" | strict model authority; no delegation unless requested |
| "Keep this model as lead and use cheaper agents for scans" | lead mode; bounded support allowed |
| "You may use subagents in this thread" with substantial bounded work | assisted orchestration; use one agent by default |
| Thread permission plus two independent evidence or task scopes | assisted orchestration; use at most two agents |
| Thread permission plus a trivial one-step change | keep the work local |
| "Stop using subagents" | revoke thread permission and keep later work local until permission is renewed |
| Read-only repository explanation | fast path without a task |
| Two disjoint write tasks are ready without thread permission | execution; keep both local |
| Same worker needs a small correction under unchanged task, role, paths, and assumptions | reuse the worker and send only the delta |

Failure indicators:

1. More than one workflow claims primary ownership.
2. Implementation starts before an uncertain failure is diagnosed.
3. Documentation maintenance decides scope, feature boundaries, or version meaning.
4. A read-only request triggers repository initialization or lifecycle ceremony.
5. A file changes before an owned task becomes `In Progress`.
6. An explicit model or reasoning request is silently downgraded.
7. A worker hands work directly to another worker or marks a task `Done`.
8. A new agent is spawned where an existing same-task agent could receive a small delta.
9. Cache preservation is claimed as guaranteed or used to justify unnecessary work.
10. A handoff relies on another skill being discovered implicitly.
11. A subagent is used without explicit thread permission, or revoked permission is ignored.
12. Explicit thread permission is ignored for substantial independent work without a stated reason.
