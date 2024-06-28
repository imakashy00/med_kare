// import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';


import Chat from "./components/Chat"
import Homepage from "./components/Homepage"


const App = () => {
  return (
    <Router>    
        <Routes>
            <Route path="/" element={<Homepage />} />
            <Route path="/chat" element={<Chat />} />
        </Routes>
    </Router>
  )
}

export default App
