import { Metadata } from 'next';
import Link from 'next/link';
import { getTranslations } from 'next-intl/server';
import { RegisterForm } from '@/components/features/auth/RegisterForm';
import { Card } from '@/components/ui/Card';
import { LanguageSwitcher } from '@/components/features/shared/LanguageSwitcher';

export async function generateMetadata({ params: { locale } }: { params: { locale: string } }): Promise<Metadata> {
  const t = await getTranslations({ locale, namespace: 'auth' });

  return {
    title: `${t('register')} | TodoApp`,
    description: t('register'),
  };
}

export default function RegisterPage({ params: { locale } }: { params: { locale: string } }) {
  return (
    <div className={`min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 via-white to-gray-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-12 px-4 sm:px-6 lg:px-8 ${locale === 'ur' ? 'font-urdu' : ''}`}>
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <Link href={`/${locale}`}>
            <h1 className="text-4xl font-bold text-primary-600 dark:text-primary-400 mb-2">
              TodoApp
            </h1>
          </Link>
          <div className="flex justify-center mt-4">
            <LanguageSwitcher />
          </div>
        </div>

        {/* Register Card */}
        <Card variant="elevated" padding="lg">
          <RegisterForm locale={locale} />
        </Card>
      </div>
    </div>
  );
}
