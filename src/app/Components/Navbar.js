import React from 'react'
import styles from "../styles/Navbar.module.css"
import Image from "next/image";
import logo from "../../../public/logo.png";
import UserNotLoggedIn from './UserNotLoggedIn';
import UserLoggedIn from './UserLoggedIn';
import {getAuth} from "firebase/auth";
import { useAuthState } from "react-firebase-hooks/auth";


function Navbar() {

  const auth = getAuth()
  const [user, loading, error] = useAuthState(auth);

  return (
    <div className={styles.navbar}>
        <div className={styles.logocontainer}>
          <Image className={styles.logo} src={logo}  /> 
          <h1 className={styles.logotext}>Auto-Code</h1>
        </div>
       {user ?  <UserLoggedIn/> : <UserNotLoggedIn/>}
      
      </div>
  )
}

export default Navbar