import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";


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
  console.log("IN ADIN")

  const [stockInfo, setStockInfo] = useState(null);
  const [loading, setLoading] = useState(false); // To track loading state

  // Hardcoded issuer_code for ADIN
  const issuer_code = "ADIN";

  // Function to fetch stock data for ADIN
  const fetchStockInfo = async () => {
    setLoading(true);
    try {
      // Assuming Flask is running on localhost:5000
      console.log("TRYING...");

      const response = await axios.get('http://localhost:5000/api/stocks/ADIN');
      console.log("Received stock data:", response.data);
      setStockInfo(response.data);
    } catch (error) {
      console.error("Error fetching stock info:", error);
      alert("Failed to load stock data, please try again later.");
    }
    setLoading(false);
  };


  // Fetch stock info on mount
  useEffect(() => {
    fetchStockInfo(); // Fetch data for ADIN
  }, []); // Empty dependency array to run once on mount

  return (
      <div style={infoPageStyles.container}>
        {/* Display Issuer Code */}
        <h1 style={infoPageStyles.header}>Stock Information for ADIN</h1>

        {/* Display loading message */}
        {loading && <p>Loading...</p>}

        {/* Display stock info */}
        {stockInfo && !loading ? (
            <div>
              {/* Render the stock data here */}
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
            </div>
        ) : (
            <p>No data available</p>
        )}
      </div>
  );
};

export default Info;
