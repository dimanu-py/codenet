# Change Password

## Purpose

Let an authenticated account holder change their password, closing out any sessions that may have been established under the old, possibly-compromised password.

## Behavior

- Changing the password requires two things at once: a valid, unexpired access token (identifying the account via its `sub` claim, using the same lightweight bearer-token verification introduced for [session-revocation.md](session-revocation.md)) **and** the account's current plaintext password in the request body. Neither alone is sufficient — the access token proves "you're logged in," the current password proves "you still know the secret," independent of whether the access token itself might have been stolen.
- The account to change is derived entirely from the access token; it is never taken from a path parameter or request body. This differs deliberately from `signup`, where the account id is client-generated pre-authentication — here the account already exists and is authenticated, so accepting it as separate input would only create a class of "does the path match the token" mismatch bugs for no benefit.
- On success, the account's password is updated and persisted, and — reusing the exact mechanism built for `/sessions/revoke-all` — **every** session for that account is revoked, with no exception for the session behind the very request that changed the password. This matches the literal requirement: changing the password forces revoking all tokens, full stop.
- As with revoke-all, "revoked" means those sessions can no longer be used to refresh; an access token issued from one of them that hasn't yet naturally expired keeps authenticating elsewhere until it does (see [session-revocation.md](session-revocation.md), decision 1). The caller is not handed a new session as part of this response — the next time they need one, they log in with the new password like anyone else.
- No new password strength/complexity rules are introduced. `signup` accepts any non-empty password string today; `change-password` mirrors that rather than inventing a stricter rule that doesn't exist anywhere else in this module yet.

## Contract

### `PATCH /accounts/password`

- Requires `Authorization: Bearer <access_token>` — a structurally valid, unexpired access token.
- Request body (JSON): `{ "current_password": "string", "new_password": "string" }`
- `200 OK`: `{ "changed": true }`
- `401 Unauthorized`, error type `invalid_access_token`: the `Authorization` header is missing, malformed, or the access token is expired or has an invalid signature.
- `401 Unauthorized`, error type `invalid_current_password`: the access token is valid but `current_password` does not match the account's stored password.
- `422 Unprocessable Entity`: `current_password` or `new_password` is missing or empty.

## Edge cases

- Missing, malformed, or expired `Authorization` header → `401 invalid_access_token`.
- `current_password` does not match the account's stored password → `401 invalid_current_password`.
- `current_password` or `new_password` missing/empty → `422`.
- On success, every session for the account is revoked, including the one tied to the access token used to make this call — no exception.
- On success, any of the account's refresh tokens fail afterward exactly as an unknown/revoked refresh token would ([session-refresh.md](session-refresh.md), `invalid_refresh_token`).
- Changing the password when the account currently has zero active sessions still succeeds; revoking zero sessions is a no-op, not an error.
- Logging in again after a successful change requires the new password — the old password no longer authenticates.

## Decisions

1. **Requires both a valid access token and the current plaintext password**, not either alone.
   Rationale: a stolen access token alone must not be enough to lock the real owner out by changing their password to something only the attacker knows.
   Discarded: authorization via access token only — rejected for the reason above.

2. **Account id comes only from the access token**, never from a path parameter or body field.
   Rationale: avoids an entire class of "does the path's account id match the token's account id" mismatch/IDOR-style checks that would otherwise be needed.
   Discarded: `PATCH /accounts/{account_id}/password`, mirroring `signup`'s route shape — rejected because `signup`'s use of a path id is specific to it happening pre-authentication with a client-generated id, which doesn't apply here.

3. **No new password strength rules.**
   Rationale: consistency — `signup` has none today, so `change-password` inventing one would be a new, unrequested requirement decoupled from this spec's purpose.
   Discarded: minimum length/complexity validation — out of scope; would apply to `signup` too if ever introduced.

4. **Password change revokes every session, including the caller's own, with no exception.**
   Rationale: matches the explicit original requirement ("changing the password forces revoking all tokens") literally, and keeps this cascade's semantics identical to the general-purpose `revoke-all` endpoint rather than introducing a second, slightly different variant of "revoke all."
   Discarded: reissuing a fresh session in the response so the caller isn't logged out of their own change-password flow — rejected as a quiet exception to an otherwise absolute rule, and as scope the original request didn't ask for.

## Open questions

- Whether `new_password` must differ from `current_password` was not part of the original requirement and is not enforced by this spec. Flagging it as a conscious omission rather than a decided "no" — revisit if it turns out to matter.
- Carried over: whether any of the auth endpoints (`login`, `refresh`, `revoke`, `revoke-all`, and now `change-password`) should be rate-limited remains an open, cross-cutting API concern.

## Related features

See [change-password.feature](../features/change-password.feature).
