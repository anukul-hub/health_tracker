import React, { useState } from 'react';
import axios from 'axios'; // Import axios for HTTP requests
import '../styles/Chatbot.css';

const Chatbot = ({ onQuerySubmit }) => {
  const [userInput, setUserInput] = useState('');
  const [response, setResponse] = useState(null); // State to hold the response
  const [loading, setLoading] = useState(false); // State to show loading indicator
  const [error, setError] = useState(null); // State to hold error messages
  const [userQuestion, setUserQuestion] = useState(null); // State to store the user's question


  const handleInputChange = (event) => {
    setUserInput(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setResponse(null);
    setUserQuestion(userInput); // Store the user input before resetting

    try {
      const result = await axios.post('http://127.0.0.1:8000/query/ask', { question: userInput });
      setResponse(result.data); // Correctly accessing the response data
    } catch (err) {
      setError('An error occurred while processing your request.');
    } finally {
      setLoading(false);
      setUserInput('');
    }
  };

  return (
    <div className="chatbot">
      <div className="chatbox">
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={userInput}
            onChange={handleInputChange}
            placeholder="Ask me anything about your health data"
            className="chat-input"
          />
          <button type="submit" className="send-btn" disabled={loading}>
            {loading ? 'Sending...' : 'Send'}
          </button>
        </form>
        {loading && <div>Loading...</div>}
        {error && <div className="error">{error}</div>}
        {response && (
          <div className="response">
            <p><strong>User Question:</strong> {userQuestion}</p>
            <p><strong>SQL Query:</strong> {response.query}</p>
            <p><strong>Result:</strong> {JSON.stringify(response.result)}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Chatbot;

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

