# mvxworld-auth

Cloudflare Worker that handles passphrase verification for the MVXWorld online studio.

Uses Argon2id (memory-hard key derivation) with server-side verification. The passphrase hash is stored as a Worker secret — never exposed in source code.

## Setup

### Prerequisites

- Node.js 18+
- Cloudflare account (free tier works)
- `wrangler` CLI: `npm install -g wrangler`

### 1. Install dependencies

```bash
cd workers/mvxworld-auth
npm install
```

### 2. Authenticate with Cloudflare

```bash
wrangler login
```

### 3. Create KV namespace for rate limiting

```bash
wrangler kv namespace create RATE_LIMIT_KV
```

Copy the returned ID into `wrangler.jsonc` → `kv_namespaces[0].id`.

### 4. Generate secrets

```bash
npm run setup
```

The script prompts for a passphrase and outputs two secrets:
- `ARGON2_HASH` — the Argon2id hash of your passphrase
- `JWT_SECRET` — a random signing key for session tokens

### 5. Set Worker secrets

```bash
wrangler secret put ARGON2_HASH    # paste the Argon2id hash
wrangler secret put JWT_SECRET     # paste the JWT signing key
```

### 6. Deploy

```bash
wrangler deploy
```

### 7. DNS

Add a CNAME record in your DNS settings:

```
auth.mvxworld.art → mvxworld-auth.<your-subdomain>.workers.dev
```

Or configure a Workers route in `wrangler.jsonc`.

## Development

```bash
# Local dev server
npm run dev

# Run tests
npm test

# Deploy
npm run deploy
```

## Architecture

```
POST /verify   { passphrase } → { ok, token } | { error }
POST /validate { token }      → { valid }      | { error }
OPTIONS        (CORS preflight)
```

### Rate Limiting

- 5 attempts per IP per 15-minute window
- Stored in Cloudflare KV
- Resets on successful auth or after window expires

### Sessions

- HMAC-SHA256 signed JWT
- 24-hour expiry
- Stored in browser sessionStorage
- Validated server-side on page reload

## Files

```
src/
  index.ts       — Main request handler, CORS, routing
  auth.ts        — Argon2id verify, JWT sign/verify, constant-time compare
  rate-limit.ts  — KV-based per-IP rate limiting
  types.ts       — TypeScript interfaces
scripts/
  setup.mjs      — Generates Argon2id hash and JWT secret
test/
  auth.test.ts   — Unit tests (16 tests)
wrangler.jsonc   — Worker configuration
```

## Secrets

| Secret | Set via | Purpose |
|--------|---------|---------|
| `ARGON2_HASH` | `wrangler secret put` | Argon2id hash of the passphrase |
| `JWT_SECRET` | `wrangler secret put` | HMAC-SHA256 key for JWT signing |

These are encrypted at rest and never exposed in source code or the Cloudflare dashboard API.

## Argon2id Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| memoryCost | 32768 KB (32 MB) | Fits free tier's 128 MB isolate limit |
| timeCost | 3 | ~700ms per hash on Cloudflare edge |
| parallelism | 1 | Single-threaded in Workers |
| hashLength | 32 bytes | Standard 256-bit output |
