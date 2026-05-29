# Skills Discovery

A small introduction to each skill provided in this project to understand what they do and how to use them.

## [`adr`](./adr/SKILL.md)

Skill to create or improve Architecture Decision Records (ADRs) under `docs/adrs/` following the project's documentation standard.

**Use when:**
- Discussing a new convention or pattern that should be documented
- Requesting improvements to existing ADR documentation
- Reviewing a plan that was rejected for not following repository conventions

**What it does:**
- Identifies conventions and decisions from the conversation
- Creates or updates ADR files with consistent structure
- Establishes a clear record for team decisions and conventions to follow in future discussions and implementations

## [`design-doc`](./design-doc/SKILL.md)

Skill to create or improve design documents under `docs/design_docs/` capturing feature ideas, requirements, and implementation plans.

**Use when:**
- Planning a new feature that needs requirements and implementation steps
- Discussing architectural changes that should be documented before coding
- Updating the status of an existing design doc as implementation progresses

**What it does:*
- Extracts feature ideas, requirements, and implementation details from the conversation
- Creates or updates design docs with a consistent format and structure
- Provides a clear roadmap for implementation and a reference for future discussions and decisions

## [`mutation-testing`](./mutation-testing/SKILL.md)

Skill to apply mutation testing analysis in Python codebases using `mutmut`. The main objetive is to determine how effective our 
tests are at detecting real bugs.

**Use when:**
- Analyzing changes in a branch to identify weak test
- Verifying TDD effectiveness ensuring behavior is tested instead of just execution
- Validating refactoring didn't break existing functionality
- Identifying edge cases

**What it does:*
- Runs mutation testing on the relevant codebase
- Analyzes results to identify weak tests and areas for improvement
- Provides actionable recommendations to enhance test quality and coverage

## [`test-desiderata`](./test-desiderata/SKILL.md)

Skill for analyzing and improving test quality using Kent Beck's Test Desiderata framework.

**Use when:**
- Analyzing test file
- Reviewing test code
- Asking about test quality or best practices
- Requesting suggestions for test improvements

**What it does:*
- Evaluates tests across 12 dimensions
- Provides actionable recommendations for improvement
- Helps teams enhance test quality and maintainability

## [`hamburger-method`](./hamburger-method/SKILL.md)

Applies the Hamburger Method (by Gojko Adzic) to slice features into vertical deliverable pieces.

**Use when:**
- Breaking down large features into layers
- Generating multiple implementation options per layer
- Composing minimal vertical slices for fast delivery

## [`story-splitting`](./story-splitting/SKILL.md)

Detects stories that are too big and applies proven splitting heuristics.

**Use when:**
- Stories feel too large or vague
- Multiple features are bundled together
- Need help breaking down requirements

## [`complexity-review`](./complexity-review/SKILL.md)

Reviews technical proposals against complexity dimensions with basal cost analysis.

**Use when:**
- Evaluating technical solutions or designs
- Proposing system architectures
- Making technology choices

**What it does:**
- Questions every complexity driver with probing questions
- Proposes progressively simpler alternatives
- Identifies what can be postponed until there's real data
- Challenges assumptions about scale, performance, and reliability

## [`micro-steps-coach`](./micro-steps-coach/SKILL.md)

Breaks down ANY work into 1-3 hour micro-steps with zero downtime.

**Use when:**
- Facing large refactorings or technical improvements
- Any work that feels too big or risky
- Making breaking changes (DB schema, API contracts, service migrations)

**What it does:**
- Forces 1-3 hour granularity for all work types
- Detects risky/breaking changes automatically
- Applies expand-contract pattern for safe changes
- Each step is deployable, reversible, and safe

## [`xp-refactor`](./xp-refactor/SKILL.md)

Applies XP Simple Design principles when refactoring code — reduce duplication, improve clarity, and keep the fewest elements needed.

**Use when:**
- Cleaning up or improving existing code
- Reducing duplication and accidental complexity
- Refactoring with a focus on maintainability

**What it does:**
- Analyzes code for duplication, unclear naming, and complexity
- Prioritizes refactors by ROI
- Applies XP Simple Design: passes tests, expresses intent, no duplication, fewest elements
- Ensures the result is simpler and more maintainable than before
