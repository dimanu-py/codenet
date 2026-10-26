# Authorization Enforcement

## Purpose

Gate specific actions behind a required rule, deny by default when an account doesn't hold it, and use this mechanism to finally close the "these endpoints aren't protected yet" gap flagged since [roles-and-rules.md](roles-and-rules.md).

## Behavior

- A reusable dependency, `RequiresRule(rule_name)`, is attached to a route exactly the way other request dependencies already are in this codebase (e.g. `OAuth2PasswordRequestForm` via `Depends()`). No middleware, decorator, or central route→permission registry is introduced — this is the one dependency-injection pattern already idiomatic here.
- Checking a request does three things, in order:
  1. Verify the `Authorization` bearer access token (signature and expiry) and extract the account id. This formalizes, as a concrete port, the same lightweight check that `session-revocation` and `change-password` already relied on informally — `TokenVerifier`, living in `auth/session/domain` as the natural counterpart to the existing `TokenIssuer`. Failure here → `401 invalid_access_token`, unchanged from those specs.
  2. Resolve the account's currently active roles into their granted rule set — "currently active" excludes anything expired, per `temporary-role-assignment`'s lazy-expiry rule; an assignment that's lapsed is invisible here exactly as it is when listing.
  3. Check whether the required rule is in that set. Present → the request proceeds normally. Absent (including an account with zero role assignments at all — this is where deny-by-default actually happens) → `403 Forbidden`.
- This first pass supports exactly **one required rule per protected action** — no AND/OR combinations of multiple rules. Nothing in the original request calls for that, and it's additive to introduce later without breaking this contract.
- The `403` response names the specific missing rule (e.g. `"missing_rule": "iam:manage"`). A rule name is not a secret the way a refresh token is, so withholding it would only cost legitimate API consumers debuggability for no real security benefit.
- The mechanism connecting token verification (owned by `auth`) to rule resolution (owned by `iam`) lives in `iam`'s infra layer — the same place `AccountExistenceChecker` already reaches into `auth`, per `role-assignment.md`'s decision 2. No new kind of cross-context coupling is introduced.
- **Endpoints protected by `iam:manage`** (all from `iam`, all mutating or account-specific): `POST /app/iam/rules/{rule_id}` (create rule), `POST /app/iam/roles/{role_id}` (create role), `POST .../accounts/{account_id}/roles/{role_id}` (assign), `DELETE .../accounts/{account_id}/roles/{role_id}` (unassign), `GET .../accounts/{account_id}/roles` (an account's specific grants).
- **Endpoints left open**: `GET /app/iam/rules` and `GET /app/iam/roles` — pure catalog reads with no account-specific data. Listing what rules/roles *exist* is metadata, not a privilege-escalation or privacy concern on its own; only creating them, assigning them, or revealing what a *specific account* holds is gated.

## Bootstrap

Protecting `iam`'s own mutating endpoints with a rule creates an unavoidable chicken-and-egg problem: nothing can call `assign` to grant the first `iam:manage` without already holding it. This is resolved **out-of-band**, not in application code: a one-time deployment migration/seed script inserts the first rule (`iam:manage`), the first role, and its first assignment directly, bypassing the API entirely. This spec does not implement that script (it's an operational/deployment concern, not an API feature) — it only requires that such a seed exists before this spec is deployed, or every protected `iam` endpoint becomes permanently unreachable.

An event-driven "assign a default role automatically when an account is created" capability was discussed and deliberately deferred to its own future spec — it solves a different problem (giving every new signup some default role) and doesn't by itself resolve this bootstrap paradox unless it special-cases "the first account ever," which is exactly the stateful check the migration-seed approach avoids. It would also require building this codebase's first-ever event consumer/dispatcher (an `EventBus` and outbox table already exist but nothing currently reads from them), which is real scope beyond what this spec needs.

## Contract

No new endpoints. Five existing `iam` endpoints (listed above) now additionally require `Authorization: Bearer <access_token>`, and the caller's account must hold `iam:manage`.

