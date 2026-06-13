import { verifyPassphrase } from "./auth";
import { checkRateLimit, resetRateLimit } from "./rate-limit";
import type { Env, VerifyRequest, VerifyResponse, ValidateResponse } from "./types";

// --- JWT helpers (HMAC-SHA256, no external library) ---

function base64url(data: Uint8Array | string): string {
  const bytes = typeof data === "string" ? new TextEncoder().encode(data) : data;
  let binary = "";
  for (let i = 0; i < bytes.length; i++) binary += String.fromCharCode(bytes[i]);
  return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function base64urlDecode(str: string): Uint8Array {
  const padded = str.replace(/-/g, "+").replace(/_/g, "/") + "=".repeat((4 - (str.length % 4)) % 4);
  const binary = atob(padded);
  return new Uint8Array([...binary].map((c) => c.charCodeAt(0)));
}

async function hmacKey(secret: string): Promise<CryptoKey> {
  return crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign", "verify"]
  );
}

async function signJWT(secret: string, payload: Record<string, unknown>, expiresInSec: number): Promise<string> {
  const header = base64url(JSON.stringify({ alg: "HS256", typ: "JWT" }));
  const now = Math.floor(Date.now() / 1000);
  const body = base64url(JSON.stringify({ ...payload, iat: now, exp: now + expiresInSec }));
  const data = `${header}.${body}`;
  const key = await hmacKey(secret);
  const sig = new Uint8Array(await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(data)));
  return `${data}.${base64url(sig)}`;
}

async function verifyJWT(secret: string, token: string): Promise<Record<string, unknown> | null> {
  const parts = token.split(".");
  if (parts.length !== 3) return null;

  const [header, body, sig] = parts;
  const key = await hmacKey(secret);
  const valid = await crypto.subtle.verify(
    "HMAC",
    key,
    base64urlDecode(sig),
    new TextEncoder().encode(`${header}.${body}`)
  );
  if (!valid) return null;

  const payload = JSON.parse(new TextDecoder().decode(base64urlDecode(body)));
  if (payload.exp && payload.exp < Math.floor(Date.now() / 1000)) return null;

  return payload;
}

// --- Request handlers ---

function corsHeaders(origin: string): Record<string, string> {
  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
  };
}

function jsonResponse(data: unknown, status: number, cors: Record<string, string>): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", ...cors },
  });
}

function getClientIP(request: Request): string {
  return request.headers.get("CF-Connecting-IP") || request.headers.get("X-Forwarded-For") || "unknown";
}

async function handleVerify(request: Request, env: Env, cors: Record<string, string>): Promise<Response> {
  if (request.method !== "POST") {
    return jsonResponse({ ok: false, error: "Method not allowed" } satisfies VerifyResponse, 405, cors);
  }

  const ip = getClientIP(request);

  // Rate limit check
  const rl = await checkRateLimit(ip, env.RATE_LIMIT_KV);
  if (!rl.allowed) {
    return jsonResponse(
      { ok: false, error: "Too many attempts. Try again later.", retryAfter: rl.retryAfter } satisfies VerifyResponse,
      429,
      { ...cors, "Retry-After": String(rl.retryAfter) }
    );
  }

  // Parse request
  let body: VerifyRequest;
  try {
    body = await request.json();
  } catch {
    return jsonResponse({ ok: false, error: "Invalid JSON" } satisfies VerifyResponse, 400, cors);
  }

  if (!body.passphrase || typeof body.passphrase !== "string") {
    return jsonResponse({ ok: false, error: "Missing passphrase" } satisfies VerifyResponse, 400, cors);
  }

  if (!env.ARGON2_HASH) {
    return jsonResponse({ ok: false, error: "Server not configured" } satisfies VerifyResponse, 500, cors);
  }

  // Verify passphrase
  const valid = verifyPassphrase(body.passphrase, env);

  if (!valid) {
    return jsonResponse(
      { ok: false, error: "Invalid frequency" } satisfies VerifyResponse,
      401,
      cors
    );
  }

  // Success — reset rate limit and issue JWT
  await resetRateLimit(ip, env.RATE_LIMIT_KV);
  const token = await signJWT(env.JWT_SECRET, { sub: "studio" }, 24 * 60 * 60);

  return jsonResponse({ ok: true, token } satisfies VerifyResponse, 200, cors);
}

async function handleValidate(request: Request, env: Env, cors: Record<string, string>): Promise<Response> {
  if (request.method !== "POST") {
    return jsonResponse({ valid: false, error: "Method not allowed" } satisfies ValidateResponse, 405, cors);
  }

  let body: { token?: string };
  try {
    body = await request.json();
  } catch {
    return jsonResponse({ valid: false, error: "Invalid JSON" } satisfies ValidateResponse, 400, cors);
  }

  if (!body.token || typeof body.token !== "string") {
    return jsonResponse({ valid: false, error: "Missing token" } satisfies ValidateResponse, 400, cors);
  }

  const payload = await verifyJWT(env.JWT_SECRET, body.token);
  if (!payload) {
    return jsonResponse({ valid: false, error: "Invalid or expired token" } satisfies ValidateResponse, 401, cors);
  }

  return jsonResponse({ valid: true } satisfies ValidateResponse, 200, cors);
}

// --- Main Worker export ---

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const origin = env.ALLOWED_ORIGIN || "https://mvxworld.art";
    const cors = corsHeaders(origin);

    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors });
    }

    const url = new URL(request.url);

    try {
      switch (url.pathname) {
        case "/verify":
          return await handleVerify(request, env, cors);
        case "/validate":
          return await handleValidate(request, env, cors);
        default:
          return jsonResponse({ error: "Not found" }, 404, cors);
      }
    } catch (err) {
      return jsonResponse({ error: "Internal server error" }, 500, cors);
    }
  },
};
