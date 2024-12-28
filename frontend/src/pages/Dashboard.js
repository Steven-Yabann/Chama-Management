import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
    const navigate = useNavigate();
    const [groups, setGroups] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchUserGroups = async () => {
        setLoading(true);
        setError(null);
        try {
            const token = localStorage.getItem('access_token');
            const response = await axios.get('http://127.0.0.1:8000/api/groups/user/', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            console.log(response.data);
            setGroups(response.data);
        } catch (error) {
            console.error('Failed to fetch user groups:', error.response?.data || error.message);
            setError('Failed to load your groups. Please try again later.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchUserGroups();
    }, []);

    const viewGroupDetails = (id) => {
        navigate(`/group/${id}`);
    };

    return (
        <div className="container mt-5">
            <h1 className="text-center mb-4">My Chama Groups</h1>

            {/* Error Message */}
            {error && (
                <div className="alert alert-danger" role="alert">
                    {error}
                </div>
            )}

            {/* Loader */}
            {loading && (
                <div className="text-center">
                    <div className="spinner-border text-primary" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </div>
                </div>
            )}

            {/* Groups List */}
            {!loading && !error && groups.length > 0 && (
                <div className="row">
                    {groups.map((group) => (
                        <div className="col-md-4 mb-4" key={group.groupId}>
                            <div className="card shadow">
                                <div className="card-body">
                                    <h5 className="card-title">{group.name}</h5>
                                    <p className="card-text">{group.description}</p>
                                    <p className="text-muted">
                                        <small>Admin: {group.admin || 'Unknown Admin'}</small>
                                    </p>
                                    <button
                                        className="btn btn-primary btn-sm"
                                        onClick={() => viewGroupDetails(group.groupId)}
                                    >
                                        View Group
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* No Groups Found */}
            {!loading && !error && groups.length === 0 && (
                <div className="text-center text-muted">
                    <p>You are not a member of any Chama group yet.</p>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
