// import React from 'react'

const Footer = () => {
  return (
    <div className="text-2xl flex flex-col justify-center mt-[50px] items-center pt-20">
        <div className="text-green-600">
            &copy; MedBuddy 2023. All rights reserved.
            <div className="border-b border-green-900 w-1/1"></div>
        </div>
        <div className="flex justigy-center items-center p-5">
            <ul className="flex justify-center items-center text-blue-900 space-x-[80px]">
                <li><a href="mailto:imakashy00@gamil.com" target="_blank">Email</a></li>
                <li><a href="https://github.com/imakashy00/" target="_blank">Github</a></li>
                <li><a href="https://linkedin.com/in/imakashy00/" target="_blank">LinkedIn</a></li>                
            </ul>
        </div>
    </div>
  )
}

export default Footer