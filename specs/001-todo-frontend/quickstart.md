# Quickstart Guide: Todo Frontend Application

## Prerequisites
- Node.js 18.x or higher
- npm or yarn package manager
- Access to the backend API (FastAPI server)

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Environment Configuration
Create a `.env.local` file in the project root with the following variables:
```env
NEXT_PUBLIC_API_BASE_URL=<backend-api-base-url>
NEXT_PUBLIC_BETTER_AUTH_URL=<better-auth-url>
BETTER_AUTH_SECRET=<auth-secret>
NEXTAUTH_SECRET=<nextauth-secret> # if using nextauth as fallback
```

### 4. Run the Development Server
```bash
npm run dev
# or
yarn dev
```

The application will be available at http://localhost:3000

## Key Features

### Authentication
- Users can sign in/sign up using the Better Auth integration
- JWT tokens are managed automatically
- Protected routes redirect unauthenticated users to login

### Task Management
- Create tasks with title, description, due date, and priority
- View all tasks with visual priority indicators
- Filter and sort tasks by various criteria
- Update task details and completion status
- Delete tasks

### Eisenhower Matrix Visualization
- Tasks are visually categorized using color-coded badges:
  - Red: Urgent and Important
  - Orange: Urgent but Not Important
  - Yellow: Not Urgent but Important
  - Gray: Not Urgent and Not Important
- Completed tasks are visually distinct from pending tasks

## Project Structure
```
frontend/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Authentication-related pages
│   │   ├── sign-in/       # Login page
│   │   └── sign-up/       # Registration page
│   ├── dashboard/         # Main dashboard page
│   ├── tasks/             # Task management pages
│   │   ├── create/        # Create new task
│   │   ├── [id]/          # Individual task view/edit
│   │   └── layout.tsx     # Task section layout
│   ├── globals.css        # Global styles
│   └── layout.tsx         # Root layout
├── components/            # Reusable UI components
│   ├── auth/              # Authentication components
│   ├── tasks/             # Task-specific components
│   ├── ui/                # Generic UI primitives
│   └── providers/         # Context providers
├── lib/                   # Utility functions and services
│   ├── auth/              # Authentication utilities
│   ├── api/               # API service layer
│   └── utils/             # Helper functions
├── hooks/                 # Custom React hooks
└── types/                 # TypeScript type definitions
```

## API Integration
The application connects to the backend via the API service layer which handles:
- JWT token inclusion in all requests
- Error handling and status code interpretation
- Request/response transformation
- Automatic token refresh on expiration

## Development Commands
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter