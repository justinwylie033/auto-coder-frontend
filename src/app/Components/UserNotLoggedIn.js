import { Button } from "@mui/material";
import React, { useState } from "react";
import { auth } from "./firebase";
import { useAuthState } from "react-firebase-hooks/auth";
import styles from "../styles/UserNotLoggedIn.module.css";
import LoginModal from "./LoginModal";
import SignupModal from "./SignupModal";

function UserNotLoggedIn() {
  const [user, loading, error] = useAuthState(auth);
  const [showLogin, setShowLogin] = useState(false);
  const [showSignup, setShowSignup] = useState(false);

  function closeLogin() {
    setShowLogin(false);
  }

  function closeSignup() {
    setShowSignup(false);
  }

  return (
    <div className={styles.buttoncontainer}>
      <Button
        onClick={() => setShowLogin(true)}
        className={styles.memberbuttons}
      >
        {" "}
        Login{" "}
      </Button>
      <Button
        onClick={() => setShowSignup(true)}
        className={styles.memberbuttons}
      >
        Join
      </Button>
      {showLogin ? (
        <LoginModal open={showLogin} handleClose={closeLogin} />
      ) : null}
      {showSignup ? (
        <SignupModal open={showSignup} handleClose={closeSignup} />
      ) : null}
    </div>
  );
}

export default UserNotLoggedIn;