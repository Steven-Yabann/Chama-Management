import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Register = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        username: '',
        email: '',
        password: '',
        password1: '',
        user_type: 'member',
    })

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/auth/register/', formData);
            navigate('/');
        } catch (error) {
            if (error.response) {
                // Log the detailed errors sent from the backend
                console.error('Registration failed:', error.response.data);
    
                // Optionally, show specific errors to the user
                alert(`Registration failed: ${JSON.stringify(error.response.data)}`);
            } else {
                console.error('An unexpected error occurred:', error.message);
            }
        }
    }

    const handleChange = (e) =>{
        setFormData({ ...formData, [e.target.name]: e.target.value });
    }

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <div className="card">
                        <div className="card-body">
                            <h1 className="card-title text-center">Register</h1>
                            <form onSubmit={handleRegister}>
                                <div className="mb-3">
                                    <label className="form-label">First Name</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        name="first_name"
                                        placeholder="Enter your first name"
                                        value={formData.first_name}
                                        onChange={handleChange}
                                    />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Last Name</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        name="last_name"
                                        placeholder="Enter your last name"
                                        value={formData.last_name}
                                        onChange={handleChange}
                                    />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Username</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        name="username"
                                        placeholder="Enter your username"
                                        value={formData.last_name}
                                        onChange={handleChange}
                                    />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Email</label>
                                    <input
                                        type="email"
                                        className="form-control"
                                        name="email"
                                        placeholder="Enter your email"
                                        value={formData.email}
                                        onChange={handleChange}
                                    />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Password</label>
                                    <input
                                        type="password"
                                        className="form-control"
                                        name="password"
                                        placeholder="Enter your password"
                                        value={formData.password}
                                        onChange={handleChange}
                                    />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Confirm Password</label>
                                    <input
                                        type="password"
                                        className="form-control"
                                        name="password1"
                                        placeholder="Confirm your password"
                                        value={formData.password1}
                                        onChange={handleChange}
                                    />
                                </div>
                                <div className="d-grid">
                                    <button type="submit" className="btn btn-success">Register</button>
                                </div>
                                <div className="mt-3 text-center">
                                    <small>
                                        Already have an account? <a href="/">Login</a>
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

    export default Register;