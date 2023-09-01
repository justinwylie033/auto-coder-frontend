import React from "react";
import styles from "../styles/AutoExpandTextArea.module.css";

const AutoExpandTextArea = ({ value, onChange, placeholder, type, readOnly }) => {
  
  const codeStyle = type === "code" ? {
    fontFamily: "'Courier New', Courier, monospace",
    backgroundColor: "#f5f5f5",
    color: "#333",
    border: "1px solid #ddd",
    borderRadius: "4px",
    padding: "10px",
    whiteSpace: "pre-wrap",
  } : {};

  // Count the number of newline characters and add 1
  const rowCount = (value.match(/\n/g) || []).length + 1;

  return (
    <div className={styles.container}>
      <textarea 
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          rows={rowCount}  // Dynamic row count based on content
          className={styles.output}
          style={codeStyle}  // Apply the code styles if type is "code"
          readOnly={readOnly}
      />
    </div>
  );
};

export default AutoExpandTextArea;
