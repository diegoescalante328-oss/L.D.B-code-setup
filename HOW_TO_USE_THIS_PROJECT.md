# HOW TO USE THIS PROJECT

## Purpose of this file

This file is the practical operator manual for this repository.

Use it when you want to understand how to actually run work through this system, not just what files exist. It explains how the repository is meant to be used, how tasks should move through it, when to use each template, how planning fits in, how validation fits in, and what good completion looks like.

This file is the bridge between:

- `README.md` for project overview
- `AGENTS.md` for top-level operating rules
- protocol docs for detailed workflow
- standards docs for quality requirements
- templates for structured inputs and outputs
- examples for reference patterns
- GitHub templates for issue and PR flow

---

# 1. What this project is

This repository is a Codex-first project operating system.

It is designed to help a human and Codex work together in a repeatable, disciplined way across many tasks and many projects without rewriting the same instructions every time.

The repository gives you:

- a top-level operating model
- a staged execution workflow
- planning structure for larger work
- validation expectations
- documentation expectations
- completion and handoff structure
- reusable templates
- example artifacts
- issue and pull request support

The goal is to reduce prompt repetition, improve consistency, prevent scope drift, improve validation discipline, and make final outputs easier to review.

This repository is not just a folder of templates. It is a system for running work.

---

# 2. Who this project is for

This project is for:

- a solo developer or operator using Codex repeatedly
- a person who wants a structured way to run project work through GitHub and Codex
- someone who wants tasks to be better scoped before implementation starts
- someone who wants stronger validation and handoff
- someone who wants the repository itself to carry the instructions instead of repeating them in every prompt
- someone who wants a reusable execution framework instead of one-off task prompts

This project is especially useful when tasks vary in size and risk and you want a system that handles both quick changes and larger multi-step work.

---

# 3. How to think about this repository

The easiest way to understand this project is to think of each part as having a specific job.

## `AGENTS.md`
This is the top-level operating rule file for Codex.

It tells Codex how to behave in this repository. It should stay concise and operational. It does not hold every detail. It enforces the main workflow, routing, and discipline rules.

## Protocol docs
These define the actual execution process in detail.

They explain the staged workflow, task classes, planning requirements, failure handling, and recovery rules.

## Standards docs
These define quality expectations.

They explain what good validation looks like, what good documentation looks like, what coding behavior should look like, and what safety expectations apply.

## Templates
These are structured starting points.

Use them to define new tasks, create plans, write completion reports, and standardize issues and pull requests.

## Examples
These show what good usage looks like in practice.

Use them as models, not as blind copy-paste truth.

## Plans
This is where active execution planning lives for non-trivial or high-risk work.

Plans make larger tasks more specific before implementation begins.

## Reports
These define how work is handed off at the end.

They help ensure final outputs are structured, honest, and reviewable.

## GitHub templates
These support the issue and pull request workflow.

They help turn requests into structured inputs and make reviews more consistent.

---

# 4. Recommended order to read the repository

Use this reading order when you are new to the repository or returning after time away.

## First pass
1. `README.md`
2. `HOW_TO_USE_THIS_PROJECT.md`
3. `AGENTS.md`

## Second pass
4. the project profile document under `docs/` if one exists
5. `docs/protocols/project_execution_protocol.md`
6. `docs/protocols/stage_definitions.md`
7. `docs/protocols/failure_and_recovery.md`

## Third pass
8. `docs/standards/validation_matrix.md`
9. `docs/standards/coding_rules.md`
10. `docs/standards/documentation_rules.md`
11. `docs/standards/security_rules.md`

## Fourth pass
12. `docs/templates/project_intake_template.md`
13. `docs/templates/codex_task_template.md`
14. `docs/templates/execplan_template.md`
15. `docs/reports/completion_report_template.md`

## Fifth pass
16. example artifacts, if present
17. `.github/ISSUE_TEMPLATE/`
18. `.github/pull_request_template.md`

Use this order because it moves from overview, to operating rules, to process, to standards, to templates, to examples.

