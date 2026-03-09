# Environment Variables — Setup Guides

All secrets are managed from the admin dashboard at `/dashboard/secrets` and stored in NeonDB.
You only need **4 vars on Vercel** and **2 secrets on GitHub Actions** to bootstrap the system.

---

## Bootstrap Variables (set manually — not in dashboard)

These must be set before the dashboard is reachable. Set them in Vercel → Settings → Environment Variables and locally in `.env.local`.

| Variable | Platform | Description | Guide |
|---|---|---|---|
| `DATABASE_URL` | Vercel + local | NeonDB connection string | [neondb.md](./neondb.md) |
| `PIPELINE_SECRET_KEY` | Vercel + GitHub Actions | Authenticates pipeline → API calls | [bootstrap.md](./bootstrap.md) |
| `DASHBOARD_PASSWORD` | Vercel | Dashboard login password | [bootstrap.md](./bootstrap.md) |
| `AUTH_TOKEN` | Vercel | Session cookie signing secret | [bootstrap.md](./bootstrap.md) |
| `APP_URL` | GitHub Actions | Vercel deployment URL | [bootstrap.md](./bootstrap.md) |

---

## Secrets (managed from Dashboard → Secrets page)

Once the dashboard is deployed, add all other keys at `/dashboard/secrets`. They are stored encrypted in NeonDB and fetched by the pipeline at runtime — no GitHub Actions secrets needed beyond the 2 bootstrap ones.

| Variable | Service | Guide |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude AI (script generation) | [anthropic.md](./anthropic.md) |
| `ELEVENLABS_API_KEY` | ElevenLabs (TTS voiceover) | [elevenlabs.md](./elevenlabs.md) |
| `ELEVENLABS_VOICE_ID` | ElevenLabs (which voice to use) | [elevenlabs.md](./elevenlabs.md) |
| `FAL_KEY` | fal.ai — Kling 2.6 Pro video clips | [fal.md](./fal.md) |
| `R2_ACCOUNT_ID` | Cloudflare R2 | [cloudflare-r2.md](./cloudflare-r2.md) |
| `R2_ACCESS_KEY_ID` | Cloudflare R2 | [cloudflare-r2.md](./cloudflare-r2.md) |
| `R2_SECRET_ACCESS_KEY` | Cloudflare R2 | [cloudflare-r2.md](./cloudflare-r2.md) |
| `R2_BUCKET_NAME` | Cloudflare R2 | [cloudflare-r2.md](./cloudflare-r2.md) |
| `R2_PUBLIC_URL` | Cloudflare R2 (public CDN URL) | [cloudflare-r2.md](./cloudflare-r2.md) |
| `YOUTUBE_CLIENT_ID` | Google Cloud OAuth 2.0 | [youtube.md](./youtube.md) |
| `YOUTUBE_CLIENT_SECRET` | Google Cloud OAuth 2.0 | [youtube.md](./youtube.md) |
| `YOUTUBE_REFRESH_TOKEN` | YouTube — long-lived token | [youtube.md](./youtube.md) |
| `TELEGRAM_BOT_TOKEN` | Telegram bot | [telegram.md](./telegram.md) |
| `TELEGRAM_CHAT_ID` | Telegram chat/group ID | [telegram.md](./telegram.md) |
| `RESEND_API_KEY` | Resend email | [resend.md](./resend.md) |
| `RESEND_FROM_EMAIL` | Verified sender address | [resend.md](./resend.md) |
| `CONTACT_NOTIFICATION_EMAIL` | Where to receive alerts | [resend.md](./resend.md) |
| `GH_TOKEN` | GitHub PAT (repo + actions:read + workflow) | [github.md](./github.md) |
| `GH_REPO` | `username/repo-name` | [github.md](./github.md) |
| `GH_WORKFLOW_FILE` | e.g. `publish.yml` | [github.md](./github.md) |
| `APP_URL` | Vercel deployment URL | [bootstrap.md](./bootstrap.md) |
| `BACKGROUND_MUSIC_URL` | Direct MP3 URL (optional) | [bootstrap.md](./bootstrap.md) |

---

## Quick-start order

1. [neondb.md](./neondb.md) — create database first
2. [bootstrap.md](./bootstrap.md) — generate secrets, deploy to Vercel, add 2 GitHub secrets
3. [anthropic.md](./anthropic.md) — Claude script generation
4. [elevenlabs.md](./elevenlabs.md) — ElevenLabs voiceover
5. [fal.md](./fal.md) — Kling 2.6 Pro video clips
6. [cloudflare-r2.md](./cloudflare-r2.md) — video storage + Storage dashboard page
7. [youtube.md](./youtube.md) — OAuth setup + refresh token (**requires both upload + readonly scopes**)
8. [telegram.md](./telegram.md) — pipeline notifications
9. [resend.md](./resend.md) — email notifications
10. [github.md](./github.md) — trigger pipeline from dashboard

---

## YouTube scope note

The refresh token must be generated with **both** OAuth scopes:
- `https://www.googleapis.com/auth/youtube.upload` — to publish videos
- `https://www.googleapis.com/auth/youtube.readonly` — to sync engagement stats (views, likes, comments)

Run `python scripts/get_youtube_token.py` — it requests both scopes automatically. If you have an old token with only `upload` scope, revoke it at [myaccount.google.com/permissions](https://myaccount.google.com/permissions) and re-run the script.

---

## R2 Storage dashboard

The **Dashboard → Storage** page connects directly to your R2 bucket and lets you:
- Browse all files with folder navigation
- Preview videos inline (HTML5 player) and images
- Delete orphaned files (videos not referenced by any DB record are flagged)
- Upload files via drag-and-drop (for manual additions)

It uses the same `R2_*` credentials stored in NeonDB. Configure them at `/dashboard/secrets` → Cloudflare R2.
