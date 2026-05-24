# Libermall ID — Brand Book

Версия 2.0 · 2026-05-24 · **Dark + Yellow**

## Tone of voice

Libermall ID — утилитарная инфраструктура. Не «волшебство», а **надёжный, прозрачный, технически грамотный** SSO-сервис.

| | Yes | No |
|---|---|---|
| Стиль | конкретный, технический, дружелюбный | маркетинговый, восторженный |
| Голос | «работает за 5 минут», «JWT RS256», «один аккаунт» | «изменит мир», «революционно» |

## Логотип

### Главный знак
Ромб (diamond) с двумя угловыми скобками `<` и `>` внутри + текст «Libermall ID».

- Ромб: `#FFD60A` (primary)
- Скобки: `#0D0D0F` (фон) — стиль кода-скобок, означает «открытое API»
- Текст «Libermall ID»: `#FFFFFF` на тёмном фоне, `#0D0D0F` на светлом
- Шрифт: Inter, weight 700, letter-spacing -0.5

### Запрещено
- Менять цвета (только официальные)
- Удалять скобки внутри ромба
- Деформировать ромб (только пропорциональное масштабирование)
- Использовать на shrillyellow фоне (исключает читабельность)

## Цветовая палитра

### Brand colors

| Имя | HEX | Использование |
|---|---|---|
| **Primary (Yellow)** | `#FFD60A` | Лого ромб, CTA-кнопки, акценты, ссылки |
| **Primary hover** | `#FFCB1A` | hover state для primary |
| **BG (Charcoal)** | `#0D0D0F` | Основной фон страниц |
| **Card BG** | `#1A1A1F` | Карточки, формы, navbar |
| **Card hover** | `#22222A` | hover state для cards |
| **Border** | `#2A2A33` | Границы карточек |
| **White** | `#FFFFFF` | Основной текст |
| **Text-soft** | `#D0D0D8` | Body text |
| **Muted** | `#6E6E78` | Captions, метаданные |

### Status colors

| Имя | HEX |
|---|---|
| **Green** | `#2ECC71` |
| **Orange** | `#FFB02E` |
| **Red** | `#EF4444` |

## Типографика

- **Inter** — основной (400, 500, 600, 700)
- **JetBrains Mono** — для кода
- **Fallback:** `-apple-system, BlinkMacSystemFont, sans-serif`

### Шкала

| Класс | Size | Weight | Letter-spacing |
|---|---|---|---|
| H1 (hero) | `clamp(2.4rem, 4.5vw, 4rem)` | 700 | -0.03em |
| H1 (article) | 2.4rem | 700 | -0.02em |
| H2 | 2rem | 700 | -0.02em |
| H3 | 1.2rem | 600 | 0 |
| H4 | 0.85rem | 600 | 0.06em (UPPERCASE) |
| Body | 1rem | 400 | 0 |
| Lead | 1.1rem | 400 | 0 |

### Line-height
- Body: 1.6
- Headings: 1.05–1.2

## Компоненты

### Button-primary
- Background: `#FFD60A` → hover `#FFCB1A`
- Color: `#0D0D0F` (чёрный текст на жёлтом)
- Padding: `14px 28px`
- Border-radius: `12px`
- Font-weight: 600

### Button-secondary
- Background: `#1A1A1F`
- Border: 1px solid `#2A2A33` → hover `#FFD60A`
- Color: `#FFFFFF` → hover `#FFD60A`

### Card
- Background: `#1A1A1F`
- Border: 1px solid `#2A2A33`
- Border-radius: `20px`
- Padding: `32px`
- Hover: `translateY(-2px)` + `border-color: #FFD60A`

### Input
- Background: `#0D0D0F`
- Border: 1px solid `#2A2A33`
- Border-radius: `10px`
- Padding: `12px 16px`
- Focus: border `#FFD60A`, shadow `0 0 0 3px rgba(255,214,10,0.15)`
- Placeholder: `#6E6E78`

## Иконография

- Стиль: outline (stroke 2px), скруглённые концы
- Источник: Lucide или Bootstrap Icons
- Размер: 16 (inline), 20 (button), 24 (standalone), 36 (cards)
- Цвет: `currentColor` (наследует) или `#FFD60A` для акцентов

## Контент-блоки

### Hero illustration
- Полупрозрачный glow `radial-gradient(rgba(255,214,10,0.06)...)`
- Floating product cards (анимация `floaty` 6s)
- Dashboard mock с тёмными background

### Stats bar
- 6 счётчиков: пользователи / аккаунты / верифицированные / продукты / uptime / поддержка
- Цвет иконок: `#FFD60A`

### Integration strip
- 4 протокола в боксах: OpenID Connect, OAuth 2.0, SAML 2.0, SDK
- Каждый с цветным significantly жёлтым icon

## OpenGraph cover (1200×630)
- Фон `#0D0D0F` с decorative orbs `rgba(255,214,10, 0.06)`
- Логотип-ромб 140×140 слева
- Title: Inter 64px white
- Subtitle: Inter 32px primary
- Brand line: «id.libermall.com» внизу muted

## Файлы

- `public/assets/logo.svg` — главный лого (white text)
- `public/favicon.svg` — diamond-only иконка
- `public/assets/og-cover.svg` — OG cover 1200×630 (dark)

## История версий

- **v2.0** (2026-05-24) — Dark + Yellow re-brand (по мокапу). Diamond logo с brackets. Primary `#FFD60A` (вместо `#2A7BFF`)
- **v1.0** (2026-05-24) — Initial light theme с primary `#2A7BFF`
