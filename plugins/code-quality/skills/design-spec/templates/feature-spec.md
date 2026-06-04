# Feature Spec Template

Guide for generating interactive HTML spec tools for **features and interactions** (search, filtering, drag-and-drop, notifications, form wizards, authentication flows, etc.).

> ## ✅ This is the template that's already doing it right — keep it that way
>
> Feature specs are where this tool shines: the high-value decisions are **behavioral forks** (which flow merges with which, where output lands, how a multi-step process is expressed, what path a feature takes), and this template's Layout/Behavior axes already capture those. Two guardrails:
>
> 1. **Lock Visual controls if a design system exists.** A feature lives inside the app's existing visual language — don't expose color/radius/typography knobs; hard-code the project tokens. The Visual table below is greenfield-only.
> 2. **Derive the real forks from the requirements, not the tables.** The tables are a generic menu; the decisions that actually need alignment are usually feature-specific (e.g. "results store: local table vs external backend vs dual-write", "stage X: evaluated vs passed-through-but-not-evaluated"). Make those the controls. Tag each with a `ref` to its requirement (see SKILL.md "Decision Anchors").

## Control Categories

### Layout Controls

| Control | Type | Default | Notes |
|---------|------|---------|-------|
| Trigger Position | select (inline, header, floating, sidebar, contextual) | inline | Where the feature lives |
| Panel Position | select (dropdown, modal, drawer-right, drawer-bottom, inline-expand) | dropdown | Where results/output shows |
| Panel Width | range (200–800px) | 400px | For drawers/modals |
| Panel Height | select (auto, fixed, full-screen) | auto | |
| Z-Index Layer | select (inline, overlay, modal, toast) | overlay | Stacking context |
| Anchor Point | select (top-left, top-right, bottom, center) | bottom | Relative positioning |
| Responsive Collapse | select (same, full-screen, bottom-sheet, hidden) | bottom-sheet | Mobile behavior |

### Visual Controls — ⚠️ GREENFIELD ONLY

**Skip if the project has a design system** — the feature inherits the app's visual language; lock tokens as constants. Greenfield features only.

| Control | Type | Default | Notes |
|---------|------|---------|-------|
| Surface Color | color | #ffffff | Panel/container background |
| Overlay Background | color + opacity | rgba(0,0,0,0.5) | Backdrop for modals |
| Accent Color | color + HSL | hsl(220, 80%, 50%) | Active/selected states |
| Success Color | color | #10b981 | Positive feedback |
| Error Color | color | #ef4444 | Error states |
| Warning Color | color | #f59e0b | Warning states |
| Border Style | select (none, subtle, prominent) | subtle | |
| Shadow | select (none, sm, md, lg) | md | |
| Animation Style | select (none, fade, slide, scale, spring) | fade | Entry/exit |
| Animation Duration | range (100–500ms) | 200ms | |
| Blur Backdrop | checkbox | false | Frosted glass effect |

### Behavior Controls

| Control | Type | Default | Notes |
|---------|------|---------|-------|
| Trigger Action | select (click, hover, focus, keyboard, auto) | click | What opens/starts the feature |
| Dismiss Action | select (click-outside, escape, explicit-close, any) | click-outside | What closes it |
| Debounce | range (0–1000ms) | 300ms | For search/input features |
| Minimum Characters | range (0–5) | 1 | Before triggering |
| Max Results | range (3–50) | 10 | |
| Keyboard Navigation | checkbox | true | Arrow keys, enter |
| Selection Mode | select (single, multi, range, none) | single | |
| Confirmation Required | checkbox | false | Extra step before action |
| Undo Support | checkbox | false | Allow reversal |
| Optimistic Updates | checkbox | false | Immediate UI feedback |
| Error Recovery | select (retry-button, auto-retry, dismiss, inline-message) | retry-button | |
| Loading Indicator | select (inline-spinner, skeleton, progress-bar, shimmer) | inline-spinner | |
| Empty State | select (message, illustration, suggestion, none) | message | |
| Persistence | select (none, session, local-storage, server) | none | Remember state |
| Real-time Updates | checkbox | false | Live data changes |
| Rate Limiting | select (none, throttle, debounce, queue) | debounce | |

### Content Controls

| Control | Type | Default | Notes |
|---------|------|---------|-------|
| Placeholder Text | text | "Search..." | Input placeholder |
| No Results Text | text | "No results found" | Empty state message |
| Loading Text | text | "Loading..." | While fetching |
| Success Message | text | "Done!" | After completion |
| Error Message | text | "Something went wrong" | On failure |
| Help Text | text | "" | Supplementary guidance |
| Show Count/Badge | checkbox | true | Result/item count |
| Show Shortcuts | checkbox | false | Keyboard shortcut hints |
| Show History | checkbox | false | Previous interactions |
| Show Suggestions | checkbox | true | Recommended actions |
| Grouping | select (none, category, type, recency) | none | Result organization |
| Result Format | select (text-only, with-icon, with-thumbnail, with-description) | with-icon | |

## Presets

Include presets tailored to the feature type:

**Search**: Command Palette (Cmd+K), Header Search, Filter Search, Instant Search, Fuzzy Match
**Notifications**: Toast Stack, Bell Menu, Banner, Inline Alerts, Push Permission
**Drag & Drop**: Kanban, Sortable List, File Upload, Reorder Grid, Transfer Lists
**Forms**: Step Wizard, Accordion, Live Validation, Autosave, Inline Edit
**Auth**: Login Modal, Magic Link, OAuth Buttons, 2FA Flow, Session Timeout

## Preview Requirements

- Show the feature in context (e.g., search bar inside a header, notification in a page corner)
- Interactive demo: user can trigger the feature and see states
- State timeline: show sequence of states (idle → active → loading → results → complete)
- Include sample data that demonstrates edge cases (long text, many items, errors)
- Show keyboard interaction (highlight what key does what)

## Spec Output Notes

For feature specs, include:
- `states`: State machine definition (idle, active, loading, success, error)
- `transitions`: What triggers state changes
- `dataFlow`: Input → processing → output description
- `accessibility`: ARIA roles, keyboard nav, screen reader announcements

Example addition to spec:
```json
{
  "decisions": { ... },
  "interaction": {
    "states": {
      "idle": { "trigger": "click or Cmd+K" },
      "active": { "shows": "input + recent history" },
      "searching": { "shows": "input + spinner + partial results" },
      "results": { "shows": "input + result list + count" },
      "empty": { "shows": "input + empty state message" },
      "error": { "shows": "input + error + retry button" }
    },
    "transitions": [
      { "from": "idle", "to": "active", "on": "trigger" },
      { "from": "active", "to": "searching", "on": "input >= minChars", "debounce": "300ms" },
      { "from": "searching", "to": "results", "on": "data received" },
      { "from": "searching", "to": "empty", "on": "no results" },
      { "from": "searching", "to": "error", "on": "fetch failed" },
      { "from": "*", "to": "idle", "on": "dismiss" }
    ],
    "accessibility": {
      "role": "combobox",
      "aria-expanded": "true when active",
      "aria-activedescendant": "current highlighted result",
      "announcements": ["X results found", "No results", "Error occurred"]
    }
  }
}
```
