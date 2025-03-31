import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "./styles.css";

function Login({ setIsAuthenticated }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(""); 
        setLoading(true);

        try {
            const response = await fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();
            if (response.ok) {
                sessionStorage.setItem("token", data.token);
                setIsAuthenticated(true);
                navigate("/predict", { replace: true });
            } else {
                setError(data.error || "Invalid credentials. Please try again.");
            }
        } catch (error) {
            setError("Network error. Please check your connection.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <nav className="navbar">
                <h2 className="navbar-brand">RecidiVision</h2>
            </nav>

            <div className="form-container">
                <h2 className="title">Login</h2>
                <form onSubmit={handleSubmit}>
                    <label>Username:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        disabled={loading}
                    />

                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        disabled={loading}
                    />

                    {error && <div className="result error">{error}</div>}

                    <button type="submit" className="submit-btn" disabled={loading}>
                        {loading ? "Logging in..." : "Login"}
                    </button>
                </form>
            </div>
        </>
    );
}

export default Login;
