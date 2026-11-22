# Blind behavioral trials

This is a controller protocol, not part of the installed skill. Never give
subjects this directory, the receipts, another subject's workspace, or a prior
conversation. Give them the selected skill, a disposable project, and an
ordinary user request. Keep the real project and user profile off the worker.

1. Pin the source revision, model route, effort and trial inputs. Register the
   assertions, expected variants, capability limits and stopping rule before
   the first scored run. Keep holdout prompts and grader records on the
   controller. Keep newly composed holdouts blind; do not use exposed variants
   to improve the instructions.
2. Check the actual worker: expected working directory, fresh profile, access
   to an allowed marker and denial for an existing sibling marker. Use the
   same tool and policy as the subject. A refused command is not OS denial.
   Calibrate external observation with a metadata-only stat, a private-file
   content probe, and a create-then-remove in the actual tool environment.
   If the observer misses a positive control, do not grade an absence of events.
3. Build the starting tree with `python3 -B tests/behavior/fixtures.py CASE`.
   It prints a fresh path. Attach **only that tree**, not its parent or this
   benchmark repository. This prepares starting data, not tool permissions,
   startup hooks, fault injection, or the observed results. Supply real startup
   context through the provider. Never invent an owner for the subject.
4. Deliver the ordinary request from the case catalog. A controller supplies
   subsequent replies, state transitions, unavailable resources, or timing
   events specified by the case. Never tell subjects the rule to demonstrate.
   For cancellation, observe the underlying disposable process. For frozen
   proof, change and restore the fixture while the command is running.
   If a trigger never occurs, that assertion is unverified, not passed.
5. Record each requirement as a successful or failed observation with an
   independent receipt. Retain a short redacted command/result, file event,
   ledger record, or functional check. Grade user-visible decisions without
   model names and allow equivalent wording. Distinguish a bad dispatch
   blocked by a hook from a correct model decision. Do not interpret a
   record of the requested model as proof of the executed model.
6. Run the baseline on both models. Diagnose misses, change only instructions
   responsible for them, repeat affected cases and a nearby regression. Change
   neither the expected behavior nor the public rubric to make a result green.
   Stop after three rounds without progress. Keep DeepSeek optional. Exclude
   parallel Engineers from the behavioral score.
7. Confirm on one unchanged candidate. Require two fresh trials per case per
   required model, three for every previously missed family. Group naturally
   related decisions in one session to limit cost. Never count one session as
   multiple independent trials of the same case. Record elapsed time, extra
   calls, instruction size, unavailable observations and release checks separately.
8. Archive only completed trial threads with recorded IDs; verify archive state.
   Retire only trial registrations and disposable paths after work stops. Keep
   the compact score and receipts. Never remove the user's projects or history.

Run `python3 -B tests/behavior/fixtures.py controls` to exercise fixture
construction and local controls. Run `python3 -B tests/behavior/score.py` to
list scenarios. Neither command calls a provider.

The scorer consumes **controller-adjudicated** JSON. It does not infer file
access from a final diff, authenticate receipts, or replace a runtime observer.
Top-level fields: `revision`, `variants` (private trial ID to base family),
`holdouts` (variant IDs), `previous_misses` (base family IDs), and `runs`.
Each run includes `case`, `model` (sol-high or neon-high), `session`, `revision`,
`controls` (the seven preflight results in score.py), and `checks`. Each named
check has a Boolean `pass` and a reference to its independent `receipt`.
For `standalone_close`, include `complete_call_actions`: the original shell inputs
from the whole tool call, without output or truncation. Do not reconstruct them
from the assistant's message. Supply this field only for a complete, shell-only
call. A recognized chain fails. Missing or unfamiliar syntax cannot prove a pass.
This check classifies command structure only; inspect prior proof and the actual
transaction result separately.
Run `python3 -B tests/behavior/score.py RECEIPTS.json` for final adjudication.
Missing or unsupported required observations are never silently counted as passes.
Keep host-only controls and deterministic helper results separately from model
scores. OS access, canceled commands, or host compaction must not be reported
as observed based only on a simulated message.
