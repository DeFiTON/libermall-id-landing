# Changelog

All notable changes to this repository are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] — 2026-05-25

### Added
- Full English landing site (25 pages) — first public release under the LiberMall org.
- README with Google/OpenAI-grade structure: badges, quickstart, comparison table, architecture diagram, roadmap.
- `LICENSE` (MIT), `CONTRIBUTING.md`, `SECURITY.md`, `BRANDBOOK.md`.
- `docs/architecture.md` + `docs/integration.md` — extended developer documentation.
- Ecosystem cross-links to `dex.libermall.com` (Libermall DEX on TON) and `pay.libermall.com` (PayLibermall) on every relevant page.
- `scripts/i18n_ru_to_en.py` — repeatable RU → EN translation tool used during the rebrand.

### Changed
- Repository moved from `DeFiTON/libermall-id-landing` to `LiberMall/libermall-id-landing` (org transfer).
- Default content language: `ru` → `en`. `og:locale` `ru_RU` → `en_US`. JSON-LD `inLanguage` `ru-RU` → `en-US`.
- All footer links, sitemap entries, and meta tags point to the new repo URL.

### Fixed
- 7 HTML pages were linking to the private `DeFiTON/libermall-id` repo from the footer; now point to the public `LiberMall/libermall-id-landing`.

## [0.3.0] — 2026-05-24

### Added
- 25 marketing pages live at [`id.libermall.com`](https://id.libermall.com).
- Real Libermall M-shield logo (yellow `#FFD60A` with SVG glow filter).
- Branded Casdoor `/login` and `/signup` via `signinHtml` / `signupHtml` overrides.
- Telegram Mini App at `id.libermall.com/app/`.
- `@LibermallIDbot` (id `8986664495`) with `/start`, `/apps`, `/profile`, `/help`.
- Custom auth flow: `/login`, 3-step `/signup`, `/dashboard`, mobile 6-digit confirm.
- SEO sweep: OG / Twitter Card on every page, JSON-LD `WebPage` + `BreadcrumbList`, `robots.txt`, `sitemap.xml`, branded `/404`.

## [0.2.0] — 2026-05-24

### Added
- First OAuth client wired up: [`sites.reviews`](https://sites.reviews) "Sign in / Sign up with Libermall ID" buttons.
- OAuth applications pre-configured for `tonchat.ai`, `ton.ceo`, `dex.libermall.com`, `pay.libermall.com`, `card.libermall.com`, `libermall.com`.
- JWT signing certificate `cert-libermall-id` (RS256, 4096-bit).
- Telegram OAuth provider registered with `@LibermallIDbot`.

## [0.1.0] — 2026-05-24

### Added
- Casdoor self-hosted on dedicated Fornex VPS `89.127.218.87`.
- Docker Compose: Casdoor + PostgreSQL 16 + Redis 7.
- Let's Encrypt SSL for `id.libermall.com`.
- Nginx reverse proxy.
