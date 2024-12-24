import React, { useState } from 'react';
import axios from 'axios';

const Login = () =>{
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin =async (e) => {
        e.preventDefault();
        try{
            const response = await axios.post('http://127.0.0.1:8000/api/auth/login/', {
                username,
                password,
            });

            const tokenResponse = await axios.post('http://127.0.0.1:8000/api/auth/token/', {
                username,
                password,
            })

            // Store tokens in localStorage
            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);

            alert('Login succesful')
        }catch (error){
            console.error('Login failed:', error.response?.data || error.message);
        }
    };

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <div className="card">
                        <div className="card-body">
                            <h1 className="card-title text-center">Login</h1>
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