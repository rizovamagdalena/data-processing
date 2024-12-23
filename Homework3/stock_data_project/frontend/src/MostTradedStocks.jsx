import React, { useState, useEffect } from "react";
import axios from "axios";

const MostTradedStocks = () => {
    const [stockCodes, setStockCodes] = useState([]);
    const [stockData, setStockData] = useState([]);
    const [filteredStockData, setFilteredStockData] = useState([]);
    const [loading, setLoading] = useState(false);

    const periods = ["1M", "1Y"]; // Keep only this month and this year
    const [selectedPeriod, setSelectedPeriod] = useState("1M"); // Default time period

    // Step 1: Fetch the list of stock codes
    const fetchStockCodes = async () => {
        setLoading(true);
        try {
            const response = await axios.get("http://localhost:5000/api/stocks");
            setStockCodes(Object.keys(response.data)); // Store stock codes
            fetchStockData(response.data); // Start fetching data for all stocks
        } catch (error) {
            console.error("Error fetching stock codes:", error);
        }
    };

    // Step 2: Fetch the stock data for each code with limited size
    const fetchStockData = async (codes) => {
        // Batch fetch in chunks of, e.g., 10 codes at a time
        const chunkSize = 10;
        const chunkedCodes = [];
        console.log(codes)
        for (let i = 0; i < codes.length; i += chunkSize) {
            chunkedCodes.push(codes.slice(i, i + chunkSize));
        }

        try {
            // Use `Promise.all` for concurrent fetching in batches
            const batchResponses = await Promise.all(
                chunkedCodes.map(async (chunk) => {
                    const stockDataPromises = chunk.map((code) =>
                        axios.get(`http://localhost:5000/api/stocks/${code}`)
                    );
                    return Promise.all(stockDataPromises);
                })
            );

            const allStockData = batchResponses.flat().map((res) => res.data.flat());
            console.log(allStockData);
            setStockData(allStockData);
            filterDataByPeriod(allStockData, selectedPeriod); // Filter data for selected period
        } catch (error) {
            console.error("Error fetching stock data:", error);
        }
        setLoading(false);
    };

    // Step 3: Filter stock data by the selected time period
    const filterDataByPeriod = (data, period) => {
        const currentDate = new Date();
        const startOfYear = new Date(currentDate.getFullYear(), 0, 1);
        const startOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);

        let filteredData = [];

        // Filter stocks based on selected period (1M or 1Y)
        data.forEach((stock) => {
            const stockTotal = stock.reduce((acc, row) => {
                const rowDate = parseDate(row.date);
                if ((period === "1M" && rowDate >= startOfMonth) ||
                    (period === "1Y" && rowDate >= startOfYear)) {
                    acc += row.quantity;
                }
                return acc;
            }, 0);

            if (stockTotal > 0) {
                filteredData.push({
                    stock: stock[0].code,
                    totalQuantity: stockTotal,
                });
            }
        });

        console.log("FILTERED "+ filteredData); // Log filtered data before setting it

        // Sort the stocks by total quantity in descending order
        filteredData.sort((a, b) => b.totalQuantity - a.totalQuantity);

        // Keep only the most traded (no duplicates)
        setFilteredStockData(filteredData);
    };

    // Helper functions to parse date
    const parseDate = (dateString) => {
        const [day, month, year] = dateString.split(".").map((part) => parseInt(part, 10));
        return new Date(year, month - 1, day);
    };

    useEffect(() => {
        fetchStockCodes(); // Fetch stock codes when component mounts
    }, []);

    useEffect(() => {
        if (stockData.length > 0) {
            filterDataByPeriod(stockData, selectedPeriod);
        }
    }, [selectedPeriod, stockData]);

    return (
        <div style={{ padding: "20px", color: "white", background: "linear-gradient(to right, #0a2a43, #003256, #16313d)" }}>
            <h1 style={{ textAlign: "center", fontSize: "2rem", color: "#F6C5A3" }}>Most Traded Stocks</h1>

            {/* Time Period Buttons */}
            <div style={{ margin: "20px 0", textAlign: "center" }}>
                {periods.map((period) => (
                    <button
                        key={period}
                        onClick={() => setSelectedPeriod(period)}
                        style={{
                            backgroundColor: selectedPeriod === period ? "#F0A000" : "#F6C5A3",
                            padding: "10px 20px",
                            fontSize: "1.1rem",
                            borderRadius: "25px",
                            margin: "0 10px",
                            border: "none",
                            cursor: "pointer",
                            transition: "background-color 0.3s",
                        }}
                    >
                        {period}
                    </button>
                ))}
            </div>

            {loading ? (
                <p style={{ textAlign: "center", fontSize: "1.2rem" }}>Loading...</p>
            ) : (
                <div>
                    {/* Display filtered stock data in a table */}
                    <table style={{ width: "100%", borderCollapse: "collapse", marginTop: "30px", borderRadius: "12px", boxShadow: "0 10px 30px rgba(0, 0, 0, 0.2)" }}>
                        <thead style={{ backgroundColor: "#1976D2", color: "white" }}>
                        <tr>
                            <th>Stock Code</th>
                            <th>Total Quantity</th>
                        </tr>
                        </thead>
                        <tbody>
                        {filteredStockData.slice(0, 20).map((stock, index) => (
                            <tr key={index} style={{ backgroundColor: "#223f5b", color: "white" }}>
                                <td>{stock.stock}</td>
                                <td>{stock.totalQuantity}</td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default MostTradedStocks;
