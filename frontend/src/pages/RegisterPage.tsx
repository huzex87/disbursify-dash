import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Mail, Lock, Eye, EyeOff, User, Phone } from 'lucide-react';
import { Button, Input } from '../components/ui';
import { useAuthStore } from '../stores/authStore';
import './Auth.css';

const registerSchema = z.object({
    first_name: z.string().min(2, 'First name is required'),
    last_name: z.string().min(2, 'Last name is required'),
    email: z.string().email('Please enter a valid email'),
    phone: z.string().optional(),
    password: z.string().min(8, 'Password must be at least 8 characters'),
    password_confirm: z.string(),
    terms: z.boolean().refine(val => val === true, 'You must accept the terms'),
}).refine(data => data.password === data.password_confirm, {
    message: "Passwords don't match",
    path: ['password_confirm'],
});

type RegisterFormData = z.infer<typeof registerSchema>;

export const RegisterPage: React.FC = () => {
    const navigate = useNavigate();
    const { register: registerUser, isLoading } = useAuthStore();
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState('');

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<RegisterFormData>({
        resolver: zodResolver(registerSchema),
    });

    const onSubmit = async (data: RegisterFormData) => {
        setError('');
        try {
            await registerUser({
                email: data.email,
                password: data.password,
                password_confirm: data.password_confirm,
                first_name: data.first_name,
                last_name: data.last_name,
            });
            navigate('/login', { state: { registered: true } });
        } catch (err: any) {
            setError(err.response?.data?.error?.message || 'Registration failed. Please try again.');
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

                        <div className="auth-stats">
                            <div className="auth-stat">
                                <span className="auth-stat-value">10,000+</span>
                                <span className="auth-stat-label">Businesses Managed</span>
                            </div>
                            <div className="auth-stat">
                                <span className="auth-stat-value">₦50B+</span>
                                <span className="auth-stat-label">Transactions Tracked</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right side - Register form */}
                <div className="auth-form-container">
                    <div className="auth-form-wrapper">
                        <div className="auth-form-header">
                            <h2>Create your account</h2>
                            <p>Start your 14-day free trial</p>
                        </div>

                        {error && (
                            <div className="auth-error">
                                {error}
                            </div>
                        )}

                        <form onSubmit={handleSubmit(onSubmit)} className="auth-form">
                            <div className="auth-form-row">
                                <Input
                                    label="First Name"
                                    placeholder="John"
                                    leftIcon={<User />}
                                    error={errors.first_name?.message}
                                    {...register('first_name')}
                                />
                                <Input
                                    label="Last Name"
                                    placeholder="Doe"
                                    error={errors.last_name?.message}
                                    {...register('last_name')}
                                />
                            </div>

                            <Input
                                label="Email"
                                type="email"
                                placeholder="you@example.com"
                                leftIcon={<Mail />}
                                error={errors.email?.message}
                                {...register('email')}
                            />

                            <Input
                                label="Phone (Optional)"
                                type="tel"
                                placeholder="+234 800 000 0000"
                                leftIcon={<Phone />}
                                {...register('phone')}
                            />

                            <Input
                                label="Password"
                                type={showPassword ? 'text' : 'password'}
                                placeholder="Min 8 characters"
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

                            <Input
                                label="Confirm Password"
                                type={showPassword ? 'text' : 'password'}
                                placeholder="Confirm your password"
                                leftIcon={<Lock />}
                                error={errors.password_confirm?.message}
                                {...register('password_confirm')}
                            />

                            <label className="auth-checkbox">
                                <input type="checkbox" {...register('terms')} />
                                <span>
                                    I agree to the{' '}
                                    <a href="/terms" target="_blank" className="auth-link">Terms of Service</a>
                                    {' '}and{' '}
                                    <a href="/privacy" target="_blank" className="auth-link">Privacy Policy</a>
                                </span>
                            </label>
                            {errors.terms && (
                                <span className="auth-field-error">{errors.terms.message}</span>
                            )}

                            <Button type="submit" fullWidth isLoading={isLoading}>
                                Create Account
                            </Button>
                        </form>

                        <p className="auth-footer-text">
                            Already have an account?{' '}
                            <Link to="/login" className="auth-link">
                                Sign in
                            </Link>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};
