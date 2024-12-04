import React from "react";
import { useNavigate } from "react-router-dom";

const homePageStyles = {
    container: {
        textAlign: "center",
        padding: "50px",
        color: "white",
        background: "linear-gradient(to right, #001232, #0a2440, #23395d)",
        height: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "column",
    },
    header: {
        fontSize: "2.5rem",
        marginBottom: "30px",
    },
    buttonsContainer: {
        display: "grid", // Change to grid layout
        gridTemplateColumns: "repeat(2, 1fr)", // Two buttons per row
        gap: "20px", // Add gap between buttons
        width: "60%", // Adjust width to control button size
        margin: "0 auto", // Center the buttons horizontally
    },
    button: {
        padding: "15px 30px",
        fontSize: "18px",
        cursor: "pointer",
        backgroundColor: "#0ac4ff",
        color: "white",
        border: "2px solid #ffffff", // Add border to buttons
        borderRadius: "10px",
        transition: "background-color 0.3s ease-in-out",
        fontWeight: "bold",
        outline: "none",
    },
    buttonHover: {
        backgroundColor: "#001232",
    },
};

const Home = () => {
    const navigate = useNavigate();

    const goToPage = (page) => {
        navigate(`/${page}`);
    };

    return (
        <div style={homePageStyles.container}>
            <h1 style={homePageStyles.header}>Welcome to the Stock App</h1>
            <div style={homePageStyles.buttonsContainer}>
                <button style={homePageStyles.button} onClick={() => goToPage("search")}>
                    SEARCH STOCKS
                </button>
                <button style={homePageStyles.button} onClick={() => goToPage("most-traded")}>
                    COMPANY LIST
                </button>
                <button style={homePageStyles.button} onClick={() => goToPage("top-news")}>
                    TOP NEWS
                </button>
                <button style={homePageStyles.button} onClick={() => goToPage("comparison")}>
                    COMPARISON
                </button>
            </div>
        </div>
    );
};

export default Home;
