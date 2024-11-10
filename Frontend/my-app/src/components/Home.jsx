import { useState } from 'react';
import axios from 'axios';
import { Camera, Send, Loader2, Settings, PlusCircle } from 'lucide-react';
import { Button } from "./ui/button";
import { Input } from "./ui/input";
// import { Separator } from "./ui/separator";
import { ScrollArea } from "./ui/scroll-area";
import { Avatar, AvatarFallback } from "./ui/avatar";

import {
  Card,
  CardContent,
  // CardDescription,
  // CardFooter,
  CardHeader,
  CardTitle,
} from "./ui/card";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu";

const SkinCareAI = () => {
  const [conversations, setConversations] = useState([
    { id: 1, name: 'Skin Analysis', messages: [] },
    { id: 2, name: 'Product Recommendations', messages: [] }
  ]);
  const [activeConversation, setActiveConversation] = useState(1);
  const [message, setMessage] = useState('');
  const [imagePreview, setImagePreview] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Handle image upload and set preview
  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImagePreview(file);  // Store the file object instead of base64 string
    }
  };

  // Handle sending message and making API request
  const handleSendMessage = async () => {
    if (message.trim() || imagePreview) {
      const newMessage = {
        id: Date.now(),
        text: message,
        image: imagePreview ? URL.createObjectURL(imagePreview) : null, // Display image preview
        sender: 'user',
        timestamp: new Date().toISOString()
      };

      // Update the conversation with the new message
      setConversations(prev => 
        prev.map(conv => 
          conv.id === activeConversation
            ? { ...conv, messages: [...conv.messages, newMessage] }
            : conv
        )
      );

      setMessage('');
      setImagePreview(null);
      setIsLoading(true);

      // Prepare FormData for API request
      const formData = new FormData();
      formData.append('prompt_text', message);
      if (imagePreview) {
        formData.append('image', imagePreview); // Send the file object
      }

      try {
        // Send the form data to the backend (Gemini API)
        const response = await axios.post('http://localhost:8000/api/skin-care-suggestions/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        // Log the full response to debug
        console.log('AI Response:', response.data); // Check if the response contains 'suggestions' or an error

        if (response.data && response.data.suggestions) {
          const aiResponse = {
            id: Date.now(),
            text: response.data.suggestions, // Use the suggestions from the response
            sender: 'ai',
            timestamp: new Date().toISOString()
          };

          // Add the AI response to the active conversation
          setConversations(prev => 
            prev.map(conv => 
              conv.id === activeConversation
                ? { ...conv, messages: [...conv.messages, aiResponse] }
                : conv
            )
          );
        } else {
          console.error('No suggestions found in the response');
        }
      } catch (error) {
        console.error('Error sending message:', error);
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <Card className="w-64 h-full rounded-none border-r">
        <CardHeader className="space-y-1 px-4">
          <div className="flex items-center justify-between">
            <CardTitle>SkinCare AI</CardTitle>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon">
                  <Settings className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuLabel>Settings</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem>Profile</DropdownMenuItem>
                <DropdownMenuItem>Preferences</DropdownMenuItem>
                <DropdownMenuItem>Help</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
          <Button className="w-full" size="sm">
            <PlusCircle className="mr-2 h-4 w-4" />
            New Chat
          </Button>
        </CardHeader>
        <ScrollArea className="flex-1 px-2">
          {conversations.map(conv => (
            <Button
              key={conv.id}
              variant={activeConversation === conv.id ? "secondary" : "ghost"}
              className="w-full justify-start mb-1"
              onClick={() => setActiveConversation(conv.id)}
            >
              {conv.name}
            </Button>
          ))}
        </ScrollArea>
      </Card>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        <ScrollArea className="flex-1 p-4">
          <div className="space-y-4">
            {conversations.find(c => c.id === activeConversation)?.messages.map(msg => (
              <div
                key={msg.id}
                className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className="flex items-start gap-3 max-w-[70%]">
                  {msg.sender === 'ai' && (
                    <Avatar>
                      <AvatarFallback>AI</AvatarFallback>
                    </Avatar>
                  )}
                  <Card className={msg.sender === 'user' ? 'bg-primary text-primary-foreground' : ''}>
                    <CardContent className="p-3">
                      {msg.image && (
                        <img
                          src={msg.image}
                          alt="Uploaded skin"
                          className="mb-2 rounded-lg max-w-xs"
                        />
                      )}
                      <p>{msg.text}</p>
                      <p className="text-xs mt-1 opacity-70">
                        {new Date(msg.timestamp).toLocaleTimeString()}
                      </p>
                    </CardContent>
                  </Card>
                  {msg.sender === 'user' && (
                    <Avatar>
                      <AvatarFallback>ME</AvatarFallback>
                    </Avatar>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="flex items-start gap-3">
                  <Avatar>
                    <AvatarFallback>AI</AvatarFallback>
                  </Avatar>
                  <Card>
                    <CardContent className="p-3">
                      <Loader2 className="w-5 h-5 animate-spin" />
                    </CardContent>
                  </Card>
                </div>
              </div>
            )}
          </div>
        </ScrollArea>

        {/* Input Area */}
        <Card className="mx-4 mb-4">
          <CardContent className="p-4">
            {imagePreview && (
              <div className="mb-3">
                <img
                  src={URL.createObjectURL(imagePreview)}  // Preview the selected image
                  alt="Preview"
                  className="h-20 rounded-lg"
                />
              </div>
            )}
            <div className="flex items-center space-x-2">
              <input
                type="file"
                accept="image/*"
                id="image-upload"
                className="hidden"
                onChange={handleImageUpload}
              />
              <Button
                variant="outline"
                size="icon"
                asChild
              >
                <label htmlFor="image-upload">
                  <Camera className="h-4 w-4" />
                </label>
              </Button>
              <Input
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type your message..."
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              />
              <Button onClick={handleSendMessage} size="icon">
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default SkinCareAI;
