import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    // Use standard Node.js test environment instead of Workers pool
    // to avoid version compatibility issues with @cloudflare/vitest-pool-workers
    environment: "node",
    testTimeout: 30000,
  },
});
