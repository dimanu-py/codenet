# Temporary Role Assignment

## Purpose

Let a role be assigned to an account for a bounded amount of time, after which it stops counting as assigned automatically, without any separate action to remove it.

## Behavior

- The existing assign endpoint ([role-assignment.md](role-assignment.md)) gains an optional `expires_in_minutes` field. Omitted → the assignment is permanent, exactly as before. Present and a positive integer → the assignment is temporary, expiring `expires_in_minutes` minutes after the call is made (`expires_at = now + expires_in_minutes`, using the same `Clock` abstraction already used elsewhere in this codebase, not the database's own clock).
- There is one assignment table, not two: a permanent assignment is simply one whose expiry is unset. This is why the same endpoint, rather than a distinct one, was chosen for temporary assignment.
- **Expiry is lazy, not actively swept.** Nothing deletes an expired assignment row on a timer or via a background job. Instead, anywhere an assignment is read or checked — listing an account's roles today, and later the enforcement check — an assignment whose `expires_at` has passed is treated exactly as if it doesn't exist, without needing to have been physically removed first. This avoids introducing any new scheduling/job infrastructure for what only needs to be a read-time comparison against the current time.
- **Re-assigning always expresses the caller's current intent and overwrites whatever was there.** Since assignment is inherently declarative ("ensure this account has this role, under these terms"), a second `assign` call for the same `(account_id, role_id)` pair always wins, regardless of what existed before:
  - Assigning permanently over an existing temporary assignment clears its expiry — it becomes permanent.
  - Assigning temporarily over an existing permanent assignment sets an expiry — it becomes temporary.
  - Assigning temporarily over an existing (still-active) temporary assignment resets the expiry to `now + expires_in_minutes` from *this* call — it does not extend or ignore the previous expiry.
  - Assigning anything over an already-expired temporary assignment behaves like a fresh assignment (see the lazy-expiry point above — an expired row isn't "still there" for this purpose).
- **Listing an account's roles excludes expired assignments** and reports each remaining role's expiry, or `null` for permanent ones.

## Contract

### `POST /app/iam/accounts/{account_id}/roles/{role_id}` (extended)

- Request body (JSON, all optional): `{ "expires_in_minutes": integer }`
- `202 Accepted`: `{ "accepted": true }` — same as [role-assignment.md](role-assignment.md); behavior only changes in whether the resulting assignment carries an expiry.
- `404 Not Found`: unchanged — `account_id` or `role_id` doesn't exist.
- `422 Unprocessable Entity`: `expires_in_minutes` is present but not a positive integer (zero, negative, or non-integer).

### `GET /app/iam/accounts/{account_id}/roles` (extended)

- `200 OK`: `{ "roles": [ { "id": "string", "name": "string", "expires_at": "ISO-8601 string or null" }, ... ] }`
- An assignment whose `expires_at` has already passed is not included in the list at all.

## Edge cases

- `expires_in_minutes` present and `0` → `422`.
- `expires_in_minutes` present and negative → `422`.
- `expires_in_minutes` omitted entirely → unchanged, permanent assignment (backward-compatible with [role-assignment.md](role-assignment.md)).
- Assigning the same role again with a different `expires_in_minutes` while the previous temporary assignment is still active → expiry resets relative to the new call's time, not extended or averaged.
- Assigning permanently over an active temporary assignment → becomes permanent (`expires_at` cleared).
- Assigning temporarily over a permanent assignment → becomes temporary.
- Assigning any role over an already-expired temporary assignment → behaves as a brand-new assignment, not an "already assigned" no-op.
- Unassigning an already-expired temporary assignment → still `202`, no error — consistent with unassign's existing unconditional idempotency in [role-assignment.md](role-assignment.md).
- Listing roles for an account whose only assignment has expired → `200` with an empty `roles` list, same as having no assignment at all.

## Decisions

1. **One assignment table with a nullable `expires_at`**, not two separate concepts for permanent vs. temporary.
   Rationale: a permanent assignment is naturally "a temporary one with no expiry" — modeling it as one thing keeps the endpoint, the data model, and the read-time logic (listing, later enforcement) uniform.
   Discarded: a distinct endpoint/table for temporary assignments — rejected per the earlier decision in this conversation, to avoid two mental models for one underlying fact.

2. **Expiry is lazy (checked at read time), never actively swept by a background job.**
   Rationale: the only thing "expiry" needs to do is make a past-due assignment invisible wherever assignments are read — a timestamp comparison achieves that with zero new infrastructure. Building a scheduled cleanup job would be solving a storage-hygiene problem (stale rows lingering in the table) that hasn't been raised as an actual requirement.
   Discarded: a periodic job (cron/worker) that deletes expired rows — deferred; nothing about correctness depends on it, only long-run table size, which isn't a concern this spec was asked to address.

3. **Re-assignment always overwrites in favor of the newest call's intent**, whether that means adding an expiry, clearing one, or resetting one.
   Rationale: assignment is declarative — "ensure this account has this role, under these terms" — so the most recent call should always describe the current desired state. Any other rule (first-wins, longest-wins, error-on-conflict) would require the caller to first read the current state before deciding how to call assign, defeating the point of an idempotent, declarative operation.
   Discarded: rejecting a second assign call with a conflicting duration/permanence as an error — would turn a normally idempotent operation into one that requires read-before-write.

4. **Listing excludes expired assignments entirely, rather than including them with a flag.**
   Rationale: consistent with "expired behaves as unassigned" everywhere else in this spec — a caller listing an account's roles wants to know what currently applies, not a history of what once did.
   Discarded: returning expired assignments with an `is_expired: true` marker — would turn this endpoint into a partial audit log, which isn't its purpose and isn't something this spec was asked to provide.

## Open questions

- Whether expired assignments should ever be purged from storage (and how) is explicitly out of scope — see Decision 2.
- Carried over: whether any of the auth/IAM endpoints should be rate-limited remains an open, cross-cutting concern.

## Related features

See [temporary-role-assignment.feature](../features/temporary-role-assignment.feature).
