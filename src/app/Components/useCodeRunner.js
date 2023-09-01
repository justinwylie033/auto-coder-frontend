import { useReducer } from "react";
import * as codeApi from "./codeApi";

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

export const useCodeRunner = () => {
  const [state, dispatch] = useReducer(reducer, initialState);

  const generateAndRunCode = async (code_requirements) => {
    dispatch({ type: "UPDATE_STATE", payload: { statusMessage: "Generating new code...", isLoading: true } });
    
    const generatedCode = await codeApi.generateCode(code_requirements);
    dispatch({ type: "UPDATE_STATE", payload: { code: generatedCode.code, statusMessage: "Generated new code." } });

    await codeApi.installPackages(generatedCode.code);
    dispatch({ type: "UPDATE_STATE", payload: { statusMessage: "Packages installed successfully." } });

    let codeToExecute = generatedCode.code;
    let attempts = 0;
    let executionResult;

    do {
      dispatch({ type: "UPDATE_STATE", payload: { statusMessage: "Testing/Executing code...", isLoading: true } });
      
      executionResult = await codeApi.executeCode(codeToExecute);

      if (executionResult.status !== "success") {
        const fixResponse = await codeApi.fixCode(codeToExecute, executionResult.error);
        codeToExecute = fixResponse.corrected_code;
        attempts++;
        dispatch({ 
          type: "UPDATE_STATE", 
          payload: { 
            error: executionResult.error,
            statusMessage: `Error encountered. Attempting to fix (Attempt ${attempts})...`
          } 
        });
      }
    } while (executionResult.status !== "success" && attempts < 10);

    if (executionResult.status === "success") {
      const description = await codeApi.describeFunction(codeToExecute);
      
      dispatch({
        type: "UPDATE_STATE",
        payload: {
          statusMessage: "Code executed successfully!",
          output: executionResult.output,
          efficiency: executionResult.efficiency,
          isLoading: false,
          functionDescription: description.description,
        },
      });
    } else {
      dispatch({
        type: "UPDATE_STATE",
        payload: { statusMessage: `Failed to execute code successfully after ${attempts} attempts.` },
      });
    }
  };

  return {
    state,
    generateAndRunCode,
    dispatch
  };
};
