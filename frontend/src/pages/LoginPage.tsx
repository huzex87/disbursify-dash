import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Mail, Lock, Eye, EyeOff } from 'lucide-react';
import { Button, Input } from '../components/ui';
import { useAuthStore } from '../stores/authStore';
import logo from '../assets/logo-premium.png';
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
                            <img src={logo} alt="Dash" className="premium-logo-glow" style={{ width: '120px', height: 'auto', marginBottom: 'var(--space-8)' }} />
                        </div>
                        <h1 className="auth-brand-title">Dash</h1>
                        <p className="auth-brand-tagline">The future of portfolio entrepreneurship.</p>

                        <div className="auth-features">
                            <div className="auth-feature-premium">
                                <div className="feature-dot"></div>
                                <span>Real-time Financial Intelligence</span>
                            </div>
                            <div className="auth-feature-premium">
                                <div className="feature-dot"></div>
                                <span>Multi-Business Unified Control</span>
                            </div>
                            <div className="auth-feature-premium">
                                <div className="feature-dot"></div>
                                <span>Institutional-Grade Security</span>
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
