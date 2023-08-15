import React, {useState} from 'react'
import Button from '@mui/material/Button'
import styles from '../styles/OptionToolbar.module.css'

function OptionToolbar({handleGenerateMode, handleFixMode, handleImproveMode, Generate, Fix, Improve}) {

  return (
    <div className={styles.OptionToolbar}>
        <Button onClick={handleGenerateMode} className={`${styles.OptionBtn} ${Generate ? styles.OptionBtnActive : ""}`} >Generate</Button>
        <Button onClick={handleFixMode} className={`${styles.OptionBtn} ${Fix ? styles.OptionBtnActive : ""}`} >Fix</Button>
        <Button onClick={handleImproveMode} className={`${styles.OptionBtn} ${Improve ? styles.OptionBtnActive : ""}`} >Improve</Button>


    </div>
  )
}

export default OptionToolbar