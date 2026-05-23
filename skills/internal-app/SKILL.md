---
name: cloudflare-internal-app
description: Use when creating or advising on quick internal apps with Cloudflare Workers, D1, Wrangler, Bun, custom domains, cron triggers, Worker secrets, or lightweight server-rendered dashboards like x-rank.
---

# Cloudflare Internal App Stack

Use this skill when the user wants a small internal app that needs simple hosting, a database, scheduled jobs, custom domains, secrets, or admin endpoints without running a server or Kubernetes deployment.

## Default Stack

- Runtime: Cloudflare Workers
- Language: TypeScript
- Tooling: Bun plus Wrangler
- Database: Cloudflare D1 for relational state
- Scheduler: Worker cron triggers
- Secrets: Cloudflare Worker secrets
- Hosting: Cloudflare custom domain route
- UI: server-rendered HTML from the Worker unless a client app is clearly needed
- Auth: Cloudflare Access for human SSO, bearer secrets for machine/admin endpoints
  Prefer this stack for quick internal dashboards, small admin tools, reporting pages, webhook receivers, scheduled sync jobs, and apps with modest relational data needs.
  Do not default to this stack for long-running processes, WebSocket-heavy apps, large file storage, background jobs longer than Worker limits, complex React apps, or services that need private VPC access unless the user explicitly accepts those constraints.

## Project Shape

Recommended minimal layout:

```txt
my-app/
  package.json
  tsconfig.json
  wrangler.toml
  worker/
    index.ts
  migrations/
    0001_initial.sql
  README.md
```

Use this `package.json` script shape:

```json
{
  "type": "module",
  "scripts": {
    "dev": "wrangler dev --local",
    "deploy": "wrangler deploy",
    "db:create": "wrangler d1 create my-app",
    "db:migrate": "wrangler d1 migrations apply my-app --local && wrangler d1 migrations apply my-app --remote",
    "typecheck": "tsc -p tsconfig.json --noEmit"
  },
  "devDependencies": {
    "@cloudflare/workers-types": "latest",
    "typescript": "latest",
    "wrangler": "latest"
  }
}
```

Use Bun commands: `bun install`, `bun run typecheck`, `bun run deploy`, and `bunx wrangler ...`.

## Wrangler Config

Use this as the baseline:

```toml
name = "my-app"
main = "worker/index.ts"
compatibility_date = "2026-05-17"
workers_dev = false
routes = [
  { pattern = "my-app.example.com", custom_domain = true }
]
[[d1_databases]]
binding = "DB"
database_name = "my-app"
database_id = "replace-after-db-create"
migrations_dir = "migrations"
[triggers]
crons = ["0 * * * *"]
```

Set `workers_dev = false` for internal apps unless the user explicitly wants a public `workers.dev` endpoint.

## Worker Design

Keep the Worker simple:

- Route with `new URL(request.url).pathname` until a router is justified.
- Return `GET /health` with JSON.
- Render simple HTML on `GET /`.
- Put admin actions under `/admin/...`.
- Protect admin actions with a Worker secret or Cloudflare Access.
- Use `ctx.waitUntil(...)` for work that can continue after the response.
- Use `scheduled(...)` for cron-driven jobs.
  Admin bearer auth pattern:

```ts
const auth = request.headers.get("authorization");
if (auth !== `Bearer ${env.ADMIN_SECRET}`) {
  return new Response("Unauthorized", { status: 401 });
}
```

## Setup Workflow

For a new app:

1. Create files and install dependencies with Bun.
2. Create the D1 database with `bun run db:create`.
3. Copy the returned `database_id` into `wrangler.toml`.
4. Add SQL migrations under `migrations/`.
5. Apply migrations with `bun run db:migrate`.
6. Set secrets with `bunx wrangler secret put NAME`.
7. Typecheck with `bun run typecheck`.
8. Deploy with `bun run deploy`.
9. Verify `GET /health` and the custom domain.

## GitHub Actions Deploy

Use GitHub Actions when the app should deploy on push:

```yaml
name: My App
on:
  push:
    branches:
      - main
    paths:
      - my-app/**
      - .github/workflows/my-app.yml
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: my-app-${{ github.ref }}
  cancel-in-progress: true
jobs:
  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: my-app
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Bun
        uses: oven-sh/setup-bun@v2
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 24
      - name: Install dependencies
        run: bun install --frozen-lockfile
      - name: Typecheck
        run: bun run typecheck
      - name: Deploy with Wrangler
        run: bun run deploy
        env:
          CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
```

Required GitHub secrets:

- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_API_TOKEN`
  Worker runtime secrets still belong in Cloudflare via `wrangler secret put`, not in the repo.

## Auth Guidance

For internal human access, prefer Cloudflare Access in front of the custom domain. The Worker does not need to implement OAuth or SSO if Cloudflare Access handles identity at the edge.
For admin endpoints and scheduled/manual actions, use a separate Worker secret such as `ADMIN_SECRET` or `REFRESH_SECRET` and require a bearer token.
For public read-only dashboards, public `GET /` is acceptable if the data is intended to be visible.

## Decision Checklist

Before building, clarify only what materially changes the stack:

- Does the app need human SSO? If yes, use Cloudflare Access.
- Does it need relational persistence? If yes, use D1.
- Does it need scheduled refresh/sync? If yes, use Worker cron.
- Does it need external API credentials? If yes, use Worker secrets.
- Does it need complex interactivity? If no, server-render HTML. If yes, consider Pages plus a client app.
- Does it need long-running jobs or private network access? If yes, consider another platform.

## Common Commands

```sh
bun install
bun run dev
bun run db:create
bun run db:migrate
bunx wrangler secret put ADMIN_SECRET
bun run typecheck
bun run deploy
```

Manual admin request example:

```sh
curl -X POST https://my-app.example.com/admin/refresh \
  -H "Authorization: Bearer $ADMIN_SECRET"
```

## Quality Bar

- Keep the first version small and direct.
- Avoid frameworks until there is a clear reason.
- Avoid app-level OAuth unless Cloudflare Access cannot satisfy the requirement.
- Include a `README.md` with setup, secrets, deploy, and manual admin commands.
- Include `GET /health` for verification.
- Run `bun run typecheck` before considering the app ready.
