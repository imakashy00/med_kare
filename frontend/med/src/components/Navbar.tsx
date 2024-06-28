// import React from 'react'
import { NavLink } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className='w-full h-[100px] flex items-center justify-between  px-10'>
        <h1 className='text-4xl text-green-500 font-bold'>MedBuddy</h1>
        <ul className='flex space-x-10 text-2xl'>
          <li>
            <NavLink 
              to="/" 
              className={({ isActive }) => isActive ? 'text-green-500 border-b border-green-400' : 'hover:text-green-500'}
            >
              Home
            </NavLink>
          </li>
          <li>
            <NavLink 
              to="/chat" 
              className={({ isActive }) => isActive ? 'text-green-500 border-b border-green-400' : 'hover:text-green-500'}
            >
              Chat
            </NavLink>
          </li>
        </ul>
      </nav>
  )
}

export default Navbar