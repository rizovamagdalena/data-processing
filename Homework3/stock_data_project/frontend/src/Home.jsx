import React, { useEffect, useState } from "react";
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
        position: "relative",
    },
    hero: {
        fontSize: "3rem",
        fontWeight: "700",
        marginBottom: "20px",
        textTransform: "uppercase",
        letterSpacing: "2px",
        textShadow: "2px 2px 8px rgba(0,0,0,0.5)",
    },
    tagline: {
        fontSize: "1.5rem",
        margin: "10px 0 40px",
        fontStyle: "italic",
        color: "#b0c7d4",
    },
    buttonsContainer: {
        display: "grid",
        gridTemplateColumns: "repeat(2, 1fr)",
        gap: "30px",
        width: "70%",
        margin: "0 auto",
        animation: "scaleUp 1.5s ease-out",
    },
    button: {
        padding: "15px 30px",
        fontSize: "18px",
        cursor: "pointer",
        backgroundColor: "#0ac4ff",
        color: "white",
        border: "none",
        borderRadius: "50px",  // Rounded buttons for a modern look
        transition: "0.3s ease-out",
        fontWeight: "bold",
        outline: "none",
        boxShadow: "0 10px 15px rgba(0, 150, 255, 0.2)",
        transform: "scale(1)",
    },
    buttonHover: {
        backgroundColor: "#001232",
        transform: "scale(1.05)",
        boxShadow: "0 20px 30px rgba(0, 150, 255, 0.3)",
    },
    stockSnippet: {
        backgroundColor: "#203855",
        padding: "20px",
        borderRadius: "12px",
        width: "80%",
        margin: "20px auto",
        boxShadow: "0 10px 20px rgba(0, 0, 0, 0.4)",
    },
    stockTitle: {
        fontSize: "1.8rem",
        marginBottom: "10px",
        fontWeight: "600",
    },
    stockDetails: {
        fontSize: "1.2rem",
        color: "#b0c7d4",
    },
    '@keyframes scaleUp': {
        '0%': { transform: 'scale(0.8)' },
        '100%': { transform: 'scale(1)' }
    }
};

const Home = () => {
    const navigate = useNavigate();
    const [featuredStock, setFeaturedStock] = useState(null);

    useEffect(() => {
        // Fetch the featured stock of the day from the backend
        const fetchFeaturedStock = async () => {
            try {
                const response = await fetch("/api/featured-stock");  // Adjust the URL to your backend
                if (!response.ok) {
                    throw new Error("Failed to fetch featured stock");
                }
                const data = await response.json();
                setFeaturedStock(data);  // Set the fetched data to state
            } catch (error) {
                console.error(error);
            }
        };

        fetchFeaturedStock();
    }, []);

    const goToPage = (page) => {
        navigate(`/${page}`);
    };

    return (
        <div style={homePageStyles.container}>
            <div style={homePageStyles.hero}>Welcome to the Macedonian Stock Market</div>
            <div style={homePageStyles.tagline}>Stay ahead with insights, live prices, and trends of the Macedonian stock market.</div>

            {/* Buttons */}
            <div style={homePageStyles.buttonsContainer}>
                <button style={homePageStyles.button} onClick={() => goToPage("search")}>
                    SEARCH STOCKS
                </button>
                <button style={homePageStyles.button} onClick={() => goToPage("most-traded")}>
                    MOST TRADED STOCKS
                </button>
                <button style={homePageStyles.button} onClick={() => goToPage("stock-trends")}>
                    STOCK TRENDS
                </button>
                <button style={homePageStyles.button} onClick={() => goToPage("stock_indicators/ADIN/1D")}>
                    STOCK INDICATORS
                </button>
            </div>
        </div>
    );
};

export default Home;
