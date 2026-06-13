import { describe, it, expect } from "vitest";
import { verifyPassphrase, hashPassphrase, constantTimeEqual, parseArgon2Hash, encodeArgon2Hash } from "../src/auth";

// Test Argon2id hash for passphrase "test-frequency-2026"
// Salt: 0x0102030405060708090a0b0c0d0e0f10
const TEST_ENCODED_HASH =
  "$argon2id$v=19$m=32768,t=3,p=1$AQIDBAUGBwgJCgsMDQ4PEA==$089zn1cbQdpjcrlO6WyA7AiHnkMtcD66wrttGI+YK9o=";

function makeEnv(overrides: Record<string, unknown> = {}) {
  return {
    ARGON2_HASH: TEST_ENCODED_HASH,
    JWT_SECRET: "test-jwt-secret-32-chars-long!!",
    RATE_LIMIT_KV: {} as any,
    ALLOWED_ORIGIN: "https://mvxworld.art",
    ARGON2_TIME_COST: "3",
    ARGON2_MEMORY_COST: "32768",
    ARGON2_PARALLELISM: "1",
    ...overrides,
  } as any;
}

describe("constantTimeEqual", () => {
  it("returns true for equal strings", () => {
    expect(constantTimeEqual("abcdef", "abcdef")).toBe(true);
  });

  it("returns false for different strings", () => {
    expect(constantTimeEqual("abcdef", "abcdeg")).toBe(false);
  });

  it("returns false for different lengths", () => {
    expect(constantTimeEqual("abc", "abcd")).toBe(false);
  });

  it("returns true for empty strings", () => {
    expect(constantTimeEqual("", "")).toBe(true);
  });
});

describe("parseArgon2Hash", () => {
  it("parses a valid Argon2id hash", () => {
    const result = parseArgon2Hash(TEST_ENCODED_HASH);
    expect(result.version).toBe(19);
    expect(result.memoryCost).toBe(32768);
    expect(result.timeCost).toBe(3);
    expect(result.parallelism).toBe(1);
    expect(result.salt.length).toBe(16);
    expect(result.hash.length).toBe(32);
  });

  it("throws on invalid format", () => {
    expect(() => parseArgon2Hash("not-a-hash")).toThrow("Invalid Argon2id hash format");
  });

  it("throws on wrong algorithm", () => {
    expect(() => parseArgon2Hash("$argon2i$v=19$m=32768,t=3,p=1$AQIDBA==$AQIDBA==")).toThrow(
      "Invalid Argon2id hash format"
    );
  });
});

describe("encodeArgon2Hash", () => {
  it("round-trips through parse", () => {
    const parsed = parseArgon2Hash(TEST_ENCODED_HASH);
    const encoded = encodeArgon2Hash(parsed.salt, parsed.hash, parsed.memoryCost, parsed.timeCost, parsed.parallelism);
    expect(encoded).toBe(TEST_ENCODED_HASH);
  });
});

describe("verifyPassphrase", () => {
  it("accepts correct passphrase", () => {
    const env = makeEnv();
    expect(verifyPassphrase("test-frequency-2026", env)).toBe(true);
  });

  it("rejects wrong passphrase", () => {
    const env = makeEnv();
    expect(verifyPassphrase("wrong-passphrase", env)).toBe(false);
  });

  it("rejects empty passphrase", () => {
    const env = makeEnv();
    expect(verifyPassphrase("", env)).toBe(false);
  });

  it("is case-sensitive", () => {
    const env = makeEnv();
    expect(verifyPassphrase("Test-Frequency-2026", env)).toBe(false);
  });
});

describe("hashPassphrase", () => {
  it("produces consistent output for same input and salt", () => {
    const env = makeEnv();
    const hash1 = hashPassphrase("test-frequency-2026", env);
    const hash2 = hashPassphrase("test-frequency-2026", env);
    expect(hash1).toBe(hash2);
  });

  it("produces different output for different input", () => {
    const env = makeEnv();
    const hash1 = hashPassphrase("test-frequency-2026", env);
    const hash2 = hashPassphrase("different-passphrase", env);
    expect(hash1).not.toBe(hash2);
  });

  it("returns a 64-char hex string", () => {
    const env = makeEnv();
    const hash = hashPassphrase("test-frequency-2026", env);
    expect(hash).toMatch(/^[0-9a-f]{64}$/);
  });
});

describe("timing attack resistance", () => {
  it("takes similar time for correct and incorrect passphrases", () => {
    const env = makeEnv();

    // Warm up
    verifyPassphrase("test-frequency-2026", env);
    verifyPassphrase("wrong", env);

    // Measure correct passphrase
    const iterations = 3;
    const correctTimes: number[] = [];
    const incorrectTimes: number[] = [];

    for (let i = 0; i < iterations; i++) {
      const start1 = performance.now();
      verifyPassphrase("test-frequency-2026", env);
      correctTimes.push(performance.now() - start1);

      const start2 = performance.now();
      verifyPassphrase("wrong-passphrase-here", env);
      incorrectTimes.push(performance.now() - start2);
    }

    const avgCorrect = correctTimes.reduce((a, b) => a + b) / iterations;
    const avgIncorrect = incorrectTimes.reduce((a, b) => a + b) / iterations;

    // Both should take roughly the same time (Argon2id is deterministic cost)
    // Allow 50% variance since both go through the same Argon2id computation
    const ratio = avgCorrect / avgIncorrect;
    expect(ratio).toBeGreaterThan(0.5);
    expect(ratio).toBeLessThan(2.0);
  });
});
