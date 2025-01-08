import React, { useState, useEffect } from 'react';
import '../styles/Sidebar.css';

const Sidebar = () => {
  const [tables, setTables] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedTable, setExpandedTable] = useState(null); // State to manage expanded table

  useEffect(() => {
    const fetchTables = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/tables/table-structure'); // Update the endpoint URL
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setTables(data);
      } catch (error) {
        setError('Error fetching table structure');
        console.error('Error fetching table structure:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTables();
  }, []);

  const toggleTable = (tableName) => {
    setExpandedTable(expandedTable === tableName ? null : tableName);
  };

  return (
    <div className="sidebar" aria-label="Sidebar with database tables">
      <h3 className="sidebar-header">Database Tables</h3>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p className="error" role="alert">{error}</p>
      ) : (
        <ul className="table-list">
          {tables.map((table, index) => (
            <li key={index} className="table-item">
              <div
                className="table-name"
                onClick={() => toggleTable(table.name)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => e.key === 'Enter' && toggleTable(table.name)}
                aria-expanded={expandedTable === table.name}
                aria-controls={`columns-${index}`}
              >
                <strong>{table.name}</strong>
              </div>
              {expandedTable === table.name && (
                <ul className="column-list" id={`columns-${index}`}>
                  {table.columns.map((column, idx) => (
                    <li key={idx} className="column-item">
                      {column}
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Sidebar;


// import React, { useState, useEffect } from 'react';
// import '../styles/Sidebar.css';

// const Sidebar = () => {
//   const [tables, setTables] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);
//   const [expandedTable, setExpandedTable] = useState(null); // State to manage expanded table

//   useEffect(() => {
//     const fetchTables = async () => {
//       try {
//         const response = await fetch('http://127.0.0.1:8000/tables/table-structure'); // Update the endpoint URL
//         if (!response.ok) {
//           throw new Error('Network response was not ok');
//         }
//         const data = await response.json();
//         setTables(data);
//       } catch (error) {
//         setError('Error fetching table structure');
//         console.error('Error fetching table structure:', error);
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchTables();
//   }, []);

//   const toggleTable = (tableName) => {
//     setExpandedTable(expandedTable === tableName ? null : tableName);
//   };

//   return (
//     <div className="sidebar">
//       <h3 className="sidebar-header">Database Tables</h3>
//       {loading ? (
//         <p>Loading...</p>
//       ) : error ? (
//         <p className="error">{error}</p>
//       ) : (
//         <ul className="table-list">
//           {tables.map((table, index) => (
//             <li key={index} className="table-item">
//               <div
//                 className="table-name"
//                 onClick={() => toggleTable(table.name)}
//               >
//                 <strong>{table.name}</strong>
//               </div>
//               {expandedTable === table.name && (
//                 <ul className="column-list">
//                   {table.columns.map((column, idx) => (
//                     <li key={idx} className="column-item">
//                       {column}
//                     </li>
//                   ))}
//                 </ul>
//               )}
//             </li>
//           ))}
//         </ul>
//       )}
//     </div>
//   );
// };

// export default Sidebar;


// import React, { useState, useEffect } from 'react';
// import '../styles/Sidebar.css';

// const Sidebar = () => {
//   const [tables, setTables] = useState([]);
//   const [loading, setLoading] = useState(true); // State for loading indicator
//   const [error, setError] = useState(null); // State for error handling

//   useEffect(() => {
//     const fetchTables = async () => {
//       try {
//         const response = await fetch('/table-structure'); // Adjusted the endpoint
//         if (!response.ok) {
//           throw new Error('Network response was not ok');
//         }
//         const data = await response.json();
//         setTables(data);
//       } catch (error) {
//         setError('Error fetching table structure');
//         console.error('Error fetching table structure:', error);
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchTables();
//   }, []);

//   return (
//     <div className="sidebar">
//       <h3>Database Tables</h3>
//       {loading ? (
//         <p>Loading...</p>
//       ) : error ? (
//         <p className="error">{error}</p>
//       ) : (
//         <ul>
//           {tables.map((table, index) => (
//             <li key={index}>
//               <strong>{table.name}</strong>
//               <ul>
//                 {table.columns.map((column, idx) => (
//                   <li key={idx}>{column}</li>
//                 ))}
//               </ul>
//             </li>
//           ))}
//         </ul>
//       )}
//     </div>
//   );
// };

// export default Sidebar;


// import React, { useState, useEffect } from 'react';
// import '../styles/Sidebar.css';

// const Sidebar = () => {
//   const [tables, setTables] = useState([]);

//   useEffect(() => {
//     const fetchTables = async () => {
//       try {
//         // Fetch table metadata from backend API using relative URL (after setting up proxy)
//         const response = await fetch('tables/table-structure'); // Proxy will forward this to the backend
//         const data = await response.json();
//         setTables(data);
//       } catch (error) {
//         console.error('Error fetching table structure:', error);
//       }
//     };

//     fetchTables();
//   }, []);

//   return (
//     <div className="sidebar">
//       <h3>Database Tables</h3>
//       <ul>
//         {tables.map((table, index) => (
//           <li key={index}>
//             <strong>{table.name}</strong>
//             <ul>
//               {table.columns.map((column, idx) => (
//                 <li key={idx}>{column}</li>
//               ))}
//             </ul>
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// };

// export default Sidebar;




// import React, { useState, useEffect } from 'react';
// import '../styles/Sidebar.css';

// const Sidebar = () => {
//   const [tables, setTables] = useState([]);

//   useEffect(() => {
//     // Fetch table metadata from backend API using relative URL (after setting up proxy)
//     fetch('tables/table-structure')  // Proxy will forward this to the backend
//       .then(response => response.json())
//       .then(data => setTables(data))
//       .catch(error => console.error('Error fetching table structure:', error));
//   }, []);

//   return (
//     <div className="sidebar">
//       <h3>Database Tables</h3>
//       <ul>
//         {tables.map((table, index) => (
//           <li key={index}>
//             <strong>{table.name}</strong>
//             <ul>
//               {table.columns.map((column, idx) => (
//                 <li key={idx}>{column}</li>
//               ))}
//             </ul>
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// };

// export default Sidebar;





// // import React, { useState, useEffect } from 'react';
// // import '../styles/Sidebar.css';

// // const Sidebar = () => {
// //   const [tables, setTables] = useState([]);

// //   useEffect(() => {
// //     // Fetch table metadata from backend API
// //     fetch('/backend/api/table-structure')  // This should match your backend route
// //       .then(response => response.json())
// //       .then(data => setTables(data))
// //       .catch(error => console.error('Error fetching table structure:', error));
// //   }, []);

// //   return (
// //     <div className="sidebar">
// //       <h3>Database Tables</h3>
// //       <ul>
// //         {tables.map((table, index) => (
// //           <li key={index}>
// //             <strong>{table.name}</strong>
// //             <ul>
// //               {table.columns.map((column, idx) => (
// //                 <li key={idx}>{column}</li>
// //               ))}
// //             </ul>
// //           </li>
// //         ))}
// //       </ul>
// //     </div>
// //   );
// // };

// // export default Sidebar;
