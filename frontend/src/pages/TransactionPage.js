import React, { useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

const TransactionPage = () => {
    const { groupId } = useParams();
    const [transactionType, setTransactionType] = useState('deposit');
    const [amount, setAmount] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState(null);
    const navigate = useNavigate();

    const handleTransaction = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setSuccessMessage(true);

        try {
            const token = localStorage.getItem('access_token');
            const userId = localStorage.getItem('id');
            const data = {
                user_id: userId,
                amount: amount,
                group_id: groupId,
                transaction_type: transactionType,
            };
            console.log(data);
            const response = await axios.patch(`http://127.0.0.1:8000/api/savings/`,
                data,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            setSuccessMessage(`${transactionType === 'deposit' ? 'Deposit' : 'Withdrawal'} successful!`);
            setAmount('');
        } catch (error) {
            console.error('Failed to process transaction:', error.response?.data || error.message);
            setError(
                error.response?.data.error ||
                `Failed to process the ${transactionType}. Please try again.`
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="container mt-5">
            <h1 className="text-center mb-4">
                {transactionType === 'deposit' ? 'Deposit Money' : 'Withdraw Money'}
            </h1>
            {error && (
                <div className="alert alert-danger" role="alert">
                    {error}
                </div>
            )}
            {successMessage && (
                <div className="alert alert-success" role="alert">
                    {successMessage}
                </div>
            )}

            <form onSubmit={handleTransaction} className="shadow p-4">
                <div className="mb-3">
                    <label htmlFor="transactionType" className="form-label">
                        Transaction Type
                    </label>
                    <select
                        id="transactionType"
                        className="form-select"
                        value={transactionType}
                        onChange={(e) => setTransactionType(e.target.value)}
                    >
                        <option value="deposit">Deposit</option>
                        <option value="withdrawal">Withdraw</option>
                    </select>
                </div>
                <div className="mb-3">
                    <label htmlFor="amount" className="form-label">
                        Amount
                    </label>
                    <input
                        type="number"
                        id="amount"
                        className="form-control"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        required
                        min="1"
                        step="0.01"
                    />
                </div>
                <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={loading || !amount}
                >
                    {loading ? 'Processing...' : 'Submit'}
                </button>
            </form>
            <button
                className="btn btn-secondary mt-3"
                onClick={() => navigate(`/group/${groupId}`)}
            >
                Back to Group Details
            </button>
        </div>
    );
}

export default TransactionPage;