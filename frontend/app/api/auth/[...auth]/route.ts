// pages/api/auth/[...auth].ts or app/api/auth/[...auth]/route.ts
import { auth } from '@/lib/auth-server';

export const { GET, POST } = auth;