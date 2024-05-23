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

const App: React.FC = () => {
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
                if (typeof responseData === 'object' && responseData.hasOwnProperty('doctor')) {
                    console.log(responseData);
                    const matchResponse = await axios.post('http://127.0.0.1:8000/match_doctor', responseData);
                    const matchedDoctor = matchResponse.data;
                    console.log(matchedDoctor);
                    if (matchedDoctor.length!==0){
                        console.log(matchedDoctor);
                        for (const doctor of matchedDoctor) {
                            const doctorDetails = `Name: ${doctor.Name}, Specialization: ${doctor.Specialization}, Experience: ${doctor.Experience},Rating: ${doctor.Rating}, Address: ${doctor.Address.Street},Contact: ${doctor.Contact.Email}, Fees: ${doctor.Fees} `;
                            setMessages(prevMessages => [
                                ...prevMessages,
                                { text: doctorDetails, sender: 'gemini' }
                            ]);
                            const docDetails = await axios.post('http://127.0.0.1:8000/gemini_data',{
                                Text:`Hey Med remember these ${doctorDetails}.`
                            });
                            console.log(docDetails.data);
                        }

                    }
                    else {
                        const nodoc = await axios.post('http://127.0.0.1:8000/gemini_data', {
                            Text: "Hey Med return in text format that user has either given incomplete query or query is not clear and if had provide the necessary and no doctor is found in database return that you are trying to collaborate to /Specializatio/ in /Location/. Do not say that you are under development just say we  are trying to collaborate with them."
                        });
                        const nodocData = nodoc.data;
                        setMessages(prevMessages => [
                            ...prevMessages,
                            { text: nodocData, sender: 'gemini' }
                        ]);
                    }
                }
                else {
                    setMessages(prevMessages => [
                        ...prevMessages,
                        { text: responseData, sender: 'gemini' }
                    ]);
                }

            } catch (error) {
                console.error('Error fetching data:', error);
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

export default App;
