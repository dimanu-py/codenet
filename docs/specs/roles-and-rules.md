# Roles & Rules

## Purpose

Establish the foundational authorization vocabulary — rules as reusable permission identifiers, and roles as named, reusable sets of rules — that every later piece of the RBAC epic (assignment, temporary assignment, enforcement) builds on.

## Behavior

- A **rule** is a persisted, uniquely-named permission identifier, e.g. `account:create`, `role:assign`. It's deliberately just a name — a `resource:action`-style naming convention is expected but not structurally enforced (no separate `resource`/`action` fields), keeping the shape as simple as the other identifier value objects already in this codebase (`AccountEmail`, `AccountUsername`).
- A **role** is a persisted, uniquely-named set of references to existing rules. A role always references at least one rule — an empty role is functionally identical to having no role at all and would only exist as a footgun.
- Rules exist independently of any role and are meant to be referenced by more than one role — that's the entire point of having a `Rule` as its own entity instead of a free-text string duplicated across roles: a shared, typo-proof vocabulary.
- Both rules and roles are identified by a client-generated id passed in the URL path, consistent with how `signup` already works (`POST /accounts/{account_id}`) — not server-generated ids.
- This spec covers only creation and listing for both resources. There is no update, rename, or delete yet, mirroring how `account` itself has only ever had `signup` in this codebase — those are their own specs if and when they're needed.
- Listing is included for both resources, despite the otherwise minimal scope, because discoverability is central to the purpose here: you cannot compose a role without knowing what rules exist, and the next spec (role assignment) cannot happen without knowing what roles exist.

**Known limitation, not a decision:** none of the four endpoints below are protected by any authorization check. The mechanism that would protect them — deny-by-default enforcement — is a later spec in this epic, and enforcement itself depends on roles and rules already existing to enforce against. Until that enforcement spec ships, any caller, authenticated or not, can define arbitrary rules and roles. This should be treated as a gap to close immediately once enforcement exists (at which point "manage roles/rules" should itself require a permission), not as an accepted end state.

## Contract

### `POST /app/iam/rules/{rule_id}`

- Path parameter: `rule_id` (client-generated UUID).
- Request body (JSON): `{ "name": "string" }`
- `202 Accepted`: `{ "accepted": true }`
- `409 Conflict`, error type `conflict_error`: a rule with this `name` already exists.
- `422 Unprocessable Entity`: `name` missing or empty.

### `GET /app/iam/rules`

- `200 OK`: `{ "rules": [ { "id": "string", "name": "string" }, ... ] }`

### `POST /app/iam/roles/{role_id}`

- Path parameter: `role_id` (client-generated UUID).
- Request body (JSON): `{ "name": "string", "rule_ids": ["string", ...] }`
- `202 Accepted`: `{ "accepted": true }`
- `409 Conflict`, error type `conflict_error`: a role with this `name` already exists.
- `404 Not Found`, error type `not_found_error`: one or more of the given `rule_ids` does not exist. The whole creation fails — nothing is created partially.
- `422 Unprocessable Entity`: `name` missing/empty, or `rule_ids` missing or an empty list.

### `GET /app/iam/roles`

- `200 OK`: `{ "roles": [ { "id": "string", "name": "string", "rules": [ { "id": "string", "name": "string" }, ... ] }, ... ] }`

## Edge cases

- Creating a rule with a name that already exists → `409 conflict_error`.
- Creating a rule with a missing/empty `name` → `422`.
- Creating a role with a name that already exists → `409 conflict_error`.
- Creating a role with an empty `rule_ids` list, or the field missing entirely → `422`.
- Creating a role where any single `rule_id` doesn't correspond to an existing rule → `404 not_found_error`; no role is created, even for the valid rule ids in the same request.
- Creating a role referencing the same valid `rule_id` more than once in the list — treated as that rule being included once (no duplicate-reference error, no duplicate storage).
- Listing rules or roles when none exist yet → `200` with an empty list, not an error.

## Decisions

1. **New bounded context `src/iam/`**, separate from `src/auth/`, containing `rule` and `role` (and later, assignment and enforcement).
   Rationale: `src/auth/` today is purely about authentication (account, session) — proving who you are. Roles and rules are authorization — deciding what you're allowed to do. Conflating the two would make `auth` a catch-all as the system grows, and this boundary is expensive to redraw later.
   Discarded: `src/auth/role/` and `src/auth/rule/` alongside `account`/`session` — rejected for the reason above.

2. **A rule is a flat, unique `name` string**, not structured `resource`/`action` fields.
   Rationale: matches the simplicity of other identifier value objects in this codebase; a naming convention (`resource:action`) achieves the same clarity for humans without schema rigidity, and nothing today needs to query rules by resource or action independently.
   Discarded: structured `{resource, action}` fields — adds rigidity for a querying need that doesn't exist yet.

3. **Rule and role ids are client-generated**, supplied via the URL path.
   Rationale: consistency with the existing `signup` convention.
   Discarded: server-generated ids — would be inconsistent with the only other creation endpoint in this codebase.

4. **Rule names and role names are both unique.**
   Rationale: a rule's entire purpose is to be a shared, referenceable identifier across roles — duplicate names would make "which rule is this" ambiguous. Role names being unique keeps them meaningful to whoever is managing them.
   Discarded: allowing duplicate names — undermines the reason rules exist as their own entity in the first place.

5. **A role must reference at least one existing rule; an invalid reference fails the entire creation.**
   Rationale: an empty role is a pointless object that does nothing under deny-by-default; silently dropping unknown rule ids would hide a caller's mistake instead of surfacing it.
   Discarded: allowing empty roles, and silently ignoring unknown `rule_ids` — both rejected as silent-failure surprises.

6. **Scope is create + list only, for both resources, in this spec.**
   Rationale: mirrors the minimal-slice pattern used throughout this epic so far (`account` itself has never had update/delete, only `signup`); update/rename/delete can be specced separately once there's a concrete need.
   Discarded: full CRUD for both resources in this first spec — unnecessary scope for what's needed to unblock the next spec (assignment).

## Open questions

- How rule/role management endpoints get protected once enforcement exists is explicitly deferred — see "Known limitation" above. This spec does not attempt a bootstrapping answer (e.g. a seeded superadmin) since that only makes sense once the enforcement mechanism itself is specced.
- Carried over: whether any of the auth/IAM endpoints should be rate-limited remains an open, cross-cutting concern.

## Related features

See [roles-and-rules.feature](../features/roles-and-rules.feature).
