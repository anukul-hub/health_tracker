import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import '../styles/Chatbot.css';

const Chatbot = () => {
  const [userInput, setUserInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [chatHistory, setChatHistory] = useState([]); // State to store the conversation history
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const storedHistory = localStorage.getItem('chatHistory');
    if (storedHistory) {
      setChatHistory(JSON.parse(storedHistory));
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
  }, [chatHistory]);

  const handleInputChange = (event) => {
    setUserInput(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!userInput.trim()) return;

    setLoading(true);
    setError(null);

    const userMessage = { sender: 'user', text: userInput };
    setChatHistory((prev) => [...prev, userMessage]);

    try {
      const response = await axios.post('http://127.0.0.1:8000/query/ask', { question: userInput });

      const botMessage = {
        sender: 'bot',
        text: userInput, // The user's question
        query: response.data.query,
        result: response.data.result,
      };

      setChatHistory((prev) => [...prev, botMessage]);
    } catch (err) {
      setError('An error occurred while processing your request.');
      setChatHistory((prev) => [
        ...prev,
        { sender: 'bot', text: 'An error occurred while processing your request.' },
      ]);
    } finally {
      setLoading(false);
      setUserInput('');
    }
  };

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatHistory]);

  return (
    <div className="chatbot">
      <div className="chatbox">
        <div className="chat-history">
          {chatHistory.map((message, index) =>
            message.sender === 'user' ? (
              <div key={index} className="chat-message user-message">
                <p><strong>User Query:</strong> {message.text}</p>
              </div>
            ) : (
              <div key={index} className="chat-message bot-message">
                {/* <p><strong>Bot Response:</strong> {message.text}</p> */}
                {message.query && (
                  <>
                    <p><strong>SQL Query:</strong> {message.query}</p>
                    <p><strong>Result:</strong> {JSON.stringify(message.result, null, 2)}</p>
                  </>
                )}
              </div>
            )
          )}
          <div ref={messagesEndRef}></div>
        </div>
        <form onSubmit={handleSubmit} className="chat-form">
          <input
            type="text"
            value={userInput}
            onChange={handleInputChange}
            placeholder="Ask me anything about your health data"
            className="chat-input"
            aria-label="Chat input"
          />
          <button type="submit" className="send-btn" disabled={loading}>
            {loading ? 'Sending...' : 'Send'}
          </button>
        </form>
        {error && <div className="error">{error}</div>}
      </div>
    </div>
  );
};

export default Chatbot;

// import React, { useState, useEffect, useRef } from 'react';
// import axios from 'axios';
// import '../styles/Chatbot.css';

// const Chatbot = ({ onQuerySubmit }) => {
//   const [userInput, setUserInput] = useState('');
//   const [response, setResponse] = useState(null); // State to hold the response
//   const [loading, setLoading] = useState(false); // State to show loading indicator
//   const [error, setError] = useState(null); // State to hold error messages
//   const [userQuestion, setUserQuestion] = useState(null); // State to store the user's question
//   const [chatHistory, setChatHistory] = useState([]); // State to store the conversation history
//   const messagesEndRef = useRef(null); // Ref to handle auto-scroll

//   // Load chat history from localStorage on component mount
//   useEffect(() => {
//     const storedHistory = localStorage.getItem('chatHistory');
//     if (storedHistory) {
//       setChatHistory(JSON.parse(storedHistory));
//     }
//   }, []);

//   // Save chat history to localStorage whenever it changes
//   useEffect(() => {
//     localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
//   }, [chatHistory]);

//   const handleInputChange = (event) => {
//     setUserInput(event.target.value);
//   };

//   const handleSubmit = async (event) => {
//     event.preventDefault();
//     setLoading(true);
//     setError(null);
//     setResponse(null);
//     setUserQuestion(userInput); // Store the user input before resetting

//     const userMessage = { sender: 'user', text: userInput };
//     setChatHistory((prev) => [...prev, userMessage]);

