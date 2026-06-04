# Component Spec Template

Guide for generating interactive HTML spec tools for **single UI components** (button, card, modal, input, nav item, avatar, badge, toast, etc.).

> ## ⚠️ Read this before using the tables below
>
> A single component is the **thing most likely to be mis-used as a "style tweaker"** — and that's almost always the wrong use. Two rules override the tables:
>
> 1. **If the project has a design system, LOCK the Visual controls.** A `Button` inside a real app does NOT get a color picker or radius slider — those come from `:root` vars / Tailwind config / the component lib. Read them, hard-code as constants, expose none. The Visual table below is **greenfield-only** (inventing a component with no design language to inherit).
>
> 2. **What's worth speccing for a component is its STATES & VARIANTS, not its pixels**: which states exist (default/hover/loading/disabled/error/empty), which variants the team needs, interaction edge cases (click while loading? content overflow? no data?), which props/slots it exposes. If a decision is "one person just picks it," it doesn't need a control.
>
> Rule of thumb: if your component spec is mostly color/radius/shadow sliders and the component lives in a real app, you're speccing the wrong layer — spec the states and variants instead.

## Control Categories

### Layout Controls

| Control | Type | Default | Notes |
|---------|------|---------|-------|
| Width | range (50px–800px) or select (fit-content, full-width, fixed) | fit-content | Show px value |
| Height | range (24px–600px) or auto | auto | |
| Padding | range (0–4rem) | 1rem | Option: uniform or per-side |
| Margin | range (0–4rem) | 0 | |
| Display | select (inline-flex, flex, block, inline) | inline-flex | |
| Alignment | button group (left, center, right) | center | |
| Gap (internal) | range (0–2rem) | 0.5rem | For multi-element components |
| Aspect Ratio | select (auto, 1:1, 16:9, 4:3) | auto | For media components |

### Visual Controls — ⚠️ GREENFIELD ONLY

**Skip if the project has a design system** — lock these tokens as constants instead. Applies only to components invented with no existing visual language.

| Control | Type | Default | Notes |
|---------|------|---------|-------|
| Background Color | color + HSL sliders | #ffffff | Show hex + hsl |
| Text Color | color + HSL sliders | #1a1a1a | |
| Primary/Accent Color | color + HSL sliders | hsl(220, 80%, 50%) | Used for interactive states |
| Border Width | range (0–4px) | 1px | |
| Border Color | color | #e0e0e0 | |
| Border Radius | range (0–24px) | 8px | |
| Shadow | select (none, sm, md, lg, xl) | sm | Show shadow preview |
| Font Size | range (12–32px) | 14px | |
| Font Weight | select (300, 400, 500, 600, 700) | 500 | |
| Line Height | range (1–2) | 1.5 | |
| Opacity | range (0–1) | 1 | |
| Transition Duration | range (0–500ms) | 150ms | |

### Behavior Controls

| Control | Type | Default | Notes |
|---------|------|---------|-------|
| Hover Effect | select (none, darken, lighten, scale, shadow) | darken | Preview on hover |
| Active/Press Effect | select (none, scale-down, darken, inset-shadow) | scale-down | |
| Focus Style | select (ring, outline, glow, none) | ring | |
| Disabled State | checkbox | false | Show disabled appearance |
| Loading State | select (none, spinner, skeleton, pulse) | none | |
| Animation In | select (none, fade, slide-up, scale, bounce) | none | |
| Click Feedback | select (none, ripple, flash, scale) | none | |
| Cursor | select (pointer, default, not-allowed) | pointer | |

### Content Controls

| Control | Type | Default | Notes |
|---------|------|---------|-------|
| Label Text | text input | "Button" | Live updates preview |
| Icon Position | select (none, left, right, only) | none | |
| Icon | select from common set | — | Only if icon enabled |
| Secondary Text | text input | "" | Subtitle/description |
| Badge/Count | text input | "" | Optional badge overlay |
| Truncation | select (none, ellipsis, wrap) | none | |
| Max Lines | range (1–5) | 1 | Only if truncation enabled |

## Presets

Include 3–5 presets relevant to the specific component. Examples for common components:

**Button**: Minimal, Rounded, Bold, Ghost, Branded
**Card**: Flat, Elevated, Bordered, Compact, Hero
**Modal**: Centered, Slide-up, Fullscreen, Drawer, Alert
**Input**: Default, Floating Label, Minimal, Outlined, Filled

## Preview Requirements

- Render the component at actual size in the preview panel
- Show hover/active/focus states on interaction
- Include a "states grid" toggle showing: Default, Hover, Active, Focus, Disabled, Loading
- Provide a light/dark background toggle behind the preview
- Show the component at multiple sizes if size is configurable

## Spec Output Notes

For component specs, the JSON output should also include:
- `variants`: Array of state variants (hover, active, disabled) with their visual diffs
- `slots`: Named content slots with expected content type
- `props`: Suggested component API (prop name → type → default)

Example addition to spec:
```json
{
  "decisions": { ... },
  "api": {
    "variants": ["default", "primary", "ghost", "danger"],
    "slots": {
      "icon": { "type": "ReactNode", "position": "left|right" },
      "label": { "type": "string", "required": true }
    },
    "props": {
      "size": { "type": "sm|md|lg", "default": "md" },
      "loading": { "type": "boolean", "default": false },
      "disabled": { "type": "boolean", "default": false }
    }
  }
}
```
