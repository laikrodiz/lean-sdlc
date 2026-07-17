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
| "Fix a typo in a comment" | fast path unless meaning changes |

Failure indicators:

1. More than one workflow claims primary ownership.
2. Implementation starts before an uncertain failure is diagnosed.
3. Documentation maintenance decides scope, feature boundaries, or version meaning.
4. A read-only request triggers repository initialization or lifecycle ceremony.
5. A handoff relies on another skill being discovered implicitly.
