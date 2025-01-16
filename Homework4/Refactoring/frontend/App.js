import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./Home";
import MostTradedStocks from "./MostTradedStocks";  // Other pages
import StockIndicators from "./StockIndicators";
import StockTrends from "./StockTrends";
import Search from "./Search"; // Info page for stock details
import DataInfo from "./DataInfo"; //

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/most-traded" element={<MostTradedStocks />} />
                <Route path="/stock_indicators/ADIN/1D" element={<StockIndicators />} />
                <Route path="/stock-trends" element={<StockTrends />} />
                <Route path="/search" element={<Search />} />
                <Route path="/api/stocks/:code" element={<DataInfo />} />

            </Routes>
        </Router>
    );
};

export default App;
