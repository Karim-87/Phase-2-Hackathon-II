# Quickstart Guide: Frontend Modernization

## Prerequisites
- Node.js 18+ installed
- Access to the existing backend API
- Understanding of Next.js 16+ with App Router
- Familiarity with Tailwind CSS

## Setup

1. **Clone the repository** (if starting fresh):
```bash
git clone <repository-url>
cd <project-directory>
```

2. **Navigate to frontend directory**:
```bash
cd frontend
```

3. **Install dependencies**:
```bash
npm install
```

4. **Start the development server**:
```bash
npm run dev
```

5. **Access the application**:
Open http://localhost:3000 in your browser

## Frontend Skills Reference

### Modern Button Implementation
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
```

### Hero Section Structure
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
```

### Modern Card Component
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
```

### Layout Grid System
```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}
```

## Development Workflow

1. **Identify components to modernize** using the skills map:
   - Buttons → modern-button.skill.md
   - Cards → modern-card.skill.md
   - Landing page → hero-section.skill.md
   - Grids → layout-grid.skill.md

2. **Create a new branch** for your changes:
```bash
git checkout -b feature/001-frontend-modernization
```

3. **Update components incrementally**, testing each change:
```bash
npm run dev
```

4. **Verify functionality** remains intact after each update

5. **Commit changes** with descriptive messages:
```bash
git add .
git commit -m "feat: modernize task card component with modern-card.skill.md"
```

## Testing Guidelines

1. **Visual regression testing**: Compare before/after screenshots
2. **Responsiveness**: Test on multiple screen sizes
3. **Accessibility**: Verify keyboard navigation and screen reader compatibility
4. **Performance**: Ensure animations run smoothly (60fps target)
5. **Functionality**: Confirm all existing features still work as expected

## Environment Variables
Ensure the following are configured in your `.env.local`:
```
BACKEND_API_URL=http://localhost:8000
```

## Troubleshooting

**Issue**: Styles not applying correctly
**Solution**: Check Tailwind CSS configuration and ensure classes aren't being purged

**Issue**: Animations are janky
**Solution**: Reduce animation complexity or use CSS transforms for better performance

**Issue**: Responsive layouts broken
**Solution**: Verify media queries and grid/flexbox properties