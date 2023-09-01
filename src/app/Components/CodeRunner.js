import React, { useReducer } from "react";
import styles from "../styles/CodeRunner.module.css";
import { useAuthState } from "react-firebase-hooks/auth";
import { auth } from "./firebase";
import { apiRequest } from "./api";
import ResultsSection from "./ResultsSection";
import SearchBox from "./SearchBox";

const initialState = {
  code_requirements: "",
  code: "",
  output: "",
  efficiency: "",
  error: "",
  statusMessage: "",
  isLoading: false,
  functionDescription: "",
};

function reducer(state, action) {
  switch (action.type) {
    case "UPDATE_STATE":
      return { ...state, ...action.payload };
    default:
      throw new Error("Unexpected action");
  }
}

const CodeRunner = () => {
  const [state, dispatch] = useReducer(reducer, initialState);
  const [user] = useAuthState(auth);

  const updateState = (data) =>
    dispatch({ type: "UPDATE_STATE", payload: data });

  const generateAndRunCode = async (e) => {
    e.preventDefault();

    let attempts = 0; // Track the number of attempts

    try {
      // Generate function
      updateState({ statusMessage: "Generating new code...", isLoading: true });
      const generatedCode = await apiRequest("generate-code", {
        prompt: state.code_requirements,
      });
      updateState({
        code: generatedCode.code,
        statusMessage: "Generated new code.",
      });

      // Install packages
      updateState({
        statusMessage: "Installing required packages...",
        isLoading: true,
      });
      await apiRequest("install-packages", { code: generatedCode.code });
      updateState({ statusMessage: "Packages installed successfully." });

      let codeToExecute = generatedCode.code;
      let executionResult;

      do {
        // Test/Execute
        updateState({
          statusMessage: "Testing/Executing code...",
          isLoading: true,
        });
        executionResult = await apiRequest("execute-code", {
          code: codeToExecute,
        });

        if (executionResult.status !== "success") {
          console.log("Attempting to fix code with data:", {
            code: codeToExecute,
            info: executionResult.error,
          }); // Add this line for logging
          updateState({
            error: executionResult.error,
            statusMessage: `Error encountered. Attempting to fix (Attempt ${
              attempts + 1
            })...`,
          });
          const fixResponse = await apiRequest("fix-code", {
            code: codeToExecute,
            info: executionResult.error,
          });
          codeToExecute = fixResponse.corrected_code; // Update the code to the fixed version
        }

        attempts++;
      } while (executionResult.status !== "success" && attempts < 10);

      if (executionResult.status === "success") {
        updateState({
          statusMessage: "Code executed successfully!",
          output: executionResult.output,
          efficiency: executionResult.efficiency, // Added this line
          isLoading: false,
        });

        // Generate function description
        const description = await apiRequest("describe-function", {
          code: codeToExecute,
        });
        updateState({
          functionDescription: description.description,
          statusMessage: "Function described successfully.",
        });
      } else {
        updateState({
          statusMessage: `Failed to execute code successfully after ${attempts} attempts.`,
        });
      }
    } catch (err) {
      updateState({ error: err.message, statusMessage: "", isLoading: false });
    }
  };

  return (
    <div className={styles.container}>
      <form
        className={styles.codeForm}
        onSubmit={generateAndRunCode}
        aria-label="code-runner-form"
      >
        <SearchBox
          value={state.code_requirements}
          onChange={(e) => updateState({ code_requirements: e.target.value })}
          placeholder="Search The Functionary..."
          aria-label="search-box"
        />
      </form>
      <StatusMessage message={state.statusMessage || state.error} />
      <FunctionDescription description={state.functionDescription} />
      <ResultsSection code={state.code} efficiency={state.efficiency} />
      <OutputSection output={state.output} />
      
      {state.isLoading && <LoadingIndicator />}
    </div>
  );
};

const LoadingIndicator = () => (
  <div className={styles.loadingIndicator}>Loading...</div>
);

const StatusMessage = ({ message }) => (
  <div className={styles.updates}>{message}</div>
);

const FunctionDescription = ({ description }) =>
  description && (
    <div className={styles.functionDescription}>
      <h2>Description:</h2>
      <p>{description}</p>
    </div>
  );


const OutputSection = ({ output }) => (
  <section className={styles.output}>
    <pre>{output}</pre>
  </section>
);

const EfficiencySection = ({ efficiency }) => (
  <section className={styles.efficiency}>
    <h3>Efficiency:</h3>
    <pre>{efficiency}</pre>
  </section>
);


export default CodeRunner;
