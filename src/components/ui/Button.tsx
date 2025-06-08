import React from 'react';
import { cn } from '../../lib/utils';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  asChild?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', asChild = false, children, ...props }, ref) => {
    if (asChild && React.isValidElement(children)) {
      return React.cloneElement(children as React.ReactElement<any>, {
        className: cn(
          'inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
          {
            'bg-blue-500 text-white hover:bg-blue-600 focus-visible:ring-blue-500': variant === 'primary',
            'border border-gray-200 bg-white hover:bg-gray-100 focus-visible:ring-gray-500': variant === 'secondary',
            'bg-red-500 text-white hover:bg-red-600 focus-visible:ring-red-500': variant === 'danger',
            'border border-gray-300 bg-white text-gray-700 hover:bg-gray-100 focus-visible:ring-gray-500': variant === 'outline',
            'h-8 px-3 text-sm': size === 'sm',
            'h-10 px-4 text-base': size === 'md',
            'h-12 px-6 text-lg': size === 'lg',
          },
          className,
          (children as React.ReactElement<any>).props.className
        ),
        ...props
      });
    }
    
    return (
      <button
        ref={ref}
        className={cn(
          'inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
          {
            'bg-blue-500 text-white hover:bg-blue-600 focus-visible:ring-blue-500': variant === 'primary',
            'border border-gray-200 bg-white hover:bg-gray-100 focus-visible:ring-gray-500': variant === 'secondary',
            'bg-red-500 text-white hover:bg-red-600 focus-visible:ring-red-500': variant === 'danger',
            'border border-gray-300 bg-white text-gray-700 hover:bg-gray-100 focus-visible:ring-gray-500': variant === 'outline',
            'h-8 px-3 text-sm': size === 'sm',
            'h-10 px-4 text-base': size === 'md',
            'h-12 px-6 text-lg': size === 'lg',
          },
          className
        )}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';