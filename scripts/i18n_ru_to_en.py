#!/usr/bin/env python3
"""
Full RU → EN translation pass for all HTML pages.
Also rewrites repo path DeFiTON/libermall-id-landing → LiberMall/libermall-id-landing.

Replacements are anchored to safe boundaries:
- `>TEXT<`        — full inner text of a tag
- `"TEXT"`        — full attribute value
- `>TEXT </`      — text followed by close tag
- ` TEXT.` / `! ` — sentence punctuation
- exact start-of-line / end-of-line phrases

Multi-line phrases use re.DOTALL only inside known wrappers.

Run from repo root:
    python3 scripts/i18n_ru_to_en.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

# ────────────────────────────────────────────────────────────────────────────
# Plain, safe whole-phrase replacements. Each contains enough context
# (tags, quotes, punctuation) to avoid colliding with shorter words.
# ────────────────────────────────────────────────────────────────────────────
REPLACEMENTS: list[tuple[str, str]] = [
    # ── repo path ──
    ("DeFiTON/libermall-id-landing", "LiberMall/libermall-id-landing"),
    ("DeFiTON/libermall-id-bot",     "LiberMall/libermall-id-bot"),
    ("DeFiTON/libermall-id-miniapp", "LiberMall/libermall-id-miniapp"),
    ("github.com/DeFiTON/libermall-id", "github.com/LiberMall/libermall-id"),
    ("github.com/DeFiTON",            "github.com/LiberMall"),
    ("DeFiTON/libermall-id",         "LiberMall/libermall-id"),

    # ── document language ──
    ('<html lang="ru">', '<html lang="en">'),
    ('content="ru_RU"', 'content="en_US"'),
    ('"inLanguage": "ru-RU"', '"inLanguage": "en-US"'),
    ('"priceCurrency": "RUB"', '"priceCurrency": "USD"'),

    # ── currencies ──
    ("RUB",     "USD"),
    ("$240/мес", "$240/mo"),
    ("$1,500+/мес", "$1,500+/mo"),
    ("$25/мес", "$25/mo"),
    ("$300+/мес", "$300+/mo"),
    ("$99/мес", "$99/mo"),
    ("/мес", "/mo"),

    # ── attribute values (always quoted) ──
    ('aria-label="Меню"',           'aria-label="Menu"'),
    ('aria-label="Открыть меню"',   'aria-label="Open menu"'),

    # ── nav tab labels (>TEXT<) ──
    (">Продукты<",        ">Products<"),
    (">Разработчикам<",   ">Developers<"),
    (">О проекте<",       ">About<"),
    (">Войти<",           ">Sign in<"),
    (">Войти</a>",        ">Sign in</a>"),
    (">Создать аккаунт<", ">Create account<"),
    (">Создать аккаунт</a>", ">Create account</a>"),
    (">Создать<",         ">Create<"),
    (">Меню<",            ">Menu<"),
    (">Документация<",    ">Documentation<"),
    (">Интегрировать<",   ">Integrate<"),
    (">Экосистема<",      ">Ecosystem<"),
    (">Контакт<",         ">Contact<"),
    (">Приватность<",     ">Privacy<"),
    (">Условия<",         ">Terms<"),
    (">Продукт<",         ">Product<"),
    (">Юридическое<",     ">Legal<"),
    (">Тарифы<",          ">Pricing<"),
    (">Сравнение<",       ">Compare<"),
    (">Сценарии использования<", ">Use cases<"),
    (">Кейсы<",           ">Customers<"),
    (">Клиенты<",         ">Customers<"),
    (">Безопасность<",    ">Security<"),
    (">Статус<",          ">Status<"),
    (">История изменений<", ">Changelog<"),
    (">Блог<",            ">Blog<"),
    (">Quickstart<",      ">Quickstart<"),
    (">API Playground<",  ">API Playground<"),

    # ── hero / index ──
    (">Один аккаунт<br>для всей <span class=\"accent\">экосистемы</span><",
     '>One account<br>for the entire <span class="accent">ecosystem</span><'),
    ("Libermall ID — единый Single Sign-On для Sites.Reviews, TonChat AI, TON.CEO, DEX, Card и Marketplace. Войдите один раз — пользуйтесь везде.",
     "Libermall ID is the single sign-on layer for Sites.Reviews, TonChat AI, TON.CEO, DEX, PayLibermall, Card and Marketplace. Sign in once, use everywhere."),
    (">Создать аккаунт →<", ">Create account →<"),
    (">У меня уже есть<",   ">I already have one<"),
    (">Бесплатно навсегда<", ">Free forever<"),
    (">Бесплатно<",          ">Free<"),
    (">Open source<",        ">Open source<"),
    (">Принимается во всей экосистеме Libermall<",
     ">Accepted across the entire Libermall ecosystem<"),
    (">Identity layer для экосистемы Libermall<",
     ">Identity layer for the Libermall ecosystem<"),

    # ── product cards ──
    (">Каталог отзывов<",  ">Reviews & ratings<"),
    (">AI-помощник<",      ">AI assistant<"),
    (">Mastodon-сеть<",    ">Mastodon network<"),
    (">Биржа на TON<",     ">TON DEX<"),
    (">Виртуальные карты<", ">Virtual cards<"),
    (">Маркетплейс<",      ">Marketplace<"),

    # ── feature bar ──
    (">Один логин для всех продуктов Libermall<",
     ">One login for every Libermall product<"),
    (">Industry-standard auth и защита данных<",
     ">Industry-standard auth and data protection<"),
    (">Активность, репутация и настройки в одном месте<",
     ">Activity, reputation and settings in one place<"),
    (">Без паролей, без подтверждения email<",
     ">No passwords, no email confirmations<"),

    # ── why-id cards ──
    (">Спроектирован для удобства и безопасности<",
     ">Designed for convenience and security<"),
    (">Каждая деталь — оптимизирована под seamless experience во всех продуктах экосистемы Libermall.<",
     ">Every detail is engineered for a seamless experience across every Libermall product.<"),
    (">Telegram, TON Connect, email или social. Без паролей и confirmation-писем.<",
     ">Telegram, TON Connect, email or social. No passwords, no confirmation emails.<"),
    (">OpenID Connect, OAuth 2.0, SAML, 2FA, шифрование и audit log из коробки.<",
     ">OpenID Connect, OAuth 2.0, SAML, 2FA, encryption and audit log out of the box.<"),
    (">Кошельки, отзывы, рейтинг трейдера, накопления на Card — единая история.<",
     ">Wallets, reviews, trader rating, Card balance — a single user history.<"),

    # ── ecosystem section ──
    (">Все связано. Все под одним аккаунтом.<",
     ">Everything connected. All under one account.<"),
    (">Все продукты экосистемы →<", ">All ecosystem products →<"),

    # ── auth methods ──
    (">5 способов войти. Один аккаунт.<",
     ">5 ways to sign in. One account.<"),
    (">Любой способ ведёт к одному и тому же профилю. Привяжите несколько — каждый станет резервным.<",
     ">Every method leads to the same profile. Link multiple — each becomes a backup.<"),
    (">Один тап в @LibermallIDbot. HMAC-подпись от Telegram.<",
     ">One tap in @LibermallIDbot. Signed with HMAC by Telegram.<"),
    (">Введите email, получите ссылку, кликните.<",
     ">Enter your email, get a link, click it.<"),
    (">~3 сек<", ">~3 sec<"),
    (">0 полей<", ">0 fields<"),
    (">15 мин<",  ">15 min<"),

    # ── steps ──
    (">Регистрация — меньше минуты<", ">Sign-up in under a minute<"),
    (">Выберите способ<",   ">Choose a method<"),
    (">Telegram, TON Connect, email или social<",
     ">Telegram, TON Connect, email or social<"),
    (">Подтвердите в провайдере<",
     ">Confirm with your provider<"),
    (">Один тап в Telegram или подпись в TON-кошельке<",
     ">One tap in Telegram or sign with your TON wallet<"),
    (">Готово<", ">Done<"),
    (">Аккаунт активен во всей экосистеме Libermall<",
     ">Your account is active across the entire Libermall ecosystem<"),

    # ── mobile section ──
    (">Удобно с любого устройства<",
     ">Comfortable on any device<"),
    (">Адаптивный веб + Telegram Mini App. Один профиль — везде.<",
     ">Responsive web + Telegram Mini App. One profile — everywhere.<"),
    (">Откройте Mini App прямо в Telegram — не нужно скачивать приложение. Привязка кошельков, управление сессиями, переход в любой продукт экосистемы — без выхода из мессенджера.<",
     ">Open the Mini App right inside Telegram — no install needed. Link wallets, manage sessions, jump into any ecosystem product without leaving the messenger.<"),
    (">Открыть @LibermallIDbot<", ">Open @LibermallIDbot<"),
    (">Один аккаунт для всей экосистемы<", ">One account for the entire ecosystem<"),
    (">Войдите в любой сервис Libermall<",  ">Sign in to any Libermall service<"),
    (">Войдите, чтобы продолжить во всех сервисах экосистемы.<",
     ">Sign in to continue across the ecosystem.<"),

    # ── standards ──
    (">Построено на доверенных стандартах<",
     ">Built on trusted standards<"),
    (">Modern authentication протоколы для secure и interoperable будущего. Никакого vendor lock-in — стандартный OpenID Connect работает с любым языком и фреймворком.<",
     ">Modern authentication protocols for a secure, interoperable future. Zero vendor lock-in — standard OpenID Connect works with any language or framework.<"),

    # ── developers section ──
    (">Подключите свой сервис<br>за 5 минут<",
     ">Connect your service<br>in 5 minutes<"),
    (">Стандартный OpenID Connect + готовые SDK. Нулевой vendor lock-in.<",
     ">Standard OpenID Connect + ready-made SDKs. Zero vendor lock-in.<"),
    (">SAML 2.0 для enterprise<", ">SAML 2.0 for enterprise<"),
    (">JWT RS256, 4096-bit ключ<", ">JWT RS256, 4096-bit key<"),
    (">SDK: Laravel, Next.js, Node, Python<", ">SDKs: Laravel, Next.js, Node, Python<"),
    (">Документация<", ">Documentation<"),

    # ── code comment ──
    ("<span class=\"c-com\">// Авторизуйте пользователя за 5 строк</span>",
     "<span class=\"c-com\">// Authenticate a user in 5 lines</span>"),

    # ── security ──
    (">Безопасность на уровне инфраструктуры<",
     ">Infrastructure-grade security<"),
    (">Industry-standard стек защиты. Без компромиссов на скорости разработки.<",
     ">Industry-standard defence stack. No compromise on development speed.<"),
    (">Industry-standard стек защиты, прозрачно описанный и публично проверяемый.<",
     ">Industry-standard defence stack — transparently documented and publicly verifiable.<"),
    (">4096-bit подпись, JWKS rotation<", ">4096-bit signing, JWKS rotation<"),
    (">Casdoor core + наш UI на GitHub<", ">Casdoor core + our UI on GitHub<"),
    (">Изолированный VPS, ваш контроль<", ">Isolated VPS, your control<"),
    (">Revoke devices, активные сессии<", ">Revoke devices, active sessions<"),

    # ── pricing ──
    (">Бесплатно для пользователей. Понятно для разработчиков.<",
     ">Free for users. Transparent for developers.<"),
    (">Никаких скрытых платежей. Зарегистрируйтесь и используйте — мы зарабатываем на enterprise-интеграциях.<",
     ">No hidden fees. Sign up and use it — we make money on enterprise integrations.<"),
    (">Личный аккаунт<", ">Personal account<"),
    ("Бесплатно <small>навсегда</small>", "Free <small>forever</small>"),
    ("$0 <small>навсегда</small>",         "$0 <small>forever</small>"),
    ("Free <small>до 10K MAU</small>",    "Free <small>up to 10K MAU</small>"),
    (">Для пользователей всех продуктов Libermall.<",
     ">For users of every Libermall product.<"),
    (">Для пользователей и indie-проектов.<",
     ">For end-users and indie projects.<"),
    (">Все способы входа<", ">All sign-in methods<"),
    (">Все 5 способов входа<", ">All 5 sign-in methods<"),
    (">Привязка кошельков, email<", ">Link wallets and email<"),
    (">2FA, audit log, sessions<", ">2FA, audit log, sessions<"),
    (">Mini App + бот<", ">Mini App + bot<"),
    (">До 10 redirect URIs<", ">Up to 10 redirect URIs<"),
    (">10K MAU бесплатно<", ">10K MAU free<"),
    (">Запросить ключ<", ">Request a key<"),
    (">Whitelabel, SAML, SLA, dedicated support.<",
     ">Whitelabel, SAML, SLA, dedicated support.<"),
    (">Безлимитный MAU<", ">Unlimited MAU<"),
    (">Связаться<", ">Contact us<"),
    (">Recommended<", ">Recommended<"),
    (">Подключите свой сервис как OAuth-клиент.<",
     ">Connect your service as an OAuth client.<"),

    # ── FAQ ──
    (">Частые вопросы<", ">Frequently asked questions<"),
    (">Сколько стоит Libermall ID?<", ">How much does Libermall ID cost?<"),
    (">Где хранятся мои данные?<", ">Where is my data stored?<"),
    (">Что если я потеряю доступ к Telegram?<", ">What if I lose access to Telegram?<"),
    (">Можно ли использовать без Telegram?<", ">Can I use it without Telegram?<"),
    (">Что такое cross-product profile?<", ">What is a cross-product profile?<"),
    (">Это open source?<", ">Is it open source?<"),

    # ── FAQ answers ──
    (">Бесплатно навсегда для пользователей. Для разработчиков — бесплатный tier OIDC до 10K MAU, дальше — по согласованию. Enterprise (SAML, SCIM, SLA) — custom pricing.<",
     ">Free forever for users. For developers — a free OIDC tier up to 10K MAU; beyond that — by arrangement. Enterprise (SAML, SCIM, SLA) — custom pricing.<"),
    (">На изолированном VPS в Frankfurt. Профиль и сессии — PostgreSQL, кэш — Redis. Резервные копии шифруются. Ваш TG-id, email и привязанные кошельки видим только мы — третьим сторонам не передаём (кроме как через ваш явный OAuth consent).<",
     ">On an isolated VPS in Frankfurt. Profiles and sessions in PostgreSQL, cache in Redis. Backups are encrypted. Your Telegram id, email and linked wallets are visible only to us — never shared with third parties without your explicit OAuth consent.<"),
    (">Привяжите второй способ входа (TON Connect или email) — это резерв. Также можно настроить 2FA recovery codes. Восстановление через support — только если есть подтверждение владения аккаунтом.<",
     ">Link a second sign-in method (TON Connect or email) as a backup. You can also set up 2FA recovery codes. Support-based recovery is available only with verified proof of ownership.<"),
    (">Да. Доступны TON Connect (Tonkeeper/MyTonWallet), email magic-link, Apple ID и Google. Telegram — самый быстрый способ, но не единственный.<",
     ">Yes. TON Connect (Tonkeeper / MyTonWallet), email magic link, Apple ID and Google are available. Telegram is the fastest, but not the only option.<"),
    (">Ваш профиль (имя, аватар, привязанные кошельки) виден во всех продуктах экосистемы. Накопления на Card, рейтинг трейдера на DEX, отзывы на Sites.Reviews — всё под одним аккаунтом.<",
     ">Your profile (name, avatar, linked wallets) is visible across the whole ecosystem. Card balance, DEX trader rating, Sites.Reviews reviewer rep — all under one account.<"),
    (">Auth core — Casdoor (BSD 3-Clause). Наш UI и бот — MIT на github.com/DeFiTON. Кастомные адаптеры для TG и TON — тоже public.<",
     ">Auth core is Casdoor (BSD 3-Clause). Our UI and bot are MIT-licensed on github.com/LiberMall. Custom TG and TON adapters are public too.<"),

    # ── final CTA ──
    (">Готовы войти в экосистему?<", ">Ready to enter the ecosystem?<"),
    (">Один аккаунт открывает доступ ко всему. Без паролей, без подписок, без скрытых платежей.<",
     ">One account unlocks everything. No passwords, no subscriptions, no hidden fees.<"),
    (">Документация для разработчиков<", ">Developer documentation<"),

    # ── footer ──
    (">Identity layer для экосистемы Libermall.<", ">Identity layer for the Libermall ecosystem.<"),
    ("© 2026 Libermall. Все права защищены.", "© 2026 Libermall. All rights reserved."),

    # ── products.html specifics ──
    (">Продукты экосистемы Libermall<",
     ">Products of the Libermall ecosystem<"),
    (">Каталог всех сервисов, которые работают через Libermall ID.<",
     ">Catalog of every service that uses Libermall ID for authentication.<"),

    # ── developers.html titles ──
    ("<title>Разработчикам — Libermall ID</title>",
     "<title>Developers — Libermall ID</title>"),
    ('<meta property="og:title" content="Libermall ID для разработчиков">',
     '<meta property="og:title" content="Libermall ID for developers">'),
    ('<meta name="twitter:title" content="Разработчикам — Libermall ID">',
     '<meta name="twitter:title" content="Developers — Libermall ID">'),
    ('"name": "Разработчикам",', '"name": "Developers",'),
    ('"name": "Разработчикам", "item":', '"name": "Developers", "item":'),

    # ── about.html titles ──
    (">Единая идентификация<br>для <span class=\"accent\">Web3-экосистемы</span><",
     '>Unified identity<br>for the <span class="accent">Web3 ecosystem</span><'),
    (">Зачем мы это делаем<", ">Why we do this<"),

    # ── login titles ──
    ("<title>Войти — Libermall ID</title>",
     "<title>Sign in — Libermall ID</title>"),
    ('<meta property="og:title" content="Войти — Libermall ID">',
     '<meta property="og:title" content="Sign in — Libermall ID">'),
    ('<meta name="twitter:title" content="Войти — Libermall ID">',
     '<meta name="twitter:title" content="Sign in — Libermall ID">'),
    ('"name": "Войти",', '"name": "Sign in",'),
    ('"name": "Войти", "item":', '"name": "Sign in", "item":'),

    # ── dashboard titles ──
    ("<title>Профиль — Libermall ID</title>", "<title>Profile — Libermall ID</title>"),
    ('<meta property="og:title" content="Профиль — Libermall ID">',
     '<meta property="og:title" content="Profile — Libermall ID">'),
    ('<meta name="twitter:title" content="Профиль — Libermall ID">',
     '<meta name="twitter:title" content="Profile — Libermall ID">'),

    # ── confirm.html ──
    ("<title>Подтверждение входа — Libermall ID</title>",
     "<title>Confirm sign-in — Libermall ID</title>"),
    ('<meta property="og:title" content="Подтверждение входа — Libermall ID">',
     '<meta property="og:title" content="Confirm sign-in — Libermall ID">'),
    ('<meta name="twitter:title" content="Подтверждение входа — Libermall ID">',
     '<meta name="twitter:title" content="Confirm sign-in — Libermall ID">'),
    ("Libermall ID — единая идентификация для всей экосистемы Libermall.",
     "Libermall ID — unified identity for the entire Libermall ecosystem."),
    (">Подтвердите вход<", ">Confirm sign-in<"),
    ("Мы отправили 6-значный код в",
     "We sent a 6-digit code to"),
    ("Откройте бот и подтвердите запрос.",
     "Open the bot and confirm the request."),
    ("Код действителен", "Code valid for"),
    (">Подтвердить<", ">Confirm<"),
    (">Это не я · отменить<", ">Not me · cancel<"),
    ("Никогда не сообщайте этот код посторонним. Libermall ID не запрашивает код в чатах или по почте.",
     "Never share this code with anyone. Libermall ID never asks for the code in chats or by email."),
    ("Код истёк.", "Code expired."),
    ("Запросить новый", "Request a new one"),

    # ── 404 page ──
    ("<title>404 — страница не найдена · Libermall ID</title>",
     "<title>404 — page not found · Libermall ID</title>"),
    ('content="Page not found. Вернитесь на главную Libermall ID."',
     'content="Page not found. Go back to the Libermall ID home page."'),
    (">Возможно вы перешли по устаревшей ссылке. Откройте главную или ",
     ">You may have followed a stale link. Go to the home page or "),
    (">На главную<", ">Back to home<"),
    (">Связаться с поддержкой<", ">Contact support<"),
    (">свяжитесь с нами<", ">contact us<"),

    # ── about.html long text ──
    ("Libermall ID решает фрагментацию аккаунтов между продуктами экосистемы.",
     "Libermall ID solves account fragmentation across the ecosystem."),

    # ── pricing ──
    (">Free для всех пользователей навсегда. Платим только за enterprise-фичи.<",
     ">Free forever for every user. You only pay for enterprise features.<"),

    # ── compare page ──
    (">Libermall ID vs другие identity-сервисы<",
     ">Libermall ID vs other identity services<"),
    (">Открытое сравнение фичей и цен. Без маркетинговой шелухи.<",
     ">An honest comparison of features and pricing. No marketing fluff.<"),
    (">Цена за 10K MAU<", ">Price for 10K MAU<"),
    (">Цена за 100K MAU<", ">Price for 100K MAU<"),
    (">✓ 6+ продуктов<", ">✓ 6+ products<"),

    # ── customers page ──
    (">Истории интеграций<", ">Integration stories<"),
    (">Как продукты экосистемы Libermall и partners используют единый identity.<",
     ">How Libermall ecosystem products and partners run on a unified identity layer.<"),
    (">Users / 1 мес<", ">Users / month<"),

    # ── status page ──
    (">Все системы работают штатно<", ">All systems operational<"),
    (">Реальное состояние всех endpoint'ов и сервисов Libermall ID.<",
     ">Live state of all Libermall ID endpoints and services.<"),
    (">за последние 90 дней<", ">over the last 90 days<"),
    (">небольшая деградация · 12:30 UTC<", ">minor degradation · 12:30 UTC<"),
    (">7 дней без инцидентов<", ">7 days without incidents<"),
    ("Подпишитесь на updates в",
     "Subscribe to updates via"),

    # ── blog ──
    (">Identity для Web3-эпохи<", ">Identity for the Web3 era<"),
    (">Гайды по интеграции, технические разборы, обновления продукта.<",
     ">Integration guides, technical deep-dives, product updates.<"),
    ("Гайды, обновления и кейсы Libermall ID. Identity для Web3-проектов.",
     "Guides, releases and case studies from Libermall ID. Identity for Web3 projects."),
    (">Подключаем Libermall ID к Laravel за 5 минут<",
     ">Wire up Libermall ID to Laravel in 5 minutes<"),
    (">Почему мы выбрали JWT RS256 с 4096-битным ключом<",
     ">Why we chose JWT RS256 with a 4096-bit key<"),
    (">TON Connect как Identity Provider в OAuth flow<",
     ">TON Connect as an Identity Provider in an OAuth flow<"),

    # ── changelog ──
    (">Что нового<", ">What's new<"),
    (">Каждый релиз Libermall ID — здесь. RSS-feed: ",
     ">Every Libermall ID release lives here. RSS feed: "),
    (">Полноценный сайт + dashboard<", ">Full landing site + dashboard<"),
    (">Новый брендовый сайт по design-system showcase<",
     ">New branded site showcasing the design system<"),
    (">Dashboard /dashboard со списком сессий и подключённых аккаунтов<",
     ">Dashboard /dashboard with session list and linked accounts<"),

    # ── api playground ──
    (">Попробуйте API в реальном времени<",
     ">Try the API in real time<"),
    (">Интерактивный explorer для OIDC endpoints Libermall ID.<",
     ">Interactive explorer for Libermall ID OIDC endpoints.<"),
    (">Доступные endpoints<", ">Available endpoints<"),
    (">Authorization (опционально)<", ">Authorization (optional)<"),

    # ── docs-quickstart ──
    (">Quickstart · 5 минут<", ">Quickstart · 5 minutes<"),
    (">Интеграция Libermall ID за 5 минут<",
     ">Integrate Libermall ID in 5 minutes<"),
    (">Шаги<", ">Steps<"),

    # ── integrate.html ──
    (">Добавьте кнопку<br><span class=\"accent\">«Continue with Libermall ID»</span><",
     '>Add the button<br><span class="accent">"Continue with Libermall ID"</span><'),
    (">Подключите свой сервис к экосистеме Libermall. Получите доступ к ",
     ">Connect your service to the Libermall ecosystem. Get instant access to "),

    # ── privacy / terms ──
    (">Политика конфиденциальности<", ">Privacy Policy<"),
    (">Условия использования<",      ">Terms of Service<"),
    (">Версия 1.0.<", ">Version 1.0.<"),
    (">Содержание<", ">Contents<"),
    (">Кто мы<", ">Who we are<"),
    (">Какие данные собираем<", ">What data we collect<"),
    (">Зачем мы это делаем<", ">Why we collect it<"),
    (">Кому передаём данные<", ">Who we share it with<"),
    (">Принятие условий<", ">Acceptance<"),
    (">Описание сервиса<", ">Description of the service<"),
    (">Регистрация и аккаунт<", ">Registration and account<"),
    (">Запрещено<", ">Prohibited<"),
    (">Сторонние сервисы<", ">Third-party services<"),
    (">Доступность сервиса<", ">Service availability<"),
    (">Прекращение доступа<", ">Termination<"),
    (">Изменения условий<", ">Changes to the terms<"),
    (">Ответственность<", ">Liability<"),
    (">Юрисдикция<", ">Jurisdiction<"),

    # ── legal pages ──
    ("Эффективен с 2026-05-24. Version 1.0.",
     "Effective from 2026-05-24. Version 1.0."),
    (">1. Стороны<", ">1. Parties<"),
    (">2. Предмет обработки<", ">2. Scope of processing<"),
    (">1. Уровни SLA по плану<", ">1. SLA tiers by plan<"),
    (">Growth<", ">Growth<"),
    (">Enterprise<", ">Enterprise<"),
    (">1 рабочий день<", ">1 business day<"),
    (">1 час (critical) · 4 часа (high)<", ">1 hour (critical) · 4 hours (high)<"),

    # ── robots.txt comment ──
    ("# Приватные / auth-flow страницы — не индексируем",
     "# Private / auth-flow pages — do not index"),

    # ── style.css comment ──
    ("/* ── why-id (3 cards с иконками вверху) ── */",
     "/* ── why-id (3 cards with top icons) ── */"),
]


try:
    from extra_replacements import EXTRA_REPLACEMENTS
    REPLACEMENTS.extend(EXTRA_REPLACEMENTS)
except ImportError:
    pass


def translate_file(path: Path) -> int:
    text = original = path.read_text(encoding="utf-8")
    changes = 0
    for ru, en in REPLACEMENTS:
        count = text.count(ru)
        if count:
            text = text.replace(ru, en)
            changes += count
    if text != original:
        path.write_text(text, encoding="utf-8")
    return changes


CYRILLIC = re.compile(r'[Ѐ-ӿ]')


def main() -> int:
    if not PUBLIC.exists():
        print(f"[!] public/ not found at {PUBLIC}", file=sys.stderr)
        return 1

    total = 0
    leftovers: dict[str, int] = {}
    for path in sorted(PUBLIC.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix not in {".html", ".xml", ".txt", ".css", ".js", ".svg", ".webmanifest"}:
            continue
        n = translate_file(path)
        total += n
        text = path.read_text(encoding="utf-8")
        cyrillic_lines = sum(1 for ln in text.splitlines() if CYRILLIC.search(ln))
        if cyrillic_lines:
            leftovers[path.relative_to(PUBLIC).as_posix()] = cyrillic_lines

    print(f"[✓] {total} replacements; {len(leftovers)} files still contain cyrillic lines:")
    for k, v in sorted(leftovers.items(), key=lambda kv: -kv[1])[:40]:
        print(f"  {v:>4}  {k}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
