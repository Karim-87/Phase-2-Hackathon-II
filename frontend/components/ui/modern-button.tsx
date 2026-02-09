import React from 'react';

interface ModernButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'success' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  isLoading?: boolean;
  onClick?: () => void;
  className?: string;
  type?: 'button' | 'submit' | 'reset';
}

const ModernButton: React.FC<ModernButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  isLoading = false,
  onClick,
  className = '',
  type = 'button',
}) => {
  // Base glassmorphism styles
  const baseClasses = `
    glass-button
    relative
    overflow-hidden
    border
    transition-all
    duration-300
    ease-in-out
    transform
    focus:outline-none
    focus:ring-2
    focus:ring-offset-2
    disabled:opacity-50
    disabled:cursor-not-allowed
  `;

  // Size variants
  const sizeClasses = {
    sm: 'px-3 py-2 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  // Variant styles — solid colors for visibility
  const variantClasses = {
    primary: `
    
      bg-indigo-700
      border-indigo-700
      text-black
      hover:bg-indigo-700
      focus:ring-indigo-500
    `,
    secondary: `
      bg-gray-200
      border-gray-300
      text-gray-800
      hover:bg-gray-300
      focus:ring-gray-400
    `,
    success: `
      bg-emerald-600
      border-emerald-700
      text-white
      hover:bg-emerald-700
      focus:ring-emerald-500
    `,
    danger: `
      bg-red-600
      border-red-700
      text-white
      hover:bg-red-700
      focus:ring-red-500
    `,
  };

  const isDisabled = disabled || isLoading;
  const classes = `${baseClasses} ${sizeClasses[size]} ${variantClasses[variant]} ${isLoading ? 'opacity-70' : ''} ${className}`;

  return (
    <button
      type={type}
      className={classes}
      onClick={onClick}
      disabled={isDisabled}
      style={{
        borderRadius: 'var(--radius-lg)',
      }}
      aria-disabled={isDisabled}
    >
      {isLoading && (
        <span className="inline-block animate-spin rounded-full h-4 w-4 border-2 border-current border-b-transparent mr-2 align-middle" />
      )}
      {children}
    </button>
  );
};

export default ModernButton;