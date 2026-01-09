import { NextRequest, NextResponse } from 'next/server';

// This function protects routes that require authentication
export function middleware(request: NextRequest) {
  // Get the token from cookies or headers
  const token = request.cookies.get('jwt_token')?.value ||
                request.headers.get('authorization')?.replace('Bearer ', '');

  // Define protected routes
  const protectedPaths = ['/dashboard', '/tasks', '/api/tasks'];
  const currentPath = request.nextUrl.pathname;

  // Check if the current path is protected
  const isProtected = protectedPaths.some(path =>
    currentPath.startsWith(path)
  );

  // If accessing a protected route without a valid token, redirect to sign-in
  if (isProtected && !token) {
    return NextResponse.redirect(new URL('/(auth)/sign-in', request.url));
  }

  // Continue with the request
  return NextResponse.next();
}

// Define which paths the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};