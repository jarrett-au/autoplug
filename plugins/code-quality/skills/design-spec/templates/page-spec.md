# Page Spec Template

Guide for generating interactive HTML spec tools for **full page layouts** (dashboard, login page, settings, landing page, profile, list view, detail view, etc.).

> ## ⚠️ Read this before using the tables below
>
> The control tables in this template are **greenfield-biased** — they over-index on Visual (colors, radius, typography) and generic-page Layout knobs. **For a page inside an existing product, most of these are the WRONG controls.** Two rules override the tables:
>
> 1. **If the project has a design system, LOCK the Visual controls** (background/colors/radius/typography/density). Read the real tokens (`:root` vars, Tailwind config, component lib) and hard-code them as constants — do not expose them. The Visual table below applies **only to greenfield pages with no design system**.
>
> 2. **The decisions worth speccing for a real page are usually behavioral/structural**, and they're **page-specific** — they won't be in any generic table. Examples from real features: "which two flows merge into one tabbed page", "where do results get stored & rendered", "which sub-tabs go under this import screen", "what's shown vs hidden and why", "how is a multi-stage process expressed in the UI". Derive these from the actual requirements; the tables are only a fallback menu for the generic 20%.
>
> Rule of thumb: if you find yourself adding a border-radius slider to a page that lives in a real app, stop — you're speccing the wrong thing. Spend that control on the genuine fork the team actually needs to align on.

## Control Categories

### Layout Controls

| Control | Type | Default | Notes |
|---------|------|---------|-------|
| Page Width | select (full, contained-1200, contained-960, narrow-720) | contained-1200 | |
| Sidebar | select (none, left-240, left-280, left-320, right) | none | |
| Header Height | range (48–96px) | 64px | |
| Header Position | select (static, sticky, fixed) | sticky | |
| Footer | checkbox + height | false | |
| Content Columns | select (1, 2, 3, sidebar+main, main+aside) | 1 | |
| Column Gap | range (0–4rem) | 2rem | |
| Section Spacing | range (1–8rem) | 3rem | Between major sections |
| Page Padding | range (0–4rem) | 1.5rem | Horizontal page margins |
| Content Max Width | range (600–1400px) | 1200px | Within container |
| Responsive Strategy | select (stack, hide-sidebar, collapse-nav, drawer) | stack | |
| Breakpoints | multi-select (sm:640, md:768, lg:1024, xl:1280) | md, lg | |

### Visual Controls — ⚠️ GREENFIELD ONLY

**Skip this entire category if the project has a design system.** Lock the tokens as constants instead. These controls apply only when designing a page with no existing visual language to inherit.

| Control | Type | Default | Notes |
|---------|------|---------|-------|
| Background | color | #ffffff | |
| Surface Color | color | #f9fafb | Cards/panels |
| Text Color | color | #111827 | |
| Muted Text | color | #6b7280 | Secondary text |
| Primary Color | color + HSL | hsl(220, 80%, 50%) | Accent/action |
| Divider Style | select (none, line, shadow, gap) | line | Between sections |
| Card Style | select (flat, bordered, elevated, filled) | bordered | |
| Header Style | select (transparent, solid, blur, shadow) | solid | |
| Typography Scale | select (compact, default, spacious) | default | Adjusts all text sizes |
| Base Font Size | range (14–18px) | 16px | |
| Heading Font | select (same, serif, mono, display) | same | |
| Border Radius Theme | range (0–16px) | 8px | Applied to all elements |
| Density | select (compact, comfortable, spacious) | comfortable | Affects all spacing |

### Behavior Controls

| Control | Type | Default | Notes |
|---------|------|---------|-------|
| Navigation Type | select (top-tabs, sidebar-links, breadcrumb, hamburger) | top-tabs | |
| Scroll Behavior | select (paginated, infinite-scroll, virtual-list, static) | static | |
| Loading Pattern | select (skeleton, spinner, progressive, shimmer) | skeleton | |
| Error State | select (inline, toast, modal, banner) | inline | |
| Empty State | select (illustration, text-only, cta-button, none) | illustration | |
| Search | checkbox + position (header, sidebar, floating) | false | |
| Filters | select (none, top-bar, sidebar, dropdown) | none | |
| Sorting | checkbox | false | |
| Pagination | select (none, bottom, top-and-bottom, load-more) | none | |
| Notifications | select (none, bell-icon, banner, toast) | none | |
| Dark Mode Toggle | checkbox | false | |

### Content Controls

| Control | Type | Default | Notes |
|---------|------|---------|-------|
| Header Content | multi-select (logo, nav, search, user-menu, notifications) | logo, nav, user-menu | |
| Hero Section | checkbox + style (centered, split, background-image) | false | |
| Sidebar Sections | multi-select (nav, filters, stats, recent, help) | nav | |
| Main Content | select (cards-grid, table, list, form, mixed) | cards-grid | |
| Cards Per Row | range (1–6) | 3 | If cards-grid selected |
| Show Breadcrumb | checkbox | false | |
| Show Page Title | checkbox | true | |
| Show Subtitle | checkbox | false | |
| Footer Content | multi-select (links, copyright, social, newsletter) | copyright | |
| Content Density | select (sparse-10, medium-20, dense-50) | medium-20 | Items per view |

## Presets

Include presets tailored to the page type:

**Dashboard**: Admin Panel, Analytics, Kanban Board, Overview, CRM
**Landing Page**: SaaS Hero, Product, Documentation, Portfolio, Pricing
**Settings**: Tabbed, Sidebar Nav, Single Column, Sectioned
**List/Table**: Data Table, Card Grid, Feed, Timeline

## Preview Requirements

- Render full page at scale (fit viewport or scrollable)
- Responsive toggle: show Mobile / Tablet / Desktop side by side or switchable
- Section labels/overlays toggle (shows region names)
- Grid/spacing overlay toggle (shows column guides)
- Placeholder content appropriate to the page type (use realistic lorem text, numbers, avatars)

## Spec Output Notes

For page specs, include:
- `regions`: Named page regions with their layout role
- `responsive`: Breakpoint-specific overrides
- `sections`: Ordered list of content sections with visibility flags
- `navigation`: Nav structure and active state behavior

Example addition to spec:
```json
{
  "decisions": { ... },
  "structure": {
    "regions": {
      "header": { "position": "sticky", "height": "64px" },
      "sidebar": { "width": "280px", "collapsible": true },
      "main": { "maxWidth": "960px" },
      "footer": { "visible": false }
    },
    "sections": [
      { "id": "hero", "visible": true, "style": "centered", "ref": "spec.md#FR-UI-1" },
      { "id": "features", "visible": true, "columns": 3 },
      { "id": "cta", "visible": true, "style": "banner" }
    ],
    "responsive": {
      "768": { "sidebar": "hidden", "nav": "hamburger" },
      "640": { "columns": 1, "padding": "1rem" }
    }
  }
}
```

(`ref` on a section/region links it to the governing requirement — see SKILL.md "Decision Anchors".)
