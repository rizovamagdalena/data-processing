import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";

const infoPageStyles = {
    container: {
        minHeight: "100vh", // Ensure container stretches to full viewport height
        padding: "20px",
        textAlign: "center",
        color: "white",
        background: "linear-gradient(to right, #0a2a43, #003256, #16313d)",
        fontFamily: "'Roboto', sans-serif",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
    },
    header: {
        fontSize: "2.5rem",
        marginBottom: "20px",
        color: "#F6C5A3",
        letterSpacing: "2px",
    },
    timeButtons: {
        marginTop: "30px",
        marginBottom: "40px",
        display: "flex",
        justifyContent: "center",
        gap: "15px",
    },
    timeButton: {
        backgroundColor: "#F6C5A3", // Default yellowish color
        color: "white",
        padding: "12px 25px",
        fontSize: "1.1rem",
        border: "none",
        borderRadius: "30px",
        cursor: "pointer",
        transition: "all 0.3s ease",
        fontWeight: "bold",
        textTransform: "uppercase",
        letterSpacing: "1px",
    },
    timeButtonActive: {
        backgroundColor: "#F0A000", // Lighter shade when pressed
        transform: "scale(1.1)",
    },
    timeButtonHover: {
        backgroundColor: "#f0b6a1", // Color when hovered
        transform: "scale(1.05)",
    },
    table: {
        marginTop: "30px",
        width: "90%",
        margin: "0 auto",
        borderCollapse: "separate",
        borderSpacing: "0",
        borderRadius: "12px",
        boxShadow: "0 10px 30px rgba(0, 0, 0, 0.2)",
    },
    tableHeader: {
        backgroundColor: "#1976D2",
        color: "white",
        fontSize: "1.2rem",
        padding: "15px 20px",
        textTransform: "uppercase",
        textAlign: "center",
        borderTopLeftRadius: "12px",
        borderTopRightRadius: "12px",
    },
    tableRow: {
        backgroundColor: "#223f5b",
        color: "white",
        padding: "10px",
        textAlign: "center",
        transition: "background-color 0.3s ease",
    },
    tableData: {
        padding: "12px 20px",
        textAlign: "center",
        borderBottom: "2px solid #3b5a73",
        fontSize: "1rem",
    },
    loadingText: {
        fontSize: "1.2rem",
        color: "#ffffff",
        marginTop: "20px",
    },
};




const parseDate = (dateString) => {
    const [year, month, day] = dateString.split("-").map(part => parseInt(part, 10));
    return new Date(year, month - 1, day); // JavaScript Date expects month in 0-indexed
    //return new Date(year, month, day);
};

