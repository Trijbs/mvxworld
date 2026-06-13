#!/usr/bin/env node

/**
 * Setup script for mvxworld-auth.
 * Generates an Argon2id hash and JWT secret for the Cloudflare Worker.
 *
 * Usage:
 *   cd workers/mvxworld-auth
 *   npm run setup
 *
 * Then follow the prompts to set the secrets via wrangler.
 */

import { createInterface } from "node:readline";
import { randomBytes } from "node:crypto";

// Import @noble/hashes for Argon2id
const { argon2id } = await import("@noble/hashes/argon2");
const { utf8ToBytes, bytesToHex } = await import("@noble/hashes/utils");

const ARGON2_PARAMS = {
  t: 3,
  m: 32768,
  p: 1,
  dkLen: 32,
};

function prompt(question) {
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer);
    });
  });
}

function bytesToB64(bytes) {
  let binary = "";
  for (let i = 0; i < bytes.length; i++) binary += String.fromCharCode(bytes[i]);
  return btoa(binary);
}

async function main() {
  console.log("\n╔══════════════════════════════════════════╗");
  console.log("║   mvxworld-auth · Argon2id Setup         ║");
  console.log("╚══════════════════════════════════════════╝\n");

  console.log("This script generates the secrets needed for the auth Worker.\n");

  // Get passphrase
  const passphrase = await prompt("Enter your passphrase: ");
  if (!passphrase || passphrase.length < 8) {
    console.error("Error: Passphrase must be at least 8 characters.");
    process.exit(1);
  }

  const confirmPassphrase = await prompt("Confirm passphrase: ");
  if (passphrase !== confirmPassphrase) {
    console.error("Error: Passphrases do not match.");
    process.exit(1);
  }

  console.log("\nHashing with Argon2id (this may take a few seconds)...");
  console.log(`  memoryCost: ${ARGON2_PARAMS.m} KB (${ARGON2_PARAMS.m / 1024} MB)`);
  console.log(`  timeCost: ${ARGON2_PARAMS.t}`);
  console.log(`  parallelism: ${ARGON2_PARAMS.p}`);

  const salt = randomBytes(16);
  const inputBytes = utf8ToBytes(passphrase);
  const start = Date.now();
  const hashBytes = argon2id(inputBytes, salt, ARGON2_PARAMS);
  const elapsed = Date.now() - start;

  console.log(`  Hash computed in ${elapsed}ms\n`);

  // Encode in standard Argon2 format
  const encoded = `$argon2id$v=19$m=${ARGON2_PARAMS.m},t=${ARGON2_PARAMS.t},p=${ARGON2_PARAMS.p}$${bytesToB64(salt)}$${bytesToB64(hashBytes)}`;

  // Generate JWT secret
  const jwtSecret = randomBytes(32).toString("hex");

  console.log("─── Secrets ───────────────────────────────\n");
  console.log("Set these via wrangler:\n");
  console.log(`  wrangler secret put ARGON2_HASH`);
  console.log(`  ↓ paste this value:\n`);
  console.log(`  ${encoded}\n`);
  console.log(`  wrangler secret put JWT_SECRET`);
  console.log(`  ↓ paste this value:\n`);
  console.log(`  ${jwtSecret}\n`);
  console.log("─── Deploy ────────────────────────────────\n");
  console.log("  npx wrangler deploy\n");
  console.log("─── DNS ───────────────────────────────────\n");
  console.log("  Add a CNAME record in your DNS:");
  console.log("  auth.mvxworld.art → mvxworld-auth.<your-subdomain>.workers.dev\n");
  console.log("Done.");
}

main().catch((err) => {
  console.error("Setup failed:", err);
  process.exit(1);
});
