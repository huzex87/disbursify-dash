import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
    LayoutDashboard,
    Building2,
    Receipt,
    BarChart3,
    Bell,
    Settings,
    LogOut,
    ChevronLeft,
    Users
} from 'lucide-react';
import { useAuthStore } from '../../stores/authStore';
import logo from '../../assets/logo-premium.png';
import './Sidebar.css';

interface SidebarProps {
    isCollapsed: boolean;
    onToggle: () => void;
}

const navItems = [
    { path: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/businesses', icon: Building2, label: 'Businesses' },
    { path: '/transactions', icon: Receipt, label: 'Transactions' },
    { path: '/reports', icon: BarChart3, label: 'Reports' },
    { path: '/team', icon: Users, label: 'Team' },
    { path: '/alerts', icon: Bell, label: 'Alerts' },
];

export const Sidebar: React.FC<SidebarProps> = ({ isCollapsed, onToggle }) => {
    const navigate = useNavigate();
    const { user, logout } = useAuthStore();

    const handleLogout = async () => {
        await logout();
        navigate('/login');
    };

    return (
        <aside className={`sidebar ${isCollapsed ? 'sidebar-collapsed' : ''}`}>
            {/* Logo */}
            <div className="sidebar-header">
                <div className="sidebar-logo">
                    <div className="logo-icon">
                        <img src={logo} alt="Logo" style={{ width: isCollapsed ? '32px' : '40px', transition: 'width 0.3s' }} />
                    </div>
                    {!isCollapsed && (
                        <div className="logo-text">
                            <span className="logo-brand">Dash</span>
                        </div>
                    )}
                </div>
                <button className="sidebar-toggle" onClick={onToggle} aria-label="Toggle sidebar">
                    <ChevronLeft />
                </button>
            </div>

            {/* Navigation */}
            <nav className="sidebar-nav">
                <ul className="nav-list">
                    {navItems.map(({ path, icon: Icon, label }) => (
                        <li key={path}>
                            <NavLink
                                to={path}
                                className={({ isActive }) => `nav-link ${isActive ? 'nav-link-active' : ''}`}
                            >
                                <Icon className="nav-icon" />
                                {!isCollapsed && <span className="nav-label">{label}</span>}
                            </NavLink>
                        </li>
                    ))}
                </ul>
            </nav>

            {/* Footer */}
            <div className="sidebar-footer">
                <NavLink to="/settings" className="nav-link">
                    <Settings className="nav-icon" />
                    {!isCollapsed && <span className="nav-label">Settings</span>}
                </NavLink>

                <div className="sidebar-user">
                    <div className="user-avatar">
                        {user?.avatar_url ? (
                            <img src={user.avatar_url} alt={user.full_name} />
                        ) : (
                            <span>{user?.first_name?.[0] || user?.email?.[0].toUpperCase()}</span>
                        )}
                    </div>
                    {!isCollapsed && (
                        <div className="user-info">
                            <span className="user-name">{user?.full_name || user?.email}</span>
                            <span className="user-role">Admin</span>
                        </div>
                    )}
                </div>

                <button className="nav-link logout-btn" onClick={handleLogout}>
                    <LogOut className="nav-icon" />
                    {!isCollapsed && <span className="nav-label">Logout</span>}
                </button>
            </div>
        </aside>
    );
};