//     try {
//       const result = await axios.post('http://127.0.0.1:8000/query/ask', { question: userInput });
//       const botMessage = {
//         sender: 'bot',
//         text: `SQL Query: ${result.data.query}, Result: ${JSON.stringify(result.data.result)}`,
//       };
//       setResponse(result.data); // Correctly accessing the response data
//       setChatHistory((prev) => [...prev, botMessage]);
//     } catch (err) {
//       const errorMessage = { sender: 'bot', text: 'An error occurred while processing your request.' };
//       setError('An error occurred while processing your request.');
//       setChatHistory((prev) => [...prev, errorMessage]);
//     } finally {
//       setLoading(false);
//       setUserInput('');
//     }
//   };

//   useEffect(() => {
//     if (messagesEndRef.current) {
//       messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
//     }
//   }, [chatHistory]);

//   return (
//     <div className="chatbot">
//       <div className="chatbox">
//         <div className="chat-history">
//           {chatHistory.map((message, index) => (
//             <div
//               key={index}
//               className={`chat-message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
//             >
//               <p>{message.text}</p>
//             </div>
//           ))}
//           <div ref={messagesEndRef}></div>
//         </div>
//         <form onSubmit={handleSubmit} className="chat-form">
//           <input
//             type="text"
//             value={userInput}
//             onChange={handleInputChange}
//             placeholder="Ask me anything about your health data"
//             className="chat-input"
//             aria-label="Chat input"
//           />
//           <button type="submit" className="send-btn" disabled={loading || !userInput.trim()}>
//             {loading ? 'Sending...' : 'Send'}
//           </button>
//         </form>
//         {loading && <div className="loading">Loading...</div>}
//         {error && <div className="error" role="alert">{error}</div>}
//         {response && (
//           <div className="response">
//             <p><strong>User Question:</strong> {userQuestion}</p>
//             <p><strong>SQL Query:</strong> {response.query}</p>
//             <p><strong>Result:</strong> {JSON.stringify(response.result)}</p>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// };

// export default Chatbot;

// import React, { useState, useEffect, useRef } from 'react';
// import axios from 'axios'; // Import axios for HTTP requests
// import '../styles/Chatbot.css';

// const Chatbot = ({ onQuerySubmit }) => {
//   const [userInput, setUserInput] = useState('');
//   const [response, setResponse] = useState(null); // State to hold the response
//   const [loading, setLoading] = useState(false); // State to show loading indicator
//   const [error, setError] = useState(null); // State to hold error messages
//   const [userQuestion, setUserQuestion] = useState(null); // State to store the user's question
//   const messagesEndRef = useRef(null); // Ref to handle auto-scroll

//   const handleInputChange = (event) => {
//     setUserInput(event.target.value);
//   };

//   const handleSubmit = async (event) => {
//     event.preventDefault();
//     setLoading(true);
//     setError(null);
//     setResponse(null);
//     setUserQuestion(userInput); // Store the user input before resetting

//     try {
//       const result = await axios.post('http://127.0.0.1:8000/query/ask', { question: userInput });
//       setResponse(result.data); // Correctly accessing the response data
//     } catch (err) {
//       setError('An error occurred while processing your request.');
//     } finally {
//       setLoading(false);
//       setUserInput('');
//     }
//   };

//   useEffect(() => {
//     if (messagesEndRef.current) {
//       messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
//     }
//   }, [response]);

//   return (
//     <div className="chatbot">
//       <div className="chatbox">
//         <form onSubmit={handleSubmit} className="chat-form">
//           <input
//             type="text"
//             value={userInput}
//             onChange={handleInputChange}
//             placeholder="Ask me anything about your health data"
//             className="chat-input"
//             aria-label="Chat input"
//           />
//           <button type="submit" className="send-btn" disabled={loading || !userInput.trim()}>
//             {loading ? 'Sending...' : 'Send'}
//           </button>
//         </form>
//         {loading && <div className="loading">Loading...</div>}
//         {error && <div className="error" role="alert">{error}</div>}
//         {response && (
//           <div className="response">
//             <p><strong>User Question:</strong> {userQuestion}</p>
//             <p><strong>SQL Query:</strong> {response.query}</p>
//             <p><strong>Result:</strong> {JSON.stringify(response.result)}</p>
//           </div>
//         )}
//         <div ref={messagesEndRef}></div>
//       </div>
//     </div>
//   );
// };