---

# 5. Top-level map of the repository

This section explains how the major parts are supposed to be used.

## `README.md`
Use this for a broad overview of the repository.

Read it first when you need the big picture.

## `HOW_TO_USE_THIS_PROJECT.md`
Use this file as the practical manual.

Read it when you want to know how to operate the system correctly.

## `AGENTS.md`
Use this as the top-level rule file for Codex.

When prompting Codex, you should usually tell it to follow `AGENTS.md`.

## `PLANS.md` if present
If the repository includes a top-level `PLANS.md`, use it as the high-level guide for how planning works in this repository.

It should explain when a plan is required, where plans live, and how plans relate to execution.

## `docs/protocols/`
Use this folder for the detailed workflow model.

These files define the stages, task classes, and failure / recovery expectations.

## `docs/standards/`
Use this folder for quality requirements.

These files define what validation, documentation, coding discipline, and security-aware behavior should look like.

## `docs/templates/`
Use this folder when starting new work or when shaping outputs.

These files are the reusable structures for intake, task prompting, planning, and reporting.

## `docs/reports/`
Use this folder for the final reporting structure.

This is what a good handoff should align to.

## Example artifact locations
If the repository includes example artifacts, use them as reference models for how to fill out the templates and how the workflow should look in practice.

Examples should support the templates, not replace them.

## `plans/active/`
Use this for active plans for current non-trivial or high-risk work.

If the repository uses ExecPlans, this is usually where they should live.

## `.github/`
Use this folder for GitHub-native workflow support.

Issue templates help define work. The PR template helps standardize reviews and validation reporting.

---

# 6. Quick start in 5 minutes

If you want the fastest correct way to use this repository, do this:

## For a small task
1. Read `AGENTS.md`
2. Check `docs/protocols/stage_definitions.md` to confirm the task is actually small
3. Define the task clearly with scope, success criteria, and validation expectations
4. Prompt Codex to follow `AGENTS.md` and complete the task
5. Require a final handoff with files changed, commands run, validation results, risks, and follow-up recommendations

## For a non-trivial task
1. Read `AGENTS.md`
2. Confirm the task is non-trivial using `docs/protocols/stage_definitions.md`
3. Create a plan using the repository planning system
4. Place the plan in the correct location, usually `plans/active/`
5. Have Codex follow the plan and `AGENTS.md`
6. Require validation and a structured completion report

## For a high-risk task
1. Read `AGENTS.md`
2. Confirm the task is high-risk using `docs/protocols/stage_definitions.md`
3. Create a plan before implementation
4. Include rollback and recovery notes
5. Require stronger validation and careful stop-condition handling
6. Require a very explicit final report

---

# 7. Which file do I use?

Use this section as a decision guide.

| Situation | What to use first | What to use next |
|---|---|---|
| I need the big picture | `README.md` | `HOW_TO_USE_THIS_PROJECT.md` |
| I need to know how Codex should behave | `AGENTS.md` | protocol docs |
| I am starting a new task | `docs/templates/project_intake_template.md` or `docs/templates/codex_task_template.md` | task classification docs |
| I am doing non-trivial work | planning system (`PLANS.md` if present, otherwise ExecPlan template) | `plans/active/` |
| I need to know whether a task is small or risky | `docs/protocols/stage_definitions.md` | `docs/protocols/project_execution_protocol.md` |
| I need to know how to validate work | `docs/standards/validation_matrix.md` | PR template and completion report template |
| I need to know how to report completion | `docs/reports/completion_report_template.md` | `.github/pull_request_template.md` |
| I want to see a good example | example artifacts | corresponding templates |
| I want to change the system itself | `AGENTS.md`, protocol docs, standards docs, templates, examples, or project profile depending on the type of change | this file |

---

# 8. How to start a new task

This repository works best when you begin by defining the task clearly.

## Step 1: Define the task
Write down:
- what the task is
- why it exists
- what the current state is
- what the desired end state is

