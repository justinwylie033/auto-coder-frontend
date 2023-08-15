import React, { useState, useEffect, useReducer } from "react";
import axios from "axios";
import AutoExpandTextarea from "./AutoExpandTextArea";
import styles from "../styles/CodeRunner.module.css";
import { Button, IconButton } from "@mui/material";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import OptionToolbar from "./OptionToolbar";
import { useAuthState } from "react-firebase-hooks/auth";
import { auth } from "./firebase";

const languages = [
  "Python",
  "JavaScript",
  "CPP",
  "Java",
  "HTML",
  "CSS",
  "JSX",
  "SQL",
  "PHP",
  "Swift",
  "C#",
  "Go",
];
const initialError =
  "An error occurred while processing the code requirements.";

const initialState = {
  language: "Python",
  code_requirements: "",
  code: "",
  output: "",
  expandOutput: false,
  error: "",
  container_name: "",
  evaluation: "",
  mode: "",
};

const LanguageButton = ({ language, currentLanguage, dispatch }) => (
  <Button
    className={`${styles.LangButton} ${
      currentLanguage === language ? styles.selected : ""
    }`}
    onClick={() => dispatch({ type: "UPDATE_STATE", payload: { language } })}
  >
    {language}
  </Button>
);

function reducer(state, action) {
  switch (action.type) {
    case "UPDATE_STATE":
      return {
        ...state,
        ...action.payload,
      };
    default:
      throw new Error("Unexpected action");
  }
}

const CodeRunner = () => {
  const [state, dispatch] = useReducer(reducer, initialState);

  const {
    language,
    code_requirements,
    code,
    output,
    error,
    container_name,
    evaluation,
    expandOutput,
    mode,
  } = state;
  const [user, loading, auth_error] = useAuthState(auth);

  useEffect(() => {
    if (user) {
      // have to dispatch an action here make sure an actual user object is passed
      dispatch({
        type: "UPDATE_STATE",
        payload: { container_name: "docker_" + user.uid },
      });
    }
  }, [user]);

  const handleRequest = async (url, payload) => {
    console.log(`Sending request to ${url}`);
  
    try {
      const response = await axios.post(`http://localhost:5000/${url}`, payload);
  
      const data = {
        ...payload, // maintain old state
        ...response.data, // update state with response
      };
  
      dispatch({ type: "UPDATE_STATE", payload: data });
  
      console.log("Got response:", response);
  
      return data;
    } catch (e) {
      dispatch({
        type: "UPDATE_STATE",
        payload: { error: e.message, expandOutput: false },
      });
      return null;
    }
  };
  
  const runCode = (payload) => handleRequest("run-code", payload);
  const improveCode = (payload) => handleRequest("improve-code", payload);
  const evaluateCode = (payload) => handleRequest("evaluate-code", payload);
  const generateCode = () =>
    handleRequest("get-initial-code", {
      language,
      code_requirements,
      container_name,
    });


// in generateWorkingCode:
const generateWorkingCode = async (e) => {
  e.preventDefault();

  let payload = {
    language,
    code_requirements,
    container_name,
  };

  payload = await generateCode(payload);

  let evalResponse = null;

  do {
    payload = await runCode(payload);
    payload = await improveCode(payload);

    evalResponse = await evaluateCode(payload);
  } while (evalResponse?.evaluation === "no");
};

  return (
    <div className={styles.container}>
      <form className={styles.codeForm} onSubmit={generateWorkingCode}>
        <div className={styles.ButtonContainer}>
          {languages.map((lang) => (
            <LanguageButton
              key={lang}
              language={lang}
              currentLanguage={state.language}
              dispatch={dispatch}
            />
          ))}
        </div>
        <OptionToolbar
          setMode={(mode) =>
            dispatch({ type: "UPDATE_STATE", payload: { mode } })
          }
          mode={state.mode}
        />{" "}
        <textarea
          className={styles.codeInput}
          name="code_requirements"
          id="code_requirements"
          rows="10"
          cols="50"
          placeholder="Please Enter your code requirements >>>"
          value={code_requirements}
          onChange={(e) =>
            dispatch({
              type: "UPDATE_STATE",
              payload: { code_requirements: e.target.value },
            })
          }
        />
        <IconButton className={styles.submitBtn} type="submit">
          <PlayArrowIcon />
        </IconButton>
        <br />
      </form>
      {code && (
        <AutoExpandTextarea
          placeholder="Your output will appear here"
          value={code ? code.toString() : ""}
          shouldExpand={expandOutput}
          className={`${styles.codeOutput} ${
            expandOutput ? styles.expanded : ""
          }`}
        />
      )}
      {error && (
        <section>
          <h3>Error:</h3>
          <pre className={styles.error}>{error}</pre>
        </section>
      )}
      {output && (
        <section>
          <pre className={styles.output}>{output}</pre>
        </section>
      )}
    </div>
  );
};

export default CodeRunner;
