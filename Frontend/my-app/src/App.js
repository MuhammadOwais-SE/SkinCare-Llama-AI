import React, { useState, useEffect} from 'react';
import './App.css';
import axios from 'axios';

function App() {
    console.log("API URL:", process.env.REACT_APP_API_URL);

    // const [refresh, setRefresh] = useState(false) //First Method
    const [messages, setMessages] = useState([]); //second method
    // console.log('refresh..')

    // Testing the end points
    const endpoint = `${process.env.REACT_APP_API_URL}/messages/`;
    const fetch_Data = async () => {
        console.log('fetching...');
        try {
            const response = await axios.get(endpoint);
            console.log(response);
            setMessages(response.data); // Assuming `response.data` is an array of messages
        } catch (error) {
            console.error("Error fetching data:", error.message || error);
            alert("Failed to fetch data. Please check the console for details.");
        }
    };
    

    const post_Data = async () => {
        const message_text = 'Hello there, Posting Data';
        const is_ai_response = false;
        const body = { message_text, is_ai_response }; // Match Django model field names
        const response = await axios.post(endpoint, body);
        console.log(response);
        return response.data;
    };
    

    const handleSendData = async() => {
        const newData = await post_Data()
        //... some logic to add data
        if (newData) {
            setMessages(prevState => [...prevState, newData])
            // setRefresh(prevState => !prevState) //First method
        }
    }

    useEffect(() => {
        //interactions with external world
        fetch_Data()
    }, []) 
    //refresh        //set the dependency 

    const [activeTab, setActiveTab] = useState('Skin Analysis');
    // const [messages, setMessages] = useState([]);

    const handleTabChange = (tab) => {
        setActiveTab(tab);
        setMessages([]); // Clear messages when switching tabs
    };

    const sendMessage = async (e) => {
        e.preventDefault();
        //for testing
        try {
            // Call handleSendData, which calls post_Data internally
            await handleSendData();
        } catch (error) {
            console.error("Error sending message:", error);
        }

        const userInput = e.target.message.value;

        if (userInput.trim()) {
            setMessages((prevMessages) => [
                ...prevMessages,
                { sender: 'user', text: userInput },
            ]);

            const botResponse = getChatbotResponse(userInput);
            setMessages((prevMessages) => [
                ...prevMessages,
                { sender: 'bot', text: botResponse },
            ]);

            e.target.message.value = ''; // Clear input field
        }
    };

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { sender: 'user', image: reader.result },
                ]);

                setMessages((prevMessages) => [
                    ...prevMessages,
                    { sender: 'bot', text: 'Thanks for uploading an image! 😊' },
                ]);
            };
            reader.readAsDataURL(file);
        }
    };

    const getChatbotResponse = (input) => {
        if (input.toLowerCase().includes('acne')) {
            return 'For acne, I recommend using a product with salicylic acid or benzoyl peroxide. Consult a dermatologist for further advice.';
        } else if (input.toLowerCase().includes('dry skin')) {
            return 'For dry skin, try using a moisturizer with hyaluronic acid or ceramides. Drinking plenty of water also helps!';
        } else if (input.toLowerCase().includes('rash')) {
            return 'For rashes, consider a mild hydrocortisone cream. If the rash persists, consult a healthcare provider.';
        } else {
            return 'I need more information about your concern to recommend a product or medicine!';
        }
    };

    return (
        <div className="app">
            <div className="sidebar">
                <div className="sidebar-header">
                    <img src="/logo4.png" alt="Logo" className="main-icon" />
                    <h2 id="main-heading">SkinCare AI</h2>
                </div>
                <button onClick={() => handleTabChange('New Chat')}>New Chat</button>
                <button
                    className={activeTab === 'Skin Analysis' ? 'active' : ''}
                    onClick={() => handleTabChange('Skin Analysis')}
                >
                    Skin Analysis
                </button>
            </div>

            <div className="chat-interface">
                <div className="header">
                    <h3>{activeTab}</h3>
                </div>
                <div className="chat-window">
                          {messages.map((msg, index) => (
                          <div
                              key={index}
                              className={`chat-message ${
                                  msg.sender === 'user' ? 'user-message' : 'bot-message'
                              }`}
                          >
                              {msg.sender === 'bot' && (
                                  <div className="bot-response">
                                      <img
                                          src="/bot.png"
                                          alt="Bot Logo"
                                          className="bot-logo"
                                      />
                                      <div className="message-box">{msg.text}</div>
                                  </div>
                              )}
                              {msg.sender === 'user' && <div className="message-box">{msg.text}</div>}
                              {msg.image && (
                                  <img src={msg.image} alt="Uploaded" className="uploaded-image" />
                              )}
                          </div>
                      ))}
                  </div>

                <form onSubmit={sendMessage} className="chat-input">
                    <input type="text" name="message" placeholder="Type your message..." />
                    <label className="upload-btn">
                        <img src="/img.png" alt="Upload" className="upload-icon" />
                        <input
                            type="file"
                            accept="image/*"
                            onChange={handleImageUpload}
                            style={{ display: 'none' }}
                        />
                    </label>
                    <button type="submit">Send</button>
                </form>
            </div>
        </div>
    );
}

export default App;
