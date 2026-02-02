import React from 'react';
import clsx from 'clsx';
import './Card.css';

interface CardProps {
    children: React.ReactNode;
    className?: string;
    variant?: 'default' | 'outlined' | 'elevated';
    padding?: 'none' | 'sm' | 'md' | 'lg';
    onClick?: () => void;
    as?: 'div' | 'article' | 'section';
}

export const Card: React.FC<CardProps> = ({
    children,
    className,
    variant = 'default',
    padding = 'md',
    onClick,
    as: Component = 'div',
}) => {
    return (
        <Component
            className={clsx(
                'card',
                `card-${variant}`,
                `card-p-${padding}`,
                onClick && 'card-clickable',
                className
            )}
            onClick={onClick}
        >
            {children}
        </Component>
    );
};

interface CardHeaderProps {
    children: React.ReactNode;
    className?: string;
    action?: React.ReactNode;
}

export const CardHeader: React.FC<CardHeaderProps> = ({ children, className, action }) => (
    <div className={clsx('card-header', className)}>
        <div className="card-header-content">{children}</div>
        {action && <div className="card-header-action">{action}</div>}
    </div>
);

interface CardTitleProps {
    children: React.ReactNode;
    className?: string;
    subtitle?: React.ReactNode;
}

export const CardTitle: React.FC<CardTitleProps> = ({ children, className, subtitle }) => (
    <div className={clsx('card-title-wrapper', className)}>
        <h3 className="card-title">{children}</h3>
        {subtitle && <p className="card-subtitle">{subtitle}</p>}
    </div>
);

export const CardContent: React.FC<{ children: React.ReactNode; className?: string }> = ({
    children,
    className,
}) => <div className={clsx('card-content', className)}>{children}</div>;

export const CardFooter: React.FC<{ children: React.ReactNode; className?: string }> = ({
    children,
    className,
}) => <div className={clsx('card-footer', className)}>{children}</div>;
