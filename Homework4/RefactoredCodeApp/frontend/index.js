// index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';  // Import App.js

// Create a root element and render the app inside it
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
