
```md
---
name: hero-section
description: Build modern animated hero sections for landing pages. Use for homepage and product introductions.
---

# Hero Section Design

## Instructions

1. **Layout**
   - Full viewport height (min-h-screen)
   - Centered content
   - Clear visual hierarchy

2. **Visual Style**
   - Gradient or subtle animated background
   - Large bold headline
   - One primary CTA button

3. **Animations**
   - Fade-in on load
   - Staggered text animations
   - Optional parallax effect

## Best Practices
- Headline under 10 words
- Mobile-first design
- Single primary CTA
- Avoid heavy animations on low-end devices

## Example Structure

```jsx
<section className="hero min-h-screen flex items-center justify-center">
  <div className="hero-content text-center">
    <h1 className="animate-fade-in">Build Faster Frontends</h1>
    <p className="animate-fade-in-delay">
      Modern UI powered by AI
    </p>
    <button className="cta-button">Get Started</button>
  </div>
</section>
