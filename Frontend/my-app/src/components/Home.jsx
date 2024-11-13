import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Camera, Send, Loader2, Settings, PlusCircle, Trash2, Image as ImageIcon } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { useToast } from "@/components/ui/use-toast";
import { Badge } from "@/components/ui/badge";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

const SkinCareAI = () => {
  const { toast } = useToast();
  const scrollAreaRef = useRef(null);
  const [conversations, setConversations] = useState([
    { id: 1, name: 'Skin Analysis', messages: [] },
    { id: 2, name: 'Product Recommendations', messages: [] }
  ]);
  const [activeConversation, setActiveConversation] = useState(1);
  const [message, setMessage] = useState('');
  const [imagePreview, setImagePreview] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [newChatName, setNewChatName] = useState('');

  useEffect(() => {
    if (scrollAreaRef.current) {
      const scrollArea = scrollAreaRef.current;
      scrollArea.scrollTop = scrollArea.scrollHeight;
    }
  }, [conversations]);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        toast({
          title: "File too large",
          description: "Please select an image under 5MB",
          variant: "destructive",
        });
        return;
      }
      
      if (!file.type.startsWith('image/')) {
        toast({
          title: "Invalid file type",
          description: "Please select an image file",
          variant: "destructive",
        });
        return;
      }
      
      setImagePreview(file);
    }
  };

  const handleNewChat = () => {
    const newId = Math.max(...conversations.map(c => c.id)) + 1;
    const newConversation = {
      id: newId,
      name: newChatName || `New Chat ${newId}`,
      messages: []
    };
    setConversations([...conversations, newConversation]);
    setActiveConversation(newId);
    setNewChatName('');
  };

  const handleDeleteConversation = (id) => {
    setConversations(conversations.filter(conv => conv.id !== id));
    if (activeConversation === id) {
      setActiveConversation(conversations[0]?.id);
    }
  };

  const handleSendMessage = async () => {
    if (!message.trim() && !imagePreview) return;
    
    try {
      setIsLoading(true);
      
      // Create new message object
      const newMessage = {
        id: Date.now(),
        text: message,
        image: imagePreview ? URL.createObjectURL(imagePreview) : null,
        sender: 'user',
        timestamp: new Date().toISOString()
      };

      // Update UI with user message
      setConversations(prev =>
        prev.map(conv =>
          conv.id === activeConversation
            ? { ...conv, messages: [...conv.messages, newMessage] }
            : conv
        )
      );

      // Prepare form data
      const formData = new FormData();
      formData.append('message', message);  // Changed from 'prompt_text' to 'message'
      formData.append('conversation_id', activeConversation);
      if (imagePreview) {
        formData.append('image', imagePreview);
      }

      // Make API request
      const response = await axios.post(
        'http://localhost:8000/api/messages/',
        formData,
        {
          headers: { 
            'Content-Type': 'multipart/form-data',
            // Add any required authentication headers here
          },
        }
      );

      // Handle API response
      if (response.data) {
        // Assuming your Django backend returns a response with AI message
        const aiResponse = {
          id: Date.now() + 1,
          text: response.data.response || response.data.message, // Handle both possible response formats
          sender: 'ai',
          timestamp: new Date().toISOString()
        };

        setConversations(prev =>
          prev.map(conv =>
            conv.id === activeConversation
              ? { ...conv, messages: [...conv.messages, aiResponse] }
              : conv
          )
        );
      }

      // Clear input states
      setMessage('');
      setImagePreview(null);
      
    } catch (error) {
      console.error('Error:', error);
      toast({
        title: "Error",
        description: error.response?.data?.error || "Failed to send message. Please try again.",
        variant: "destructive",
      });
      
      const errorMessage = {
        id: Date.now(),
        text: 'Sorry, there was an error processing your request. Please try again.',
        sender: 'ai',
        timestamp: new Date().toISOString()
      };
      
      setConversations(prev =>
        prev.map(conv =>
          conv.id === activeConversation
            ? { ...conv, messages: [...conv.messages, errorMessage] }
            : conv
        )
      );
    } finally {
      setIsLoading(false);
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
              <DropdownMenuContent align="end" className="w-48">
                <DropdownMenuLabel>Settings</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem>
                  <span>Profile</span>
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <span>Preferences</span>
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <span>Help</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
          
          {/* New Chat Dialog */}
          <AlertDialog>
            <AlertDialogTrigger asChild>
              <Button className="w-full" size="sm">
                <PlusCircle className="mr-2 h-4 w-4" />
                New Chat
              </Button>
            </AlertDialogTrigger>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>Create New Chat</AlertDialogTitle>
                <AlertDialogDescription>
                  Enter a name for your new chat session
                </AlertDialogDescription>
              </AlertDialogHeader>
              <Input
                value={newChatName}
                onChange={(e) => setNewChatName(e.target.value)}
                placeholder="Chat name"
                className="my-4"
              />
              <AlertDialogFooter>
                <AlertDialogCancel>Cancel</AlertDialogCancel>
                <AlertDialogAction onClick={handleNewChat}>Create</AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </CardHeader>

        <ScrollArea className="flex-1 px-2">
          {conversations.map(conv => (
            <div key={conv.id} className="flex items-center gap-2 mb-1">
              <Button
                variant={activeConversation === conv.id ? "secondary" : "ghost"}
                className="w-full justify-start"
                onClick={() => setActiveConversation(conv.id)}
              >
                {conv.name}
                {conv.messages.length > 0 && (
                  <Badge variant="secondary" className="ml-2">
                    {conv.messages.length}
                  </Badge>
                )}
              </Button>
              <AlertDialog>
                <AlertDialogTrigger asChild>
                  <Button variant="ghost" size="icon" className="h-8 w-8">
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </AlertDialogTrigger>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle>Delete Conversation</AlertDialogTitle>
                    <AlertDialogDescription>
                      Are you sure you want to delete this conversation? This action cannot be undone.
                    </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel>Cancel</AlertDialogCancel>
                    <AlertDialogAction onClick={() => handleDeleteConversation(conv.id)}>
                      Delete
                    </AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </div>
          ))}
        </ScrollArea>
      </Card>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        <ScrollArea className="flex-1 p-4" ref={scrollAreaRef}>
          <div className="space-y-4">
            {conversations.find(c => c.id === activeConversation)?.messages.map(msg => (
              <div
                key={msg.id}
                className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className="flex items-start gap-3 max-w-[70%]">
                  {msg.sender === 'ai' && (
                    <Avatar>
                      <AvatarImage src="/ai-avatar.png" />
                      <AvatarFallback>AI</AvatarFallback>
                    </Avatar>
                  )}
                  <Card className={msg.sender === 'user' ? 'bg-primary text-primary-foreground' : ''}>
                    <CardContent className="p-3">
                      {msg.image && (
                        <div className="mb-2">
                          <img
                            src={msg.image}
                            alt="Uploaded skin"
                            className="rounded-lg max-w-xs object-cover"
                          />
                        </div>
                      )}
                      <p className="whitespace-pre-wrap">{msg.text}</p>
                      <p className="text-xs mt-1 opacity-70">
                        {new Date(msg.timestamp).toLocaleTimeString()}
                      </p>
                    </CardContent>
                  </Card>
                  {msg.sender === 'user' && (
                    <Avatar>
                      <AvatarImage src="/user-avatar.png" />
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
                    <AvatarImage src="/ai-avatar.png" />
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
              <div className="mb-3 relative inline-block">
                <img
                  src={URL.createObjectURL(imagePreview)}
                  alt="Preview"
                  className="h-20 rounded-lg"
                />
                <Button
                  variant="destructive"
                  size="icon"
                  className="absolute -top-2 -right-2 h-6 w-6 rounded-full"
                  onClick={() => setImagePreview(null)}
                >
                  <Trash2 className="h-3 w-3" />
                </Button>
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
                className={imagePreview ? 'opacity-50' : ''}
                disabled={!!imagePreview}
              >
                <label htmlFor="image-upload" className="cursor-pointer">
                  <Camera className="h-4 w-4" />
                </label>
              </Button>
              <Input
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type your message..."
                onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
                disabled={isLoading}
              />
              <Button 
                onClick={handleSendMessage} 
                size="icon"
                disabled={isLoading || (!message.trim() && !imagePreview)}
              >
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