## Step 2: Define scope
List:
- what is in scope
- what is out of scope
- any constraints
- any forbidden changes

## Step 3: Define quality expectations
List:
- success criteria
- failure criteria
- validation commands or validation expectations
- any documentation updates that may be needed

## Step 4: Classify the task
Use `docs/protocols/stage_definitions.md` to decide whether the task is:
- small
- non-trivial
- high-risk

## Step 5: Choose the right starting structure
Use one of these:

### Use the project intake template when
- you are scoping work before handing it to Codex
- the task is not yet fully shaped
- you want a structured planning input

### Use the Codex task template when
- the task is ready to delegate directly
- you already know the scope and validation expectations

### Use an issue template when
- you want the task to live as a GitHub issue
- you want the task request itself to be structured and reviewable

## Step 6: Decide whether planning is required
Use the planning system if the task is non-trivial or high-risk.

## Step 7: Delegate the task correctly
Tell Codex to follow `AGENTS.md`, and where relevant, the active plan.

---

# 9. How to handle a small task

Small tasks should move quickly, but not carelessly.

## What counts as a small task
Use `docs/protocols/stage_definitions.md` as the source of truth, but in general a small task:
- affects only a few files
- does not change architecture
- does not introduce new dependencies
- does not require schema or config changes
- has a low blast radius
- has straightforward validation

## What to do
1. Confirm the task is truly small
2. Define the objective, scope, and validation
3. Prompt Codex to follow `AGENTS.md`
4. Have Codex perform Discovery, focused Implementation, Validation, and Handoff
5. Review the final output

## Is an ExecPlan required?
Usually no.

A small task should not be forced through heavy planning unless the task reveals hidden risk or ambiguity after Discovery.

## What level of validation is expected?
Only the validation that actually applies, but it still must be explicit.

Examples:
- a doc-only change may only need a manual review
- a small code change may need lint, tests, or a focused smoke check
- a template wording change may need consistency checks against related files

## What final output should be required?
Even for a small task, require:
- summary
- files changed
- commands run
- validation results
- known risks
- follow-up recommendations

---

# 10. How to handle a non-trivial task

Non-trivial tasks are where this repository becomes most valuable.

## What counts as a non-trivial task
Use `docs/protocols/stage_definitions.md` as the source of truth, but in general a non-trivial task:
- affects multiple files
- changes interfaces, structure, or workflow
- increases blast radius
- has more than one implementation step
- benefits from an explicit plan before implementation

## Why stronger planning is needed
Without a plan, non-trivial work is more likely to:
- drift in scope
- miss related files
- skip validation
- produce weaker handoff
- introduce partially thought-through changes

## What to do
1. Define the task clearly
2. Confirm the task is non-trivial
3. Create a plan using the repository planning system
4. Put the plan in the correct location
5. Require Codex to use the plan and `AGENTS.md`
6. Require validation against the plan
7. Require the final handoff to report against the plan

## What a good plan should do
A good plan should:
- define the objective
- define the start point and end point
- define scope
- identify target files
- identify risks
- define validation
- define done criteria
- define rollback notes when relevant

## Where plans live
Use the repository’s actual planning system.

Typically:
- active plans live in `plans/active/`
- plan structure comes from `docs/templates/execplan_template.md`
- a planning guide may live in `PLANS.md` if present

## How the plan constrains implementation
The plan should limit implementation drift by making clear:
- which files are expected to change
- what the ordered steps are
- what success looks like
- what risks must be watched
- what validation must happen

## How validation and handoff connect to the plan
The completion report should show whether the task met the plan’s objective, validation expectations, and done definition.

---

# 11. How to handle a high-risk task

High-risk tasks require more control.

## What counts as high-risk
Use `docs/protocols/stage_definitions.md` as the source of truth, but high-risk work commonly includes:
- destructive changes
- auth or permissions changes
- deployment-sensitive changes
- config-sensitive changes
- file movement or data movement
- schema or migration work
- security-sensitive surfaces

