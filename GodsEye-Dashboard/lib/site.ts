/** Centralized product/marketing URLs (no hardcoding in components). */

export const SITE = {
  name: "God's Eye",
  tagline: "See inside your AI.",
  githubUrl:
    process.env.NEXT_PUBLIC_GITHUB_URL?.trim() ||
    "https://github.com/Kunal-Vijay/AI-Observablity-Platform",
  productRepoUrl:
    process.env.NEXT_PUBLIC_PRODUCT_GITHUB_URL?.trim() ||
    "https://github.com/anishwar-007/TracerAI",
} as const;
