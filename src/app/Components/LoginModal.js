import React, { useEffect, useState } from "react";
import { auth, EmailPasswordLogin, signInWithGoogle } from "./firebase";
import { useAuthState } from "react-firebase-hooks/auth";
import { Button, Modal } from "@mui/material";
import styles from "../styles/Login.module.css";

function LoginModal({ open, handleclose }) {
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

  const handleStandardLogin = (e) => {
    e.preventDefault();
    EmailPasswordLogin(auth, email, password);
    handleclose()

  };

  return (
    <Modal className={styles.loginbox} open={open} onClose={handleclose}>
      <div className={styles.logincontainer}>
        <h2>Login</h2>

        
          <div className={styles.loginfields}>
          <form onSubmit={handleStandardLogin}>
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
            <Button onClick={handleStandardLogin} className={styles.loginbutton}> Login </Button>
            </form>
        </div>
      </div>
    </Modal>
  );
}

export default LoginModal;
