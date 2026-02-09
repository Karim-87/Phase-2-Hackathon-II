---
id: 3
title: frontend-modernization-tasks
stage: tasks
date: 2026-01-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-frontend-modernization
branch: 001-frontend-modernization
user: Claude Sonnet
command: /sp.tasks
labels: [tasks, frontend, modernization, implementation]
links:
  spec: specs/001-frontend-modernization/spec.md
  plan: specs/001-frontend-modernization/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-frontend-modernization/tasks.md
tests:
  - specs/001-frontend-modernization/tasks.md
---

## Prompt

/sp.tasks Generate an implementation task list to upgrade the Next.js frontend using Frontend_Skills

Input:
- Existing Next.js frontend codebase
- Frontend skills located in .claude/skills/Frontend_Skills/*.md
- Upgrade plan defined in /sp.plan

Objectives:
- Break the frontend upgrade into small, safe, reversible tasks
- Ensure each task maps to exactly one Frontend_Skill
- Avoid any backend, API, or data-layer changes

Task Groups:

Task Group 1: Project & Component Audit
- Identify all page-level components (app/pages or app/router)
- Identify shared UI components (buttons, cards, layouts)
- Mark legacy or inconsistent UI patterns

Task Group 2: Core UI Component Upgrades
- Refactor primary and secondary buttons using modern-button skill
- Standardize CTA components and interaction states
- Replace legacy cards with modern-card components
- Normalize spacing, border radius, and shadows

Task Group 3: Page-Level Enhancements
- Upgrade homepage using hero-section skill
- Apply layout-grid skill to listing, dashboard, and collection pages
- Ensure consistent layout containers across pages

Task Group 4: Responsiveness & Accessibility
- Validate mobile, tablet, and desktop layouts
- Add keyboard navigation and focus indicators
- Add alt text and ARIA labels where required
- Verify contrast ratios for text and buttons

Task Group 5: Performance & Cleanup
- Remove unused CSS and redundant components
- Ensure animations are GPU-friendly and minimal
- Validate image optimization and lazy loading

Task Group 6: Verification & Documentation
- Verify no visual regressions or broken flows
- Cross-check success criteria from /sp.specify
- Document each change and the Frontend_Skill used

Constraints:
- One task should affect one logical UI area only
- Do not combine multiple skills in a single task
- Preserve existing business logic and data flow
- Avoid introducing new dependencies unless already present

Deliverables:
- Ordered task list suitable for /sp.implement
- Clear skill-to-task mapping
- Low-risk execution seque

## Response snapshot

Successfully generated comprehensive task list for frontend modernization. The tasks are organized into 6 phases:

1. **Phase 1**: Project Setup (4 tasks)
2. **Phase 2**: Foundational Updates (4 tasks)
3. **Phase 3**: [US1] Modernize UI Components (12 tasks) - P1 priority
4. **Phase 4**: [US2] Improve Responsiveness (6 tasks) - P2 priority
5. **Phase 5**: [US3] Enhance Accessibility (6 tasks) - P3 priority
6. **Phase 6**: Verification & Polish (8 tasks)

Key features of the task list:
- Each task follows the required format: `- [ ] T### [US#] Description with file path`
- Tasks are organized by user story priority (P1, P2, P3)
- Clear mapping between tasks and Frontend_Skills
- Independent test criteria defined for each user story
- Parallel execution opportunities identified
- MVP scope defined (US1 only)
- Risk mitigation through incremental delivery approach

The task list enables systematic application of Frontend_Skills:
- modern-button.skill.md → Tasks T020-T025 (buttons across pages)
- modern-card.skill.md → Task T030 (TaskCard component)
- layout-grid.skill.md → Tasks T011, T031 (layouts and grids)
- hero-section.skill.md → Task T032 (dashboard header)

## Outcome

- ✅ Impact: Created complete, ordered task list for frontend modernization implementation
- 🧪 Tests: Tasks organized for safe, incremental delivery with independent verification
- 📁 Files: Generated tasks.md with proper phase structure and skill mapping
- 🔁 Next prompts: Ready for implementation with /sp.implement
- 🧠 Reflection: Tasks follow checklist format and enable parallel execution where appropriate

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to implementation phase