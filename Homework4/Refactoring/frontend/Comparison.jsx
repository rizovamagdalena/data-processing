// src/pages/Comparison.jsx
import React from "react";

const comparisonPageStyles = {
    body: {
        fontFamily: "Arial, sans-serif",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        margin: "0",
        backgroundColor: "#f0f0f0",
    },
    title: {
        fontSize: "2.5rem",
        color: "#333",
    },
};

const Comparison = () => {
    return (
        <div style={comparisonPageStyles.body}>
            <h1 style={comparisonPageStyles.title}>Comparison Page</h1>
        </div>
    );
};

export default Comparison;
