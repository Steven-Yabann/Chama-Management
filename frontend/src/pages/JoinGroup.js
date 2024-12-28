import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const JoinGroup = () => {
    const [groupCode, setGroupCode] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleJoinGroup = async(e) => {
        e.preventDefault();
        setLoading(true);

        try{
            const token = localStorage.getItem('access_token');
            await axios.post('http://127.0.0.1:8000/api/groups/join/',
                {group_code : groupCode},
                {headers : {
                    Authorization : `Bearer ${token}`
                }}
            );
            alert('Successfully joined group!');
            navigate('/dashboard')
        } catch(error){
            console.error('Failed to join group:', error.response?.data || error.message);
        } finally{
            setLoading(true);
        }
    };

    return(
        <div className="container mt-5">
            <h1 className="text-center mb-4">Join a Group</h1>
            <form onSubmit={handleJoinGroup} className="shadow p-4 bg-light rounded">
                <div className="mb-3">
                    <label htmlFor="groupCode" className="form-label">
                        Group Code
                    </label>
                    <input
                        type="text"
                        id="groupCode"
                        className="form-control"
                        value={groupCode}
                        onChange={(e) => setGroupCode(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="btn btn-success w-100" disabled={loading}>
                    {loading ? (
                        <span>
                            <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                            Joining Group...
                        </span>
                    ) : (
                        'Join Group'
                    )}
                </button>
            </form>
        </div>
    );
};

export default JoinGroup;
