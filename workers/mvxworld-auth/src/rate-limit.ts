import type { Env } from "./types";

/** Maximum failed attempts before lockout */
const MAX_ATTEMPTS = 5;

/** Rate limit window in seconds (15 minutes) */
const WINDOW_SECONDS = 15 * 60;

/** Rate limit check result */
export interface RateLimitResult {
  allowed: boolean;
  remaining: number;
  retryAfter?: number;
}

/**
 * Check and update rate limit for a given IP address.
 * Uses KV for persistence with eventual consistency (acceptable for this use case).
 */
export async function checkRateLimit(
  ip: string,
  kv: KVNamespace
): Promise<RateLimitResult> {
  const key = `rl:${ip}`;
  const now = Date.now();

  const stored = await kv.get(key, { type: "json" }) as {
    count: number;
    firstAttempt: number;
  } | null;

  if (!stored) {
    // First attempt — record it
    await kv.put(
      key,
      JSON.stringify({ count: 1, firstAttempt: now }),
      { expirationTtl: WINDOW_SECONDS }
    );
    return { allowed: true, remaining: MAX_ATTEMPTS - 1 };
  }

  // Check if window has expired
  if (now - stored.firstAttempt > WINDOW_SECONDS * 1000) {
    // Window expired — reset
    await kv.put(
      key,
      JSON.stringify({ count: 1, firstAttempt: now }),
      { expirationTtl: WINDOW_SECONDS }
    );
    return { allowed: true, remaining: MAX_ATTEMPTS - 1 };
  }

  // Within window — check count
  if (stored.count >= MAX_ATTEMPTS) {
    const elapsed = now - stored.firstAttempt;
    const retryAfter = Math.ceil((WINDOW_SECONDS * 1000 - elapsed) / 1000);
    return { allowed: false, remaining: 0, retryAfter };
  }

  // Increment count
  const newCount = stored.count + 1;
  const remainingTtl = Math.ceil(
    (WINDOW_SECONDS * 1000 - (now - stored.firstAttempt)) / 1000
  );

  if (newCount >= MAX_ATTEMPTS) {
    // This attempt triggers lockout
    await kv.put(
      key,
      JSON.stringify({ count: newCount, firstAttempt: stored.firstAttempt }),
      { expirationTtl: remainingTtl }
    );
    return { allowed: false, remaining: 0, retryAfter: remainingTtl };
  }

  await kv.put(
    key,
    JSON.stringify({ count: newCount, firstAttempt: stored.firstAttempt }),
    { expirationTtl: remainingTtl }
  );
  return { allowed: true, remaining: MAX_ATTEMPTS - newCount };
}

/**
 * Reset rate limit for a given IP (e.g., after successful auth).
 */
export async function resetRateLimit(
  ip: string,
  kv: KVNamespace
): Promise<void> {
  await kv.delete(`rl:${ip}`);
}
