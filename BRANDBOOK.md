# Libermall ID — Brand Book

Версия 1.0 · 2026-05-24

## Миссия и tone of voice

Libermall ID — это утилитарная инфраструктура. Не «волшебство», не «революция», а **надёжный, прозрачный, технически грамотный** сервис идентификации.

| | Yes | No |
|---|---|---|
| Стиль | конкретный, технический, дружелюбный | маркетинговый, восторженный |
| Голос | «работает за 5 минут», «JWT RS256», «один аккаунт» | «изменит мир», «революционно» |
| Примеры | «7000+ пользователей экосистемы» | «миллионы fanатов!!!» |

## Логотип

### Главный лого
Galочка (check-mark) внутри скруглённого квадрата + текстовая часть «Libermall ID».

- Цвет квадрата: `#2A7BFF` (primary)
- Цвет галочки: `#FFFFFF`
- Шрифт текста: Inter, weight 700, letter-spacing -0.5
- Цвет «Libermall»: `#17212B` (secondary)
- Цвет «ID»: `#2A7BFF` (accent)

### Иконка (favicon)
Только квадрат с галочкой. Размеры 40×40, 128×128.

### Варианты
- **Полноцветный** — на светлом фоне
- **Инвертированный** — на тёмном (footer, OG-cover) — текст белый, квадрат остаётся primary
- **Монохромный** — только для печати

### Запрещено
- Изменять пропорции
- Менять цвета (кроме официальных вариантов)
- Удалять фон у иконки
- Добавлять тени и градиенты

## Цветовая палитра

### Brand colors

| Имя | HEX | RGB | Использование |
|---|---|---|---|
| **Primary** | `#2A7BFF` | 42, 123, 255 | CTA-кнопки, логотип, акценты |
| **Primary-dark** | `#1E5DCE` | 30, 93, 206 | hover для primary |
| **Secondary** | `#17212B` | 23, 33, 43 | Тёмные блоки, основной текст, footer |

### Backgrounds

| Имя | HEX | Использование |
|---|---|---|
| **BG** | `#EEF3FB` | Основной фон страниц |
| **BG-soft** | `#F8FAFD` | Альтернативный светлый |
| **BG-card** | `#FFFFFF` | Карточки и формы |

### Status colors

| Имя | HEX | Использование |
|---|---|---|
| **Green** | `#2ECC71` | Success, верификация, надёжность |
| **Orange** | `#FFB02E` | Warning, средний риск, звёзды |
| **Red** | `#EF4444` | Error, high risk, негатив |

### Text

| Имя | HEX | Использование |
|---|---|---|
| **Text** | `#17212B` | Основной текст |
| **Muted** | `#64748B` | Вторичный, lead-параграф, footer-text |
| **Border** | `#E5EAF1` | Границы карточек, hr |

## Типографика

### Шрифты
- **Основной:** [Inter](https://fonts.google.com/specimen/Inter) — weights 400, 500, 600, 700
- **Монo (код):** [JetBrains Mono](https://www.jetbrains.com/lp/mono/) — 400, 500
- **Fallback:** `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`

### Шкала

| Класс | Size | Weight | Letter-spacing | Использование |
|---|---|---|---|---|
| H1 (hero) | `clamp(2.4rem, 5vw, 3.6rem)` | 700 | -0.04em | Главные заголовки |
| H1 (article) | 2.4rem | 700 | -0.02em | Заголовки страниц |
| H2 | 2.2rem | 700 | -0.02em | Section titles |
| H3 | 1.2rem | 600 | 0 | Card titles |
| H4 | 0.9rem | 600 | 0.04em | Footer headers (UPPERCASE) |
| Body | 1rem | 400 | 0 | Основной текст |
| Lead | 1.25rem | 400 | 0 | Lead-параграф |
| Small | 0.875rem | 400 | 0 | Captions, метаданные |
| Code | 0.9em | 400 | 0 | inline `code` блоки |

### Line-height
- Body: 1.6
- Headings: 1.1–1.2

## Компоненты

### Button-primary
- Background: `#2A7BFF` → hover `#1E5DCE`
- Color: `#FFFFFF`
- Padding: `14px 28px`
- Border-radius: `12px`
- Font-weight: 600

### Button-outline
- Background: transparent → hover `#FFFFFF`
- Border: 1px solid `#E5EAF1` → hover `#2A7BFF`
- Color: `#17212B` → hover `#2A7BFF`

### Card
- Background: `#FFFFFF`
- Border: 1px solid `#E5EAF1`
- Border-radius: `20px`
- Padding: `32px`
- Hover: `translateY(-2px)` + shadow

### Input
- Background: `#FFFFFF`
- Border: 1px solid `#E5EAF1`
- Border-radius: `10px`
- Padding: `12px 16px`
- Focus: border `#2A7BFF`, shadow `0 0 0 3px rgba(42,123,255,0.15)`

## Иконография

- Стиль: outline (stroke 2px), скруглённые концы
- Источник: [Lucide](https://lucide.dev) или Bootstrap Icons
- Размер default: 16px (inline), 20px (in buttons), 24px (standalone), 48px (cards)
- Цвет: наследует от parent (`currentColor`)

## Гайдлайны для маркетинга

### OpenGraph cover (1200×630)
- Фон: light gradient `#EEF3FB → #FFFFFF`
- Лого в углу: large quad + check-mark
- Title: Inter 68px bold
- Subtitle: Inter 32px primary
- Brand line: «id.libermall.com» внизу

### Social posts
- Брендовый шаблон: квадрат 1080×1080 или вертикаль 1080×1920
- Лого вверху-слева
- Plain background `#EEF3FB`
- Acentный текст — primary
- Body text — secondary

## Файлы

- `public/assets/logo.svg` — полный лого
- `public/favicon.svg` — иконка
- `public/assets/og-cover.svg` — OG-cover (рендерить в PNG через rsvg-convert при необходимости)

## Использование

При создании любых маркетинговых материалов Libermall ID — следовать этому гайду. Сомнения — спросить через PR-issue в [DeFiTON/libermall-id-landing](https://github.com/DeFiTON/libermall-id-landing).
