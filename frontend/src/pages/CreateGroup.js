import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const CreateGroup = () =>{
    const navigate = useNavigate();
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [loading, setLoading] = useState(false);

    const handleCreateGroup = async(e) =>{
        e.preventDefault();
        setLoading(true);
        try {
            const token = localStorage.getItem('access_token');
            await axios.post(
                'http://127.0.0.1:8000/api/groups/create/',
                { name, description },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            alert('Group created successfully!');
            navigate('/dashboard');
        } catch (error) {
            console.error('Failed to create group:', error.response?.data || error.message);
        } finally {
            setLoading(false);
        }
    };

    return(
        <div className="container mt-5">
            <h1 className="text-center mb-4">Create a New Group</h1>
            <form onSubmit={handleCreateGroup} className="shadow p-4 bg-light rounded">
                <div className="mb-3">
                    <label htmlFor="groupName" className="form-label">
                        Group Name
                    </label>
                    <input
                        type="text"
                        id="groupName"
                        className="form-control"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="groupDescription" className="form-label">
                        Group Description
                    </label>
                    <textarea
                        id="groupDescription"
                        className="form-control"
                        rows="3"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        required
                    ></textarea>
                </div>
                <button type="submit" className="btn btn-primary w-100" disabled={loading}>
                    {loading ? (
                        <span>
                            <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                            Creating Group...
                        </span>
                    ) : (
                        'Create Group'
                    )}
                </button>
            </form>
        </div>
    );
};

export default CreateGroup;