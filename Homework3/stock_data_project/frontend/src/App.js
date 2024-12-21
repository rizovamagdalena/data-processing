import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./Home";
import MostTradedStocks from "./MostTradedStocks";  // Other pages
import Comparison from "./Comparison";
import TopNews from "./TopNews";
import Search from "./Search"; // Info page for stock details
import Info from "./Info"; //

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/most-traded" element={<MostTradedStocks />} />
                <Route path="/comparison" element={<Comparison />} />
                <Route path="/top-news" element={<TopNews />} />
                <Route path="/search" element={<Search />} />
                <Route path="/info/:code" element={<Info />} />

            </Routes>
        </Router>
    );
};

export default App;