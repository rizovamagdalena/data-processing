// src/pages/TopNews.jsx
import React from "react";

const topNewsPageStyles = {
body: {
fontFamily: "Arial, sans-serif",
display: "flex",
justifyContent: "center",
alignItems: "center",
height: "100vh",
margin: "0",
backgroundColor: "#f0f0f0",
},
title: {
fontSize: "2.5rem",
color: "#333",
},
};

const TopNews = () => {
return (
<div style={topNewsPageStyles.body}>
  <h1 style={topNewsPageStyles.title}>Top News Page</h1>
</div>
);
};

export default TopNews;