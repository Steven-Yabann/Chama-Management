import './App.css';
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
// import Dashboard from './pages/Dashboard';
// import CreateGroup from './pages/CreateGroup';
// import JoinGroup from './pages/JoinGroup';
// import GroupDetails from './pages/GroupDetails';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/register" element={<Register />} />
      {/* <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/create-group" element={<CreateGroup />} />
      <Route path="/join-group" element={<JoinGroup />} />
      <Route path="/group/:id" element={<GroupDetails />} /> */}
    </Routes>
  )
}

export default App;
