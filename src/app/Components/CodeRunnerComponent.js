import React, { useState, useEffect } from "react";
import axios from 'axios';

function CodeRunnerComponent({ codeRequirements, user }) {
  const [user, loading, auth_error] = useAuthState(auth);
  const [language, setLanguage] = useState("Python");
  const [code, setCode] = useState("");
  const [output, setOutput] = useState([]);
  const [expandOutput, setExpandOutput] = useState(false);
  const [error, setError] = useState("");
  const [container_name, setContainerName] = useState("");
  const [params, setParams] = useState({});
  const [evaluation, setEvaluation] = useState("");

  useEffect(() => {
    setContainerName(user ? "docker_" + user.uid : "default_container_name");
  }, [user]);

  useEffect(() => {
    setParams({
      language: language,
      code: code,
      container_name: container_name,
      code_output: output,
    });
  }, [language, code, codeRequirements, container_name, output]);

  const handleRequest = async (url) => {
    try {
      const response = await axios.post(`http://localhost:5000/${url}`, params);
      
      setError(response?.data?.message || '');
      setOutput(response?.data?.output || []);
      setError(response?.data?.error || '');
      setCode(response?.data?.code || '');
      setExpandOutput(true);
      setEvaluation(response?.data?.evaluation || '');

      consolse.log(response.data);

      return response.data;
    } catch (e) {
      setError(e.message);
      setExpandOutput(false);
      return null;
    }
  };

  const generateCode = () => handleRequest("get-initial-code");
  const runCode = () => handleRequest("run-code");
  const improveCode = () => handleRequest("improve-code");
  const evaluateCode = () => handleRequest("evaluate-code");

  async function generateWorkingCode() {

    e.preventDefault();
    
    await generateCode();

    while (evaluation === "no") {
      await improveCode();
      await runCode();
      await evaluateCode();
    }
  }

  return (
    // Your JSX goes here
    
  );
}

export default CodeRunnerComponent;