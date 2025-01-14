import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = () => {
    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container-fluid">
            <Link className="navbar-brand" to="/dashboard">
                Microfinance App
            </Link>
            <div className="collapse navbar-collapse">
                <ul className="navbar-nav me-auto">
                    <li className="nav-item">
                        <Link className="nav-link" to="/create-group">
                            Create Group
                        </Link>
                    </li>
                    <li className="nav-item">
                        <Link className="nav-link" to="/join-group">
                            Join Group
                        </Link>
                    </li>
                    <li className="nav-item">
                        <Link className="nav-link" to="/dashboard/loans">
                            Loans
                        </Link>
                    </li>
                </ul>
            </div>
        </div>
    </nav>  
    );
}

export default NavBar;