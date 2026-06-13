import { argon2id } from "@noble/hashes/argon2";
import { utf8ToBytes, bytesToHex } from "@noble/hashes/utils";
import type { Env } from "./types";

/**
 * Hash a passphrase using Argon2id with the configured parameters.
 * Returns a hex-encoded hash string.
 */
export function hashPassphrase(
  passphrase: string,
  env: Env
): string {
  const timeCost = parseInt(env.ARGON2_TIME_COST || "3", 10);
  const memoryCost = parseInt(env.ARGON2_MEMORY_COST || "32768", 10);
  const parallelism = parseInt(env.ARGON2_PARALLELISM || "1", 10);

  // Extract salt from the stored hash (first 32 bytes = 64 hex chars after the $argon2id$ params$ prefix)
  // The stored format is: $argon2id$v=19$m=32768,t=3,p=1$<salt_b64>$<hash_b64>
  // We hash with the same salt from the stored value
  const storedParams = parseArgon2Hash(env.ARGON2_HASH);
  const salt = storedParams.salt;

  const inputBytes = utf8ToBytes(passphrase);
  const hashBytes = argon2id(inputBytes, salt, {
    t: timeCost,
    m: memoryCost,
    p: parallelism,
    dkLen: 32,
  });

  return bytesToHex(hashBytes);
}

/**
 * Parse an Argon2 encoded hash string.
 * Format: $argon2id$v=19$m=32768,t=3,p=1$<salt_b64>$<hash_b64>
 */
export function parseArgon2Hash(encoded: string): {
  version: number;
  memoryCost: number;
  timeCost: number;
  parallelism: number;
  salt: Uint8Array;
  hash: Uint8Array;
} {
  const parts = encoded.split("$");
  if (parts.length !== 6 || parts[1] !== "argon2id") {
    throw new Error("Invalid Argon2id hash format");
  }

  const version = parseInt(parts[2].replace("v=", ""), 10);
  const params = parts[3].split(",");
  const memoryCost = parseInt(params[0].replace("m=", ""), 10);
  const timeCost = parseInt(params[1].replace("t=", ""), 10);
  const parallelism = parseInt(params[2].replace("p=", ""), 10);

  const salt = b64ToBytes(parts[4]);
  const hash = b64ToBytes(parts[5]);

  return { version, memoryCost, timeCost, parallelism, salt, hash };
}

/**
 * Encode a passphrase hash in standard Argon2id format.
 */
export function encodeArgon2Hash(
  salt: Uint8Array,
  hashBytes: Uint8Array,
  memoryCost: number,
  timeCost: number,
  parallelism: number
): string {
  return `$argon2id$v=19$m=${memoryCost},t=${timeCost},p=${parallelism}$${bytesToB64(salt)}$${bytesToB64(hashBytes)}`;
}

/**
 * Constant-time string comparison to prevent timing attacks.
 * Compares two hex strings byte-by-byte.
 */
export function constantTimeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let result = 0;
  for (let i = 0; i < a.length; i++) {
    result |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return result === 0;
}

/**
 * Verify a passphrase against the stored Argon2id hash.
 */
export function verifyPassphrase(
  passphrase: string,
  env: Env
): boolean {
  const storedParams = parseArgon2Hash(env.ARGON2_HASH);
  const timeCost = parseInt(env.ARGON2_TIME_COST || "3", 10);
  const memoryCost = parseInt(env.ARGON2_MEMORY_COST || "32768", 10);
  const parallelism = parseInt(env.ARGON2_PARALLELISM || "1", 10);

  const inputBytes = utf8ToBytes(passphrase);
  const hashBytes = argon2id(inputBytes, storedParams.salt, {
    t: timeCost,
    m: memoryCost,
    p: parallelism,
    dkLen: 32,
  });

  const computedHex = bytesToHex(hashBytes);
  const storedHex = bytesToHex(storedParams.hash);

  return constantTimeEqual(computedHex, storedHex);
}

// --- Base64 helpers (standard Argon2 base64, NOT URL-safe) ---

function b64ToBytes(b64: string): Uint8Array {
  // Standard base64 decode
  const binary = atob(b64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes;
}

function bytesToB64(bytes: Uint8Array): string {
  let binary = "";
  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}
