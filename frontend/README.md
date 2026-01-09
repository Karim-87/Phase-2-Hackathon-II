# Todo Frontend Application

A multi-user todo application with Eisenhower Matrix prioritization built with Next.js 16, TypeScript, and Tailwind CSS.

## Features

- User authentication and authorization
- Create, read, update, and delete tasks
- Eisenhower Matrix priority visualization
- Task filtering and sorting
- Responsive design for mobile and desktop
- JWT-based authentication

## Tech Stack

- Next.js 16 with App Router
- TypeScript
- Tailwind CSS for styling
- Better Auth for authentication
- SWR for data fetching
- React Hooks for state management

## Getting Started

### Prerequisites

- Node.js 18.x or higher
- npm or yarn package manager
- Access to the backend API (FastAPI server)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

3. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

4. Create a `.env.local` file in the frontend directory with the following variables:
   ```env
   NEXT_PUBLIC_API_BASE_URL=<backend-api-base-url>
   NEXT_PUBLIC_BETTER_AUTH_URL=<better-auth-url>
   ```

### Running the Development Server

```bash
npm run dev
# or
yarn dev
```

The application will be available at http://localhost:3000

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Base URL for the authentication service

## Scripts

- `npm run dev`: Start the development server
- `npm run build`: Build the application for production
- `npm run start`: Start the production server
- `npm run lint`: Run the linter

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

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request