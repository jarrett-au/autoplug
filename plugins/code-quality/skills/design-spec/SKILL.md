---
name: design-spec
description: |
  Use when creating an interactive HTML design-spec tool for UX, architecture, or product decisions
  where implicit choices must become explicit forks. The user adjusts options and exports a structured
  decision-ledger spec traced to requirements. Trigger for 'make a design spec', 'create an
  interactive spec', 'explore UX decisions', or 'freeze design-system tokens'.
user-invocable: true
argument-hint: "[description of what to spec]"
---

# Design Spec

Generate interactive single-file HTML prototypes that let users configure design decisions and export a structured specification for later implementation.

## What this tool is actually for (read first)

The naive framing is "visually tweak colors/spacing → get a mockup." That framing is wrong for most real work. **In any project with an existing design system, the visual tokens (colors, radius, fonts, spacing) are GIVEN constants — they are not the decisions worth aligning on.** The decisions worth aligning on are almost always **behavioral and structural**: which flows merge, where data lands, what's shown vs hidden, how stages are expressed, which path a feature takes.

So the real value of this tool is **forcing implicit architectural/UX forks into explicit either-or choices** the user can see and pick — then recording those picks as a spec that traces back to requirements. Treat it as a **decision-alignment tool**, not a visual-design toy.

Practical consequences (apply these by default):
1. **Detect the design system first.** If the target project has CSS variables / theme tokens / a component library (shadcn, MUI, Tailwind config, `:root` vars), READ them and **hard-code them as locked constants** in the HTML. Do NOT expose them as controls. Add a visible note like "视觉令牌已锁定为项目风格，不作可调项".
2. **Weight controls toward Behavior + Content, not Visual + Layout.** The default control templates over-index on visual knobs (HSL sliders, border-radius); in real projects those are the *least* useful. Spend your control budget on the genuine forks.
3. **HSL color sliders are for greenfield-only.** Only expose color/typography controls when the user is designing something with NO existing design system. If a design system exists, color controls are noise — and that's exactly the collaborative scenario where this tool matters most, so getting this right is the difference between useful and useless.

> **The one exception: `system-spec`.** Everything above ("lock the visuals") assumes you're speccing something that *consumes* a design system. But `system-spec` is how a design system gets *created* — there, exposing full color/typography/spacing controls is the entire point. The rule inverts: greenfield-visual is correct, and the output is reusable named tokens that the other three templates will then lock. See `templates/system-spec.md`.

## Modes

### Generation Mode (default)

User invokes `/design-spec <description>` → Claude generates a single-file HTML with:
- Live preview panel
- Control panel with adjustable parameters
- Spec output panel (JSON + Markdown tabs)
- Export buttons (file download + clipboard copy)

### Implementation Mode

User provides a `.design-spec.json` or `.design-spec.md` file → Claude reads the spec and implements production code matching all recorded decisions.

### Freeze Mode (finalize)

When decisions are settled and the user wants a clean deliverable ("生成最终事实源" / "定稿" / "freeze" / "给开发的版本"), produce a **second, separate HTML file** that is the frozen source of truth:
- **No controls panel, no spec-output panel** — just the app, rendered at the confirmed decisions (hard-code the chosen values as constants).
- Faithfully renders every screen/state the feature has (not just one).
- Keep an optional, **default-off** "annotation" toggle that overlays the spec/decision references (see Decision Anchors below) — so developers can flip it on to see "this UI ↔ which decision ↔ which code", but it doesn't clutter the default view.
- Name it distinctly from the iteration tool, e.g. `<feature>.frontend.html` (frozen) vs `<feature>.design-spec.html` (iteration tool). Both coexist: the design-spec stays editable, the frozen file is the dev reference.

> Why this is a first-class mode: without it, users manually copy the iteration tool into a "clean" version by hand — splitting one source of truth into two divergent files. Freeze Mode makes "lock the decisions and ship a clean reference" a one-command operation.

---

## Template Selection

Choose the template based on what the user is speccing:

| Template | When to use | Examples |
|----------|-------------|----------|
| `component-spec` | Single UI element | Button, card, modal, input, nav item |
| `page-spec` | Full page/screen layout | Dashboard, login page, settings page |
| `feature-spec` | Behavior/interaction design | Search, filtering, drag-and-drop, notifications |
| `system-spec` | Design system / tokens | Color palette, typography scale, spacing system |

If unclear, ask: "Is this a single component, a full page, a feature/behavior, or a design system?"

---

