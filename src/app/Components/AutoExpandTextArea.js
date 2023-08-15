import React from "react";
import styles from "../styles/AutoExpandTextArea.module.css";

const AutoExpandTextArea = ({ value, shouldExpand }) => {
  return (
    <div className={styles.outputContainer}>
      {value && (
          <code className={`${styles.output} ${shouldExpand ? styles.expanded : ""}`}>
            {value}
          </code>
      )}
    </div>
  );
};

export default AutoExpandTextArea;
