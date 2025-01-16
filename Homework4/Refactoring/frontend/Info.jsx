import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom"; // To access the route parameter
import axios from "axios";

// Inline styles for layout and presentation
const infoPageStyles = {
  container: {
    padding: "20px",
    textAlign: "center",
    color: "white",
    background: "linear-gradient(to right, #001232, #0a2440, #23395d)",
  },
  header: {
    fontSize: "2.5rem",
    marginBottom: "20px",
  },
  selector: {
    padding: "10px",
    fontSize: "1.2rem",
    backgroundColor: "#0ac4ff",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
  table: {
    marginTop: "20px",
    width: "80%",
    margin: "0 auto",
    borderCollapse: "collapse",
  },
  tableHeader: {
    backgroundColor: "#0ac4ff",
    color: "white",
    padding: "10px",
  },
  tableRow: {
    backgroundColor: "#23395d",
    color: "white",
    padding: "8px",
  },
  tableData: {
    padding: "8px",
    textAlign: "center",
  },
};

const Info = () => {
  const { issuer_code } = useParams(); // Get the issuer_code from the URL
  //const [stockInfo, setStockInfo] = useState(null);
  const [stockInfo, setStockInfo] = useState([]);
  const [period, setPeriod] = useState("ALL"); // Default period
  const [loading, setLoading] = useState(false); // To track loading state

  // Function to calculate the date range based on the selected period
  const getDateRange = (period) => {
    const endDate = new Date();
    let startDate = new Date();

    switch (period) {
      case "1D":
        startDate.setDate(endDate.getDate() - 1);
        break;
      case "7D":
        startDate.setDate(endDate.getDate() - 7);
        break;
      case "1M":
        startDate.setMonth(endDate.getMonth() - 1);
        break;
      case "1Y":
        startDate.setFullYear(endDate.getFullYear() - 1);
        break;
      default: // "ALL"
        startDate = null;
        break;
    }

    return {
      start_date: startDate ? startDate.toISOString().split("T")[0] : null, // Format to YYYY-MM-DD
      end_date: endDate.toISOString().split("T")[0], // Format to YYYY-MM-DD
    };
  };

  // Function to fetch stock data based on the period
  const fetchStockInfo = async (period) => {
    setLoading(true); // Set loading to true before fetching data

    const { start_date, end_date } = getDateRange(period); // Get the date range for the period

    try {
      const response = await axios.get(`/api/stocks/${issuer_code}`, {
        params: {
          start_date,
          end_date,
        },
      });
      setStockInfo(response.data.data); // Assuming the backend returns data in a 'data' field
    } catch (error) {
      console.error("Error fetching stock info:", error);
      alert("Failed to load stock data, please try again later.");
    }
    setLoading(false); // Set loading to false after data is fetched
  };

  // Fetch stock info on mount or when the issuer_code or period changes
  useEffect(() => {
    fetchStockInfo(period); // Fetch data based on the current period
  }, [issuer_code, period]); // Dependency on issuer_code and period

  return (
    <div style={infoPageStyles.container}>
      <h1 style={infoPageStyles.header}>Stock Information for {issuer_code}</h1>

      {/* Dropdown to select the period */}
      <div>
        <label>Select period: </label>
        <select
          value={period}
          onChange={(e) => setPeriod(e.target.value)} // Update period when user selects a new one
          style={infoPageStyles.selector}
        >
          <option value="1D">1 Day</option>
          <option value="7D">1 Week</option>
          <option value="1M">1 Month</option>
          <option value="1Y">1 Year</option>
          <option value="ALL">All Time</option>
        </select>
      </div>

      {/* Display loading message */}
      {loading && <p>Loading...</p>}

      {/* Display stock info */}
      {stockInfo && stockInfo.length > 0 ? (
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
            {stockInfo.map((row, index) => (
                <tr key={index} style={infoPageStyles.tableRow}>
                    <td style={infoPageStyles.tableData}>{row.date}</td>
                    <td style={infoPageStyles.tableData}>{row.last_price}</td>
                    <td style={infoPageStyles.tableData}>{row.max_price}</td>
                    <td style={infoPageStyles.tableData}>{row.min_price}</td>
                    <td style={infoPageStyles.tableData}>{row.avg_price}</td>
                    <td style={infoPageStyles.tableData}>{row.percent_change}</td>
                    <td style={infoPageStyles.tableData}>{row.quantity}</td>
                    <td style={infoPageStyles.tableData}>{row.revenue_best_denars}</td>
                    <td style={infoPageStyles.tableData}>{row.total_revenue_denars}</td>
                </tr>
            ))}
        </tbody>
    </table>
    ) : (
         <p>No data available</p>
        )}
    </div>
  );
};

export default Info;
