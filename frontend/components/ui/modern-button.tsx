import React from 'react';

interface ModernButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'success' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  className?: string;
  type?: 'button' | 'submit' | 'reset';
}

const ModernButton: React.FC<ModernButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
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

  // Variant styles based on design tokens
  const variantClasses = {
    primary: `
      bg-[rgba(var(--primary),0.2)]
      border-[rgba(var(--primary),0.3)]
      text-white
      backdrop-blur-md
      hover:bg-[rgba(var(--primary),0.3)]
      hover:border-[rgba(var(--primary),0.4)]
      focus:ring-[rgba(var(--primary),0.5)]
    `,
    secondary: `
      bg-[rgba(var(--secondary),0.2)]
      border-[rgba(var(--border),0.3)]
      text-[rgb(var(--text-primary))]
      backdrop-blur-md
      hover:bg-[rgba(var(--secondary-hover),0.3)]
      hover:border-[rgba(var(--border),0.4)]
      focus:ring-[rgba(var(--primary),0.5)]
    `,
    success: `
      bg-[rgba(var(--success),0.2)]
      border-[rgba(var(--success),0.3)]
      text-white
      backdrop-blur-md
      hover:bg-[rgba(var(--success),0.3)]
      hover:border-[rgba(var(--success),0.4)]
      focus:ring-[rgba(var(--success),0.5)]
    `,
    danger: `
      bg-[rgba(var(--danger),0.2)]
      border-[rgba(var(--danger),0.3)]
      text-white
      backdrop-blur-md
      hover:bg-[rgba(var(--danger),0.3)]
      hover:border-[rgba(var(--danger),0.4)]
      focus:ring-[rgba(var(--danger),0.5)]
    `,
  };

  const classes = `${baseClasses} ${sizeClasses[size]} ${variantClasses[variant]} ${className}`;

  return (
    <button
      type={type}
      className={classes}
      onClick={onClick}
      disabled={disabled}
      style={{
        borderRadius: 'var(--radius-lg)',
      }}
      aria-disabled={disabled}
    >
      {children}
    </button>
  );
};

export default ModernButton;