/**
 * Formatting utilities for Disbursify Dash
 */

/**
 * Format amount as Nigerian Naira currency
 */
export function formatCurrency(
    amount: number,
    options?: {
        currency?: string;
        showSign?: boolean;
        compact?: boolean;
    }
): string {
    const { currency = 'NGN', showSign = false, compact = false } = options || {};

    const absAmount = Math.abs(amount);

    const formatter = new Intl.NumberFormat('en-NG', {
        style: 'currency',
        currency,
        minimumFractionDigits: 0,
        maximumFractionDigits: compact ? 0 : 2,
        notation: compact ? 'compact' : 'standard',
    });

    const formatted = formatter.format(absAmount);

    if (showSign && amount > 0) {
        return '+' + formatted;
    }

    return amount < 0 ? '-' + formatted.replace('-', '') : formatted;
}

/**
 * Format number with thousand separators
 */
export function formatNumber(
    value: number,
    options?: {
        decimals?: number;
        compact?: boolean;
    }
): string {
    const { decimals = 0, compact = false } = options || {};

    return new Intl.NumberFormat('en-NG', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals,
        notation: compact ? 'compact' : 'standard',
    }).format(value);
}

/**
 * Format date for display
 */
export function formatDate(
    date: string | Date,
    format: 'short' | 'long' | 'relative' = 'short'
): string {
    const d = typeof date === 'string' ? new Date(date) : date;

    if (format === 'relative') {
        const now = new Date();
        const diffMs = now.getTime() - d.getTime();
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

        if (diffDays === 0) return 'Today';
        if (diffDays === 1) return 'Yesterday';
        if (diffDays < 7) return `${diffDays} days ago`;
        if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;

        return d.toLocaleDateString('en-NG', { month: 'short', day: 'numeric' });
    }

    if (format === 'long') {
        return d.toLocaleDateString('en-NG', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
        });
    }

    return d.toLocaleDateString('en-NG', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    });
}

/**
 * Format percentage
 */
export function formatPercent(value: number, decimals = 1): string {
    return new Intl.NumberFormat('en-NG', {
        style: 'percent',
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals,
    }).format(value / 100);
}

/**
 * Truncate text with ellipsis
 */
export function truncate(text: string, maxLength: number): string {
    if (text.length <= maxLength) return text;
    return text.slice(0, maxLength - 3) + '...';
}

/**
 * Generate initials from name
 */
export function getInitials(name: string): string {
    return name
        .split(' ')
        .map(part => part[0])
        .join('')
        .toUpperCase()
        .slice(0, 2);
}

/**
 * Generate random color for business avatars
 */
export function generateColor(seed: string): string {
    const colors = [
        '#6B21A8', // primary purple
        '#3B82F6', // blue
        '#10B981', // green
        '#F59E0B', // amber
        '#EF4444', // red
        '#8B5CF6', // violet
        '#EC4899', // pink
        '#06B6D4', // cyan
    ];

    let hash = 0;
    for (let i = 0; i < seed.length; i++) {
        hash = seed.charCodeAt(i) + ((hash << 5) - hash);
    }

    return colors[Math.abs(hash) % colors.length];
}
