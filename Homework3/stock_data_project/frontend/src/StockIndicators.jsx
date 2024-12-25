import React, { useState, useEffect } from "react";
import axios from "axios";
import { CircularProgress, FormControl, InputLabel, Select, MenuItem, Button } from "@mui/material";

const StockIndicators = () => {
    const [stockCodes, setStockCodes] = useState([]);
    const [selectedStockCode, setSelectedStockCode] = useState("");
    const [selectedPeriod, setSelectedPeriod] = useState("1D"); // Default to "1D" for one day
    const [stockData, setStockData] = useState(null);
    const [loading, setLoading] = useState(false);

    // Fetch stock codes
    useEffect(() => {
        const fetchStockCodes = async () => {
            try {
                const response = await axios.get("http://localhost:5000/api/stocks");
                setStockCodes(Object.keys(response.data)); // Assuming stock codes are the keys
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
            const response = await axios.get(`http://localhost:5000/stock/stock_indicators/${code}/${period}`);
            setStockData(response.data); // Assuming the data is an array of objects like [{date, cci, vpt, signal}]
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
            <div style={{ marginTop: "30px", overflowX: "auto" }}>
                <table style={{ width: "100%", borderCollapse: "collapse", borderRadius: "8px" }}>
                    <thead>
                    <tr style={{ backgroundColor: "#0ac4ff", color: "white", textAlign: "left" }}>
                        <th style={{ padding: "12px", borderBottom: "2px solid #ddd" }}>Date</th>
                        <th style={{ padding: "12px", borderBottom: "2px solid #ddd" }}>CCI</th>
                        <th style={{ padding: "12px", borderBottom: "2px solid #ddd" }}>VPT</th>
                        <th style={{ padding: "12px", borderBottom: "2px solid #ddd" }}>Signal</th>
                    </tr>
                    </thead>
                    <tbody>
                    {stockData.map((indicator, index) => (
                        <tr key={index} style={{ borderBottom: "1px solid #ddd" }}>
                            <td style={{ padding: "10px", textAlign: "left" }}>{indicator.date}</td>
                            <td style={{ padding: "10px", textAlign: "left" }}>{indicator.cci}</td>
                            <td style={{ padding: "10px", textAlign: "left" }}>{indicator.vpt}</td>
                            <td style={{ padding: "10px", textAlign: "left" }}>{indicator.signal}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        );
    };

    return (
        <div style={{ padding: '40px', background: "linear-gradient(to right, #23395d, #0a2440)", minHeight: "100vh" }}>
            <h1 style={{ color: "white", textAlign: "center", marginBottom: "30px", fontWeight: "bold" }}>Stock Indicators</h1>

            {/* Dropdown for Stock Codes */}
            <FormControl fullWidth style={{ marginBottom: '20px' }}>
                <InputLabel style={{ color: "#fff" }}>Stock Code</InputLabel>
                <Select
                    value={selectedStockCode}
                    onChange={handleStockChange}
                    style={{ backgroundColor: "#fff", borderRadius: "8px" }}
                >
                    {stockCodes.map((code) => (
                        <MenuItem key={code} value={code}>{code}</MenuItem>
                    ))}
                </Select>
            </FormControl>

            {/* Dropdown for Period (1D, 1W, 1M) */}
            <FormControl fullWidth style={{ marginBottom: '20px' }}>
                <InputLabel style={{ color: "#fff" }}>Period</InputLabel>
                <Select
                    value={selectedPeriod}
                    onChange={handlePeriodChange}
                    style={{ backgroundColor: "#fff", borderRadius: "8px" }}
                >
                    <MenuItem value="1D">1 Day</MenuItem>
                    <MenuItem value="1W">1 Week</MenuItem>
                    <MenuItem value="1M">1 Month</MenuItem>
                </Select>
            </FormControl>

            {/* Loading spinner */}
            {loading && <CircularProgress style={{ display: "block", margin: "20px auto", color: "#0ac4ff" }} />}

            {/* Render stock indicators table */}
            {renderTable()}
        </div>
    );
};

export default StockIndicators;
