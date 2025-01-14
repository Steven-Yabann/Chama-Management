import React, { useEffect, useState } from "react";
import axios from "axios";

const LoanPage = () => {
    const [loans, setLoans] = useState([]);
    const [amount, setAmount] = useState("");
    const [term, setTerm] = useState("");
    const [loanId, setLoanId] = useState("");
    const [payment, setPayment] = useState("");
    const [message, setMessage] = useState("");
    const [groups, setGroups] = useState([]); // User groups
    const [selectedGroup, setSelectedGroup] = useState(); // Selected group for loan
    const token = localStorage.getItem("access_token");

    // Fetch user loans
    const fetchLoans = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/api/loans/", {
                headers: { Authorization: `Bearer ${token}` },
            });
            setLoans(response.data);
            console.log(`loans being fetched ${loans}`);
        } catch (error) {
            console.error("Failed to fetch loans:", error.response?.data || error.message);
        }
    };

    // Fetch user groups
    const fetchUserGroups = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/api/groups/user/", {
                headers: { Authorization: `Bearer ${token}` },
            });
            setGroups(response.data);
            console.log(groups)
        } catch (error) {
            console.error("Failed to fetch user groups:", error.response?.data || error.message);
        }
    };

    // Borrow loan
    const borrowLoan = async () => {
        if (!selectedGroup) {
            setMessage("Please select a group to borrow from.");
            return;
        }
        const userId = localStorage.getItem('id');
        let response_data = {
            user_id: userId,
            amount, 
            term_in_months: term, 
            group: selectedGroup, 
        }
        console.log(response_data);
        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/api/loans/",
                response_data,
                { headers: { Authorization: `Bearer ${token}` } }
            );
            setMessage("Loan borrowed successfully!");
            fetchLoans();
        } catch (error) {
            console.error("Failed to borrow loan:", error.response?.data || error.message);
            setMessage("Failed to borrow loan.");
        }
    };

    // Make payment
    const makePayment = async () => {
        if (!selectedGroup) {
            setMessage("Please select a group to repay the loan for.");
            return;
        }
        try {
            const response = await axios.post(
                `http://127.0.0.1:8000/api/loans/${loanId}/repay/`,
                { amount: payment },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            setMessage(response.data.message);
            fetchLoans();
        } catch (error) {
            console.error("Failed to make payment:", error.response?.data || error.message);
            setMessage("Failed to make payment.");
        }
    };

    useEffect(() => {
        fetchLoans();
        fetchUserGroups();
    }, []);

    return (
        <div className="container mt-5">
            <h1 className="text-center mb-4">Loan Management</h1>

            {message && (
                <div className={`alert ${message.includes("success") ? "alert-success" : "alert-danger"}`} role="alert">
                    {message}
                </div>
            )}

            <div className="row">
                {/* Borrow Loan Section */}
                <div className="col-md-6 mb-4">
                    <div className="card shadow">
                        <div className="card-body">
                            <h4 className="card-title">Borrow a Loan</h4>
                            <form>
                                <div className="mb-3">
                                    <label htmlFor="groupSelect" className="form-label">
                                        Select Group
                                    </label>
                                    <select
                                        id="groupSelect"
                                        className="form-select"
                                        value={selectedGroup}
                                        onChange={(e) => setSelectedGroup(e.target.value)}
                                    >
                                        <option value="">-- Select Group --</option>
                                        {groups.map((group) => (
                                            <option key={group.groupId} value={group.groupId}>
                                                {group.name}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                                <div className="mb-3">
                                    <label htmlFor="amount" className="form-label">
                                        Loan Amount
                                    </label>
                                    <input
                                        type="number"
                                        className="form-control"
                                        id="amount"
                                        placeholder="Enter loan amount"
                                        value={amount}
                                        onChange={(e) => setAmount(e.target.value)}
                                    />
                                </div>
                                <div className="mb-3">
                                    <label htmlFor="term" className="form-label">
                                        Loan Term (Months)
                                    </label>
                                    <input
                                        type="number"
                                        className="form-control"
                                        id="term"
                                        placeholder="Enter loan term"
                                        value={term}
                                        onChange={(e) => setTerm(e.target.value)}
                                    />
                                </div>
                                <button type="button" className="btn btn-primary" onClick={borrowLoan}>
                                    Borrow Loan
                                </button>
                            </form>
                        </div>
                    </div>
                </div>

                {/* Repay Loan Section */}
                <div className="col-md-6 mb-4">
                    <div className="card shadow">
                        <div className="card-body">
                            <h4 className="card-title">Repay a Loan</h4>
                            <form>
                                <div className="mb-3">
                                    <label htmlFor="groupSelect" className="form-label">
                                        Select Group
                                    </label>
                                    <select
                                        id="groupSelect"
                                        className="form-select"
                                        value={selectedGroup}
                                        onChange={(e) => setSelectedGroup(e.target.value)}
                                    >
                                        <option value="">-- Select Group --</option>
                                        {groups.map((group) => (
                                            <option key={group.groupId} value={group.groupId}>
                                                {group.name}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                                <div className="mb-3">
                                    <label htmlFor="loanId" className="form-label">
                                        Loan ID
                                    </label>
                                    <input
                                        type="number"
                                        className="form-control"
                                        id="loanId"
                                        placeholder="Enter loan ID"
                                        value={loanId}
                                        onChange={(e) => setLoanId(e.target.value)}
                                    />
                                </div>
                                <div className="mb-3">
                                    <label htmlFor="payment" className="form-label">
                                        Payment Amount
                                    </label>
                                    <input
                                        type="number"
                                        className="form-control"
                                        id="payment"
                                        placeholder="Enter payment amount"
                                        value={payment}
                                        onChange={(e) => setPayment(e.target.value)}
                                    />
                                </div>
                                <button type="button" className="btn btn-success" onClick={makePayment}>
                                    Make Payment
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>

            {/* Loan List Section */}
            <div className="card shadow">
                <div className="card-body">
                    <h4 className="card-title">Your Loans</h4>
                    {loans.length > 0 ? (
                        <ul className="list-group">
                            {loans.map((loan) => (
                                <li className="list-group-item d-flex justify-content-between align-items-center" key={loan.id}>
                                    <div>
                                        <strong>Loan #{loan.id}</strong> - ${parseFloat(loan.amount || 0).toFixed(2)} (Balance: ${parseFloat(loan.balance || 0).toFixed(2)})
                                    </div>
                                    <span className="badge bg-primary">Monthly Payment: ${loan.monthly_payment}</span>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p className="text-muted">You have no loans.</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default LoanPage;
