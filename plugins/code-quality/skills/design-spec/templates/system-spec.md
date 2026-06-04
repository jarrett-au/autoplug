# System Spec Template

Guide for generating interactive HTML spec tools for **design systems and multi-component token definitions** (color palettes, typography scales, spacing systems, icon sets, component libraries, theme configurations).

> ## ✅ The exception: here, Visual controls ARE the product
>
> The other templates tell you to **lock** visual tokens when a design system exists. **This template is how that design system gets created in the first place** — so the rule is inverted: full HSL color controls, typography scales, spacing systems are exactly what you SHOULD expose here. This is the one place greenfield visual exploration is the whole point.
>
> The thing to get right instead: a system spec's output is **reusable tokens**, not a one-off page. Two consequences:
> 1. **Output named tokens, not raw values** — `--primary`, `--space-4`, `--radius-md`, not `#3b82f6`/`16px` scattered inline. Downstream component/page/feature specs will *consume* these names and lock them. Make the export a token dictionary.
> 2. **The decisions worth aligning are the *system rules*** — scale method (geometric vs linear), naming convention, how many steps, semantic vs literal naming — not just "what blue." Those rules are what make the system coherent; spec them explicitly.

## Control Categories

### Layout Controls (Spacing System)

| Control | Type | Default | Notes |
|---------|------|---------|-------|
| Base Unit | range (2–8px) | 4px | Foundation for all spacing |
| Scale Method | select (linear, geometric, fibonacci, custom) | geometric | How sizes grow |
| Scale Ratio | range (1.2–2.0) | 1.5 | Multiplier between steps |
| Steps Count | range (4–12) | 8 | Number of spacing tokens |
| Container Max Width | range (960–1440px) | 1200px | Page container |
| Grid Columns | range (4–16) | 12 | Grid system |
| Grid Gutter | range (8–32px) | 16px | Column gap |
| Breakpoints | multi-input | 640, 768, 1024, 1280 | Responsive breakpoints |
| Content Width | select (narrow-640, medium-768, wide-960, full) | medium-768 | Prose/content max-width |

### Visual Controls (Color & Typography)

**Color System:**

| Control | Type | Default | Notes |
|---------|------|---------|-------|
| Primary Hue | range (0–360) | 220 | HSL hue for primary |
| Primary Saturation | range (0–100%) | 80% | |
| Primary Lightness | range (20–80%) | 50% | |
| Secondary Hue | range (0–360) | 280 | |
| Neutral Base | select (warm, cool, pure) | cool | Gray tint |
| Color Steps | range (3–11) | 9 | Shades per color (50–900) |
| Contrast Method | select (WCAG-AA, WCAG-AAA, APCA) | WCAG-AA | Accessibility standard |
| Dark Mode Strategy | select (invert, dim, custom-palette) | invert | |
| Success/Error/Warning | 3x color pickers | green/red/amber | Semantic colors |
| Surface Count | range (1–5) | 3 | Background elevation layers |

**Typography:**

| Control | Type | Default | Notes |
|---------|------|---------|-------|
| Base Size | range (14–20px) | 16px | Body text size |
| Type Scale | select (1.125 minor-second, 1.2 minor-third, 1.25 major-third, 1.333 perfect-fourth, 1.5 perfect-fifth) | 1.25 | Heading ratio |
| Heading Levels | range (3–6) | 6 | h1 through hN |
| Body Line Height | range (1.3–1.8) | 1.6 | |
| Heading Line Height | range (1.0–1.4) | 1.2 | |
| Font Stack | select (system, inter, geist, custom) | system | |
| Mono Font | select (system-mono, jetbrains, fira-code) | system-mono | |
| Font Weights | multi-select (300, 400, 500, 600, 700, 800) | 400, 500, 600, 700 | Available weights |
| Letter Spacing (headings) | range (-0.05–0.05em) | -0.02em | |
| Paragraph Spacing | range (0.5–2em) | 1em | |

### Behavior Controls (Motion & Interaction)

| Control | Type | Default | Notes |
|---------|------|---------|-------|
| Motion Preference | select (full, reduced, none) | full | Respects prefers-reduced-motion |
| Duration Base | range (100–300ms) | 150ms | Shortest animation |
| Duration Scale | range (1.2–2.0) | 1.5 | Each level multiplier |
| Easing Default | select (ease, ease-out, ease-in-out, spring, linear) | ease-out | |
| Easing Emphasis | select (cubic-bezier options) | ease-in-out | For attention |
| Focus Ring Width | range (1–4px) | 2px | |
| Focus Ring Offset | range (0–4px) | 2px | |
| Focus Ring Color | color | primary | |
| Hover Transition | range (0–300ms) | 150ms | |
| Active Scale | range (0.9–1.0) | 0.97 | Press feedback |
| Scroll Behavior | select (smooth, auto, instant) | smooth | |

