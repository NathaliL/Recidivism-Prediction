import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./Login";
import Prediction from "./Prediction";
import Navbar from "./Navbar";

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem("token");
        setIsAuthenticated(!!token);
    }, []);

    return (
        <Router>
            {isAuthenticated && <Navbar setIsAuthenticated={setIsAuthenticated} />}
            <Routes>
                <Route path="/login" element={!isAuthenticated ? <Login setIsAuthenticated={setIsAuthenticated} /> : <Navigate to="/predict" replace />} />
                <Route path="/predict" element={isAuthenticated ? <Prediction setIsAuthenticated={setIsAuthenticated} /> : <Navigate to="/login" replace />} />
                <Route path="*" element={<Navigate to={isAuthenticated ? "/predict" : "/login"} replace />} />
            </Routes>
        </Router>
    );
}

export default App;