// export default Chatbot;

// import React, { useState } from 'react';
// import axios from 'axios'; // Import axios for HTTP requests
// import '../styles/Chatbot.css';

// const Chatbot = ({ onQuerySubmit }) => {
//   const [userInput, setUserInput] = useState('');
//   const [response, setResponse] = useState(null); // State to hold the response
//   const [loading, setLoading] = useState(false); // State to show loading indicator
//   const [error, setError] = useState(null); // State to hold error messages
//   const [userQuestion, setUserQuestion] = useState(null); // State to store the user's question


//   const handleInputChange = (event) => {
//     setUserInput(event.target.value);
//   };

//   const handleSubmit = async (event) => {
//     event.preventDefault();
//     setLoading(true);
//     setError(null);
//     setResponse(null);
//     setUserQuestion(userInput); // Store the user input before resetting

//     try {
//       const result = await axios.post('http://127.0.0.1:8000/query/ask', { question: userInput });
//       setResponse(result.data); // Correctly accessing the response data
//     } catch (err) {
//       setError('An error occurred while processing your request.');
//     } finally {
//       setLoading(false);
//       setUserInput('');
//     }
//   };

//   return (
//     <div className="chatbot">
//       <div className="chatbox">
//         <form onSubmit={handleSubmit}>
//           <input
//             type="text"
//             value={userInput}
//             onChange={handleInputChange}
//             placeholder="Ask me anything about your health data"
//             className="chat-input"
//           />
//           <button type="submit" className="send-btn" disabled={loading}>
//             {loading ? 'Sending...' : 'Send'}
//           </button>
//         </form>
//         {loading && <div>Loading...</div>}
//         {error && <div className="error">{error}</div>}
//         {response && (
//           <div className="response">
//             <p><strong>User Question:</strong> {userQuestion}</p>
//             <p><strong>SQL Query:</strong> {response.query}</p>
//             <p><strong>Result:</strong> {JSON.stringify(response.result)}</p>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// };

// export default Chatbot;

// import React, { useState } from 'react';
// import axios from 'axios'; // Import axios for HTTP requests
// import '../styles/Chatbot.css';

// const Chatbot = ({ onQuerySubmit }) => {
//   const [userInput, setUserInput] = useState('');
//   const [response, setResponse] = useState(null); // State to hold the response
//   const [loading, setLoading] = useState(false); // State to show loading indicator
//   const [error, setError] = useState(null); // State to hold error messages

//   const handleInputChange = (event) => {
//     setUserInput(event.target.value);
//   };

//   const handleSubmit = async (event) => {
//     event.preventDefault();
//     setLoading(true);
//     setError(null);
//     setResponse(null);

//     try {
//       const result = await axios.post('http://127.0.0.1:8000/query/ask', { question: userInput });
//       setResponse(result.result); // Assuming the backend returns { query: '', result: '' }
//     } catch (err) {
//       setError('An error occurred while processing your request.');
//     } finally {
//       setLoading(false);
//       setUserInput('');
//     }
//   };

//   return (
//     <div className="chatbot">
//       <div className="chatbox">
//         <form onSubmit={handleSubmit}>
//           <input
//             type="text"
//             value={userInput}
//             onChange={handleInputChange}
//             placeholder="Ask me anything about your health data"
//             className="chat-input"
//           />
//           <button type="submit" className="send-btn" disabled={loading}>
//             {loading ? 'Sending...' : 'Send'}
//           </button>
//         </form>
//         {loading && <div>Loading...</div>}
//         {error && <div className="error">{error}</div>}
//         {response && (
//           <div className="response">
//             <p><strong>SQL Query:</strong> {response.query}</p>
//             <p><strong>Result:</strong> {JSON.stringify(response.result)}</p>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// };

// export default Chatbot;

