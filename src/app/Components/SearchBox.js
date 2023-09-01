import React from "react";
import styles from "../styles/SearchBox.module.css";
import { IconButton } from "@mui/material";
import SearchIcon from '@mui/icons-material/Search';

const SearchBox = ({ value, onChange, placeholder }) => {
  
  return (
    <div className={styles.container}>
      <input 
          type="text"
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          className={styles.searchInput}
      />
      <IconButton className={styles.submitBtn} type="submit">
      <SearchIcon />
    </IconButton>


    </div>
  );
};

export default SearchBox;
