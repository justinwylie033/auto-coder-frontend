import React from "react";
import styles from "../styles/CodeTextArea.module.css";

const CodeTextArea = ({ value }) => {
  
  const codeStyle = {
    fontFamily: "'Courier New', Courier, monospace",
    backgroundColor: "#f5f5f5",
    color: "#333",
    border: "1px solid #ddd",
    borderRadius: "4px",
    padding: "10px",
    whiteSpace: "pre-wrap",
  };

  // Count the number of newline characters and add 1
  const rowCount = (value.match(/\n/g) || []).length + 1;

  return (
      <textarea 
          value={value}
          rows={rowCount}
          className={styles.output}
          style={codeStyle}
          readOnly={true}
      />
  );
};

export default CodeTextArea;
