
```md
---
name: modern-card
description: Create modern responsive card components with hover effects and accessibility support. Use for dashboards, blogs, and product listings.
---

# Modern Card Component

## Instructions

1. **Card Layout**
   - Rounded corners
   - Consistent padding
   - Clear content separation (image, title, body)

2. **Hover & Shadow Effects**
   - Soft shadow on default
   - Elevated shadow on hover
   - Subtle scale or translate animation

3. **Responsive Grid**
   - CSS Grid or Flexbox
   - Auto-fit columns
   - Mobile-first approach

4. **Image Optimization**
   - Use responsive images
   - Maintain aspect ratio
   - Lazy loading where possible

5. **Accessibility**
   - Proper semantic tags
   - Keyboard focus states
   - Alt text for images
   - Sufficient color contrast

## Example Code

```css
.card {
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 40px rgba(0,0,0,0.15);
}
