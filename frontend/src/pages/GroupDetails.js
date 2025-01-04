import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

const GroupDetails = () => {
    const { groupId } = useParams();
    const [groupDetails, setGroupDetails] = useState(null);
    const [members, setMembers] = useState([]);
    const [transactions, setTransactions] = useState([]);
    const [savings, setSavings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const fetchGroupDetails = async () => {
        setLoading(true); // Start loading
        setError(null); // Clear any previous error
        try {
            const token = localStorage.getItem('access_token');

            const response = await axios.get(`http://127.0.0.1:8000/api/groups/${groupId}/details/`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            const data = response.data;
            console.log(data);
            setGroupDetails(data.group_details);
            setMembers(data.members);
            setTransactions(data.transactions);
            setSavings(data.savings);
        } catch (error) {
            console.error('Failed to fetch group data:', error.response?.data || error.message);
            setError('Failed to load group details. Please try again later.');
        } finally {
            setLoading(false); // Stop loading
        }
    };

    useEffect(() => {
        fetchGroupDetails();
    }, [groupId]);

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div className="container mt-5">
            <button
                className="btn btn-primary btn-sm mt-3"
                onClick={() => navigate(`/group/${groupId}/transaction`)}
            >
                Make a Transaction
            </button>
            {loading ? (
                <div className="text-center">
                    <div className="spinner-border text-primary" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </div>
                </div>
            ) : error ? (
                <div className="alert alert-danger text-center" role="alert">
                    {error}
                </div>
            ) : groupDetails ? (
                <>
                    <h1 className="text-center mb-4">{groupDetails.name}</h1>
                    <div className="card mb-4">
                        <div className="card-body">
                            <h5 className="card-title">Group Details</h5>
                            <p className="card-text">{groupDetails.description}</p>
                            <p className="text-muted">
                                <strong>Admin:</strong>{' '}
                                {groupDetails.admin
                                    ? `${groupDetails.admin.first_name || ''} ${groupDetails.admin.last_name || ''}`
                                    : 'Unknown Admin'}
                            </p>
                            <p className="text-muted">
                                <strong>Group Code:</strong> {groupDetails.group_code}
                            </p>
                        </div>
                    </div>

                    <h2>Group Savings</h2>
                    <ul className="list-group mb-4">
                        {savings.length > 0 ? (
                            savings.map((saving) => (
                                <li className="list-group-item" key={saving.id}>
                                    {saving.user
                                        ? `${saving.user.username || 'Unknown User'}`
                                        : 'Unknown User'}{' '}
                                    saved ${saving.amount} on {new Date(saving.saved_at).toLocaleDateString()}
                                </li>
                            ))
                        ) : (
                            <li className="list-group-item text-muted">No savings records found for this group.</li>
                        )}
                    </ul>

                    <h2>Group Members</h2>
                    <ul className="list-group mb-4">
                        {members.length > 0 ? (
                            members.map((member) => (
                                <li className="list-group-item" key={member.id}>
                                    {member.user
                                        ? `${member.user.first_name || ''} ${member.user.last_name || ''}`
                                        : 'Unknown Member'}{' '}
                                    : Joined: {new Date(member.joined_at).toLocaleDateString()}
                                </li>
                            ))
                        ) : (
                            <li className="list-group-item text-muted">No members found in this group.</li>
                        )}
                    </ul>

                    <h2>Group Transactions</h2>
                    <ul className="list-group mb-4">
                        {transactions.length > 0 ? (
                            transactions.map((transaction) => (
                                <li className="list-group-item" key={transaction.id}>
                                    {transaction.transaction_type} - ${transaction.amount} on{' '}
                                    {new Date(transaction.date).toLocaleDateString()} by{' '}
                                    {transaction.user
                                        ? `${transaction.user.first_name || ''} ${transaction.user.last_name || ''}`
                                        : 'Unknown User'}
                                </li>
                            ))
                        ) : (
                            <li className="list-group-item text-muted">No transactions found for this group.</li>
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
    );
};

export default GroupDetails;
