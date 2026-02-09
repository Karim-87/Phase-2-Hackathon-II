
```md
---
name: layout-grid
description: Generate responsive grid layouts for modern web UIs. Use for pages, dashboards, and card collections.
---

# Layout Grid System

## Instructions

- Use CSS Grid with auto-fit / minmax
- Maintain consistent gaps
- Support mobile, tablet, and desktop

## Example

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}
