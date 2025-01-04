import React from 'react';

const GroupMembers = ({ members }) => {
    return (
        <div className="container mt-5">
            <h1>Group Members</h1>
            <ul className="list-group">
                {members.length > 0 ? (
                    members.map((member) => (
                        <li className="list-group-item" key={member.id}>
                            {member.user.first_name} {member.user.last_name} (Joined: {new Date(member.joined_at).toLocaleDateString()})
                        </li>
                    ))
                ) : (
                    <li className="list-group-item text-muted">No members found in this group.</li>
                )}
            </ul>
        </div>
    );
};

export default GroupMembers;
