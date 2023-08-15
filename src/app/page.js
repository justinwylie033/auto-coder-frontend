"use client";

import Image from 'next/image'
import CodeRunner from './Components/CodeRunner'
import Navbar from './Components/Navbar';


export default function Home() {
  return (
    <div className="App">
      <Navbar/> 
      <CodeRunner /> 
    </div>
  );
}
