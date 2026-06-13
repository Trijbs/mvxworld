export interface Env {
  /** Argon2id hash of the passphrase, set via `wrangler secret put ARGON2_HASH` */
  ARGON2_HASH: string;

  /** HMAC-SHA256 key for JWT signing, set via `wrangler secret put JWT_SECRET` */
  JWT_SECRET: string;

  /** KV namespace for rate limiting */
  RATE_LIMIT_KV: KVNamespace;

  /** Allowed CORS origin */
  ALLOWED_ORIGIN: string;

  /** Argon2id time cost (default: 3) */
  ARGON2_TIME_COST: string;

  /** Argon2id memory cost in KB (default: 32768 = 32 MB) */
  ARGON2_MEMORY_COST: string;

  /** Argon2id parallelism (default: 1) */
  ARGON2_PARALLELISM: string;
}

export interface VerifyRequest {
  passphrase: string;
}

export interface VerifyResponse {
  ok: boolean;
  token?: string;
  error?: string;
  retryAfter?: number;
}

export interface ValidateResponse {
  valid: boolean;
  error?: string;
}
