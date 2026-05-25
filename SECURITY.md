# Security Policy

## Reporting a vulnerability

If you discover a security issue in Libermall ID **do not open a public GitHub issue**. Instead, contact us through one of these private channels:

| Channel | Use it for |
|---|---|
| **Email**: [`security@libermall.com`](mailto:security@libermall.com) | Most reports. PGP key on request. |
| **Telegram**: [`@LibermallIDbot`](https://t.me/LibermallIDbot) → `/security` | Quick disclosure with screenshots |
| **GitHub Security Advisory** | Private coordinated disclosure via the *Security* tab |

We'll acknowledge your report within **48 hours**, give you a triage update within **5 business days**, and aim to ship a fix within **30 days** for high-severity issues.

## Scope

The following are in-scope for Libermall ID specifically:

- The Casdoor instance at [`id.libermall.com`](https://id.libermall.com)
- The Telegram Login provider integration
- The TON Connect bridge
- This landing site (`libermall-id-landing`)
- The bot at [`@LibermallIDbot`](https://t.me/LibermallIDbot)
- The Telegram Mini App at `id.libermall.com/app/`

Out of scope:

- Vulnerabilities in upstream [Casdoor](https://github.com/casdoor/casdoor) — report directly to that project
- Phishing or social-engineering attacks against operators
- DDoS / volumetric attacks
- Theoretical CVEs without a working proof-of-concept

## Safe-harbor

We won't pursue legal action against researchers who:

1. Make a good-faith effort to avoid privacy violations and service degradation.
2. Don't exfiltrate data beyond what's needed to prove the issue.
3. Give us reasonable time to remediate before public disclosure (typically 90 days).
4. Don't exploit the issue for personal gain.

## Hall of Fame

Researchers who report valid vulnerabilities will be credited (with consent) in [CHANGELOG.md](CHANGELOG.md) and on the [security page](https://id.libermall.com/security.html).

## Supported versions

This repository ships a static site without versioning — every commit on `main` is the live version. Security fixes are applied to `main` immediately.

For the upstream Casdoor instance, we follow Casdoor's own supported-versions matrix.
