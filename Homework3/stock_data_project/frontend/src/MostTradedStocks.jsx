import React from "react";

// Example table with hardcoded data
const Table = () => {
    const tableData = [
        { stock: "ADIN", price: "45.00", volume: "5000", change: "+1.5%" },
        { stock: "SHTN", price: "35.50", volume: "3000", change: "-0.8%" },
        { stock: "TLMN", price: "25.30", volume: "4000", change: "+2.1%" },
        // Add more rows as needed
    ];

    return (
        <div style={{ flex: 1, background: "#1a2b42", padding: "20px", borderRadius: "10px" }}>
            <h2 style={{ textAlign: "center", color: "#0ac4ff" }}>Most Traded Stocks</h2>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
                <thead>
                <tr style={{ background: "#0a2440", color: "#fff" }}>
                    <th style={{ padding: "10px", border: "1px solid #ccc" }}>Stock</th>
                    <th style={{ padding: "10px", border: "1px solid #ccc" }}>Price</th>
                    <th style={{ padding: "10px", border: "1px solid #ccc" }}>Volume</th>
                    <th style={{ padding: "10px", border: "1px solid #ccc" }}>Change</th>
                </tr>
                </thead>
                <tbody>
                {tableData.map((row, index) => (
                    <tr key={index}>
                        <td style={{ padding: "10px", border: "1px solid #ccc" }}>{row.stock}</td>
                        <td style={{ padding: "10px", border: "1px solid #ccc" }}>{row.price}</td>
                        <td style={{ padding: "10px", border: "1px solid #ccc" }}>{row.volume}</td>
                        <td style={{ padding: "10px", border: "1px solid #ccc" }}>{row.change}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
};

// Example list with hardcoded items
const List = () => {
    const listItems = [
        "Company A",
        "Company B",
        "Company C",
        "Company D",
        "Company E",
        // Add more items as needed
    ];

    return (
        <div style={{ flex: 1, background: "#1a2b42", padding: "20px", borderRadius: "10px" }}>
            <h2 style={{ textAlign: "center", color: "#0ac4ff" }}>Company List</h2>
            <ul style={{ listStyle: "none", padding: 0 }}>
                {listItems.map((item, index) => (
                    <li key={index} style={{ padding: "10px", borderBottom: "1px solid #ccc" }}>
                        {item}
                    </li>
                ))}
            </ul>
        </div>
    );
};

// Main component for Most Traded Stocks page
const MostTradedStocks = () => {
    return (
        <div
            style={{
                background: "linear-gradient(to right, #001232, #0a2440, #23395d)",
                color: "white",
                padding: "50px",
                height: "100vh",
                overflowY: "scroll",
            }}
        >
            <h1 style={{ textAlign: "center", fontSize: "3rem", letterSpacing: "0.1em" }}>Most Traded Stocks</h1>
            <div className="container" style={{ display: "flex", gap: "30px", justifyContent: "center" }}>
                <Table />
                <List />
            </div>
        </div>
    );
};

export default MostTradedStocks;
