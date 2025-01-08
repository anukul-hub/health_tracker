import React from 'react';
import ReactDOM from 'react-dom/client'; // Import from 'react-dom/client'
import './index.css'; // Global styles
import App from './App'; // The main App component
import reportWebVitals from './reportWebVitals'; // Optional for performance tracking

// Rendering the App component to the root element
const root = ReactDOM.createRoot(document.getElementById('root')); // Create a root
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Optional: Performance tracking
reportWebVitals();
