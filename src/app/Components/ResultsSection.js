import React from 'react';
import styles from "../styles/CodeRunner.module.css";
import CodeTextArea from './CodeTextArea';

const ResultsSection = ({ code, efficiency }) => (
    <section className={styles.resultsSection}>
        <h2>Generated Code</h2>
        <CodeTextArea 
            placeholder="Your output will appear here"
            value={code ? code.toString() : ""}
            readOnly={true}
            type="code"
        />
        <div className={styles.codeMetrics}>
        
        <div className={styles.metric}>
        <h2>Estimated Efficiency</h2>
        <p>{efficiency || "Not evaluated"}</p>
        </div>
        <div className={styles.metric}>
        <h2>Unit Tests</h2>

            {/* Placeholder for unit tests. This should be replaced by actual unit tests results */}
            <p>🟢 All Tests Passed</p>
        </div>
        </div>

    </section>
);

export default ResultsSection;
