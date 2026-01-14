import { betterAuth } from 'better-auth';

// Initialize Better Auth server-side
export const auth = betterAuth({
  database: {
    provider: 'postgresql', // Assuming you're using PostgreSQL based on your pyproject.toml
    url: process.env.DATABASE_URL || 'postgresql://user:password@localhost:5432/todo_app',
  },
  // Define your application's authentication strategies
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Set to true in production
  },
  socialProviders: {
    // Add social providers if needed
    // google: {
    //   clientId: process.env.GOOGLE_CLIENT_ID!,
    //   clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    // },
  },
  secret: process.env.BETTER_AUTH_SECRET || 'your-secret-key-change-in-production',
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:3000',
  // Enable JWT for use with external services
  jwt: {
    secret: process.env.BETTER_AUTH_JWT_SECRET || process.env.BETTER_AUTH_SECRET || 'jwt-secret-change-in-production',
    expiresIn: '7d',
    algorithm: 'HS512',
  },
  session: {
    expiresIn: 7 * 24 * 60 * 60, // 7 days
    slidingExpiration: true, // Refresh session on activity
  },
});