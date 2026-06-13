# Authentication Flow

## Overview

The online studio at `mvxworld.art/_transmissie/console.html` uses server-side Argon2id verification via a Cloudflare Worker at `auth.mvxworld.art`.

---

## Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         BROWSER                                  │
│  _transmissie/console.html                                      │
│                                                                  │
│  1. User enters passphrase in <input type="password">           │
│  2. Presses Enter                                                │
│  3. tryUnlock() fires                                            │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │  POST /verify
                               │  { passphrase: "..." }
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CLOUDFLARE WORKER                               │
│  auth.mvxworld.art                                               │
│                                                                  │
│  4. Extract client IP from CF-Connecting-IP header              │
│  5. Check rate limit (KV: rl:{ip})                              │
│     ├─ If count >= 5 in 15 min → 429 Too Many Attempts         │
│     └─ If allowed → continue                                     │
│                                                                  │
│  6. Hash passphrase with Argon2id                               │
│     ├─ memoryCost: 32768 KB (32 MB)                             │
│     ├─ timeCost: 3                                               │
│     ├─ parallelism: 1                                            │
│     └─ Salt: extracted from stored ARGON2_HASH secret           │
│                                                                  │
│  7. Constant-time compare hash to stored ARGON2_HASH            │
│     ├─ If mismatch → 401 Invalid frequency                      │
│     └─ If match → continue                                       │
│                                                                  │
│  8. Reset rate limit for this IP (KV delete)                    │
│  9. Sign JWT with HMAC-SHA256 (JWT_SECRET)                      │
│     └─ Payload: { sub: "studio", iat, exp: +24h }              │
│  10. Return { ok: true, token: "eyJ..." }                       │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │  200 OK
                               │  { ok: true, token: "..." }
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                         BROWSER                                  │
│                                                                  │
│  11. Store JWT in sessionStorage("mvx-studio-token")            │
│  12. Hide gate, show editor                                      │
│                                                                  │
│  ── On page reload ──                                            │
│  13. Read JWT from sessionStorage                               │
│  14. POST /validate { token } to Worker                         │
│  15. If valid → skip gate, show editor                          │
│  16. If invalid/expired → clear token, show gate                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Endpoints

### POST /verify

Authenticates a passphrase and returns a JWT.

**Request:**
```json
{
  "passphrase": "your-secret-phrase"
}
```

**Success (200):**
```json
{
  "ok": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Invalid passphrase (401):**
```json
{
  "ok": false,
  "error": "Invalid frequency"
}
```

**Rate limited (429):**
```json
{
  "ok": false,
  "error": "Too many attempts. Try again later.",
  "retryAfter": 847
}
```

**Malformed request (400):**
```json
{
  "ok": false,
  "error": "Missing passphrase"
}
```

### POST /validate

Validates a JWT without re-hashing the passphrase.

**Request:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Valid (200):**
```json
{
  "valid": true
}
```

**Invalid/expired (401):**
```json
{
  "valid": false,
  "error": "Invalid or expired token"
}
```

### OPTIONS (CORS preflight)

Returns `204 No Content` with CORS headers:
```
Access-Control-Allow-Origin: https://mvxworld.art
Access-Control-Allow-Methods: POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

---

## Rate Limiting

| Parameter | Value |
|-----------|-------|
| Max attempts | 5 per IP |
| Window | 15 minutes |
| Storage | Cloudflare KV, key `rl:{ip}` |
| Lockout | 429 + `Retry-After` header (seconds) |
| Reset | On successful auth, or after window expires |

**Behavior:**
1. Each `/verify` request increments the counter for the client IP
2. After 5 failed attempts, the IP is locked out for the remainder of the 15-minute window
3. Successful authentication resets the counter
4. Counters auto-expire via KV TTL

---

## Session Management

| Property | Value |
|----------|-------|
| Token type | JWT (HMAC-SHA256) |
| Expiry | 24 hours |
| Client storage | `sessionStorage` (tab-scoped) |
| Validation | Server-side via `/validate` |

**Why sessionStorage:** Clears when the tab closes. No persistent login across browser sessions. Matching the original behavior.

**Why server-side validation on reload:** Prevents JWT forgery. Even if someone creates a fake JWT, the Worker rejects it on `/validate`.

---

## Security Properties

| Property | Status |
|----------|--------|
| Hash not in source code | ✓ Worker secret |
| Server-side verification | ✓ Cloudflare Worker |
| Brute-force protection | ✓ 5 attempts / 15 min |
| Timing-attack resistance | ✓ Constant-time compare |
| Session forgery prevention | ✓ JWT signed with secret |
| DOM bypass prevention | ✓ Editor hidden until JWT confirmed |
| CORS restriction | ✓ Only mvxworld.art |

---

## Setup

See `workers/mvxworld-auth/README.md` for full setup instructions.

Quick version:
```bash
cd workers/mvxworld-auth
npm install
npm run setup            # generates Argon2id hash + JWT secret
wrangler secret put ARGON2_HASH
wrangler secret put JWT_SECRET
wrangler deploy
```

DNS: Add CNAME `auth.mvxworld.art → mvxworld-auth.<subdomain>.workers.dev`
