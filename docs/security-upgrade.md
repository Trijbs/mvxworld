# Security Upgrade: SHA-256 → Argon2id

**Date:** 13 June 2026

---

## Executive Summary

Replaced the client-side SHA-256 passphrase gate with server-side Argon2id verification via a Cloudflare Worker. The passphrase hash is no longer exposed in public source code. Brute-force attacks are mitigated by rate limiting.

---

## Vulnerabilities Fixed

### 1. Client-side-only authentication (CRITICAL — FIXED)

**Before:** Verification was entirely client-side JavaScript. Anyone could bypass by running `document.getElementById('gate').style.display='none'` in DevTools.

**After:** Verification happens server-side on the Cloudflare Worker. The client sends the passphrase to `/verify` and receives a JWT only on success. The editor is hidden until a valid JWT is confirmed with the Worker.

### 2. Hash exposed in source code (HIGH — FIXED)

**Before:** The SHA-256 hash `ec51e69e52dff050833027e5c74a0bd3d1137c929ddad86aee9bf5c2f0807acc` was hardcoded in `_transmissie/console.html`, visible to anyone viewing the source of a public repository.

**After:** The Argon2id hash is stored as an encrypted Cloudflare Worker secret (`wrangler secret put ARGON2_HASH`). It never appears in source code, is not accessible via the repo, and cannot be read back from the Cloudflare dashboard.

### 3. SHA-256 is fast (HIGH — FIXED)

**Before:** SHA-256 is designed for speed. A modern GPU can compute ~10 billion hashes per second. Offline dictionary/brute-force attacks against the exposed hash are trivial.

**After:** Argon2id is a memory-hard key derivation function. With `memoryCost: 32768` (32 MB) and `timeCost: 3`, each hash attempt requires 32 MB of RAM and ~1 second of computation. Parallel attacks are expensive and impractical.

### 4. No rate limiting (HIGH — FIXED)

**Before:** No limit on passphrase attempts. A script could try thousands of phrases per second client-side.

**After:** Rate limiting via Cloudflare KV: 5 attempts per IP address per 15-minute window. Returns HTTP 429 with `Retry-After` header on lockout.

### 5. Session bypass (MEDIUM — FIXED)

**Before:** `sessionStorage.setItem('mvx-studio-unlocked', '1')` + page refresh = unlocked. No server-side validation.

**After:** Session persistence uses a signed JWT stored in sessionStorage. On page reload, the JWT is validated against the Worker's `/validate` endpoint. Invalid or expired tokens are rejected and cleared.

### 6. No timing-attack resistance (LOW — FIXED)

**Before:** String equality comparison (`===`) on hex hashes leaks timing information.

**After:** Constant-time comparison function (`constantTimeEqual`) used for hash comparison. Additionally, Argon2id's inherent timing variance makes timing attacks impractical.

---

## Architecture

```
Browser (console.html)          Cloudflare Worker (auth.mvxworld.art)
┌──────────────────┐            ┌─────────────────────────────┐
│ User enters      │──POST─────▶│ /verify                     │
│ passphrase       │            │  1. Rate limit check (KV)   │
│                  │            │  2. Argon2id hash(input)    │
│                  │            │  3. Constant-time compare   │
│                  │◀───────────│  4. Return JWT on success   │
│ Store JWT in     │ { ok, tk } │                             │
│ sessionStorage   │            │ Secrets:                    │
│                  │            │  ARGON2_HASH (the hash)     │
│ On reload:       │            │  JWT_SECRET (signing key)   │
│ validate JWT     │            │                             │
└──────────────────┘            └─────────────────────────────┘
```

### Argon2id Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `memoryCost` | 32768 KB (32 MB) | Fits Cloudflare free tier's 128 MB isolate limit |
| `timeCost` | 3 | ~1 second per hash on Cloudflare edge |
| `parallelism` | 1 | Single-threaded in Workers |
| `hashLength` | 32 bytes | Standard 256-bit output |

### Rate Limiting

| Parameter | Value |
|-----------|-------|
| Max attempts | 5 per IP |
| Window | 15 minutes |
| Storage | Cloudflare KV |
| Lockout response | HTTP 429 + `Retry-After` header |

### JWT Sessions

| Parameter | Value |
|-----------|-------|
| Algorithm | HMAC-SHA256 |
| Expiry | 24 hours |
| Storage (client) | sessionStorage |
| Payload | `{ sub: "studio", iat, exp }` |

---

## Migration

### Old System
- `FREQUENCY_HASH` constant in `_transmissie/console.html`
- SHA-256 hash of passphrase, hardcoded in public source
- Client-side comparison via `crypto.subtle.digest`

### New System
- `ARGON2_HASH` stored as Cloudflare Worker secret
- Argon2id hash of passphrase, never in source code
- Server-side verification on `auth.mvxworld.art`
- JWT-based session management

### Migration Steps
1. Deploy Cloudflare Worker (see `docs/authentication-flow.md`)
2. Run `npm run setup` to generate Argon2id hash
3. Set Worker secrets via `wrangler secret put`
4. Add DNS CNAME: `auth.mvxworld.art → mvxworld-auth.<subdomain>.workers.dev`
5. Deploy: `wrangler deploy`
6. Commit updated `_transmissie/console.html` (removes old SHA-256 code)

---

## Remaining Risks

| Risk | Severity | Mitigation |
|------|----------|-----------|
| KV rate limit eventual consistency | Low | Acceptable for single-user auth; 1-second window |
| Worker cold start | Negligible | V8 isolates: < 1ms cold start |
| JWT secret compromise | Medium | Rotate via `wrangler secret put JWT_SECRET`; old tokens expire in 24h |
| Path discoverability | Low | `robots.txt` `Disallow` confirms path; not linked from public pages |
| Denial of service on Worker | Low | Cloudflare's built-in DDoS protection |

---

## Files Modified

| File | Change |
|------|--------|
| `_transmissie/console.html` | Removed SHA-256, added Worker-based auth |
| `README.md` | Updated passphrase setup instructions |
| `.gitignore` | Added `.wrangler/` and `.dev.vars` |

## Files Created

| File | Purpose |
|------|---------|
| `workers/mvxworld-auth/wrangler.jsonc` | Worker config |
| `workers/mvxworld-auth/package.json` | Dependencies |
| `workers/mvxworld-auth/src/index.ts` | Main handler |
| `workers/mvxworld-auth/src/auth.ts` | Argon2id + JWT logic |
| `workers/mvxworld-auth/src/rate-limit.ts` | Rate limiting |
| `workers/mvxworld-auth/src/types.ts` | Type definitions |
| `workers/mvxworld-auth/scripts/setup.mjs` | Hash generation script |
| `workers/mvxworld-auth/test/auth.test.ts` | Unit tests |
| `docs/security-upgrade.md` | This document |
| `docs/authentication-flow.md` | Flow documentation |
