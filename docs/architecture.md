# Architecture

How Libermall ID is put together, and why.

## High-level flow

```
┌──────────────────────────────────────────────────────────────────────┐
│                      Your application                                 │
│             (Laravel / Next.js / Node / Python / curl)                │
└─────────────────────────────┬────────────────────────────────────────┘
                              │  OAuth 2.0 / OpenID Connect
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       id.libermall.com                                │
│ ┌──────────────────────────────────────────────────────────────────┐ │
│ │            nginx (TLS termination, static + reverse proxy)        │ │
│ └──┬───────────────────────────────────────────────────────────────┘ │
│    │ / · /products · /docs ...  → static (this repo)                  │
│    │ /login · /signup · /api/*  → Casdoor 127.0.0.1:8000              │
│    │ /webhook/<secret>           → @LibermallIDbot 127.0.0.1:3010    │
│    │ /app/                       → Mini App static                     │
└────┘                                                                  │
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                Casdoor (Go) — Auth core                               │
└──┬──────────────────┬──────────────────────┬─────────────────────────┘
   ▼                  ▼                      ▼
┌────────┐      ┌──────────┐         ┌─────────────────────────────┐
│ Postgres│      │  Redis   │         │     Identity Providers      │
│   16    │      │    7     │         │                              │
└────────┘      └──────────┘         │ ▪ Telegram (HMAC-SHA256)    │
                                      │ ▪ TON Connect (Ed25519)*    │
                                      │ ▪ Email magic link          │
                                      │ ▪ Apple (Sign in with Apple)│
                                      │ ▪ Google (OAuth 2.0)        │
                                      │ ▪ SAML SP / IdP             │
                                      └─────────────────────────────┘

* TON Connect = custom Go/Node bridge — see "Custom providers" below.
```

## Components

| Component | Tech | Port | Repo |
|---|---|---|---|
| Landing site (this) | static HTML + CSS | n/a | `LiberMall/libermall-id-landing` |
| Auth server | Casdoor (Go) | 127.0.0.1:8000 | upstream [casdoor/casdoor](https://github.com/casdoor/casdoor) |
| Database | PostgreSQL 16 | 127.0.0.1:5432 (Docker net) | — |
| Cache + sessions | Redis 7 | 127.0.0.1:6379 (Docker net) | — |
| Telegram bot | Node.js + Telegraf | 127.0.0.1:3010 | `LiberMall/libermall-id-bot` |
| Mini App | static HTML + WebApp SDK | n/a | `LiberMall/libermall-id-miniapp` |

All non-statics are bound to `127.0.0.1` and only reachable through nginx. UFW + fail2ban additionally lock down the host.

## Why Casdoor

We evaluated Auth0 (managed, $$$), Keycloak (Java + heavy), Authentik (great but Python ecosystem), Ory Kratos+Hydra (excellent but multi-binary). Casdoor won because:

1. **Single ~50 MB Go binary** — minimal RAM footprint on a 1 GB VPS.
2. **OIDC + OAuth 2.0 + SAML + LDAP out of the box** — no protocol glue to write.
3. **UI customizable via `signinHtml` / `signupHtml`** without forking.
4. **Open source (Apache 2.0)** — no vendor lock-in, can self-host forever.
5. **Built-in providers** for Google, Apple, GitHub, Twitter — drop in API keys.

## JWT lifecycle

- **Algorithm**: RS256 (RSA 4096-bit)
- **Issuer**: `https://id.libermall.com`
- **Audience**: per-client `client_id`
- **Lifetime**: access token 1 hour, refresh token 30 days, id_token 1 hour
- **JWKS**: published at `/.well-known/jwks`
- **Rotation**: every 90 days; previous key kept in JWKS for 7 days for graceful overlap

## User provisioning

When a new user signs in via any provider:

1. Casdoor looks up the external identifier (Telegram `user_id`, TON wallet address, email, Apple `sub`, Google `sub`).
2. If unknown, creates a new internal UUID — that's the `sub` claim, never changes.
3. Calls the configured webhook (we sync to our admin DB and `@LibermallIDbot`).
4. Issues a session cookie for the Casdoor domain.

Linking additional methods to an existing account is allowed from the dashboard at [`/dashboard.html`](../public/dashboard.html).

## Multi-tenant (per-client) config

Each application is configured as a separate `Application` in Casdoor:

```
Organization: libermall
├── Application: sites-reviews     → sites.reviews
├── Application: tonchat           → tonchat.ai
├── Application: ton-ceo           → ton.ceo
├── Application: dex               → dex.libermall.com
├── Application: paylibermall      → pay.libermall.com
├── Application: card              → card.libermall.com
└── Application: marketplace       → libermall.com
```

Each app gets its own `client_id`, `client_secret`, redirect URIs, and consent screen.

## Custom providers

Telegram Login is a built-in Casdoor provider. **TON Connect** is not — we wrote a small Go bridge that:

1. Generates a connection link with TON Connect.
2. Receives the signed proof (Ed25519 over `tonProof.payload`).
3. Verifies signature + timestamp + domain.
4. Calls Casdoor's admin API to mint a session for the wallet address.

The bridge code is in `LiberMall/libermall-id` (private — contains operational secrets); a reference implementation is on the roadmap for `@libermall/ton-connect-bridge` on npm.

## Hosting

| Resource | Spec |
|---|---|
| VPS | Fornex Frankfurt (`89.127.218.87`) |
| OS | Ubuntu 24.04 LTS |
| RAM | 1 GB + 2 GB swap |
| Disk | 10 GB SSD |
| TLS | Let's Encrypt (auto-renew) |
| Firewall | UFW (22, 80, 443 only) + fail2ban |
| Backups | Daily encrypted pg_dump → off-host |

The site is fully behind the standard rsync deploy described in [`README.md`](../README.md#deploying).
