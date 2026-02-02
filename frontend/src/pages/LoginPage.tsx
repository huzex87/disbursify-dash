import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Mail, Lock, Eye, EyeOff } from 'lucide-react';
import { Button, Input } from '../components/ui';
import { useAuthStore } from '../stores/authStore';
import './Auth.css';

const loginSchema = z.object({
    email: z.string().email('Please enter a valid email'),
    password: z.string().min(1, 'Password is required'),
    remember_me: z.boolean().optional(),
});

type LoginFormData = z.infer<typeof loginSchema>;

export const LoginPage: React.FC = () => {
    const navigate = useNavigate();
    const { login, isLoading } = useAuthStore();
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState('');

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<LoginFormData>({
        resolver: zodResolver(loginSchema),
    });

    const onSubmit = async (data: LoginFormData) => {
        setError('');
        try {
            await login(data.email, data.password, data.remember_me);
            navigate('/dashboard');
        } catch (err: any) {
            setError(err.response?.data?.error?.message || 'Login failed. Please try again.');
        }
    };

    return (
        <div className="auth-page">
            <div className="auth-container">
                {/* Left side - Branding */}
                <div className="auth-branding">
                    <div className="auth-branding-content">
                        <div className="auth-logo">
                            <svg viewBox="0 0 60 60" fill="none">
                                <rect width="60" height="60" rx="16" fill="url(#auth-logo-gradient)" />
                                <path d="M18 30L27 39L42 21" stroke="white" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
                                <defs>
                                    <linearGradient id="auth-logo-gradient" x1="0" y1="0" x2="60" y2="60" gradientUnits="userSpaceOnUse">
                                        <stop stopColor="#A855F7" />
                                        <stop offset="1" stopColor="#6B21A8" />
                                    </linearGradient>
                                </defs>
                            </svg>
                        </div>
                        <h1 className="auth-brand-title">Disbursify Dash</h1>
                        <p className="auth-brand-tagline">One Dashboard. All Your Businesses.</p>

                        <div className="auth-features">
                            <div className="auth-feature">
                                <span className="auth-feature-icon">📊</span>
                                <span>Track all your businesses in one place</span>
                            </div>
                            <div className="auth-feature">
                                <span className="auth-feature-icon">🔒</span>
                                <span>Bank-grade security with encryption</span>
                            </div>
                            <div className="auth-feature">
                                <span className="auth-feature-icon">⚡</span>
                                <span>Real-time financial insights</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right side - Login form */}
                <div className="auth-form-container">
                    <div className="auth-form-wrapper">
                        <div className="auth-form-header">
                            <h2>Welcome back</h2>
                            <p>Sign in to continue to your dashboard</p>
                        </div>

                        {error && (
                            <div className="auth-error">
                                {error}
                            </div>
                        )}

                        <form onSubmit={handleSubmit(onSubmit)} className="auth-form">
                            <Input
                                label="Email"
                                type="email"
                                placeholder="you@example.com"
                                leftIcon={<Mail />}
                                error={errors.email?.message}
                                {...register('email')}
                            />

                            <Input
                                label="Password"
                                type={showPassword ? 'text' : 'password'}
                                placeholder="Enter your password"
                                leftIcon={<Lock />}
                                rightIcon={
                                    <button
                                        type="button"
                                        className="password-toggle"
                                        onClick={() => setShowPassword(!showPassword)}
                                    >
                                        {showPassword ? <EyeOff /> : <Eye />}
                                    </button>
                                }
                                error={errors.password?.message}
                                {...register('password')}
                            />

                            <div className="auth-form-options">
                                <label className="auth-checkbox">
                                    <input type="checkbox" {...register('remember_me')} />
                                    <span>Remember me</span>
                                </label>
                                <Link to="/forgot-password" className="auth-link">
                                    Forgot password?
                                </Link>
                            </div>

                            <Button type="submit" fullWidth isLoading={isLoading}>
                                Sign In
                            </Button>
                        </form>

                        <p className="auth-footer-text">
                            Don't have an account?{' '}
                            <Link to="/register" className="auth-link">
                                Create one now
                            </Link>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};
