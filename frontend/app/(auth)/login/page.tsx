import { Metadata } from 'next';
import { LoginForm } from '@/components/features/auth/LoginForm';
import { Card } from '@/components/ui/Card';

export const metadata: Metadata = {
  title: 'Sign In - Todo App',
  description: 'Sign in to access your todo list',
};

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 px-4 py-12">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Welcome Back
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Sign in to continue managing your tasks
          </p>
        </div>

        {/* Login Card */}
        <Card variant="elevated" padding="lg" className="animate-slide-up">
          <LoginForm />
        </Card>

        {/* Footer */}
        <p className="text-center text-sm text-gray-500 dark:text-gray-400 mt-8">
          Need help?{' '}
          <a href="#" className="text-primary-600 hover:text-primary-700 dark:text-primary-400">
            Contact support
          </a>
        </p>
      </div>
    </div>
  );
}
