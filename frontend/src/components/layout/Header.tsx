import React from 'react';
import { Bell, Search, Plus, ChevronDown } from 'lucide-react';
import { useAuthStore } from '../../stores/authStore';
import { Button } from '../ui/Button';
import './Header.css';

export const Header: React.FC = () => {
    const { organizations, currentOrganizationId } = useAuthStore();

    const currentOrg = organizations.find(o => o.id === currentOrganizationId);

    return (
        <header className="header">
            <div className="header-left">
                {/* Organization Switcher */}
                <div className="org-switcher">
                    <button className="org-switcher-btn">
                        <div className="org-avatar">
                            {currentOrg?.name?.[0]?.toUpperCase() || 'O'}
                        </div>
                        <span className="org-name">{currentOrg?.name || 'Select Organization'}</span>
                        <ChevronDown className="org-chevron" />
                    </button>

                    {/* Dropdown would go here */}
                </div>
            </div>

            <div className="header-center">
                <div className="search-bar">
                    <Search className="search-icon" />
                    <input
                        type="text"
                        placeholder="Search transactions, businesses..."
                        className="search-input"
                    />
                    <kbd className="search-shortcut">⌘K</kbd>
                </div>
            </div>

            <div className="header-right">
                <Button variant="primary" size="sm" leftIcon={<Plus />}>
                    Add Transaction
                </Button>

                <button className="header-icon-btn notification-btn">
                    <Bell />
                    <span className="notification-badge">3</span>
                </button>
            </div>
        </header>
    );
};
