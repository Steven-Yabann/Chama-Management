import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import CreateGroup from './pages/CreateGroup';
import JoinGroup from './pages/JoinGroup';
import GroupDetails from './pages/GroupDetails';
import NavBar from './components/Navbar';
import TransactionPage from './pages/TransactionPage';
import LoanPage from './pages/LoanPage';


function App() {
  return (
      <div className="container">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/create-group" element={<CreateGroup />} />
          <Route path="/join-group" element={<JoinGroup />} />
          <Route path="/group/:groupId" element={<GroupDetails />} />
          <Route path="/group/:groupId/transaction" element={<TransactionPage />} />
          <Route path="/dashboard/loans" element={<LoanPage />} />
        </Routes>
      </div>
  );
}

export default App;
