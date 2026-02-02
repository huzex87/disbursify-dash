import React, { useEffect } from 'react';
import { TrendingUp, TrendingDown, Building2, Receipt, AlertCircle, ArrowUpRight } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent, Button } from '../components/ui';
import { useBusinessStore } from '../stores/businessStore';
import { useAuthStore } from '../stores/authStore';
import { formatCurrency, formatNumber } from '../utils/format';
import type { Business } from '../types';
import './Dashboard.css';

export const DashboardPage: React.FC = () => {
    const { businesses, summary, fetchBusinesses, isLoading } = useBusinessStore();
    const { currentOrganizationId } = useAuthStore();

    useEffect(() => {
        if (currentOrganizationId) {
            fetchBusinesses(currentOrganizationId);
        }
    }, [currentOrganizationId, fetchBusinesses]);

    return (
        <div className="dashboard">
            <div className="dashboard-header">
                <div>
                    <h1>Dashboard</h1>
                    <p>Welcome back! Here's an overview of your businesses.</p>
                </div>
                <Button leftIcon={<Building2 />}>Add Business</Button>
            </div>

            {/* Summary Cards */}
            <div className="dashboard-stats">
                <Card className="stat-card stat-card-primary">
                    <CardContent>
                        <div className="stat-icon">
                            <Building2 />
                        </div>
                        <div className="stat-content">
                            <span className="stat-label">Total Balance</span>
                            <span className="stat-value">{formatCurrency(summary?.total_balance || 0)}</span>
                            <div className="stat-change positive">
                                <TrendingUp />
                                <span>+12.5% from last month</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="stat-card">
                    <CardContent>
                        <div className="stat-icon stat-icon-success">
                            <TrendingUp />
                        </div>
                        <div className="stat-content">
                            <span className="stat-label">Total Income</span>
                            <span className="stat-value">{formatCurrency(2450000)}</span>
                            <span className="stat-subtext">This month</span>
                        </div>
                    </CardContent>
                </Card>

                <Card className="stat-card">
                    <CardContent>
                        <div className="stat-icon stat-icon-danger">
                            <TrendingDown />
                        </div>
                        <div className="stat-content">
                            <span className="stat-label">Total Expenses</span>
                            <span className="stat-value">{formatCurrency(890000)}</span>
                            <span className="stat-subtext">This month</span>
                        </div>
                    </CardContent>
                </Card>

                <Card className="stat-card">
                    <CardContent>
                        <div className="stat-icon stat-icon-info">
                            <Receipt />
                        </div>
                        <div className="stat-content">
                            <span className="stat-label">Transactions</span>
                            <span className="stat-value">{formatNumber(156)}</span>
                            <span className="stat-subtext">This month</span>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Main Content */}
            <div className="dashboard-grid">
                {/* Business Cards */}
                <Card className="dashboard-businesses">
                    <CardHeader action={<Button variant="ghost" size="sm">View All</Button>}>
                        <CardTitle subtitle={`${businesses.length} businesses`}>Your Businesses</CardTitle>
                    </CardHeader>
                    <CardContent>
                        {isLoading ? (
                            <div className="loading-skeleton">
                                {[1, 2, 3].map(i => (
                                    <div key={i} className="skeleton-card"></div>
                                ))}
                            </div>
                        ) : businesses.length === 0 ? (
                            <div className="empty-state">
                                <Building2 className="empty-icon" />
                                <h4>No businesses yet</h4>
                                <p>Add your first business to start tracking finances</p>
                                <Button size="sm">Add Business</Button>
                            </div>
                        ) : (
                            <div className="business-list">
                                {businesses.slice(0, 5).map((business: Business) => (
                                    <div key={business.id} className="business-item">
                                        <div
                                            className="business-avatar"
                                            style={{ backgroundColor: business.color }}
                                        >
                                            {business.name[0]}
                                        </div>
                                        <div className="business-info">
                                            <span className="business-name">{business.name}</span>
                                            <span className="business-industry">{business.industry}</span>
                                        </div>
                                        <div className="business-balance">
                                            <span className="balance-amount">
                                                {formatCurrency(business.current_balance)}
                                            </span>
                                            <span className="balance-label">Balance</span>
                                        </div>
                                        <Button variant="ghost" size="sm">
                                            <ArrowUpRight />
                                        </Button>
                                    </div>
                                ))}
                            </div>
                        )}
                    </CardContent>
                </Card>

                {/* Recent Transactions */}
                <Card className="dashboard-transactions">
                    <CardHeader action={<Button variant="ghost" size="sm">View All</Button>}>
                        <CardTitle subtitle="Last 7 days">Recent Transactions</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="transaction-list">
                            {/* Placeholder transactions */}
                            {[
                                { description: 'Payment from Client A', amount: 150000, type: 'income', date: 'Today' },
                                { description: 'Office Supplies', amount: -25000, type: 'expense', date: 'Today' },
                                { description: 'Sales Revenue', amount: 320000, type: 'income', date: 'Yesterday' },
                                { description: 'Utility Bills', amount: -45000, type: 'expense', date: 'Yesterday' },
                                { description: 'Consulting Fee', amount: 200000, type: 'income', date: '2 days ago' },
                            ].map((tx, i) => (
                                <div key={i} className="transaction-item">
                                    <div className={`transaction-icon ${tx.type}`}>
                                        {tx.type === 'income' ? <TrendingUp /> : <TrendingDown />}
                                    </div>
                                    <div className="transaction-info">
                                        <span className="transaction-desc">{tx.description}</span>
                                        <span className="transaction-date">{tx.date}</span>
                                    </div>
                                    <span className={`transaction-amount ${tx.type}`}>
                                        {tx.type === 'income' ? '+' : ''}{formatCurrency(tx.amount)}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>

                {/* Alerts */}
                <Card className="dashboard-alerts">
                    <CardHeader>
                        <CardTitle subtitle="Action needed">Alerts</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="alert-list">
                            <div className="alert-item warning">
                                <AlertCircle />
                                <div className="alert-content">
                                    <span className="alert-title">Low balance alert</span>
                                    <span className="alert-desc">Tech Solutions Ltd balance is below ₦50,000</span>
                                </div>
                            </div>
                            <div className="alert-item info">
                                <AlertCircle />
                                <div className="alert-content">
                                    <span className="alert-title">Bank sync pending</span>
                                    <span className="alert-desc">Main Business account needs reconnection</span>
                                </div>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};
