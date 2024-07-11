import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import '../App.css';
import Navbar from './Navbar';
import Footer from './Footer';

interface Message {
    text: string | JSX.Element;
    sender: string;
}


const Chat: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [pendingDetails, setPendingDetails] = useState<null | { Time: string, DocName: string, Email: string, Date: string }>(null);
    const messageContainerRef = useRef<HTMLDivElement>(null);

    const askDetails = async (Time: string, DocName: string, Email: string, Date: string) => {
        setPendingDetails({ Time, DocName, Email, Date });
        const ask = "To book the appointment, please provide your Name, Age, and Email.";
        setMessages(prevMessages => [
            ...prevMessages,
            { text: ask, sender: 'gemini' }
        ]);
    };
    const isValidObjectId = (id: string) => {
        return /^[0-9a-fA-F]{24}$/.test(id);
    };

    const handleSendMessage = async () => {
        if (input.trim()) {
            const userInput = input;
            setMessages(prevMessages => [...prevMessages, { text: userInput, sender: 'user' }]);
            setInput('');

            try {
                if (pendingDetails) {
                    
                    const userDetailsResponse = await axios.post('https://med-kare.onrender.com/gemini_data', {
                        Text: `Hey Med please extract user's name,age and email from ${userInput} and return in JSON format. format = \"user\":{\"name\":\"user_name\",\"age\":\"user_age\",\"email\":\"user_email\"}`
                    });

                    const userDetails = userDetailsResponse.data;

                    
                    if (userDetails && userDetails.user && userDetails.user.name && userDetails.user.age && userDetails.user.email) {
                        
                        const sendEmailDetails = {
                            username: userDetails.user.name,
                            userEmail: userDetails.user.email,
                            doctorName: pendingDetails.DocName,
                            doctorEmail: pendingDetails.Email,
                            date: pendingDetails.Date,
                            time: pendingDetails.Time
                        };

                        const sendEmailResponse = await axios.post('https://med-kare.onrender.com/send_email', sendEmailDetails);
                        const confirm = sendEmailResponse.data;
                        console.log(confirm)
                        setMessages(prevMessages => [
                            ...prevMessages,
                            { text: confirm.message, sender: 'gemini' }
                        ]);

                        setPendingDetails(null);
                    } else {
                        
                        const askIncompleteDetails = "Please provide your complete details: Name, Age, and Email.";
                        setMessages(prevMessages => [
                            ...prevMessages,
                            { text: askIncompleteDetails, sender: 'gemini' }
                        ]);
                    }
                } else {
                    
                    const response = await axios.post('https://med-kare.onrender.com/gemini_data', {
                        Text: userInput
                    });

                    const responseData = response.data;
                    if (typeof responseData === 'object' && 'doctor' in responseData) {
                        const sendValue = {
                            'Location': responseData.doctor.Location,
                            'Specialization': responseData.doctor.Specialization
                        };
                        const matchResponse = await axios.post('https://med-kare.onrender.com/match_doctor', sendValue);
                        const matchedDoctor = matchResponse.data;
                        if (matchedDoctor.length !== 0) {

                            const doctorInfoMessage = (
                                <div className="flex flex-col px-5 m-1">
                                    <div className="flex w-[900px] justify-evenly">
                                        <strong>Name:</strong><strong>Specialization:</strong><strong>Address:</strong><strong>Rating:</strong><strong>Experience:</strong><strong>Fees:</strong>
                                    </div>
                                    {matchedDoctor.map((doctor: any, index: number) => (
                                        <div key={index} className="flex w-[900px] justify-evenly p-3 bg-gray-100 my-2 rounded-lg">
                                            <div>{doctor.Name}</div>
                                            <div>{doctor.Specialization}</div>
                                            <div className='flex max-w-[200px]'>{doctor.Address.Street}</div>
                                            <div>{doctor.Rating}</div>
                                            <div>{doctor.Experience} Years</div>
                                            <div>{doctor.Fee}</div>
                                        </div>
                                    ))}
                                </div>
                            );

                            setMessages(prevMessages => [
                                ...prevMessages,
                                { text: doctorInfoMessage, sender: 'gemini' }
                            ]);
                            for (const doctor of matchedDoctor) {
                                const doctorDetails = {
                                    id: isValidObjectId(doctor._id) ? doctor._id : null,
                                    name: doctor.Name,
                                    specialization: doctor.Specialization,
                                    experience: doctor.Experience,
                                    rating: doctor.Rating,
                                    address: doctor.Address.Street,
                                    contact: doctor.Contact.Email,
                                    fee: doctor.Fee
                                };
                                if (doctorDetails.id !== null) {
                                    await axios.post('https://med-kare.onrender.com/gemini_data', {
                                        Text: `Store doctor details: ${JSON.stringify(doctorDetails)}`
                                    });
                                }
                            }

                        }
                        else {
                            const nodoc = await axios.post('https://med-kare.onrender.com/gemini_data', {
                                Text: "Hey Med return in text format that user has either given incomplete query or query is not clear and if had provide the necessary and no doctor is found in database return that you are trying to collaborate to /Specializatio/ in /Location/. Do not say that you are under development just say we are trying to collaborate with them."
                            });
                            const nodocData = nodoc.data;
                            setMessages(prevMessages => [
                                ...prevMessages,
                                { text: nodocData, sender: 'gemini' }
                            ]);
                        }
                    } else if (typeof responseData === 'object' && 'id' in responseData) {
                        const bookResponse = await axios.post(`https://med-kare.onrender.com/book_appointment/${responseData.id}`);
                        const selectedDoc = bookResponse.data;
                        const availTimes = (
                            <div>
                                <p>Time Slot of Dr {selectedDoc.Name}</p>
                                <div>
                                    <strong>Time Slots:</strong>
                                    {selectedDoc.TimeSlot.some((dateSlot: any) => dateSlot.TimeSlots.some((timeSlot: any) => timeSlot.isAvailable)) ?
                                        selectedDoc.TimeSlot.map((dateSlot: any, dateIndex: any) => (
                                            <div key={dateIndex} className='flex w-[600px] m-5'>
                                                <p><strong>Date:</strong> {dateSlot.Date}</p>
                                                {dateSlot.TimeSlots.some((timeSlot: any) => timeSlot.isAvailable) ?
                                                    dateSlot.TimeSlots.map((timeSlot: any, timeIndex: any) => (
                                                        timeSlot.isAvailable ?
                                                            <button
                                                                key={timeIndex}
                                                                className={`py-2 mx-2 px-4 rounded ${timeSlot.isAvailable ? 'bg-green-500 cursor-pointer' : 'bg-red-500 cursor-default'} text-white`}
                                                                onClick={() => timeSlot.isAvailable && askDetails(timeSlot.Time, selectedDoc.Name, selectedDoc.Contact.Email, dateSlot.Date)}
                                                            >
                                                                {timeSlot.Time}
                                                            </button>
                                                            : <button
                                                                key={timeIndex}
                                                                className={`py-2 mx-2 px-4 rounded ${timeSlot.isAvailable ? 'bg-green-500 cursor-pointer' : 'bg-red-500 cursor-default'} text-white`}
                                                            >
                                                                {timeSlot.Time}
                                                            </button>
                                                    ))
                                                    : <p>No slots available</p>
                                                }
                                            </div>
                                        ))
                                        : <p>No slots available</p>
                                    }
                                </div>
                            </div>
                        );
                        setMessages(prevMessages => [
                            ...prevMessages,
                            { text: availTimes, sender: 'gemini' }
                        ]);
                        await axios.post('https://med-kare.onrender.com/gemini_data', {
                            Text: `Hey Med store in your context these ${availTimes}.`
                        });
                    } else {
                        setMessages(prevMessages => [
                            ...prevMessages,
                            { text: responseData, sender: 'gemini' }
                        ]);
                    }
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
        <>
        <Navbar/>
        <div className="flex flex-col h-[800px] border-l-2 border-r-2 border-green-500 ">
            <div className="flex-grow p-4 overflow-auto" ref={messageContainerRef}>
                <div className="max-w-5xl mx-auto">
                    {messages.map((message, index) => (
                        <div key={index} className={`flex my-2 ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`p-3 rounded-lg ${message.sender === 'user' ? 'text-xl bg-white text-green-900 self-end' : 'text-xl bg-white font bold  text-black self-start'}`}>
                                {message.text}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
            <div className="p-4 bg-white ">
                <div className="flex items-center">
                    <input
                        type="text"
                        className="flex-grow p-2 border border-green-300 rounded-lg focus:outline-none focus:border-green-500"
                        placeholder = "Please wait as first reply takes time due to host's server starting policy..."
                        value={input}
                        onChange={e => setInput(e.target.value)}
                        onKeyDown={e => {
                            if (e.key === 'Enter') {
                                handleSendMessage();
                            }
                        }}
                    />
                    <button
                        className="ml-2 p-2 bg-green-600 font-bold text-white rounded-lg"
                        onClick={handleSendMessage}
                    >
                        Send
                    </button>
                </div>
            </div>
        </div>
        <Footer/>
        </>
    );
};

export default Chat;
