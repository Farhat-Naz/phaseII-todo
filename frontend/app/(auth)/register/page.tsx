import { Metadata } from 'next';
import { RegisterForm } from '@/components/features/auth/RegisterForm';
import { Card } from '@/components/ui/Card';

export const metadata: Metadata = {
  title: 'Create Account - Todo App',
  description: 'Create a new account to start managing your todos',
};

export default function RegisterPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 px-4 py-12">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Create Account
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Sign up to start organizing your tasks
          </p>
        </div>

        {/* Registration Card */}
        <Card variant="elevated" padding="lg" className="animate-slide-up">
          <RegisterForm />
        </Card>

        {/* Footer */}
        <p className="text-center text-sm text-gray-500 dark:text-gray-400 mt-8">
          By creating an account, you agree to our{' '}
          <a href="#" className="text-primary-600 hover:text-primary-700 dark:text-primary-400">
            Terms of Service
          </a>{' '}
          and{' '}
          <a href="#" className="text-primary-600 hover:text-primary-700 dark:text-primary-400">
            Privacy Policy
          </a>
        </p>
      </div>
    </div>
  );
}