## Why stronger controls are needed
High-risk work is more likely to cause:
- hard-to-reverse damage
- incomplete recovery
- validation blind spots
- unsafe guessing
- misleading completion claims

## What to do
1. Confirm the task is high-risk
2. Create a plan before implementation
3. Include rollback and recovery notes
4. Identify stop conditions explicitly
5. Require stronger validation
6. Require a careful final report

## What to include in the plan
A high-risk plan should include:
- exact objective
- exact target files or surfaces
- risk notes
- rollback trigger
- rollback action
- irreversible consequences if any
- validation plan
- done definition
- stop conditions

## Validation expectations
Validation should be stronger and more explicit than for normal work.

Use the validation matrix and include any applicable:
- tests
- lint
- typecheck
- build
- manual checks
- targeted smoke checks
- rollback verification if relevant

## Safety rule
For high-risk tasks, Codex should stop rather than guess if required information is missing.

---

# 12. How to use the planning system

This repository is designed so larger work is shaped before implementation begins.

## The purpose of planning
Planning is used to make non-trivial or high-risk work more specific, safer, and easier to review.

A plan should reduce ambiguity and constrain implementation.

## When to create a plan
Create a plan when:
- the task is non-trivial
- the task is high-risk
- multiple files are likely to change
- scope is not obvious
- there are interface, config, or structure implications
- rollback needs to be thought through
- validation needs to be defined before coding

## Where to put the plan
Use the repository’s active planning location.

Typically:
- active plans go in `plans/active/`

## What template to use
Use:
- `docs/templates/execplan_template.md`

If the repository includes a top-level `PLANS.md`, read that first to understand the planning rules for this repository.

## What fields matter most
A strong plan should clearly define:
- task
- objective
- start point
- end point
- scope
- constraints
- target files
- risks
- design contract
- implementation plan
- validation plan
- rollback / recovery
- done definition
- final report requirements

## How plans relate to implementation
Codex should not treat the plan as optional decoration.

The plan should actively shape:
- what gets changed
- what does not get changed
- how work is sequenced
- what validation is run
- how completion is judged

## How plans relate to reporting
The final report should show whether the work met:
- the objective
- the validation plan
- the done definition
- any rollback or recovery expectations if relevant

## How to keep plans useful
Good plans are:
- specific
- scoped
- operational
- honest about risks
- short enough to be usable
- detailed enough to prevent drift

Bad plans are:
- vague
- bloated
- missing file targets
- missing validation
- missing done criteria
- disconnected from implementation

---

# 13. How to use the templates

Templates are not bureaucracy. They are structure.

Use them to reduce ambiguity and standardize the inputs and outputs of work.

## `docs/templates/project_intake_template.md`
Use this when you are shaping work before delegation.

Use it for:
- defining a task clearly
- identifying scope
- identifying constraints
- identifying success and failure criteria
- identifying validation expectations

Do not use it as a final report.

## `docs/templates/codex_task_template.md`
Use this when the task is ready to hand directly to Codex.

Use it for:
- clearly framed execution requests
- structured delegation
- direct Codex prompting

Do not use it as a planning document for larger work unless the task is actually small.

## `docs/templates/execplan_template.md`
Use this when a task requires a plan.

Use it for:
- non-trivial work
- high-risk work
- work with multiple steps or multiple files
- work where validation and rollback must be defined before implementation

Do not use it for trivial changes unless the task reveals unexpected complexity.

## `docs/reports/completion_report_template.md`
Use this at the end of work.

Use it for:
- structured handoff
- clear reporting
- documenting validation results
- documenting known risks
- documenting what still needs follow-up

Do not use it as a substitute for a plan.

## GitHub issue templates
Use these when the task should start as a GitHub issue.

### Feature request template
Use for new functionality or behavior improvements.

### Bugfix request template
Use for broken behavior that should be corrected.

### Refactor request template
Use for internal cleanup or structural improvement where the behavior target is not primarily a new feature.

