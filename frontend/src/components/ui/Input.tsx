import React, { forwardRef } from 'react';
import clsx from 'clsx';
import './Input.css';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    error?: string;
    hint?: string;
    leftIcon?: React.ReactNode;
    rightIcon?: React.ReactNode;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
    ({ label, error, hint, leftIcon, rightIcon, className, id, ...props }, ref) => {
        const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;

        return (
            <div className={clsx('input-wrapper', error && 'input-error', className)}>
                {label && (
                    <label htmlFor={inputId} className="input-label">
                        {label}
                    </label>
                )}
                <div className="input-container">
                    {leftIcon && <span className="input-icon input-icon-left">{leftIcon}</span>}
                    <input
                        ref={ref}
                        id={inputId}
                        className={clsx(
                            'input',
                            leftIcon && 'input-has-left-icon',
                            rightIcon && 'input-has-right-icon'
                        )}
                        {...props}
                    />
                    {rightIcon && <span className="input-icon input-icon-right">{rightIcon}</span>}
                </div>
                {error && <span className="input-error-text">{error}</span>}
                {hint && !error && <span className="input-hint">{hint}</span>}
            </div>
        );
    }
);

Input.displayName = 'Input';
