/**
 * Dashboard Page - Main todo management page
 *
 * Features:
 * - Server Component with metadata for SEO
 * - Client-side auth check via TodoList component
 * - Renders TodoList component
 * - Responsive layout
 */

import { Metadata } from 'next';
import { TodoList } from '@/components/features/todos/TodoList';

export const metadata: Metadata = {
  title: 'My Todos | Todo App',
  description: 'Manage your tasks and stay productive',
};

export default function DashboardPage() {
  return (
    <div className="w-full">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">
          My Todos
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Manage your tasks and stay organized
        </p>
      </div>

      <TodoList />
    </div>
  );
}
