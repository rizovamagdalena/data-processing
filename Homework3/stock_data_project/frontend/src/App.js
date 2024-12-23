import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./Home";
import MostTradedStocks from "./MostTradedStocks";  // Other pages
import Comparison from "./Comparison";
import StockTrends from "./StockTrends";
import Search from "./Search"; // Info page for stock details
import DataInfo from "./DataInfo"; //

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/most-traded" element={<MostTradedStocks />} />
                <Route path="/comparison" element={<Comparison />} />
                <Route path="/stock-trends" element={<StockTrends />} />
                <Route path="/search" element={<Search />} />
                <Route path="/data-info/:code" element={<DataInfo />} />

            </Routes>
        </Router>
    );
};

export default App;