const DataInfo = () => {
    const { code } = useParams();
    //const [stockInfo, setStockInfo] = useState(null);
    const [stockInfo, setStockInfo] = useState([]);
    const [filteredStockInfo, setFilteredStockInfo] = useState(null);
    const [loading, setLoading] = useState(false);
    const [selectedPeriod, setSelectedPeriod] = useState("1D");

    const periods = ["1D", "7D", "1M", "1Y", "2Y", "10Y"];

    const fetchStockInfo = async (stockCode) => {
    setLoading(true);

    // Get the start and end dates based on selected period
    const getDatesForPeriod = (period) => {
        const currentDate = new Date();
        const endDate = currentDate.toISOString().split("T")[0]; // Format to YYYY-MM-DD
        let startDate;

        switch (period) {
            case "1D":
                startDate = endDate;  // Same day
                break;
            case "7D":
                currentDate.setDate(currentDate.getDate() - 7);
                startDate = currentDate.toISOString().split("T")[0];
                break;
            case "1M":
                currentDate.setMonth(currentDate.getMonth() - 1);
                startDate = currentDate.toISOString().split("T")[0];
                break;
            case "1Y":
                currentDate.setFullYear(currentDate.getFullYear() - 1);
                startDate = currentDate.toISOString().split("T")[0];
                break;
            case "2Y":
                currentDate.setFullYear(currentDate.getFullYear() - 2);
                startDate = currentDate.toISOString().split("T")[0];
                break;
            case "10Y":
                currentDate.setFullYear(currentDate.getFullYear() - 10);
                startDate = currentDate.toISOString().split("T")[0];
                break;
            default:
                startDate = endDate; // Default to same day if no period is selected
        }

        return { startDate, endDate };
    };

    const { startDate, endDate } = getDatesForPeriod(selectedPeriod);

    //console.log("Fetching data for period:", selectedPeriod, "Start:", startDate, "End:", endDate);

    try {
        // Pass start_date and end_date as query parameters
        const response = await axios.get(`http://localhost:5000/api/stocks/${stockCode}?start_date=${startDate}&end_date=${endDate}`);
        console.log(response.data.data);
        setStockInfo(response.data.data);
        setFilteredStockInfo(response.data.data);
    } catch (error) {
        console.error("Error fetching stock info:", error);
        alert("Failed to load stock data, please try again later.");
    }
    setLoading(false);
};

    const filterDataByPeriod = (period) => {

        setSelectedPeriod(period);

        const currentDate = new Date();
        const currentTimestamp = currentDate.getTime();

        let filteredData = [];

        switch (period) {
            case "1D":
                filteredData = stockInfo.filter((row) => {
                    const rowDate = parseDate(row[1]);
                    return isSameDay(rowDate, currentDate);
                });
                break;
            case "7D":
                filteredData = stockInfo.filter((row) => {
                    const rowDate = parseDate(row[1]);
                    return currentTimestamp - rowDate.getTime() <= 7 * 24 * 60 * 60 * 1000;
                });
                break;
            case "1M":
                filteredData = stockInfo.filter((row) => {
                    const rowDate = parseDate(row[1]);
                    return currentTimestamp - rowDate.getTime() <= 30 * 24 * 60 * 60 * 1000;
                });
                break;
            case "1Y":
                filteredData = stockInfo.filter((row) => {
                    const rowDate = parseDate(row[1]);
                    return currentTimestamp - rowDate.getTime() <= 365 * 24 * 60 * 60 * 1000;
                });
                break;
            case "2Y":
                filteredData = stockInfo.filter((row) => {
                    const rowDate = parseDate(row[1]);
                    return currentTimestamp - rowDate.getTime() <= 730 * 24 * 60 * 60 * 1000;
                });
                break;
            case "10Y":
                filteredData = stockInfo;
                break;
            default:
                filteredData = stockInfo;
        }

        setFilteredStockInfo(filteredData);
    };

    const isSameDay = (date1, date2) => {
        return date1.getDate() === date2.getDate() &&
            date1.getMonth() === date2.getMonth() &&
            date1.getFullYear() === date2.getFullYear();
    };

    useEffect(() => {
    if (code && selectedPeriod) {
        fetchStockInfo(code);
    }
}, [code, selectedPeriod]);

    return (
        <div style={infoPageStyles.container}>
            <h1 style={infoPageStyles.header}>
                Stock Information for {code}
            </h1>

            {/* Time Period Selector */}
            <div style={infoPageStyles.timeButtons}>
                {periods.map((period) => (
                    <button
                        key={period}
                        style={{
                            ...infoPageStyles.timeButton,
                            ...(selectedPeriod === period ? infoPageStyles.timeButtonActive : {}),
                        }}
                        onClick={() => filterDataByPeriod(period)}
                        onMouseEnter={(e) => e.target.style.backgroundColor = "#f0b6a1"}  // Hover effect
                        onMouseLeave={(e) => e.target.style.backgroundColor = selectedPeriod === period ? "#F0A000" : "#F6C5A3"} // Reset
                    >
                        {period}
                    </button>
                ))}
            </div>

            {loading && <p style={infoPageStyles.loadingText}>Loading...</p>}

            {/* Display stock info */}
            {filteredStockInfo && filteredStockInfo.length > 0 ? (
                <div>
                    <table style={infoPageStyles.table}>
                        <thead>
                        <tr>
                            <th style={infoPageStyles.tableHeader}>Date</th>
                            <th style={infoPageStyles.tableHeader}>Last Price</th>
                            <th style={infoPageStyles.tableHeader}>Max Price</th>
                            <th style={infoPageStyles.tableHeader}>Min Price</th>
                            <th style={infoPageStyles.tableHeader}>Avg Price</th>
                            <th style={infoPageStyles.tableHeader}>Percent Change</th>
                            <th style={infoPageStyles.tableHeader}>Quantity</th>
                            <th style={infoPageStyles.tableHeader}>Revenue Best Denars</th>
                            <th style={infoPageStyles.tableHeader}>Total Revenue Denars</th>
                        </tr>
                        </thead>
                        <tbody>
                        {filteredStockInfo.map((row, index) => (
                            <tr key={index} style={infoPageStyles.tableRow}>
                                <td style={infoPageStyles.tableData}>{row[1]}</td>
                                <td style={infoPageStyles.tableData}>{row[2]}</td>
                                <td style={infoPageStyles.tableData}>{row[3]}</td>
                                <td style={infoPageStyles.tableData}>{row[4]}</td>
                                <td style={infoPageStyles.tableData}>{row[5]}</td>
                                <td style={infoPageStyles.tableData}>{row[6]}</td>
                                <td style={infoPageStyles.tableData}>{row[7]}</td>
                                <td style={infoPageStyles.tableData}>{row[8]}</td>
                                <td style={infoPageStyles.tableData}>{row[9]}</td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            ) : (
                <p style={infoPageStyles.loadingText}>No data available</p>
            )}
        </div>
    );
};

export default DataInfo;
