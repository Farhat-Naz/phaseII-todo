import createMiddleware from 'next-intl/middleware';
import { locales, defaultLocale } from './i18n';

export default createMiddleware({
  // A list of all locales that are supported
  locales,

  // Used when no locale matches
  defaultLocale,

  // Always use locale prefix in URL (e.g., /en/dashboard, /ur/dashboard)
  localePrefix: 'always',

  // Redirect root to default locale
  defaultLocale,
});

export const config = {
  // Match all pathnames except for
  // - /api routes
  // - /_next (Next.js internals)
  // - /_static (static files)
  // - /_vercel (Vercel internals)
  // - /favicon.ico, /sitemap.xml, /robots.txt (metadata files)
  matcher: ['/', '/((?!api|_next|_static|_vercel|favicon.ico|sitemap.xml|robots.txt).*)'],
};
