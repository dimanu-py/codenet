# Session Revocation

## Purpose

Let an account invalidate a specific session (single-device logout) or all of its sessions at once (logout everywhere), so a compromised or unwanted session stops being able to obtain new access tokens.

## Behavior

- Revoking a session deletes its underlying session record outright — the same record created at login and consulted at refresh time ([session-refresh.md](session-refresh.md)). There is no soft-delete or "revoked" status kept around; a revoked session simply ceases to exist, exactly like an already-rotated refresh token already does today.
- **Revocation only affects the ability to refresh.** Once a session is revoked, its refresh token can never again be exchanged for a new access token (it behaves exactly like any other unknown/expired refresh token). It does **not** retroactively invalidate an access token that was already issued from that session — if that access token hasn't hit its own expiry yet, it keeps working normally until it does. This is a deliberate scope boundary: rejecting an already-issued access token on every request would require building the API's first bearer-token verification-and-revocation-check dependency, foundational infrastructure that overlaps with the future role/permission enforcement point (deny-by-default authorization) and is out of scope here. The practical effect is a bounded "logout lag" equal to the access token's TTL.
- A single session is revoked by presenting the refresh token that identifies it — proof of possession, exactly like the refresh endpoint. No Authorization header is required or checked.
- Revoking one session never affects any other session belonging to the same account.
- All sessions for an account are revoked at once by an authenticated caller (a valid, unexpired access token identifies the account via its `sub` claim) — no request body needed. This deletes every session row for that account, **including the session tied to the very access token used to make the call.** There is no "except my current device" exclusion in this spec.
- Revoking a session (single or all) is idempotent: presenting a refresh token that doesn't correspond to any existing session (never issued, already revoked, or already rotated) is treated the same as a successful revoke, not an error. This avoids letting the endpoint be used to probe whether a guessed refresh token value is currently valid.

## Contract

### `POST /sessions/revoke`

- Request body (JSON): `{ "refresh_token": "string" }`
- No `Authorization` header required.
- `200 OK`: `{ "revoked": true }` — always, regardless of whether the refresh token matched an existing session.
- `422 Unprocessable Entity`: returned when `refresh_token` is missing or empty.

### `POST /sessions/revoke-all`

- No request body.
- Requires `Authorization: Bearer <access_token>` — a structurally valid, unexpired access token.
- `200 OK`: `{ "revoked": true }`.
- `401 Unauthorized`, error type `invalid_access_token`: returned when the `Authorization` header is missing, malformed, or the access token is expired or has an invalid signature.

## Edge cases

- Revoking with a refresh token that was never issued, already revoked, or already rotated → `200 {"revoked": true}` (idempotent, no distinguishing error).
- Revoking with a missing/empty `refresh_token` → `422`.
- Calling revoke-all with a missing, malformed, or expired `Authorization` header → `401 invalid_access_token`.
- Revoke-all deletes the session behind the access token used to call it — the caller's own current session is not exempted.
- After either revoke endpoint succeeds, the affected session(s) can no longer be used to refresh — attempting to do so fails exactly as an unknown refresh token would ([session-refresh.md](session-refresh.md), `invalid_refresh_token`).
- Revoking one session leaves every other session for the same account untouched and able to refresh normally.
- An access token already issued from a now-revoked session is unaffected by the revocation and keeps authenticating (wherever it's checked) until it naturally expires. **Not independently testable today** — no protected endpoint exists yet anywhere in this API to observe an access token being accepted or rejected — so this is documented behavior derived directly from the design decision above, not a Gherkin scenario in this feature.

## Decisions

1. **Revocation blocks future refreshes only — it does not immediately invalidate an already-issued access token.**
   Rationale: making it immediate would require building, from scratch, the first bearer-token-verification-plus-revocation-check dependency for the entire API — foundational work that belongs with (and likely gets built alongside) the future role/permission deny-by-default enforcement point, not bolted onto this spec.
   Discarded: immediate revocation via a per-request session-store check on every protected route — deferred until that foundational authorization mechanism is actually being built.

2. **Session records are hard-deleted on revoke, not soft-deleted with a `revoked` flag.**
   Rationale: consistent with Phase 1, where a rotated refresh token already just disappears; there's no current requirement to list or audit past sessions.
   Discarded: soft delete with a `revoked_at` timestamp — revisit if a "list my sessions" or audit-trail feature is ever requested.

3. **Revoke-one is identified by refresh token in the body, with no Authorization header.**
   Rationale: symmetric with `/sessions/refresh` (Phase 1) — possession of the refresh token is the proof of identity. Requires no changes to the access token's JWT payload.
   Discarded: identifying "the current session" via a `session_id` claim embedded in the access token — would have reopened the already-shipped `JwtTokenIssuer`.

4. **Revoke-one and revoke-all are idempotent and always report success**, never revealing whether the presented refresh token matched anything.
   Rationale: prevents the endpoint from being used as an oracle to test whether a guessed/stolen refresh token value is currently valid.
   Discarded: returning a distinct error (e.g. `404`/`401`) for an unknown or already-revoked token — rejected as an information-leak side channel.

5. **Revoke-all has no "except current device" exclusion.**
   Rationale: matches the minimal-slice principle already used for Phase 1 — a "log out other sessions, keep this one" variant is a distinct, richer behavior (documented as a future option in the original slicing) that can be added later without changing this contract.
   Discarded: excluding the caller's own session from revoke-all — deferred.

## Open questions

- None currently unresolved for this spec. (Carried over from [session-refresh.md](session-refresh.md): whether `/sessions/refresh` — and now also `/sessions/revoke` / `/sessions/revoke-all` — should be rate-limited remains an open, cross-cutting API concern.)

## Related features

See [session-revocation.feature](../features/session-revocation.feature).
