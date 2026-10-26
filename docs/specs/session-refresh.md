# Session Refresh

## Purpose

Let an account keep an active session without re-authenticating with credentials each time its access token expires, by exchanging a valid refresh token for a new access token.

## Behavior

- On successful login, the system issues an access token (as today) **and** a refresh token, and persists a new session record for the account. Each login creates its own, independent session — an account can hold multiple concurrent sessions at once (e.g. one per device or browser). This is a deliberate foundation for a future per-device revocation capability, not an accident of implementation.
- Refresh tokens are opaque (not JWTs), generated with sufficient entropy to be unguessable, and stored **hashed** — never in plaintext. The plaintext value is only ever present in the response that issues it.
- A dedicated `refresh` endpoint accepts a refresh token. If it corresponds to a valid, unexpired, previously-issued and not-yet-used session, the system issues a **new** access token and a **new** refresh token, and immediately invalidates the presented refresh token (rotation). The old value can never be used again, whether by the legitimate client or anyone else who might have obtained it.
- Refresh tokens have their own expiry, configured independently from access token expiry (`REFRESH_TOKEN_EXPIRES_IN`), and are expected to live substantially longer than access tokens.
- The refresh endpoint requires only the refresh token. It does not require a valid or even present access token / Authorization header, since its entire purpose is to recover from an already-expired access token.

## Contract

### `POST /sessions/login` (existing endpoint, extended)

- Request: unchanged — `OAuth2PasswordRequestForm` (`username`, `password`).
- `200 OK`:
  ```json
  { "access_token": "string", "token_type": "bearer", "expires_in": 0, "refresh_token": "string" }
  ```
- `401 Unauthorized`: unchanged (`invalid_credentials`).
- `422 Unprocessable Entity`: unchanged.

### `POST /sessions/refresh` (new endpoint)

- Request body (JSON):
  ```json
  { "refresh_token": "string" }
  ```
- `200 OK`:
  ```json
  { "access_token": "string", "token_type": "bearer", "expires_in": 0, "refresh_token": "string" }
  ```
- `401 Unauthorized`, error type `invalid_refresh_token`: returned when the refresh token is expired, already used/rotated, or was never issued.
- `422 Unprocessable Entity`: returned when `refresh_token` is missing or empty.

## Edge cases

- Refresh token has expired → `401 invalid_refresh_token`.
- Refresh token was already used once (rotated) and is presented again → `401 invalid_refresh_token`.
- Refresh token is an arbitrary string that was never issued → `401 invalid_refresh_token`.
- `refresh_token` field missing or empty in the request body → `422`.
- The same account logs in twice (e.g. two devices): both sessions and both refresh tokens remain independently valid; refreshing one does not affect the other.
- Refresh succeeds without any Authorization header — the (possibly expired) access token is irrelevant to this endpoint.

## Decisions

1. **Storage backend is Postgres**, reusing the existing repository/criteria pattern, not DynamoDB.
   Rationale: the session store sits behind a repository interface already established across this codebase; introducing DynamoDB (new infra, new adapter, new operational surface) before the refresh/revocation model is proven adds risk with no validated need yet.
   Discarded: DynamoDB from day one — deferred to a later slice if Postgres lookup latency proves insufficient at real scale.

2. **One session record per login (multi-session per account)**, not a single record overwritten on each login.
   Rationale: a later epic requires revoking one device's session while leaving others active — only representable if each login is its own record.
   Discarded: single active session per account — would require a breaking model change before per-device revocation could be built.

3. **Refresh tokens are stored hashed**, like passwords.
   Rationale: a database compromise should not hand out live, directly usable sessions.
   Discarded: storing the plaintext token — rejected as a critical exposure on any data leak.

4. **Full rotation on every refresh, no reuse detection yet.** The presented refresh token is invalidated the instant a new one is issued; presenting it again fails as "not found."
   Rationale: standard refresh-token hygiene — a stolen-but-unused old token becomes worthless as soon as the legitimate client refreshes.
   Discarded (for now): rotation with reuse detection / session-family revocation — adds real complexity (tracking token lineage, cascading revocation) that has no effect until a revocation epic exists to act on the signal. Revisit when session revocation is specced.

5. **Refresh token is returned as a JSON body field**, consistent with how `access_token` already works in this API.
   Discarded for now: HttpOnly secure cookie — reduces XSS exposure, but introduces cookie handling, CSRF protection, and same-site assumptions this API has never had.
   **Future possibility:** if a browser-based client with a real XSS threat model becomes a requirement, revisit delivering `refresh_token` as an HttpOnly, Secure, SameSite cookie instead of a JSON field. That would need its own spec pass covering CSRF protection on `/sessions/refresh` and cookie scoping — not a drop-in change.

6. **Refresh requires only the refresh token — no Authorization header.**
   Rationale: the endpoint exists specifically to recover from an expired access token.
   Discarded: requiring a still-valid access token alongside the refresh token — defeats the purpose, since the access token is expected to already be expired when refresh is called.

## Open questions

- Should `POST /sessions/refresh` be rate-limited to blunt brute-force attempts against refresh token values? This is likely a cross-cutting API concern (would apply to `login` too) rather than something specific to this feature, and is left unresolved here.

## Related features

See [session-refresh.feature](../features/session-refresh.feature).
