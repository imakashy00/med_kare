// import React from 'react'

import Navbar from "./Navbar"
import chatbot from '../assets/chatbot.avif';
import Footer from "./Footer";

import {  useNavigate } from 'react-router-dom';

const Homepage = () => {
  const navigate = useNavigate()
  const chatPage = () => {
    navigate("/chat")
  }
  return (
    <>
      <Navbar/>
      <div className='flex h-auto mt-[50px]'>
        <div className='flex flex-col mx-[40px]'>
          <h2 className='text-7xl text-start font-bold my-5'>Revolutionising <br />Healthcare with AI</h2>
          <p className='text-3xl text-start my-5'>Medbuddy is an AI healthcare chatbot <br />which answers queries related to health and book appointment for you,<br /> all using natural languages.  </p>
          <button className=" mt-10 text-2xl text-green-600 border-2 rounded-full border-green-700 h-[50px] w-[120px] hover:bg-green-500 hover:text-white" 
          onClick={chatPage}>Chat</button>
        </div>
        <img src={chatbot} alt="Chatbot" className="object-contain h-[700px] w-[700px] mt-[-50px]" />
      </div>
      <Footer/>
    </>
  )
}

export default Homepage