## `.github/pull_request_template.md`
Use this when opening or reviewing a PR.

It should align with the validation matrix and completion report expectations.

Do not use it as the only record of planning for non-trivial work.

---

# 14. How to use the examples

If example artifacts exist in this repository, use them as reference models.

Examples are useful because they show:
- what good scope looks like
- what good success criteria look like
- what good validation reporting looks like
- what good completion reporting looks like

## How to use them correctly
Use examples to:
- see the expected shape of a good artifact
- understand how the repository vocabulary is used
- model tone and level of detail
- compare your own task artifacts against a good reference

## How not to use them
Do not:
- copy examples blindly
- assume every example fits every task
- treat example file contents as permanent policy
- use examples to override the templates or standards

Examples are models, not law.

---

# 15. How Codex should be used with this repository

This repository is built so Codex can operate with less repeated prompting and stronger repository-native guidance.

## Core rule
When delegating work, tell Codex to follow `AGENTS.md`.

That should be the default.

## For small tasks
A prompt can usually be short if the task is well-defined.

Example:

> Follow `AGENTS.md` and implement this small task.  
> Objective: [state objective]  
> Scope: [state scope]  
> Validation: [state expected validation]

## For non-trivial tasks
A prompt should reference both `AGENTS.md` and the plan.

Example:

> Follow `AGENTS.md` and use the active ExecPlan in `plans/active/[file].md`.  
> Complete the task within scope, run the defined validation, and return a full completion report.

## For high-risk tasks
A prompt should emphasize the plan, stop conditions, rollback expectations, and validation.

Example:

> Follow `AGENTS.md` and the active ExecPlan.  
> This is high-risk work.  
> Respect stop conditions, do not guess past blockers, honor rollback notes, run the validation plan, and return a structured completion report.

## What this repository is trying to prevent
This repository is designed to prevent:
- rewriting the same workflow rules in every prompt
- weak or missing planning
- vague task definitions
- undocumented scope expansion
- missing validation
- weak final handoff

## What this repository is trying to encourage
It encourages:
- repo-native instructions
- disciplined planning
- explicit validation
- honest final reporting
- repeated use with less friction

---

# 16. Sample prompts to give Codex

Use these as starting patterns.

## Small task prompt
> Follow `AGENTS.md` and complete this task.  
> Task: [task name]  
> Objective: [objective]  
> In Scope: [scope]  
> Out of Scope: [out of scope]  
> Validation: [validation expectations]  
> Return a final handoff with summary, files changed, commands run, validation results, known risks, and follow-up recommendations.

## Non-trivial task prompt
> Follow `AGENTS.md`.  
> This is non-trivial work. Create or update an ExecPlan if needed, then execute within scope.  
> Task: [task name]  
> Objective: [objective]  
> Constraints: [constraints]  
> Use the repository planning system, run the relevant validation, update docs if behavior changes, and return a full completion report.

## High-risk task prompt
> Follow `AGENTS.md`.  
> This is high-risk work. Use the planning system before implementation.  
> Respect stop conditions. Include rollback and recovery notes.  
> Do not guess past blockers.  
> Run the defined validation and return a structured completion report with risks and any remaining gaps.

---

# 17. What good final output looks like

A good final output should be structured and reviewable.

It should typically include:

## Summary
What was done and why.

## Objective Status
Whether the task was completed, partially completed, or blocked.

## Files Changed
Exactly which files were created or updated.

## Commands Run
What validation or support commands were run.

## Validation Results
What passed, what failed, and what was not run.

## Documentation Updated
Which docs were updated if behavior, setup, or limitations changed.

## Known Risks
What risks remain.

## Follow-Up Recommendations
What should happen next.

## Notes on Blockers or Partial Completion
If the task was not fully completed, say why honestly.

This should align with:
- `AGENTS.md`
- the completion report template
- the validation matrix
- the PR template

---

# 18. Task lifecycle walkthrough

This section shows how work should flow through the system.

