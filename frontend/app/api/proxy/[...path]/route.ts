import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth-server';
import { getSignedUrl } from 'better-auth/client';

// Create a proxy to your FastAPI backend
export async function GET(request: NextRequest) {
  // Check if user is authenticated with Better Auth
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  if (!session) {
    return NextResponse.json({ error: 'Not authenticated' }, { status: 401 });
  }

  // Proxy the request to your FastAPI backend
  const fastApiUrl = process.env.FASTAPI_BACKEND_URL || 'http://localhost:8000';
  const backendEndpoint = request.nextUrl.pathname.replace('/api/proxy/', '');
  
  const backendResponse = await fetch(`${fastApiUrl}/${backendEndpoint}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${session.session.token}` // or however you want to pass session info
    }
  });

  const data = await backendResponse.json();
  return NextResponse.json(data, { status: backendResponse.status });
}

export async function POST(request: NextRequest) {
  // Check if user is authenticated with Better Auth
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  if (!session) {
    return NextResponse.json({ error: 'Not authenticated' }, { status: 401 });
  }

  // Get request body
  const body = await request.json();
  
  // Proxy the request to your FastAPI backend
  const fastApiUrl = process.env.FASTAPI_BACKEND_URL || 'http://localhost:8000';
  const backendEndpoint = request.nextUrl.pathname.replace('/api/proxy/', '');
  
  const backendResponse = await fetch(`${fastApiUrl}/${backendEndpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${session.session.token}`
    },
    body: JSON.stringify(body)
  });

  const data = await backendResponse.json();
  return NextResponse.json(data, { status: backendResponse.status });
}

// Similar handlers for PUT, PATCH, DELETE
export async function PUT(request: NextRequest) {
  // Similar implementation
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  if (!session) {
    return NextResponse.json({ error: 'Not authenticated' }, { status: 401 });
  }

  const body = await request.json();
  const fastApiUrl = process.env.FASTAPI_BACKEND_URL || 'http://localhost:8000';
  const backendEndpoint = request.nextUrl.pathname.replace('/api/proxy/', '');
  
  const backendResponse = await fetch(`${fastApiUrl}/${backendEndpoint}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${session.session.token}`
    },
    body: JSON.stringify(body)
  });

  const data = await backendResponse.json();
  return NextResponse.json(data, { status: backendResponse.status });
}

export async function DELETE(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  if (!session) {
    return NextResponse.json({ error: 'Not authenticated' }, { status: 401 });
  }

  const fastApiUrl = process.env.FASTAPI_BACKEND_URL || 'http://localhost:8000';
  const backendEndpoint = request.nextUrl.pathname.replace('/api/proxy/', '');
  
  const backendResponse = await fetch(`${fastApiUrl}/${backendEndpoint}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${session.session.token}`
    }
  });

  const data = await backendResponse.json();
  return NextResponse.json(data, { status: backendResponse.status });
}

// Specify which methods this route handler supports
export const dynamic = 'force-dynamic';