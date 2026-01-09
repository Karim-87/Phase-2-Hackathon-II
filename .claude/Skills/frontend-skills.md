# Frontend Sub-Agent Skills  
**Multi-User Todo Web Application**  
**Last Updated:** January 2026

## Role of Frontend Sub-Agent
Responsible for building the complete Next.js 16+ (App Router) frontend including:
- Responsive UI/UX
- Authentication screens (signup / signin)
- Task CRUD interface
- Task list with filtering & sorting
- Priority visualization (Eisenhower matrix style)
- API integration with FastAPI backend using JWT

**Strict Rule:** All code & components MUST follow `spec_constitution.md`

## Available Skills (Tool-like Capabilities)

These are the modular "skills" the Frontend Sub-Agent should use when generating code via Claude prompts.

| Skill Name              | Description                                                                                       | When to Use                                                                                     | Output Examples                                      |
|-------------------------|---------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|------------------------------------------------------|
| `GenerateComponent`     | Creates a complete React Server/Client Component with proper types, props, and Tailwind styling | Building any UI piece: form, card, list item, modal, header, etc.                              | TaskCard.tsx, TaskForm.tsx, PriorityBadge.tsx        |
| `ApiIntegration`        | Generates fetch/axios functions or hooks that call backend API with JWT Authorization header     | Any interaction with backend (CRUD, fetch tasks, toggle complete)                              | useTasks.ts, api/tasks.ts, fetchWithAuth()           |
| `ResponsiveDesign`      | Applies Tailwind responsive classes (sm:, md:, lg:) + mobile-first approach                      | Every visual component, layout, grid, flex system                                               | Task list grid, form layout, navbar                  |
| `StateManagement`       | Implements state/logic using React hooks (useState, useEffect, useContext) or Zustand if needed | Managing tasks list, filters, form state, auth state                                            | TaskContext.tsx, useTaskFilter.ts                    |
| `AuthUI`                | Builds signup/signin forms + handles Better Auth session & JWT storage                            | Login page, protected routes, logout button                                                     | LoginForm.tsx, AuthProvider.tsx                      |
| `PriorityVisualization` | Creates visual representation of task priority (badges, colors, Eisenhower matrix quadrants)     | Task cards, filter dropdown, priority selector                                                  | PrioritySelector.tsx, EisenhowerMatrixLegend.tsx     |
| `FormHandling`          | Builds controlled forms with validation (optional zod + react-hook-form)                         | Task create/update form (title, desc, datetime, priority)                                      | TaskCreateForm.tsx                                   |
| `FilterAndSortUI`       | Generates filter controls (by priority, completion, due date) + sorting options                   | Task list header section                                                                        | TaskFilters.tsx, SortDropdown.tsx                    |
| `LayoutStructure`       | Creates main app layout (navbar, sidebar, main content, responsive mobile menu)                  | Root layout, dashboard page                                                                     | DashboardLayout.tsx, Navbar.tsx                      |
| `ProtectedRoute`        | Implements client-side route protection using Better Auth session                                 | Redirect to login if not authenticated                                                          | ProtectedRoute.tsx or middleware pattern             |
| `ErrorHandlingUI`       | Shows user-friendly error messages, loading states, empty states, toasts                          | API errors, no tasks, loading task list                                                         | ErrorMessage.tsx, LoadingSpinner.tsx, EmptyState.tsx |
| `TailwindUtility`       | Quickly generates consistent Tailwind class strings for common patterns                           | Buttons, cards, inputs, alerts, badges                                                          | buttonVariants(), cardStyles()                       |

## Recommended Technology Choices (Frontend)

- Framework: Next.js 16+ (App Router)
- Styling: Tailwind CSS (included by default in create-next-app)
- Authentication: Better Auth (with JWT plugin)
- Data Fetching: Native fetch + React Server Components where possible
- Forms: react-hook-form + zod (optional but recommended)
- State: React Context + useReducer or Zustand (for complex cases)
- Icons: lucide-react
- Date/Time: date-fns or luxon
- Toasts: sonner or react-hot-toast

## Priority Color Scheme (Consistency Rule)

Use these colors across the entire app:

```ts
const priorityColors = {
  urgent_important:     "bg-red-600 text-white",        // Do First
  urgent_not_important: "bg-orange-500 text-white",     // Do Soon
  not_urgent_important: "bg-blue-600 text-white",       // Schedule
  not_urgent_not_important: "bg-gray-500 text-white",   // Delegate / Eliminate
};