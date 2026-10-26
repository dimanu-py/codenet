# Role Assignment

## Purpose

Let a role, once defined ([roles-and-rules.md](roles-and-rules.md)), be granted to or revoked from an account permanently, and let an account's currently assigned roles be listed.

## Behavior

- An assignment links one account to one role. It has no identity of its own beyond that pair — assigning the same role to the same account more than once is not a meaningful new event, so `(account_id, role_id)` is the natural key, not a separately generated assignment id.
- **Assigning** a role validates that both the account and the role actually exist before creating the link. The account check reaches across the `auth`/`iam` boundary through a port owned by `iam` (e.g. `AccountExistenceChecker`) — only `iam`'s infra layer knows `auth` exists; its domain and application layers do not. The role check stays entirely inside `iam`, since roles are already `iam`'s own concept.
- Assigning a role that's already assigned to that account is treated as a successful no-op, not a conflict — routine "make sure this account has this role" calls shouldn't need to special-case an already-true state.
- **Unassigning** a role is unconditionally idempotent: it never validates that the account, the role, or the assignment itself currently exists. The desired end state — "this account does not have this role" — is already true in every one of those cases, so there's nothing to error about. This deliberately mirrors how `session-revocation`'s revoke endpoints behave.
- **Listing** an account's roles returns whatever is currently assigned, or an empty list if nothing is.
- This spec covers permanent assignment only. Temporary, auto-expiring assignment is a separate, follow-up spec that will decide how it relates to this contract (an added field vs. a distinct endpoint) — not decided here.

## Contract

### `POST /app/iam/accounts/{account_id}/roles/{role_id}`

- No request body — both ids fully identify the assignment.
- `202 Accepted`: `{ "accepted": true }` — whether newly created or already assigned.
- `404 Not Found`, error type `not_found_error`: `account_id` does not exist, or `role_id` does not exist (the response message distinguishes which).

### `DELETE /app/iam/accounts/{account_id}/roles/{role_id}`

- No request body.
- `202 Accepted`: `{ "accepted": true }` — always, regardless of whether the account, the role, or the assignment itself currently exists.

### `GET /app/iam/accounts/{account_id}/roles`

- `200 OK`: `{ "roles": [ { "id": "string", "name": "string" }, ... ] }` — empty list if the account has no assigned roles (including if the account itself doesn't exist; see edge cases).

## Edge cases

- Assigning a role to a nonexistent account → `404 not_found_error`.
- Assigning a nonexistent role to an existing account → `404 not_found_error`.
- Assigning a role that's already assigned to that account → `202`, no duplicate, no error.
- Unassigning a role that was never assigned → `202`, no error.
- Unassigning using a nonexistent `account_id` or `role_id` → `202`, no error (idempotent by design; see Decisions).
- Listing roles for an account with zero assignments → `200` with an empty `roles` list.
- Listing roles for an `account_id` that doesn't exist at all → `200` with an empty `roles` list, same as any account with no assignments — this endpoint does not validate account existence, only reports what's assigned (see Decisions).

## Decisions

1. **Assignment identity is the `(account_id, role_id)` pair, not a separate generated id.**
   Rationale: there's no meaningful second assignment of the same role to the same account — the pair already uniquely and completely describes the fact being recorded.
   Discarded: a separately generated `assignment_id` — adds an identity concept nothing in this spec needs.

2. **Cross-context account validation happens through a port `iam` owns, implemented in `iam`'s infra layer.**
   Rationale: keeps `iam`'s domain/application code free of any dependency on `auth`, honoring the bounded-context split just made in `roles-and-rules.md`, while still getting the data-integrity guarantee the previous spec's question asked for. The coupling is pushed to the one layer (infra) where cross-cutting, monolith-internal reads are expected to live.
   Discarded: querying `auth`'s database table directly from `iam`'s infra — would trade an explicit code dependency for an implicit, harder-to-see schema dependency. Discarded: a real network call to an `auth` HTTP endpoint — unnecessary weight for a single-deployable modular monolith.

3. **Assign validates both ids exist; unassign validates nothing and is always successful.**
   Rationale: granting access creates a new capability, so it must reference real things; revoking access only ever needs to guarantee an absence, which is already true regardless of whether the referenced ids are real. This mirrors the idempotent-revoke reasoning already established in `session-revocation.md`.
   Discarded: symmetric validation on unassign (404 if account/role/assignment doesn't exist) — would make routine cleanup calls fragile for no integrity benefit.

4. **Assigning an already-assigned role is a no-op success, not a conflict.**
   Rationale: assignment is naturally idempotent — the desired state ("this account has this role") is already achieved either way.
   Discarded: `409 Conflict` on re-assignment — would force callers to check-then-act instead of just asserting the desired state directly.

5. **Listing an account's roles does not itself validate that the account exists.**
   Rationale: keeping this endpoint free of a cross-context existence check keeps it simple and consistent with unassign's idempotent, no-validation posture; "an account with no roles" and "an account that doesn't exist" both correctly return an empty list from this endpoint's point of view.
   Discarded: validating account existence here too (404 if unknown) — would reintroduce the exact cross-context check this endpoint doesn't otherwise need, just to distinguish two cases that look identical to the caller anyway (an empty list).

## Open questions

- How temporary/expiring assignment relates to this contract (extra field on the same endpoints vs. a distinct set of endpoints) is explicitly left open for that spec.
- Carried over: whether any of the auth/IAM endpoints should be rate-limited remains an open, cross-cutting concern.

## Related features

See [role-assignment.feature](../features/role-assignment.feature).
