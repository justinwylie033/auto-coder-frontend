import { Button } from '@mui/material'
import React from 'react'
import styles from "../styles/UserLoggedIn.module.css"
import { getAuth, signOut } from "firebase/auth";
import {auth} from "./firebase"


function LogOut(){
    signOut(auth).then(() => {
        // Sign-out successful.
      }).catch((error) => {
        console.log(error)
      });
}

function UserLoggedIn() {
  return (
    <div className={styles.UserControlPanel}>

    <h3 className={styles.UsersName}> Justin Wylie</h3>

    <Button onClick={LogOut} className={styles.logoutbtn}>Sign Out</Button>

    </div>
  )
}

export default UserLoggedIn