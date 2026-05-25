# Contributing to Libermall ID

Thanks for considering a contribution! This repository is the **public landing site + brand book** for [`id.libermall.com`](https://id.libermall.com). The auth server itself is the upstream [Casdoor](https://casdoor.org/) project — for changes to authentication logic, file issues there.

## Ways to help

- **Fix a typo or broken link** → open a PR directly.
- **Improve a code example** in `docs/` or on any page in `public/` → open a PR; we love clear, copy-paste-able snippets.
- **Translate** → if you want to add a non-English version (we currently ship English only), please open a discussion first so we can coordinate the i18n pipeline.
- **Report a UX issue** → open a GitHub issue with the URL of the affected page and a screenshot.
- **Propose a new section or page** → open an issue first; landing changes that affect the marketing narrative need a quick chat with the team.

## Reporting bugs

Please include:

1. URL of the page where the issue happens.
2. Browser + version (e.g. *Chrome 138 on macOS 15*).
3. Expected vs actual behavior.
4. Screenshot or short screen recording if visual.

For security issues, see [`SECURITY.md`](SECURITY.md). Do **not** open a public issue for vulnerabilities.

## Development setup

This is a static site — no build tools, no JavaScript bundlers, no `npm install`. Everything in `public/` is what ships to the CDN.

```bash
# Clone
git clone git@github.com:LiberMall/libermall-id-landing.git
cd libermall-id-landing

# Serve locally
cd public && python3 -m http.server 8080
# → open http://localhost:8080
```

That's it. Open any `.html` in your editor, refresh the browser. The CSS lives in `public/assets/style.css`.

### When changing copy

- Brand spelling: **Libermall** (capital L, the rest lowercase) — never "LiberMall", "LiberMole", "libermall".
- Identity copy style: Auth0 / Clerk / Stytch — short, confident, value-prop first. Avoid marketing fluff.
- Ecosystem URLs always link out: [`libermall.com`](https://libermall.com), [`dex.libermall.com`](https://dex.libermall.com), [`pay.libermall.com`](https://pay.libermall.com), [`card.libermall.com`](https://card.libermall.com), [`tonchat.ai`](https://tonchat.ai), [`ton.ceo`](https://ton.ceo), [`sites.reviews`](https://sites.reviews).

### When changing styling

All styles live in [`public/assets/style.css`](public/assets/style.css). The design tokens — colour, typography, spacing — are documented in [`BRANDBOOK.md`](BRANDBOOK.md). Reusing existing components is always preferred over adding new ones.

### SEO checklist for new pages

Every new `.html` in `public/` must include:

- [ ] `<title>` — unique, 50-60 chars
- [ ] `<meta name="description">` — unique, 140-160 chars
- [ ] `<link rel="canonical">`
- [ ] Open Graph tags (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`)
- [ ] Twitter Card tags
- [ ] JSON-LD `WebPage` + `BreadcrumbList`
- [ ] Entry added to [`public/sitemap.xml`](public/sitemap.xml) (unless `noindex`)
- [ ] If private — `<meta name="robots" content="noindex,nofollow">` + entry in `Disallow` of [`public/robots.txt`](public/robots.txt)
- [ ] `alt` text on every `<img>`

## Pull-request checklist

- [ ] Branch from `main`, name it `topic/short-description`
- [ ] One logical change per PR
- [ ] No mixed cosmetic + functional edits
- [ ] Test locally with `python3 -m http.server` before opening
- [ ] Update [`CHANGELOG.md`](CHANGELOG.md) under `## Unreleased`
- [ ] Reference the related issue in the PR body: `Closes #123`

We aim to respond within 48 hours.

## Code of Conduct

This project follows the [Contributor Covenant v2.1](CODE_OF_CONDUCT.md). Be kind, be specific, ship great work.

## License

By contributing you agree your code is licensed under [MIT](LICENSE).