### Content Controls (Tokens & Naming)

| Control | Type | Default | Notes |
|---------|------|---------|-------|
| Token Format | select (css-vars, tailwind, scss, json, figma) | css-vars | Output format |
| Naming Convention | select (semantic, scale, descriptive) | semantic | e.g., --color-primary vs --blue-500 |
| Prefix | text | "" | e.g., "tk-" for all tokens |
| Include Comments | checkbox | true | In output |
| Dark Mode Tokens | checkbox | true | Generate dark variants |
| Include Opacity | checkbox | true | Color with alpha variants |
| Component Tokens | checkbox | true | Button, input, card defaults |
| Include Shadows | checkbox | true | Elevation system |
| Shadow Levels | range (2–6) | 4 | Elevation steps |
| Radius Tokens | checkbox | true | Border radius scale |
| Radius Steps | range (3–7) | 5 | sm, md, lg, xl, full |

## Presets

**Color**: Monochrome, Complementary, Analogous, Triadic, Brand-from-Logo
**Typography**: Technical (mono-heavy), Editorial (serif headings), Modern (geometric sans), Playful (rounded), Dense (compact scale)
**System**: Minimal (essential tokens only), Comprehensive (all tokens), Material-inspired, Tailwind-like, Custom (blank slate)

## Preview Requirements

- **Color palette grid**: All generated colors in a swatch grid with hex/hsl values and contrast ratios
- **Typography specimen**: All heading levels + body + small + code in actual generated sizes
- **Spacing visualization**: Boxes showing each spacing step size
- **Component previews**: Button, input, card, badge rendered with current tokens
- **Dark mode toggle**: Switch between light and dark using generated tokens
- **Contrast checker**: Show WCAG pass/fail for text on background combinations
- **Token count**: Display total number of tokens generated

## Spec Output Notes

For system specs, output tokens in the selected format plus a reference JSON:

```json
{
  "decisions": { ... },
  "tokens": {
    "colors": {
      "primary": {
        "50": "hsl(220, 80%, 97%)",
        "100": "hsl(220, 80%, 93%)",
        "500": "hsl(220, 80%, 50%)",
        "900": "hsl(220, 80%, 12%)"
      },
      "neutral": { "50": "...", "900": "..." },
      "semantic": {
        "success": "hsl(142, 71%, 45%)",
        "error": "hsl(0, 84%, 60%)",
        "warning": "hsl(38, 92%, 50%)"
      }
    },
    "typography": {
      "scale": [12, 14, 16, 20, 25, 31, 39, 49],
      "lineHeight": { "body": 1.6, "heading": 1.2, "tight": 1.1 },
      "weights": { "normal": 400, "medium": 500, "semibold": 600, "bold": 700 },
      "families": {
        "sans": "system-ui, -apple-system, sans-serif",
        "mono": "ui-monospace, 'SF Mono', monospace"
      }
    },
    "spacing": {
      "unit": "4px",
      "scale": [4, 8, 12, 16, 24, 32, 48, 64, 96, 128]
    },
    "radii": {
      "sm": "4px", "md": "8px", "lg": "12px", "xl": "16px", "full": "9999px"
    },
    "shadows": {
      "sm": "0 1px 2px rgba(0,0,0,0.05)",
      "md": "0 4px 6px rgba(0,0,0,0.07)",
      "lg": "0 10px 15px rgba(0,0,0,0.1)",
      "xl": "0 20px 25px rgba(0,0,0,0.12)"
    },
    "motion": {
      "duration": { "fast": "100ms", "normal": "150ms", "slow": "300ms", "slower": "450ms" },
      "easing": { "default": "ease-out", "emphasis": "cubic-bezier(0.4, 0, 0.2, 1)" }
    }
  },
  "output": {
    "css": ":root { --color-primary-500: hsl(220, 80%, 50%); ... }",
    "tailwind": "{ colors: { primary: { 500: 'hsl(220, 80%, 50%)' } } }",
    "scss": "$color-primary-500: hsl(220, 80%, 50%); ..."
  }
}
```

The HTML should include a "Copy Tokens" button that outputs the tokens in the selected format (CSS variables, Tailwind config, SCSS variables, or raw JSON) ready to paste into a project.
