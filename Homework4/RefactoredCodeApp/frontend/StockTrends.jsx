import React, {useEffect, useState} from "react";
import axios from "axios";
import {Line} from "react-chartjs-2";
import CircularProgress from "@mui/material/CircularProgress";
import {type} from "@testing-library/user-event/dist/type"; // You may need to install @mui/material
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

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
                setStockCodes(response.data.stocks);
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
            console.log("Stock Data:", response.data); // Log the response data to check its structure
            const stockData = Array.isArray(response.data) ? response.data : Object.values(response.data);
            console.log("Stock Data: ", stockData);
            console.log("Stock Data type:", typeof stockData)
            setSelectedStockCode(code);
            setSelectedStockData(stockData);
            } catch (error)
            {
                 console.error("Error fetching stock data:", error);
            }
        setLoading(false);
        };

    // Prepare chart data for Chart.js
    const prepareChartData = (data) => {
        if (!data || data.length === 0 || !Array.isArray(data)) return null;

        data = data.flat();
        console.log("posle if statement:", data);


        const parsePrice = (price) => {
             if (!price || typeof price !== "string") return 0; // Default to 0 if invalid
             return parseFloat(price.replace(",", ""));
        };

        // Create labels and datasets
        const labels = data.map((item) => item[1]); // Assuming the date or some category is in item[1]
        console.log("Labels: ", labels);


        const datasets = [
              {
                  label: "Average Price",
                  data: data.map((item) => parsePrice(item[2])), // Assuming avg_price is at index 2
                  borderColor: "#0ac4ff",
                  borderWidth: 2,
                  tension: 0.3,
                  pointRadius: 0,
              },
              {
                  label: "Last Price",
                  data: data.map((item) => parsePrice(item[3])), // Assuming last_price is at index 3
                  borderColor: "#ff6f61",
                  borderWidth: 2,
                  tension: 0.3,
                  pointRadius: 0,
              },
              {
                  label: "Max Price",
                  data: data.map((item) => parsePrice(item[4])), // Assuming max_price is at index 4
                  borderColor: "#28a745",
                  borderWidth: 2,
                  tension: 0.3,
                  pointRadius: 0,
              },
              {
                  label: "Min Price",
                  data: data.map((item) => parsePrice(item[5])), // Assuming min_price is at index 5
                  borderColor: "#ffc107",
                  borderWidth: 2,
                  tension: 0.3,
                  pointRadius: 0,
              },
        ];

        console.log("printing datasets:", datasets);

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
