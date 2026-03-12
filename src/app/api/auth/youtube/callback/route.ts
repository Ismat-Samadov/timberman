/**
 * GET /api/auth/youtube/callback
 * Exchanges the OAuth code for tokens and saves YOUTUBE_REFRESH_TOKEN to the DB.
 * Google redirects here after the user grants permission.
 */
import { NextRequest, NextResponse } from 'next/server';
import { getSecret, invalidateSecretsCache } from '@/lib/secrets';
import { db, settings } from '@/lib/db/schema';
import { eq } from 'drizzle-orm';

export async function GET(req: NextRequest) {
  const { searchParams } = req.nextUrl;
  const code = searchParams.get('code');
  const error = searchParams.get('error');

  if (error || !code) {
    const msg = error ?? 'no_code';
    return NextResponse.redirect(
      new URL(`/dashboard/settings/youtube-auth?error=${encodeURIComponent(msg)}`, req.url)
    );
  }

  const [clientId, clientSecret] = await Promise.all([
    getSecret('YOUTUBE_CLIENT_ID'),
    getSecret('YOUTUBE_CLIENT_SECRET'),
  ]);

  if (!clientId || !clientSecret) {
    return NextResponse.redirect(
      new URL('/dashboard/settings/youtube-auth?error=missing_credentials', req.url)
    );
  }

  const redirectUri = `${req.nextUrl.origin}/api/auth/youtube/callback`;

  let tokenData: { refresh_token?: string; access_token?: string; error?: string };
  try {
    const res = await fetch('https://oauth2.googleapis.com/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        code,
        client_id: clientId,
        client_secret: clientSecret,
        redirect_uri: redirectUri,
        grant_type: 'authorization_code',
      }),
    });
    tokenData = await res.json();
  } catch {
    return NextResponse.redirect(
      new URL('/dashboard/settings/youtube-auth?error=token_request_failed', req.url)
    );
  }

  if (tokenData.error) {
    return NextResponse.redirect(
      new URL(`/dashboard/settings/youtube-auth?error=${encodeURIComponent(tokenData.error)}`, req.url)
    );
  }

  if (!tokenData.refresh_token) {
    // This can happen if the user already granted access and Google skipped consent.
    // The prompt=consent on the auth URL should prevent this, but handle it anyway.
    return NextResponse.redirect(
      new URL('/dashboard/settings/youtube-auth?error=no_refresh_token', req.url)
    );
  }

  // Persist refresh token in the settings table (same mechanism as /api/secrets POST)
  const dbKey = 'secret_YOUTUBE_REFRESH_TOKEN';
  const existing = await db.select().from(settings).where(eq(settings.key, dbKey)).limit(1);
  if (existing.length > 0) {
    await db.update(settings)
      .set({ value: tokenData.refresh_token, updated_at: new Date() })
      .where(eq(settings.key, dbKey));
  } else {
    await db.insert(settings).values({ key: dbKey, value: tokenData.refresh_token });
  }
  invalidateSecretsCache();

  return NextResponse.redirect(
    new URL('/dashboard/settings/youtube-auth?success=true', req.url)
  );
}
