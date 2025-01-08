import React, { useState } from 'react';
import Chatbot from './components/Chatbot';
import Sidebar from './components/Sidebar';
import Message from './components/Message';
import './styles/App.css';

const App = () => {
  const [messages, setMessages] = useState([]);

  const handleQuerySubmit = async (query) => {
    // Add user message to the chat
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: query, sender: 'user' }
    ]);

    // Fetch the generated SQL query and response from backend
    const response = await fetch('http://127.0.0.1:8000/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });

    const result = await response.json();

    // Add bot response (SQL query + formatted result) to the chat
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: result.sqlQuery, sender: 'bot' },
      { text: result.queryResult, sender: 'bot' },
    ]);
  };

  return (
    <div className="app">
      <div className="sidebar-container">
        <Sidebar />
      </div>
      <div className="chat-container">
        <Chatbot onQuerySubmit={handleQuerySubmit} />
        <div className="messages">
          {messages.map((msg, index) => (
            <Message key={index} text={msg.text} sender={msg.sender} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default App;

// import React, { useState } from 'react';
// import Chatbot from './components/Chatbot';
// import Sidebar from './components/Sidebar';
// import Message from './components/Message';
// import './styles/App.css';

// const App = () => {
//   const [messages, setMessages] = useState([]);

//   const handleQuerySubmit = async (query) => {
//     // Add user message to the chat
//     setMessages([...messages, { text: query, sender: 'user' }]);

//     // Fetch the generated SQL query and response from backend
//     const response = await fetch('http://127.0.0.1:8000/query/ask', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ query }),
//     });

//     const result = await response.json();

//     // Add bot response (SQL query + formatted result) to the chat
//     setMessages([
//       ...messages,
//       { text: result.sqlQuery, sender: 'bot' },
//       { text: result.queryResult, sender: 'bot' },
//     ]);
//   };

//   return (
//     <div className="app">
//       <div className="sidebar-container">
//         <Sidebar />
//       </div>
//       <div className="chat-container">
//         <Chatbot onQuerySubmit={handleQuerySubmit} />
//         <div className="messages">
//           {messages.map((msg, index) => (
//             <Message key={index} text={msg.text} sender={msg.sender} />
//           ))}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default App;
