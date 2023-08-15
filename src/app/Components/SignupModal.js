import React, { useEffect, useState } from "react";
import { auth, registerWithEmailPassword, signInWithGoogle } from "./firebase";
import { useAuthState } from "react-firebase-hooks/auth";
import { Button, Modal } from "@mui/material";
import styles from "../styles/Login.module.css";

function SignupModal({ open, handleClose }) {
  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [user, loading, error] = useAuthState(auth);

  useEffect(() => {
    if (loading) {
      //loading screen
      return;
    }
    if (user) console.log(user.uid);
    console.log(user);
  }, [user, loading]);

  const handleStandardSignUp = (e) => {
    e.preventDefault();
    signUpWithEmailPassword(auth, email, password, displayName);
    handleClose();
  };

  return (
    <Modal className={styles.loginbox} open={open} onClose={handleClose}>
      <div className={styles.logincontainer}>
        <h2>Sign Up</h2>

        <div className={styles.loginfields}>
          <form onSubmit={handleStandardSignUp}>
            <input
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              className={styles.logindialog}
              placeholder="Display Name"
              required
            />
            <input
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className={styles.logindialog}
              placeholder="Email"
              required
            />
            <input
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className={styles.logindialog}
              placeholder="Password"
              required
            />
            <Button
              onClick={handleStandardSignUp}
              className={styles.loginbutton}
            >
              {" "}
              Sign Up{" "}
            </Button>
          </form>
        </div>
      </div>
    </Modal>
  );
}

export default SignupModal;
