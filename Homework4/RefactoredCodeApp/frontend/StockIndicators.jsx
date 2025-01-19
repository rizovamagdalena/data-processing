import React, { useState, useEffect } from "react";
import axios from "axios";
import { CircularProgress, FormControl, InputLabel, Select, MenuItem } from "@mui/material";
import { Box } from "@mui/system";

const styles = {
    container: {
        padding: '40px',
        background: "linear-gradient(to right, #23395d, #0a2440)",
        minHeight: "100vh",
        color: "white",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
    },
    header: {
        fontSize: "2.5rem",
        textAlign: "center",
        marginBottom: "20px",
        fontWeight: "bold",
        color: "#fff",  // Ensure header color is white
    },
    controls: {
        width: "100%",
        maxWidth: "600px",
        display: "grid",
        gridTemplateColumns: "repeat(2, 1fr)",
        gap: "20px",
        marginBottom: "40px",
    },
    formControl: {
        marginBottom: "20px",
        backgroundColor: "#fff",
        borderRadius: "8px",
    },
    inputLabel: {
        color: "#23395d",  // Set label color to dark shade
    },
    select: {
        backgroundColor: "#fff",
        borderRadius: "8px",
        color: "#23395d",  // Dark text for better contrast in select input
    },
    loadingSpinner: {
        display: "block",
        margin: "20px auto",
        color: "#0ac4ff",
    },
    table: {
        width: "100%",
        borderCollapse: "collapse",
        borderRadius: "8px",
        boxShadow: "0px 4px 12px rgba(0, 0, 0, 0.2)",
        backgroundColor: "#fff",
        marginTop: '20px',
    },
    headerRow: {
        backgroundColor: "#0ac4ff",
        color: "#23395d", // Text color for better visibility
        textAlign: "left",
    },
    headerCell: {
        padding: "15px",
        borderBottom: "2px solid #ddd",
        fontWeight: "bold",
        color: "#23395d",  // Dark color for header text in the table
    },
    rowEven: {
        borderBottom: "1px solid #ddd",
        backgroundColor: "#f7f7f7",
    },
    rowOdd: {
        borderBottom: "1px solid #ddd",
        backgroundColor: "#ffffff",  // Slightly contrasting background for odd rows
    },
    cell: {
        padding: "12px",
        textAlign: "left",
        color: "#23395d",  // Dark color for table cell text
    },
};

const StockIndicators = () => {
    const [stockCodes, setStockCodes] = useState([]);
    const [selectedStockCode, setSelectedStockCode] = useState("");
    const [selectedPeriod, setSelectedPeriod] = useState();
    const [stockData, setStockData] = useState(null);
    const [loading, setLoading] = useState(false);

    // Fetch stock codes
    useEffect(() => {
        const fetchStockCodes = async () => {
            try {
                const response = await axios.get("http://localhost:5000/api/stocks");
                console.log("API Response:", response.data);
                setStockCodes(response.data.stocks);//setStockCodes(Object.keys(response.data));
                console.log("Stock Codes:", Object.keys(response.data));
            } catch (error) {
                console.error("Error fetching stock codes:", error);
            }
        };
        fetchStockCodes();
    }, []);

    // Fetch stock indicators for the selected code and period
    const fetchStockIndicators = async (code, period) => {
        setLoading(true);
        try {
            const response = await axios.get(`http://localhost:5000/api/stock_indicators/${code}/${period}`);
            //console.log("Stock Data:", response.data);
            setStockData(response.data.indicators);//setStockData(response.data)
        } catch (error) {
            console.error("Error fetching stock indicators:", error);
        }
        setLoading(false);
    };

    const handleStockChange = (event) => {
        const selectedCode = event.target.value;
        setSelectedStockCode(selectedCode);
        fetchStockIndicators(selectedCode, selectedPeriod);  // Fetch for default period ("1D")
    };

    const handlePeriodChange = (event) => {
        const period = event.target.value;
        setSelectedPeriod(period);
        if (selectedStockCode) {
            fetchStockIndicators(selectedStockCode, period); // Re-fetch for the selected period
        }
    };

    const renderTable = () => {
        if (!stockData) return null;

        return (
            <Box sx={{ overflowX: 'auto', marginTop: 3 }}>
                <table style={styles.table}>
                    <thead>
                    <tr style={styles.headerRow}>
                        <th style={styles.headerCell}>Date</th>
                        <th style={styles.headerCell}>CCI</th>
                        <th style={styles.headerCell}>VPT</th>
                        <th style={styles.headerCell}>Signal</th>
                    </tr>
                    </thead>
                    <tbody>
                    {stockData.map((indicator, index) => (
                        <tr key={index} style={index % 2 === 0 ? styles.rowEven : styles.rowOdd}>
                            <td style={styles.cell}>{indicator[1]}</td>
                            <td style={styles.cell}>{indicator[3]}</td>
                            <td style={styles.cell}>{indicator[4]}</td>
                            <td style={styles.cell}>{indicator[5]}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </Box>
        );
    };

    return (
        <div style={styles.container}>
            <Box sx={{ maxWidth: 1200, margin: '0 auto' }}>
                <h1 style={styles.header}>Stock Indicators</h1>

                <div style={styles.controls}>
                    {/* Dropdown for Stock Codes */}
                    <FormControl fullWidth style={styles.formControl}>
                        <InputLabel style={styles.inputLabel}>Stock Code</InputLabel>
                        <Select
                            value={selectedStockCode}
                            onChange={handleStockChange}
                            style={styles.select}
                        >
                            {/* Log stock codes */}
                            {stockCodes.map((code) => (
                                <MenuItem key={code} value={code}>{code}</MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    {/* Dropdown for Period (1D, 1W, 1M) */}
                    <FormControl fullWidth style={styles.formControl}>
                        <InputLabel style={styles.inputLabel}>Period</InputLabel>
                        <Select
                            value={selectedPeriod}
                            onChange={handlePeriodChange}
                            style={styles.select}
                        >
                            <MenuItem value="1D">1 Day</MenuItem>
                            <MenuItem value="1W">1 Week</MenuItem>
                            <MenuItem value="1M">1 Month</MenuItem>
                        </Select>
                    </FormControl>
                </div>

                {/* Loading spinner */}
                {loading && <CircularProgress style={styles.loadingSpinner} />}

                {/* Render stock indicators table */}
                {renderTable()}
            </Box>
        </div>
    );
};

export default StockIndicators;
