import React from 'react';

const Comparison = () => {
    return (
        <div
            style={{
                backgroundColor: '#12192c', // Dark background
                color: 'white',
                fontFamily: 'Arial, sans-serif',
                textAlign: 'center',
                minHeight: '100vh', // Ensures the body spans the full height of the viewport
                margin: 0,
                padding: 0,
            }}
        >
            <h1>Comparison</h1>
            <div
                className="container"
                style={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    gap: '30px',
                    padding: '20px',
                }}
            >
                <div>
                    <h2>KMB</h2>
                    <div
                        className="chart-box"
                        style={{
                            backgroundColor: 'white',
                            border: '1px solid #cccccc',
                            borderRadius: '5px',
                            padding: '15px',
                            width: '300px',
                            height: '300px',
                        }}
                    >
                        <img
                            src="kmb-chart.png"
                            alt="KMB Chart"
                            className="chart"
                            style={{
                                width: '100%',
                                height: '100%',
                                objectFit: 'contain',
                            }}
                        />
                    </div>
                </div>
                <div>
                    <h2>REPL</h2>
                    <div
                        className="chart-box"
                        style={{
                            backgroundColor: 'white',
                            border: '1px solid #cccccc',
                            borderRadius: '5px',
                            padding: '15px',
                            width: '300px',
                            height: '300px',
                        }}
                    >
                        <img
                            src="repl-chart.png"
                            alt="REPL Chart"
                            className="chart"
                            style={{
                                width: '100%',
                                height: '100%',
                                objectFit: 'contain',
                            }}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Comparison;
