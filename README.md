# Libermall ID — Landing

Маркетинговый сайт для [https://id.libermall.com](https://id.libermall.com). Static HTML + CSS, без build steps.

Casdoor (identity server) остаётся на `/login`, `/signup`, `/callback`, `/api/*`, `/.well-known/*` — этот landing работает только на корневых маркетинговых страницах.

## Структура

```
public/
├── index.html          # главная
├── products.html       # каталог продуктов экосистемы
├── developers.html     # документация OIDC + SDK
├── integrate.html      # маркетинг для интеграторов
├── about.html          # о проекте
├── privacy.html        # политика конфиденциальности
├── terms.html          # условия использования
├── sitemap.xml
├── robots.txt
├── favicon.svg
└── assets/
    ├── logo.svg        # лого + текст
    ├── og-cover.svg    # OpenGraph 1200x630
    └── style.css       # все стили
```

## Deploy

```bash
rsync -avz --delete public/ root@89.127.218.87:/var/www/libermall-id-landing/
```

Nginx конфиг — см. [`deploy/nginx-libermall-id.conf`](deploy/nginx-libermall-id.conf) в основном репо.

## SEO

- Уникальные `<title>` и `<meta description>` на каждой странице
- Canonical URLs
- OpenGraph + Twitter Card
- JSON-LD: Organization, WebSite, SoftwareApplication
- sitemap.xml + robots.txt
- Семантическая разметка `<article>`, `<section>`, `<nav>`

## Brand Book

См. [BRANDBOOK.md](BRANDBOOK.md) — цвета, типографика, лого, компоненты.

## Лицензия

MIT.
