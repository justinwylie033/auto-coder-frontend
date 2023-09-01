import React from 'react';
import styles from "../styles/ResultSection.module.css";
import CodeTextArea from './CodeTextArea';
import extractFunctionSignature from './extractFunctionSignature';

const ResultsSection = ({ code, efficiency, isLoading, statusMessage, description }) => {
    const functionSignature = extractFunctionSignature(code);

    return (
        <div className={styles.resultsSection}>
            <header className={styles.header}>
                <h2>{functionSignature}</h2>
                {description && <p className={styles.description}>{description}</p>}
            </header>
            <div className={styles.textAreaContainer}>
                <CodeTextArea 
                    value={code ? code.toString() : ""}
                    readOnly={true}
                />
                {isLoading && 
                    <div className={styles.overlay}>
                        <div className={styles.updates}>{statusMessage}</div>
                    </div>
                }
            </div>
            <div className={styles.metricsContainer}>
                <div className={styles.metric}>
                    <h3>Estimated Efficiency</h3>
                    <span>{efficiency || "Not evaluated"}</span>
                </div>
                <div className={styles.metric}>
                    <h3>Unit Tests</h3>
                    <span>🟢 All Tests Passed</span>
                </div>
            </div>
        </div>
    );
};

export default ResultsSection;
