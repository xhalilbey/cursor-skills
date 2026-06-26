---
name: nextjs-app-router
description: Build, modify, review, or debug production Next.js applications, especially App Router projects using Server Components, Client Components, Server Actions, route handlers, middleware, caching/revalidation, metadata, auth, Supabase, Stripe, webhooks, deployment, or performance work. Use when the user asks about Next.js, React Server Components, Vercel, app directory routing, hydration issues, API routes, SSR/SSG, or full-stack web app implementation.
---

# Next.js App Router

## Operating Rules

Inspect the project first. Read `package.json`, `next.config.*`, `tsconfig.json`, `middleware.*`, `app/`, `src/app/`, `components/`, `lib/`, and any existing design system before proposing changes.

Prefer the app's existing architecture. Do not introduce a new state library, auth system, folder convention, or styling framework unless the request requires it.

Default to Server Components. Add `"use client"` only for browser state, effects, event handlers, refs, client-only libraries, or interactive UI. Keep client component boundaries as small as practical.

Use official Next.js documentation for version-sensitive behavior such as caching, Server Actions, metadata, middleware, route handlers, image optimization, and deployment differences.

## Implementation Checklist

- Preserve route ownership in `app/**/page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, and `not-found.tsx`.
- Keep data fetching close to the route or server component that owns it.
- Use route handlers for public HTTP/API surfaces and Server Actions for form-like mutations when the project already uses them.
- Validate all server inputs with an existing schema library when present.
- Never expose server secrets through `NEXT_PUBLIC_*`, client components, serialized props, logs, or error messages.
- Use `cache`, `revalidatePath`, `revalidateTag`, `unstable_noStore`/dynamic rendering choices deliberately; explain cache invalidation when changing data freshness.
- Keep loading, empty, error, and pending states feature-complete.
- Use `next/image`, `next/font`, and metadata APIs when they fit the existing stack.
- Avoid hydration mismatch by keeping time, randomness, browser-only APIs, and user-specific values out of static server markup unless guarded.

## Supabase In Next.js

If the app uses Supabase, prefer the local established client factory. Keep service-role keys server-only. For SSR/auth, verify cookies/session handling with official Supabase docs and the local middleware pattern.

When touching RLS-sensitive features, use the `supabase` and `web-security-review` skills as well.

## Verification

Run the repo's existing checks first:

```bash
npm run lint
npm run typecheck
npm run build
npm test
```

Use the package manager already present from lockfiles. For UI work, run the dev server and verify desktop and mobile widths. For production-sensitive behavior, verify `next build`, not only `next dev`.
