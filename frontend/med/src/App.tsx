import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [messages, setMessages] = useState<{ text: string | JSX.Element; sender: string }[]>([]);
    const [input, setInput] = useState('');
    const messageContainerRef = useRef<HTMLDivElement>(null);

    const handleSendMessage = async () => {
        if (input.trim()) {
            const userInput = input;
            setMessages((prevMessages) => [...prevMessages, { text: userInput, sender: 'user' }]);
            setInput('');

            try {
                const response = await axios.post('http://127.0.0.1:8000/gemini_data', {
                    Text: userInput
                });
                const responseData = response.data;

                if (Array.isArray(responseData)) {
                    const doctorInfoMessage = (
                        <div className='flex px-5 flex-col m-1'>
                            <div className=' flex w-[950px] justify-evenly'>
                                <strong>Name:</strong><strong>Specialization:</strong><strong>Address/Location:</strong><strong>Rating:</strong><strong>Experience:</strong><strong>Fees:</strong>
                            </div>
                            {responseData.map((doctor: any, index: any) => (
                                <div className=' w-[950px]'>
                                    <div key={index} className="p-3 flex justify-evenly rounded-lg bg-gray-100 my-2">
                                        <div>{doctor.name}</div>
                                        <div>{doctor.specialization}</div>
                                        <div className='flex max-w-[200px]'>{doctor.address}</div>
                                        <div>{doctor.rating}</div>
                                        <div>{doctor.experience}</div>
                                        <div>{doctor.fee}</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    );

                    setMessages((prevMessages) => [
                        ...prevMessages,
                        {text: doctorInfoMessage, sender: 'gemini'}
                    ]);
                } else {
                    setMessages((prevMessages) => [
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
        <div className="flex flex-col h-[900px] rounded-2xl bg-gray-200">
            <div className="flex-grow p-4 overflow-auto" ref={messageContainerRef}>
                <div className="max-w-5xl mx-auto">
                    {messages.map((message, index) => (
                        <div
                            key={index}
                            className={`flex flex-col  my-2 ${
                                message.sender === 'user' ? 'justify-end' : 'justify-start'
                            }`}
                        >
                            <div
                                className={` flex flex-col p-3 max-w-3/4 rounded-lg ${
                                    message.sender === 'user'
                                        ? 'bg-blue-500 text-white self-end'
                                        : 'bg-gray-100 text-black self-start'
                                }`}
                            >
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
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => {
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
}

export default App;
