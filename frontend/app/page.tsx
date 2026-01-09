'use client';

import Link from 'next/link';
import { useAuth } from '@/hooks/use-auth';

export default function HomePage() {
  const { user, isLoading } = useAuth();

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh]">
      <h1 className="text-4xl font-bold text-gray-800 mb-6">Welcome to Todo App</h1>
      <p className="text-lg text-gray-600 mb-8 text-center max-w-md">
        A multi-user todo application with Eisenhower Matrix prioritization
      </p>

      {isLoading ? (
        <p>Loading...</p>
      ) : user ? (
        <Link href="/dashboard" className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">
          Go to Dashboard
        </Link>
      ) : (
        <div className="space-y-4">
          <Link href="/(auth)/sign-in" className="block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">
            Sign In
          </Link>
          <Link href="/(auth)/sign-up" className="block bg-gray-200 text-gray-800 px-6 py-3 rounded-lg hover:bg-gray-300 transition-colors">
            Sign Up
          </Link>
        </div>
      )}
    </div>
  );
}