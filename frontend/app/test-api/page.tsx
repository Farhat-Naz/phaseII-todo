'use client';

import { useState } from 'react';

export default function TestAPIPage() {
  const [result, setResult] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const testAPI = async () => {
    setLoading(true);
    setResult('');

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      console.log('Testing API at:', apiUrl);
      console.log('Environment variables:', {
        NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
        NODE_ENV: process.env.NODE_ENV
      });

      // Test 1: Health check (hardcoded URL for debugging)
      console.log('Attempting health check...');
      const healthResponse = await fetch('http://localhost:8000/health', {
        mode: 'cors',
      });
      console.log('Health response status:', healthResponse.status);
      const healthData = await healthResponse.json();
      console.log('Health check data:', healthData);

      // Test 2: Register endpoint (hardcoded URL)
      console.log('Attempting register...');
      const registerResponse = await fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: 'test@example.com',
          password: 'TestPass123',
          name: 'Test User',
        }),
      });
      console.log('Register response status:', registerResponse.status);

      const registerData = await registerResponse.json();
      console.log('Register response:', registerData);

      setResult(JSON.stringify({
        health: healthData,
        register: registerData,
        status: registerResponse.status,
      }, null, 2));
    } catch (error) {
      console.error('API Test Error:', error);
      setResult(`Error: ${error instanceof Error ? error.message : String(error)}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold mb-4">API Connection Test</h1>
        <p className="mb-4 text-gray-600">
          API URL: {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}
        </p>

        <button
          onClick={testAPI}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Testing...' : 'Test API Connection'}
        </button>

        {result && (
          <div className="mt-4 p-4 bg-gray-100 rounded">
            <h2 className="font-bold mb-2">Result:</h2>
            <pre className="whitespace-pre-wrap text-sm">{result}</pre>
          </div>
        )}

        <div className="mt-8">
          <h2 className="font-bold mb-2">Check Browser Console (F12) for detailed logs</h2>
        </div>
      </div>
    </div>
  );
}
