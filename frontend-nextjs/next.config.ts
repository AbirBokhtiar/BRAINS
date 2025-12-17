import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactCompiler: true,
  typescript: {
    ignoreBuildErrors: true,
  },
  
  turbopack: {
    // Enables Turbopack for development builds only.
    // Recommended for most users, but can be disabled if necessary.
    rules:{},
  },
};

export default nextConfig;
