import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "./styles.css";

function Navbar({ setIsAuthenticated }) {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem("token");
        setIsAuthenticated(false);
        navigate("/login");
    };

    return (
        <nav className="navbar">
            <h2 className="navbar-brand">RecidiVision</h2>
            <div className="nav-links">
                <button className="logout-btn" onClick={handleLogout}>Logout</button>
            </div>
        </nav>
    );
}

export default Navbar;
