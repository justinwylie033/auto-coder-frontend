const { useEffect } = require("react");

const CodeRunner = () => {
    const [language, setLanguage] = useState("Python");
    const [codeRequirements, setCodeRequirements] = useState("");
    const [code, setCode] = useState("");
    const [output, setOutput] = useState([]);
    const [expandOutput, setExpandOutput] = useState(false);
    const [error, setError] = useState("");
    const [user, loading, fb_error] = useAuthState(auth);
    const [container_name, setContainerName] = useState(user ? "docker_" + user.uid : "default_container_name");
    const [params, setParams] = useState({ language: language, code: code, code_requirements: codeRequirements, container_name: container_name, code_output: output  });

  
    useEffect(() => {
      setContainerName(user ? "docker_" + user.uid : "default_container_name");
    }, [user]);

    useEffect(() => {
        setParams({ language: language, code: code, code_requirements: codeRequirements, container_name: container_name, code_output: output  });
    }, [language, code, codeRequirements, container_name, output]);

    const handleRequest = async (url, { params }) => {
        try {
          const response = await axios.post(`http://localhost:5000/${url}`, params);
          if (response.status >= 400) {
            throw new Error(response.data.message);
          }
          return response.data;
        } catch (e) {
          setError(e.message);
          setExpandOutput(false);
          return null;
        }
    };

const generateCode = async () => {
    let generateResponse = await handleRequest("get-initial-code");

    try {
        generateResponse?.code? setCode(generateResponse.code): setCode("");
        generateResponse?.error? setError(generateResponse.error) : setError("");
    }catch(e){
         setError(`An error occurred while generating the code: ${e.message}`);



const runCode = async () => {
  
    let runResponse = await handleRequest("run-code");
    try {
        runResponse?.output? setOutput(runResponse.output): setOutput([] && setError("Error running the code."));
        runResponse?.error? setError(runResponse.error) : setError("");
    }catch(e){
      setError(`An error occurred while running the code: ${e.message}`);
    }
};

const improveCode = async () => {
    let improveResponse = await handleRequest("improve-code");

    try {

    improveResponse?.code? setCode(improveResponse.code): setError("Error improving the code.");
    improveResponse?.error? setError(improveResponse.error) : setError("");
    }catch(e){
    setError(`An error occurred while improving the code: ${e.message}`);
    setCode("");
    setExpandOutput(false);
}
  
    let evaluationResponse = await handleRequest("evaluate-code");
    if (evaluationResponse.evaluation === 'no') {
      let improveResponse = await handleRequest("improve-code");
      setError(evaluationResponse.error);
      setOutput(runResponse.output);
      return runAndImproveCode(improveResponse.code, output, attempts + 1);
    }
    
    return code;
  };