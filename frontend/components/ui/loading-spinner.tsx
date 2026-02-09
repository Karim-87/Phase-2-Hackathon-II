interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  color?: string;
}

const sizeClasses = {
  sm: 'h-4 w-4 border-[2px]',
  md: 'h-8 w-8 border-[2px]',
  lg: 'h-12 w-12 border-[3px]',
};

export function LoadingSpinner({ size = 'md', color = 'blue-600' }: LoadingSpinnerProps) {
  return (
    <div className="flex justify-center items-center">
      <div
        className={`animate-spin rounded-full border-b-transparent ${sizeClasses[size]} border-${color}`}
        role="status"
        aria-label="Loading"
      />
    </div>
  );
}

export default LoadingSpinner;
