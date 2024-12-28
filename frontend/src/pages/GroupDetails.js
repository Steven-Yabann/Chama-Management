import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

const GroupDetails = () => {
    const { groupId } = useParams();
    const [groupDetails, setGroupDetails] = useState(null);
    const [members, setMembers] = useState([]);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const fetchGroupDetails = async () => {
        try {
            const token = localStorage.getItem('access_token');

            // Fetch group details
            const detailsResponse = await axios.get(`http://127.0.0.1:8000/api/groups/${groupId}/details/`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setGroupDetails(detailsResponse.data);

            // Fetch group members
            const membersResponse = await axios.get(`http://127.0.0.1:8000/api/groups/${groupId}/members/`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setMembers(membersResponse.data);
        } catch (error) {
            console.error('Failed to fetch group data:', error.response?.data || error.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchGroupDetails(); 
    }, [groupId]);

    return(
        <div className="container mt-5">
            {loading ? (
                <div className="text-center">
                    <div className="spinner-border text-primary" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </div>
                </div>
            ) : groupDetails ? (
                <>
                    <h1 className="text-center mb-4">{groupDetails.name}</h1>
                    <div className="card mb-4">
                        <div className="card-body">
                            <h5 className="card-title">Group Details</h5>
                            <p className="card-text">{groupDetails.description}</p>
                            <p className="text-muted">
                                <strong>Admin:</strong> {groupDetails.admin.username}
                            </p>
                            <p className="text-muted">
                                <strong>Group Code:</strong> {groupDetails.group_code}
                            </p>
                        </div>
                    </div>

                    <h2>Group Members</h2>
                    <ul className="list-group">
                        {members.length > 0 ? (
                            members.map((member) => (
                                <li className="list-group-item" key={member.id}>
                                    {member.user.username} (Joined: {new Date(member.joined_at).toLocaleDateString()})
                                </li>
                            ))
                        ) : (
                            <li className="list-group-item text-muted">No members found in this group.</li>
                        )}
                    </ul>
                </>
            ) : (
                <div className="text-center text-danger">
                    <p>Group not found or you do not have permission to view it.</p>
                    <button className="btn btn-secondary" onClick={() => navigate('/dashboard')}>
                        Go Back to Dashboard
                    </button>
                </div>
            )}
        </div>
    )
};

export default GroupDetails