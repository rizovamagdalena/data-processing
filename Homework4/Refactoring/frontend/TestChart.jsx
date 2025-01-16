import React from "react";
import { Line } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

// Register chart components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const TestChart = () => {
    const chartData = {
        labels: ['2024-12-01', '2024-12-02', '2024-12-03'],
        datasets: [
            {
                label: 'Sample Data',
                data: [150, 180, 170],
                borderColor: 'blue',
                backgroundColor: 'rgba(0, 123, 255, 0.2)',
                fill: true,
            },
        ],
    };

    return (
        <div style={{ width: "80%", margin: "0 auto", padding: "20px" }}>
            <h1>Test Chart</h1>
            <Line data={chartData} />
        </div>
    );
};

export default TestChart;