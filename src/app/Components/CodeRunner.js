import React from "react";
import styles from "../styles/CodeRunner.module.css";
import { useAuthState } from "react-firebase-hooks/auth";
import { auth } from "./firebase";
import { useCodeRunner } from "./useCodeRunner";
import ResultsSection from "./ResultsSection";
import SearchBox from "./SearchBox";

const CodeRunner = () => {
  const [user] = useAuthState(auth);
  const { state, generateAndRunCode, dispatch } = useCodeRunner();

  const handleSubmit = (e) => {
    e.preventDefault();
    generateAndRunCode(state.code_requirements);
  };

  const handleInputChange = (e) => {
    dispatch({
      type: "UPDATE_STATE",
      payload: { code_requirements: e.target.value },
    });
  };

  return (
    <div className={styles.container}>
      {/* Form Component */}
      <CodeRunnerForm 
        onSubmit={handleSubmit} 
        value={state.code_requirements}
        onChange={handleInputChange}
      />

      { state.functionDescription && 
        <ResultsSection
          code={state.code}
          efficiency={state.efficiency}
          isLoading={state.isLoading}
          statusMessage={state.statusMessage}
          description={state.functionDescription}
        />
      }
      

      {/* Loading Overlay */}
      {state.isLoading && <div className={styles.overlay}></div>}
    </div>
  );
};

const CodeRunnerForm = ({ onSubmit, value, onChange }) => (
  <form
    className={styles.codeForm}
    onSubmit={onSubmit}
    aria-label="code-runner-form"
  >
    <SearchBox
      value={value}
      onChange={onChange}
      placeholder="Search The Functionary..."
      aria-label="search-box"
    />
  </form>
);

export default CodeRunner;