- `401 Unauthorized`, error type `invalid_access_token`: `Authorization` header missing, malformed, or the access token is expired/has an invalid signature. Unchanged from `session-revocation`/`change-password`.
- `403 Forbidden`, error type `forbidden`: the access token is valid, but the account does not currently hold the required rule.
  ```json
  { "error_type": "forbidden", "missing_rule": "iam:manage" }
  ```
- All other response shapes for these five endpoints are unchanged from their original specs ([roles-and-rules.md](roles-and-rules.md), [role-assignment.md](role-assignment.md)).

## Edge cases

- Calling any of the five protected endpoints with no `Authorization` header → `401 invalid_access_token`.
- Calling with a valid, unexpired access token, but the account has zero role assignments → `403 forbidden`, `missing_rule: "iam:manage"` (deny-by-default in effect).
- Calling with a valid access token and an assigned role, but none of that role's rules include `iam:manage` → `403 forbidden`.
- Calling with a valid access token and a role granting `iam:manage` that has since **expired** → `403 forbidden`, exactly as if the role were never assigned (lazy expiry applies here too, not just in listing).
- Calling `GET /app/iam/rules` or `GET /app/iam/roles` with no `Authorization` header at all → succeeds, unchanged.
- An account holding `iam:manage` via a **temporary** assignment can perform any of the five protected actions until that assignment expires, identically to a permanent one — enforcement doesn't distinguish permanent from temporary, only "currently active or not."

## Decisions

1. **A single dependency (`RequiresRule`) checking one rule per protected action**, not a broader policy/rule-engine.
   Rationale: matches exactly what was asked for — deny by default unless a specific permission is held — without inventing composition logic (AND/OR of multiple rules) nobody requested yet.
   Discarded: multi-rule composition per endpoint — deferred; additive later if a real need shows up.

2. **`TokenVerifier` is formalized now as a named port in `auth/session/domain`**, symmetric to the existing `TokenIssuer`.
   Rationale: `session-revocation` and `change-password` both already depended on "verify a bearer token, get an account id" without that capability ever being given a concrete architectural home — enforcement is the first spec that actually builds and names it, but it isn't new behavior, just a formalization of what already shipped.
   Discarded: leaving token verification as an ad hoc, unnamed detail in each consuming controller — would leave three specs' worth of near-identical logic undocumented as a single shared concept.

3. **The 403 response reveals the specific missing rule.**
   Rationale: a rule name is metadata about the permission model, not a secret credential — unlike the refresh-token oracle concern in `session-revocation`, there's no exploitable disclosure here, only a usability cost to hiding it.
   Discarded: a generic, unspecific `403 forbidden` with no detail — rejected as protecting against a threat that doesn't apply here.

4. **Mutating and account-specific `iam` endpoints require `iam:manage`; pure catalog reads stay open.**
   Rationale: matches the actual risk shape — defining arbitrary rules/roles or granting/revealing account-specific access is a privilege-escalation and privacy concern; browsing the *existence* of rule/role definitions is not.
   Discarded: gating the catalog reads too — would fully close the original flagged gap's letter but not its spirit (the concern was specifically about arbitrary definition/assignment, not discoverability of names).

5. **Bootstrap is an out-of-band deployment seed, not application code.**
   Rationale: the smallest possible fix for a one-time, ops-level problem; avoids building a stateful "is the system empty" special case into the enforcement check itself, and avoids building new event-consumer infrastructure that doesn't exist yet in this codebase for a narrow one-off need.
   Discarded: an "auto-open while empty" special case in the dependency itself, and an event-driven default-role-on-signup mechanism built now — both add real complexity to solve (or over-solve) a problem a five-line migration already fully resolves. The event-driven idea is captured as a separate, future spec on its own merits.

## Open questions

- "Assign a default role automatically when an account is created" (via the existing but currently-unused `EventBus`) is explicitly deferred to its own future spec.
- Carried over: whether any of the auth/IAM endpoints should be rate-limited remains an open, cross-cutting concern.

## Related features

See [enforcement.feature](../features/enforcement.feature).