## Small task lifecycle
1. Define the task
2. Confirm it is small
3. Give Codex a structured prompt that references `AGENTS.md`
4. Have Codex perform focused Discovery and Implementation
5. Validate appropriately
6. Review the final handoff

## Non-trivial task lifecycle
1. Define the task
2. Confirm it is non-trivial
3. Create an ExecPlan
4. Store the plan in the active plans location
5. Have Codex execute within the plan and `AGENTS.md`
6. Validate using the plan and validation matrix
7. Review the completion report
8. Open or review a PR if needed

## High-risk task lifecycle
1. Define the task
2. Confirm it is high-risk
3. Create a plan before implementation
4. Add rollback / recovery notes
5. Confirm stop conditions
6. Have Codex execute conservatively
7. Perform stronger validation
8. Review the completion report carefully before merging or accepting the work

---

# 19. Common mistakes to avoid

These are the most common ways to misuse the repository.

## Skipping planning for non-trivial work
This increases drift and weakens validation.

## Making `AGENTS.md` too large
`AGENTS.md` should stay concise. Put detail in docs.

## Duplicating policy across many files
If the same rules are repeated everywhere, the system becomes harder to maintain.

## Failing to define validation
Tasks should not be delegated without some validation expectation.

## Vague success criteria
If success is vague, completion reporting becomes weak and misleading.

## Ignoring failure criteria
Failure criteria help define boundaries and keep work honest.

## Letting scope drift
A focused task should remain focused unless correctness or risk reduction requires expansion.

## Treating examples as copy-paste truth
Examples are models, not fixed answers.

## Claiming validation that was not run
All reporting must be honest.

## Treating templates as bureaucracy
Templates are meant to reduce ambiguity and improve repeated execution.

---

# 20. Recommended repeated-use workflow

This repository is meant to be used repeatedly, not once.

Use this loop:

1. Intake the task
2. Classify the task
3. Create a plan if needed
4. Delegate to Codex using `AGENTS.md`
5. Validate the work
6. Review the completion report
7. Update documentation if needed
8. Improve the system when recurring weaknesses appear

This is what makes the repository act like an operating system for ongoing work.

It should get better over time as:
- templates improve
- examples improve
- weak routing gets fixed
- ambiguous language gets clarified
- repeated patterns are pushed into the repo instead of restated in prompts

---

# 21. Where to update the system itself

Different kinds of improvements belong in different places.

## Update `AGENTS.md` when
You need to change recurring top-level operating rules for Codex.

Do not put one-off task instructions there.

## Update protocol docs when
You need to change the workflow or task-class logic.

Examples:
- changing stage requirements
- changing plan triggers
- changing failure / recovery behavior

## Update standards docs when
You need to change quality expectations.

Examples:
- validation expectations
- documentation requirements
- security-aware behavior
- coding discipline rules

## Update templates when
You need to improve the shape of task inputs or outputs.

Examples:
- better intake structure
- better plan structure
- better completion report structure

## Update examples when
You need better reference models.

Examples should improve practical usability.

## Update the project profile when
You need to change repository-specific conventions.

Examples:
- naming conventions
- preferred patterns
- where plans or examples live
- repo-specific review expectations

## Update this file when
You need to improve the practical usage guidance for the system as a whole.

This file should explain how to operate the repository, not redefine policy.

---

# 22. What not to store in this repository

This repository is best used for:
- source code
- docs
- templates
- plans
- reports
- examples
- prompts
- lightweight structured assets

Avoid treating the main repository as a dumping ground for:
- huge datasets
- large binaries
- model artifacts
- bulky generated outputs unless there is a clear reason to keep them

Use external storage or a more appropriate system for large assets.

---

# 23. Final guidance

If you are unsure how to use this repository, start here:

1. read `AGENTS.md`
2. classify the task
3. use the right template
4. create a plan if needed
5. have Codex follow the repository rules
6. require explicit validation
7. require a structured final handoff

That is the core operating pattern.

The better you keep the repository aligned, scoped, and example-backed, the more useful it becomes over time.
