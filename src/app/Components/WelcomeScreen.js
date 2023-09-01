import React, { useState, useEffect } from 'react';
import axios from 'axios';  // Ensure axios is installed

const WelcomeScreen = () => {
  const [functions, setFunctions] = useState([]);

  useEffect(() => {
    // Fetch the functions from the database
    axios.get('localhost:5000/search-code?query=') // Change the endpoint if needed
      .then(response => {
        setFunctions(response.data.results);
      })
      .catch(error => {
        console.error("There was an error fetching the data:", error);
      });
  }, []);

  return (
    <div>
      <h1>Welcome to the Code Runner App</h1>
      <p>Select a function to start:</p>
      <ul>
        {functions.map((func, index) => (
          <li key={index}>
            {func.description} {/* Or whatever key contains the function description */}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default WelcomeScreen;
