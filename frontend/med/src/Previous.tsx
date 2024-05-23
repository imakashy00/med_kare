import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

interface Message {
    text: string | JSX.Element;
    sender: string;
}

interface DoctorDetails {
    name: string;
    specialization: string;
    address: string;
    rating: number;
    experience: number;
}

interface TimeSlot {
    date: string;
    time: string;
    is_available: boolean;
}

interface Doctor {
    id: string;
    name: string;
    available_timeslots: TimeSlot[];
}

const Previous: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const messageContainerRef = useRef<HTMLDivElement>(null);

    const handleSendMessage = async () => {
        if (input.trim()) {
            const userInput = input;
            setMessages(prevMessages => [...prevMessages, { text: userInput, sender: 'user' }]);
            setInput('');

            try {
                const response = await axios.post('http://127.0.0.1:8000/gemini_data', {
                    Text: userInput
                });

                const responseData = response.data;

                if (Array.isArray(responseData)) {
                    console.log(responseData);
                    const doctorInfoMessage = (
                        <div className="flex flex-col px-5 m-1">
                        <div className="flex w-[900px] justify-evenly">
                            <strong>Name:</strong><strong>Specialization:</strong><strong>Address:</strong><strong>Rating:</strong><strong>Experience:</strong><strong>Fees:</strong>
                    </div>
                    {responseData.map((doctor: any, index: number) => (
                        <div key={index} className="flex  w-[900px] justify-evenly p-3 bg-gray-100 my-2 rounded-lg">
                        <div>{doctor.name}</div>
                        <div>{doctor.specialization}</div>
                        <div className='flex max-w-[200px]'>{doctor.address}</div>
                        <div>{doctor.rating}</div>
                        <div>{doctor.experience}</div>
                        <div>{doctor.fee}</div>
                        </div>
                    ))}
                    </div>
                );

                    setMessages(prevMessages => [
                        ...prevMessages,
                        { text: doctorInfoMessage, sender: 'gemini' }
                    ]);
                } else if (responseData && typeof responseData === 'object') {
                    if (responseData.hasOwnProperty('doctor') && typeof responseData.doctor === 'object') {
                        const doctorData = responseData.doctor;
                        console.log(doctorData)
                        const dummyDoctor = {
                            'Name':'abc',
                            // 'specialization':'Dentist',
                            // 'address':'Noida',
                            // 'rating':'4.8',
                            // 'experience':10,
                        }
                        console.log(dummyDoctor)

                        // Send a request to match the doctor in the database with doctorData as data
                        const matchResponse = await axios.post('http://127.0.0.1:8000/match_doctor', dummyDoctor);
                        const matchedDoctor = matchResponse.data as Doctor;

                        const doctorDetailsMessage = (
                            <div className="flex flex-col px-5 m-1">
                            <div className="flex w-full justify-evenly">
                                <strong>Name:</strong> {matchedDoctor.name}
                        </div>
                        <div>
                        {matchedDoctor.available_timeslots.map((slot, index) => (
                                <div key={index} className="p-3 rounded-lg bg-gray-100 my-2">
                            <div><strong>Date:</strong> {slot.date}</div>
                        <div><strong>Time:</strong> {slot.time}</div>
                        <div><strong>Available:</strong> {slot.is_available ? 'Yes' : 'No'}</div>
                        </div>
                    ))}
                        </div>
                        </div>
                    );

                        setMessages(prevMessages => [
                            ...prevMessages,
                            { text: doctorDetailsMessage, sender: 'gemini' }
                        ]);
                    }
                } else {
                    setMessages(prevMessages => [
                        ...prevMessages,
                        { text: responseData, sender: 'gemini' }
                    ]);
                }
            } catch (error) {
                console.error('Error fetching data from backend:', error);
            }
        }
    };

    useEffect(() => {
        if (messageContainerRef.current) {
            messageContainerRef.current.scrollTop = messageContainerRef.current.scrollHeight;
        }
    }, [messages]);

    return (
        <div className="flex flex-col h-screen bg-gray-200">
        <div className="flex-grow p-4 overflow-auto" ref={messageContainerRef}>
    <div className="max-w-5xl mx-auto">
    {messages.map((message, index) => (
            <div key={index} className={`flex my-2 ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
    <div className={`p-3 rounded-lg ${message.sender === 'user' ? 'bg-blue-500 text-white self-end' : 'bg-gray-100 text-black self-start'}`}>
    {message.text}
    </div>
    </div>
))}
    </div>
    </div>
    <div className="p-4 bg-white border-t">
    <div className="flex items-center">
    <input
        type="text"
    className="flex-grow p-2 border rounded-lg focus:outline-none focus:border-blue-500"
    value={input}
    onChange={e => setInput(e.target.value)}
    onKeyDown={e => {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    }}
    />
    <button
    className="ml-2 p-2 bg-blue-500 text-white rounded-lg"
    onClick={handleSendMessage}
        >
        Send
        </button>
        </div>
        </div>
        </div>
);
};

export default Previous;