## HTML Generation Guidelines

### Architecture

Generate a single self-contained HTML file. No external dependencies (inline all CSS/JS).

Three-panel layout:

```
+-------------------+---------------------------+
|  CONTROLS         |  LIVE PREVIEW             |
|  (left sidebar)   |  (top-right)              |
|  scrollable       |                           |
|  [Layout]         |                           |
|  [Visual]         |                           |
|  [Behavior]       |                           |
|  [Content]        |                           |
|                   +---------------------------+
|                   |  SPEC OUTPUT              |
|                   |  (bottom-right)           |
|                   |  [JSON] [Markdown] tabs   |
|                   |  [Export] [Copy] buttons  |
+-------------------+---------------------------+
```

### State Management

```javascript
// Single state object — source of truth
const state = { /* all configurable values */ };

// Every control calls updateAll() on change
function updateAll() {
  renderPreview();
  renderSpec();
}

// Spec records deviations from defaults + intent
function getSpec() {
  return {
    meta: { name, type, version: "1.0", created: new Date().toISOString() },
    decisions: buildDecisions(state, defaults)
  };
}
```

### Control Categories

The four categories below are the *menu* to draw from — they are NOT a quota to fill evenly. **Weight your controls toward where the real decisions are.** In practice, for any feature inside an existing product, that means mostly Behavior + Content, a few Layout, and often **zero Visual** (tokens are locked, see "What this tool is for").

1. **Layout** — structure, grid, which regions exist, how panels split, responsive strategy
2. **Visual** — colors, typography, radius, theme. **Expose ONLY if greenfield (no design system).** If a design system exists, lock these as constants instead of making them controls.
3. **Behavior** — feature toggles, interaction forks, which flow/path a feature takes, where results land, stage expression, submit/loading behavior. **This is usually where the highest-value decisions live.**
4. **Content** — section visibility, what's shown vs hidden (and *why* — e.g. "keep empty slot to signal intentional" vs "hide"), input methods, placeholder content, sub-tab naming.

Good controls are **forks with consequences** ("results store: local table / Opik / dual-write"), not cosmetic knobs ("border-radius: 0–16px"). If a control's answer is obvious or one person would just decide it alone, it doesn't need to be a control — it doesn't need alignment.

### Control Types

Use appropriate HTML inputs:
- Button groups / segmented controls — mutually exclusive forks (the workhorse: most high-value decisions are 2–4 way picks)
- `<input type="checkbox">` — boolean toggles
- `<select>` — enumerated choices with many options
- `<input type="text">` — string values
- `<input type="range">` — numeric values (always show current value label)
- `<input type="color">` + HSL sliders — **greenfield only.** Skip entirely when a design system supplies the palette.

### Presets

Include 3-5 presets as starting points. Each preset sets the entire state to a coherent configuration. Display as buttons at the top of the controls panel.

Example presets for a button component: "Minimal", "Rounded", "Bold", "Ghost", "Branded"

### Export

Provide two export mechanisms:
1. **File download** — via Blob URL (`URL.createObjectURL`)
2. **Clipboard copy** — via `navigator.clipboard.writeText()`

Both for JSON and Markdown formats.

### Intent Annotations

The spec should capture not just values but *why*. Add an "Intent" text input next to important controls. Users can optionally explain their reasoning. These become `intent` fields in the spec output.

### Decision Anchors (traceability)

A design spec that can't be joined back to the requirements doc is an orphan. Give each meaningful decision an optional **`ref`** field linking it to the source-of-truth document — a requirements/spec section, a decision ID, a ticket, whatever the project uses (e.g. `"ref": "unified-evaluation.md#D13"` or `"ref": "JIRA-412"`).

Why this matters: it turns the exported spec from an isolated design JSON into a **decision ledger that traces UI control ↔ requirement ↔ (later) implementation**. When the requirements doc evolves, you can tell which UI decisions are affected; when implementing, you know which doc section governs each choice.

- Add a small `ref` text input (or pre-fill it programmatically) on decisions that map to a documented requirement.
- In Freeze Mode, the default-off annotation overlay surfaces these `ref`s directly on the rendered UI — so a developer flipping it on sees the exact decision/section each region implements.
- `ref` is optional per-decision; omit for cosmetic or self-evident choices.

### Responsive Preview

Include a viewport size toggle in the preview panel: Mobile (375px) | Tablet (768px) | Desktop (1200px) | Full width.

---

## Spec Output Format

### JSON (`.design-spec.json`)

