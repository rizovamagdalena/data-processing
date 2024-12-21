import React from "react";

const TopNews = () => {
    return (
        <div
            style={{
                backgroundColor: "#121639", // Set background to dark blue
                minHeight: "100vh", // Ensure the background covers the full viewport height
                color: "#FFFFFF", // Set text color to white
                fontFamily: "Arial, sans-serif",
                margin: 0, // Remove default margin
                padding: 0, // Remove default padding
            }}
        >
            <div
                className="news-container"
                style={{
                    width: "600px", /* Increased width */
                    margin: "50px auto",
                    border: "2px solid #00ffcc",
                    borderRadius: "8px",
                    padding: "30px", /* Increased padding */
                    backgroundColor: "#0a0f32", // Dark background for the news box
                }}
            >
                <div
                    className="news-title"
                    style={{
                        fontSize: "24px",
                        fontWeight: "bold",
                        marginBottom: "20px",
                        textAlign: "left",
                        borderBottom: "2px solid #00ffcc",
                        paddingBottom: "5px",
                    }}
                >
                    Top News
                </div>
                <ul
                    className="news-list"
                    style={{
                        maxHeight: "300px", /* Increased height for the scrollable list */
                        overflowY: "auto",
                        padding: "0",
                        margin: "0",
                    }}
                >
                    <li className="news-item" style={{ listStyle: "none", marginBottom: "10px", lineHeight: "1.5" }}>
                        30.10.2024 – Комерцијална Банка АД Скопје – Неревидирани биланс на успех 01.01. – 30.09.
                    </li>
                    <li className="news-item" style={{ listStyle: "none", marginBottom: "10px", lineHeight: "1.5" }}>
                        31.7.2024 – Комерцијална Банка АД Скопје – Неревидирани финансиски извештаи 01.01. – 30.06.
                    </li>
                    <li className="news-item" style={{ listStyle: "none", marginBottom: "10px", lineHeight: "1.5" }}>
                        31.7.2024 – Комерцијална Банка АД Скопје – Неревидирани финансиски извештаи 01.01. – 30.06.
                    </li>
                    <li className="news-item" style={{ listStyle: "none", marginBottom: "10px", lineHeight: "1.5" }}>
                        25.4.2024 – Комерцијална Банка АД Скопје – Неревидирани биланс на успех 01.01. – 31.03.
                    </li>
                    <li className="news-item" style={{ listStyle: "none", marginBottom: "10px", lineHeight: "1.5" }}>
                        27.3.2024 – Комерцијална Банка АД Скопје – Ревидирани финансиски извештаи
                    </li>
                    <li className="news-item" style={{ listStyle: "none", marginBottom: "10px", lineHeight: "1.5" }}>
                        30.1.2024 – Комерцијална Банка АД Скопје – Неревидирани финансиски извештаи 01.01. – 31.12.
                    </li>
                    <li className="news-item" style={{ listStyle: "none", marginBottom: "10px", lineHeight: "1.5" }}>
                        30.1.2024 – Комерцијална Банка АД Скопје – Неревидирани финансиски извештаи 01.01. – 31.12.
                    </li>
                    <li className="news-item" style={{ listStyle: "none", marginBottom: "0", lineHeight: "1.5" }}>
                        26.10.2023 – Комерцијална Банка АД Скопје – Неревидирани биланс на успех 01.01. – 30.09.
                    </li>
                </ul>
            </div>
        </div>
    );
};

export default TopNews;
