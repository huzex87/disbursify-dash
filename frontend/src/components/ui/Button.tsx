import React from 'react';
import clsx from 'clsx';
import './Button.css';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
    size?: 'sm' | 'md' | 'lg';
    isLoading?: boolean;
    leftIcon?: React.ReactNode;
    rightIcon?: React.ReactNode;
    fullWidth?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
    children,
    variant = 'primary',
    size = 'md',
    isLoading = false,
    leftIcon,
    rightIcon,
    fullWidth = false,
    disabled,
    className,
    ...props
}) => {
    return (
        <button
            className={clsx(
                'btn',
                `btn-${variant}`,
                `btn-${size}`,
                fullWidth && 'btn-full',
                isLoading && 'btn-loading',
                className
            )}
            disabled={disabled || isLoading}
            {...props}
        >
            {isLoading && (
                <svg className="btn-spinner" viewBox="0 0 24 24">
                    <circle
                        className="spinner-track"
                        cx="12"
                        cy="12"
                        r="10"
                        fill="none"
                        strokeWidth="3"
                    />
                    <circle
                        className="spinner-head"
                        cx="12"
                        cy="12"
                        r="10"
                        fill="none"
                        strokeWidth="3"
                    />
                </svg>
            )}
            {!isLoading && leftIcon && <span className="btn-icon btn-icon-left">{leftIcon}</span>}
            <span className="btn-text">{children}</span>
            {!isLoading && rightIcon && <span className="btn-icon btn-icon-right">{rightIcon}</span>}
        </button>
    );
};
