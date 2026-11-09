# TaskFlow design system

## Design intent

TaskFlow should make task management feel calm and capable. The interface uses warm off-white surfaces, forest-green actions, generous whitespace, short labels, and a lightly dimensional task illustration. Visual personality comes from typography, small task details, and restrained motion; the task product does not need a decorative mascot or 3D character to explain its purpose.

## Foundations

| Token | Value | Use |
|---|---|---|
| Paper | `#f7f8f5` | App background |
| Surface | `#ffffff` | Cards and forms |
| Ink | `#17231f` | Main text and dark actions |
| Muted | `#707b75` | Supporting copy |
| Line | `#e5e9e3` | Borders and separators |
| Primary | `#14745e` | Primary action, links, active state |
| Primary hover | `#0b5c49` | Hover/focus action |
| Mint | `#dcefe6` | Secondary callouts |
| Lime | `#d8f27b` | Small accent only |
| Coral | `#d98167` | Overdue/high-attention accent |

- **Type:** system sans-serif stack for headings and body, with a heavier display weight for the wordmark and page titles. No remote font request is needed.
- **Shape:** 8–14 px control/card radii; pill styling reserved for compact labels.
- **Depth:** thin green-gray borders, modest card shadow, translucent sticky navigation.
- **Spacing:** Bootstrap 5 grid plus 8 px rhythm; page content capped at 1180 px.
- **Motion:** short hover/entrance motion; `prefers-reduced-motion` removes nonessential animation.

## Components

- **Navigation:** text wordmark with custom SVG icon; account avatar; active page treatment; POST logout; collapsible mobile navigation.
- **Primary button:** dark forest green with clear verb label and small directional cue. Hover lifts by one pixel.
- **Stat card:** metric first, label second, short explanation third. Overdue has a distinct muted coral cue.
- **Priority badge:** muted green for low, amber for medium, coral for high. Text always names the priority; color is supplementary.
- **Status badge:** neutral gray, cool blue, or muted green with visible status text.
- **Filter bar:** search + labeled native selects + explicit submit. Filters remain usable without JavaScript.
- **Task row:** title, optional description, status, priority, due date, and edit affordance. Mobile layout reflows rows into labeled cards.
- **Empty state:** brief explanation and a next action, with separate copy for empty list and no filter matches.
- **Feedback:** Django messages are announced with `role=status` and can be dismissed.

## Page layouts

| Page | Layout |
|---|---|
| Landing | Value statement and CTA beside an original task-list illustration; three concise benefit columns; final CTA |
| Register/login | Single centered form panel with field-level errors, concise help, and a link to the alternate account route |
| Dashboard | Personal greeting, five stat cards, upcoming task list, completion momentum panel |
| Task list | Page title/CTA, one responsive filter panel, result count, responsive data table/cards |
| Task form | Narrow readable panel, labels above fields, validation adjacent to field, clear save/cancel actions |
| Task detail | Task identity, status/priority, owner data, due/updated dates, edit/delete/complete controls |
| Delete confirm | Explicit target title and consequence, POST delete and safe cancel |
| Profile/password | Standard form panel; password-change success confirmation |

## Wireframe sketches

These low-fidelity structure sketches describe content order. The live templates and CSS in `templates/` and `public/static/css/app.css` are the high-fidelity implementation.

```text
Landing (desktop)                     Landing (mobile)
┌──────────────────┬───────────────┐  ┌──────────────────────┐
│ value statement  │ task-list art │  │ value statement      │
│ short explanation│ floating notes│  │ primary + login CTA  │
│ primary + login  │               │  │ task-list art        │
│ privacy cue      │               │  │ three benefits       │
└──────────────────┴───────────────┘  └──────────────────────┘

Dashboard                             Task list
┌───────────────────────────────────┐  ┌──────────────────────────────┐
│ greeting + new task               │  │ title + new task             │
│ total | pending | active | done…  │  │ search | priority | status…  │
│ upcoming deadlines │ momentum     │  │ results count                │
└───────────────────────────────────┘  │ task rows / mobile task cards│
                                       └──────────────────────────────┘
```

## Responsive and accessibility rules

- Desktop: two-column landing hero, five dashboard metrics, side-by-side upcoming and momentum panels.
- Tablet: flexible hero and filter rows; metrics flow to three columns.
- Mobile: one-column hero and values; two-column metrics; filter controls wrap; table rows become cards; controls remain touch-friendly.
- All form controls have visible or screen-reader labels. Buttons and links have meaningful names. Decorative art is hidden from assistive technology unless described as a whole.
- A skip link provides direct keyboard access to main content. Focus outlines remain visible.
- Priority/status use text as well as color. Feedback uses a live status role.
- Reduced-motion settings disable animations and smooth scrolling.
- Keep text/background contrast readable; avoid using the accent colors for long paragraphs.
- The page stylesheet and favicon are first-party files under `public/static/`; the Bootstrap stylesheet is an optional CDN enhancement, not the only source of layout/styling.

## Interaction rules

- Use hover only as reinforcement; every action remains available by keyboard and touch.
- GET is read-only. Task completion, deletion, profile changes, and logout use POST with CSRF tokens.
- No essential interaction depends on animation or JavaScript.
- Empty, validation, success, and overdue states each have explicit visible copy.

## Design QA checklist

- [ ] Check 1440, 1024, 768, 390, and 320 px widths.
- [ ] Confirm no horizontal scrolling in list/filter and form screens.
- [ ] Tab through navigation, filters, forms, and destructive confirmation.
- [ ] Check the reduced-motion media preference.
- [ ] Check priority, status, error, success, empty, and overdue contrast/content.
- [ ] Verify external CDN failure leaves the server-rendered page readable and usable.
