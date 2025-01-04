import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = ( {groupId} ) => {
    return (
        <div className="sidebar">
            <ul className="nav flex-column">
                <li className="nav-item">
                    <NavLink to={`/group/${groupId}/overview`} className="nav-link">
                        Overview
                    </NavLink>
                </li>
                <li className="nav-item">
                    <NavLink to={`/group/${groupId}/members`} className="nav-link">
                        Members
                    </NavLink>
                </li>
                <li className="nav-item">
                    <NavLink to={`/group/${groupId}/transactions`} className="nav-link">
                        Transactions
                    </NavLink>
                </li>
            </ul>
        </div>
    );
};

export default Sidebar;