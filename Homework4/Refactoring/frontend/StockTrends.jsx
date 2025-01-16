import React, { useState, useEffect } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import { Chart as ChartJS } from "chart.js/auto";
import CircularProgress from "@mui/material/CircularProgress"; // You may need to install @mui/material

const styles = {
    container: {
        display: "flex",
        height: "100vh",
        backgroundColor: "#f7f9fc",
        fontFamily: "'Roboto', sans-serif",
    },
    content: {
        flex: 3,
        padding: "20px",
        overflowY: "auto",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
    },
    sidebar: {
        flex: 1,
        padding: "20px",
        overflowY: "auto",
        backgroundColor: "#ffffff",
        borderLeft: "1px solid #d1d9e6",
    },
    title: {
        color: "#007bff",
        textAlign: "center",
        marginBottom: "20px",
    },
    noDataMessage: {
        textAlign: "center",
        color: "#666",
        fontSize: "18px",
    },
    stockCode: {
        cursor: "pointer",
        padding: "12px 16px",
        margin: "5px 0",
        borderRadius: "5px",
        backgroundColor: "#f8f9fa",
        color: "#333",
        fontWeight: "bold",
        textAlign: "center",
        transition: "background-color 0.3s, color 0.3s",
    },
    activeStockCode: {
        backgroundColor: "#007bff",
        color: "#ffffff",
    },
    chartContainer: {
        width: "100%",
        maxWidth: "800px",
    },
};

const StockPriceTrends = () => {
    const [stockCodes, setStockCodes] = useState([]);
    const [selectedStockCode, setSelectedStockCode] = useState(null);
    const [selectedStockData, setSelectedStockData] = useState([]);
    const [loading, setLoading] = useState(false);

    // Fetch stock codes on load
    useEffect(() => {
        const fetchStockCodes = async () => {
            try {
                const response = await axios.get("http://localhost:5000/api/stocks");
                setStockCodes(Object.keys(response.data));
            } catch (error) {
                console.error("Error fetching stock codes:", error);
            }
        };
        fetchStockCodes();
    }, []);

    // Fetch data for a specific stock code
    const fetchStockData = async (code) => {
        setLoading(true);
        try {
            const response = await axios.get(`http://localhost:5000/api/stocks/${code}`);
            const stockData = response.data.flat().reverse();
            setSelectedStockCode(code);
            setSelectedStockData(stockData);
        } catch (error) {
            console.error("Error fetching stock data:", error);
        }
        setLoading(false);
    };

    // Prepare chart data for Chart.js
    const prepareChartData = (data) => {
        if (!data || data.length === 0) return null;

        const parsePrice = (price) => parseFloat(price.replace(",", ""));
        const labels = data.map((item) => item.date);
        const datasets = [
            { label: "Average Price", key: "avg_price", color: "#0ac4ff" },
            { label: "Last Price", key: "last_price", color: "#ff6f61" },
            { label: "Max Price", key: "max_price", color: "#28a745" },
            { label: "Min Price", key: "min_price", color: "#ffc107" },
        ].map(({ label, key, color }) => ({
            label,
            data: data.map((item) => parsePrice(item[key])),
            borderColor: color,
            borderWidth: 2,
            tension: 0.3,
            pointRadius: 0,
        }));

        return { labels, datasets };
    };

    const chartData = prepareChartData(selectedStockData);

    return (
        <div style={styles.container}>
            <div style={styles.content}>
                <h1 style={styles.title}>Stock Price Trends</h1>
                {loading ? (
                    <CircularProgress />
                ) : chartData ? (
                    <div style={styles.chartContainer}>
                        <h2 style={{ ...styles.title, fontSize: "18px" }}>
                            Price Trends for {selectedStockCode}
                        </h2>
                        <Line
                            data={chartData}
                            options={{
                                responsive: true,
                                plugins: {
                                    legend: { position: "top" },
                                },
                                scales: {
                                    x: { grid: { display: false } },
                                    y: { grid: { color: "#ddd" } },
                                },
                            }}
                        />
                    </div>
                ) : (
                    <p style={styles.noDataMessage}>
                        Select a stock code to view trends.
                    </p>
                )}
            </div>
            <div style={styles.sidebar}>
                <h2 style={styles.title}>Stock Codes</h2>
                {stockCodes.map((code) => (
                    <div
                        key={code}
                        style={{
                            ...styles.stockCode,
                            ...(selectedStockCode === code ? styles.activeStockCode : {}),
                        }}
                        onClick={() => fetchStockData(code)}
                    >
                        {code}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default StockPriceTrends;