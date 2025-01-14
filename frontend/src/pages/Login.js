import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState(null);

    const handleLogin = async (e) => {
        e.preventDefault();
        setError(null);
        setSuccessMessage(null);
        setLoading(true);
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/auth/login/', {
                username,
                password,
            });

            const tokenResponse = await axios.post('http://127.0.0.1:8000/api/auth/token/', {
                username,
                password,
            })

            // Store tokens in localStorage
            localStorage.setItem('access_token', tokenResponse.data.access);
            localStorage.setItem('refresh_token', tokenResponse.data.refresh);

            const tokenPayload = JSON.parse(atob(tokenResponse.data.access.split('.')[1]))
            console.log(tokenPayload);
            localStorage.setItem('id', tokenPayload.id);
            localStorage.setItem('username', tokenPayload.username);
            localStorage.setItem('email', tokenPayload.email);
            localStorage.setItem('user_type', tokenPayload.user_type);

            setSuccessMessage('Login succesful')
            navigate('/dashboard');
        } catch (error) {
            console.error('Login failed:', error.response?.data || error.message);
            setError(`Login failed: ${error.response.data.error}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <div className="card">
                        <div className="card-body">
                            <h1 className="card-title text-center">Login</h1>
                            {
                                error && (
                                    <div className="alert alert-danger" role="alert">
                                        {error}
                                    </div>
                                )
                            }
                            {
                                successMessage && (
                                    <div className="alert alert-danger" role="alert">
                                        {successMessage}
                                    </div>
                                )
                            }
                            <form onSubmit={handleLogin}>
                                <div className="mb-3">
                                    <label className="form-label">Username</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        placeholder="Enter your username"
                                        value={username}
                                        onChange={(e) => setUsername(e.target.value)}
                                    />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Password</label>
                                    <input
                                        type="password"
                                        className="form-control"
                                        placeholder="Enter your password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                    />
                                </div>
                                <div className="d-grid">
                                    <button type="submit" className="btn btn-primary">Login</button>
                                </div>
                                <div className="mt-3 text-center">
                                    <small>
                                        Don't have an account? <a href="/register">Register</a>
                                    </small>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login