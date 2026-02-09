---
name: modern-button
description: Create trendy glassmorphism buttons with smooth animations. Use when user wants modern UI buttons.
---

# Modern Button Design

## Instructions

Create buttons with the following qualities:

1. **Glassmorphism**
   - Semi-transparent background
   - backdrop-filter blur
   - Soft borders

2. **Hover & Interaction**
   - Scale-up animation
   - Color and shadow transition
   - Active press feedback

3. **Responsiveness**
   - Touch-friendly padding
   - Scales properly on mobile and desktop

## Example Code

```css
.glass-button {
  padding: 12px 28px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  color: #fff;
  transition: all 0.3s ease;
}

.glass-button:hover {
  transform: scale(1.05);
  background: rgba(255, 255, 255, 0.25);
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}