```json
{
  "meta": {
    "name": "Login Form",
    "type": "component",
    "version": "1.0",
    "created": "2025-01-15T10:30:00Z",
    "template": "component-spec",
    "source_doc": "docs/specs/auth.md"
  },
  "decisions": {
    "layout": {
      "width": { "value": "400px", "intent": "Constrained for focus" },
      "padding": { "value": "2rem" }
    },
    "visual": {
      "_note": "locked to project design system — not configurable"
    },
    "behavior": {
      "validation": { "value": "on-blur", "intent": "Don't interrupt typing", "ref": "auth.md#FR-3" },
      "submitOnEnter": { "value": true },
      "resultStore": { "value": "local-table", "intent": "decouple from external backend", "ref": "auth.md#D13" }
    },
    "content": {
      "showForgotPassword": { "value": true },
      "showSocialLogin": { "value": false, "intent": "MVP - social auth later", "ref": "auth.md#NG-2" }
    }
  }
}
```

`ref` links a decision to its governing requirement (section anchor / decision ID / ticket). `_note` on a category records that it's intentionally locked (e.g. visual tokens from a design system).

### Markdown (`.design-spec.md`)

```markdown
# Login Form — Design Specification

> Generated by design-spec tool | Type: component | 2025-01-15 | Source: docs/specs/auth.md

## Layout Decisions

- **Width**: 400px — *Constrained for focus*
- **Padding**: 2rem

## Visual Decisions

- *Locked to project design system (not configurable).*

## Behavior Decisions

- **Validation**: on-blur — *Don't interrupt typing* `[auth.md#FR-3]`
- **Submit on Enter**: yes
- **Result Store**: local-table — *decouple from external backend* `[auth.md#D13]`

## Content Decisions

- **Forgot Password**: shown
- **Social Login**: hidden — *MVP - social auth later* `[auth.md#NG-2]`
```

---

## Implementation Mode Instructions

When user provides a `.design-spec.json` or `.design-spec.md`:

1. Read the spec file
2. Identify the `meta.type` to understand scope (component/page/feature/system)
3. Map each `decisions` entry to concrete code:
   - Layout decisions → CSS layout properties, Tailwind classes, or component structure
   - Visual decisions → CSS custom properties, theme tokens, or inline styles
   - Behavior decisions → event handlers, state logic, conditional rendering
   - Content decisions → component props, conditional slots, configuration
4. Respect `intent` annotations — they explain *why* a choice was made, which helps with edge cases
5. Follow `ref` anchors back to the governing requirement when a decision is ambiguous — the source doc section is authoritative over the spec JSON if they conflict
6. Treat any category marked `_note: locked` (e.g. visual tokens) as fixed project constants — do not re-derive or override them
7. Produce production-ready code matching the user's stack (React, Vue, plain HTML, etc.)

---

## Generation Checklist

Before outputting the HTML, verify:

- [ ] Single file, no external dependencies
- [ ] Three-panel layout renders correctly
- [ ] **Design system detected & locked** (if one exists: tokens hard-coded as constants, NOT exposed as controls, with a visible "locked" note)
- [ ] **Controls weighted toward the real decisions** (Behavior/Content for in-product features; Visual only if greenfield) — not an even quota across categories
- [ ] Every control is a fork that needs alignment, not a cosmetic knob one person would just decide
- [ ] Controls update preview in real-time
- [ ] Spec output reflects current state
- [ ] **Decision anchors**: high-value decisions carry an optional `ref` to the source doc / decision ID
- [ ] 3-5 presets included
- [ ] Export buttons work (JSON download, MD download, clipboard copy)
- [ ] Responsive preview toggle included
- [ ] Intent inputs on key decisions
- [ ] Clean default state (sensible starting point)
- [ ] Spec records only meaningful values (not internal UI state)

**Freeze Mode additional checks** (when finalizing):
- [ ] Separate file, named distinctly (`<feature>.frontend.html` vs the iteration `.design-spec.html`)
- [ ] No controls/spec panels — just the app at confirmed decisions
- [ ] Renders ALL screens/states, not just one
- [ ] Default-off annotation overlay surfaces `ref` anchors on the UI

---

## Template Reference

Refer to the templates in `templates/` for category-specific control guidance:

- `templates/component-spec.md` — Controls for single UI components
- `templates/page-spec.md` — Controls for page layouts
- `templates/feature-spec.md` — Controls for feature behaviors
- `templates/system-spec.md` — Controls for design system tokens
