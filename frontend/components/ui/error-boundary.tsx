'use client';

import { Component, ReactNode } from 'react';
import ModernButton from './modern-button';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onReset?: () => void;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(_error: Error, _errorInfo: React.ErrorInfo) {
    // Error captured in state via getDerivedStateFromError — no logging of potentially sensitive data
  }

  handleReset = () => {
    this.setState({ hasError: false, error: undefined });
    this.props.onReset?.();
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="flex flex-col items-center justify-center min-h-[60vh] p-6 text-center">
          <div className="w-16 h-16 mb-6 rounded-full bg-[rgba(var(--danger),0.15)] border border-[rgba(var(--danger),0.3)] flex items-center justify-center">
            <span className="text-3xl text-red-400">!</span>
          </div>
          <h2 className="text-xl font-semibold text-[rgb(var(--text-primary))] mb-2">
            Something went wrong
          </h2>
          <p className="text-sm text-[rgb(var(--text-secondary))] mb-6 max-w-md">
            An unexpected error occurred. Please try again or refresh the page.
          </p>
          <ModernButton variant="primary" onClick={this.handleReset}>
            Try again
          </ModernButton>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
