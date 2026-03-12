/**
 * GET /api/auth/youtube
 * Redirects to Google OAuth consent screen.
 * Requires YOUTUBE_CLIENT_ID to be set in secrets.
 * The redirect_uri is built from the incoming request origin so it works on any deployment.
 */
import { NextRequest, NextResponse } from 'next/server';
import { validateSession } from '@/lib/auth';
import { getSecret } from '@/lib/secrets';

const SCOPES = [
  'https://www.googleapis.com/auth/youtube.upload',
  'https://www.googleapis.com/auth/youtube.readonly',
].join(' ');

export async function GET(req: NextRequest) {
  if (!validateSession(req)) {
    return NextResponse.redirect(new URL('/login', req.url));
  }

  const clientId = await getSecret('YOUTUBE_CLIENT_ID');
  if (!clientId) {
    return NextResponse.redirect(
      new URL('/dashboard/settings/youtube-auth?error=no_client_id', req.url)
    );
  }

  const redirectUri = `${req.nextUrl.origin}/api/auth/youtube/callback`;

  const params = new URLSearchParams({
    client_id: clientId,
    redirect_uri: redirectUri,
    response_type: 'code',
    scope: SCOPES,
    access_type: 'offline',
    prompt: 'consent', // always prompt so we always get a refresh_token
  });

  return NextResponse.redirect(
    `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`
  );
}
