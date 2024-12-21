import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

// Inline styles to maintain the same appearance
const searchPageStyles = {
    container: {
        width: "70%",
        textAlign: "left",
    },
    title: {
        fontSize: "3rem",
        letterSpacing: "0.1em",
        textAlign: "center",
    },
    subtitle: {
        fontSize: "1.2rem",
        marginTop: "10px",
        letterSpacing: "0.05em",
        textAlign: "center",
    },
    searchContainer: {
        display: "flex",
        alignItems: "center",
        margin: "30px 0",
        borderBottom: "2px solid #0ac4ff",
        paddingBottom: "10px",
    },
    input: {
        flex: 1,
        padding: "10px",
        fontSize: "1rem",
        color: "#0ac4ff",
        background: "transparent",
        border: "none",
        outline: "none",
        caretColor: "#0ac4ff",
    },
    searchIcon: {
        fontSize: "1.5rem",
        color: "#0ac4ff",
        marginRight: "10px",
    },
    list: {
        marginTop: "20px",
    },
    listItem: {
        marginBottom: "20px",
    },
    listLink: {
        color: "#0ac4ff",
        textDecoration: "none",
        fontSize: "1.2rem",
        transition: "color 0.3s ease",
    },
    listLinkHover: {
        color: "#67e3ff",
    },
    backgroundEffect: {
        position: "absolute",
        top: "0",
        left: "0",
        width: "100%",
        height: "100%",
        background: "radial-gradient(circle, rgba(58,123,213,0.3) 0%, rgba(0,0,0,0) 60%)",
        zIndex: "-1",
    },
};

const Search = () => {
    const [searchQuery, setSearchQuery] = useState("");  // The current value of the search field
    const [stockCodes, setStockCodes] = useState([]);    // Matching stock codes
    const [loading, setLoading] = useState(false);       // Loading state for when search is in progress
    const navigate = useNavigate();

    // Function that handles typing input changes
    const handleSearchChange = async (e) => {

        const query = e.target.value;
        setSearchQuery(query);

        if (query.length > 0) {
            // Start loading and fetch matching codes
            setLoading(true);
            try {
                const response = await axios.get(`http://localhost:5000/api/search?query=${query}`);

                // Use Set to remove duplicates in case there are any, but backend should ensure this
                const uniqueStockCodes = Array.from(new Set(response.data));
                setStockCodes(uniqueStockCodes); // Update state with unique codes
                console.log("Received stock codes:", response.data); // Debugging
            } catch (error) {
                console.error("Error fetching stock codes:", error);
                setStockCodes([]);
            }
            setLoading(false);
        } else {
            setStockCodes([]);  // Clear suggestions if query is empty
        }
    };


    // Function that handles click on a stock code
    const handleStockClick = (code) => {
        navigate(`/info/${code}`);  // Navigate to Info page for selected code
    };

    return (
        <div style={searchPageStyles.container}>
            <h2 style={searchPageStyles.title}>Search Stocks</h2>
            <p style={searchPageStyles.subtitle}>Type to search for a stock code</p>

            <div style={searchPageStyles.searchContainer}>
                <input
                    type="text"
                    value={searchQuery}
                    onChange={handleSearchChange}
                    placeholder="Search for stocks"
                    style={searchPageStyles.input}
                    autoFocus
                />
            </div>

            {loading && <p>Loading...</p>}

            {stockCodes.length > 0 && (
                <ul style={searchPageStyles.list}>
                    {stockCodes.map((code, index) => (
                        <li
                            key={index}
                            style={searchPageStyles.listItem}
                            onClick={() => handleStockClick(code)}
                        >
                            <a
                                href="#"
                                style={searchPageStyles.listLink}
                                onMouseEnter={(e) => (e.target.style.color = searchPageStyles.listLinkHover.color)}
                                onMouseLeave={(e) => (e.target.style.color = searchPageStyles.listLink.color)}
                            >
                                {code} {/* Directly displaying the code */}
                            </a>
                        </li>
                    ))}
                </ul>
            )}

            {searchQuery && stockCodes.length === 0 && <p>No matching stocks found.</p>}

            <div style={searchPageStyles.backgroundEffect}></div> {/* Background effect */}
        </div>
    );
};

export default Search;
