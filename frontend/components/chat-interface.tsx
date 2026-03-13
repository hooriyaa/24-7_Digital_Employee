"use client";

import { useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar } from "@/components/ui/avatar";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ticketsApi, Ticket } from "@/lib/api";
import { Sparkles } from "lucide-react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

interface ApiMessage {
  id: string;
  content: string;
  role: string;
  sender_type: string;
  created_at: string;
}

// Check if a UUID is the zero placeholder
const isValidTicketId = (id: string): boolean => {
  return !!id && id !== "00000000-0000-0000-0000-000000000000" && !id.match(/^0+$/);
};

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Hello! I'm your Customer Success FTE. How can I help you today?",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isClient, setIsClient] = useState(false);
  const [currentTicket, setCurrentTicket] = useState<Ticket | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<"disconnected" | "connecting" | "connected">("disconnected");
  const scrollRef = useRef<HTMLDivElement>(null);
  const [pollingInterval, setPollingInterval] = useState<NodeJS.Timeout | null>(null);
  const lastMessageCount = useRef<number>(0);

  // Fetch latest ticket for chat session
  const fetchLatestTicket = async () => {
    try {
      setConnectionStatus("connecting");
      const tickets = await ticketsApi.getAll();
      if (tickets.length > 0) {
        // Prefer open/in_progress tickets, otherwise use most recent
        const activeTicket = tickets.find(t => t.status === "open" || t.status === "in_progress") || tickets[0];
        setCurrentTicket(activeTicket);
        setConnectionStatus("connected");
        // Load conversation messages
        if (activeTicket.conversation_id) {
          await loadConversationMessages(activeTicket.conversation_id);
          startPolling(activeTicket.conversation_id);
        }
        return activeTicket;
      }
      setConnectionStatus("disconnected");
      return null;
    } catch (error) {
      console.error("Error fetching tickets:", error);
      setConnectionStatus("disconnected");
      return null;
    }
  };

  // Load messages from conversation
  const loadConversationMessages = async (conversationId: string | null) => {
    if (!conversationId) return;

    try {
      const response = await fetch(`http://localhost:8000/api/v1/conversations/${conversationId}/messages`);
      if (response.ok) {
        const data: ApiMessage[] = await response.json();
        const messages: Message[] = data.map(msg => ({
          id: msg.id,
          role: msg.sender_type === "customer" ? "user" : "assistant",
          content: msg.content,
          timestamp: new Date(msg.created_at),
        }));
        if (messages.length > 0) {
          // Only update if messages changed
          if (messages.length !== lastMessageCount.current) {
            console.log(`📥 [CHAT] Loaded ${messages.length} messages from conversation ${conversationId}`);
            setMessages(messages);
            lastMessageCount.current = messages.length;
          }
        }
      }
    } catch (error) {
      console.error("Error loading conversation messages:", error);
    }
  };

  // Start polling for new messages
  const startPolling = (conversationId: string) => {
    // Clear existing interval
    if (pollingInterval) {
      clearInterval(pollingInterval);
    }

    console.log(`🔄 [CHAT] Starting polling for conversation ${conversationId} (every 5s)`);

    // Poll every 5 seconds for new messages (reduced from 2s to avoid excessive requests)
    // Only poll when tab is visible
    const interval = setInterval(() => {
      if (document.visibilityState === "visible") {
        loadConversationMessages(conversationId);
      }
    }, 5000);

    setPollingInterval(interval);
  };

  // Stop polling
  const stopPolling = () => {
    if (pollingInterval) {
      clearInterval(pollingInterval);
      setPollingInterval(null);
      console.log(`⏹️  [CHAT] Stopped polling`);
    }
  };

  // Ensure client-side rendering and auto-connect to ticket
  useEffect(() => {
    setIsClient(true);

    // 🔑 KEY FIX: Check localStorage FIRST for redirect from ticket creation
    const storedTicket = localStorage.getItem("selectedTicket");
    if (storedTicket) {
      console.log(`🎫 [CHAT] Found selected ticket in localStorage on mount`);
      try {
        const ticket: Ticket = JSON.parse(storedTicket);
        console.log(`🎫 [CHAT] Ticket ID: ${ticket.id}, Conversation: ${ticket.conversation_id}`);
        setCurrentTicket(ticket);
        setConnectionStatus("connected");
        if (ticket.conversation_id) {
          console.log(`🔄 [CHAT] Loading messages for conversation: ${ticket.conversation_id}`);
          loadConversationMessages(ticket.conversation_id);
          startPolling(ticket.conversation_id);
        }
      } catch (err) {
        console.error("Error parsing stored ticket:", err);
      }
    } else {
      // Only fetch from API if no stored ticket
      console.log(`🎫 [CHAT] No stored ticket, fetching from API`);
      fetchLatestTicket();
    }

    // Listen for ticket selection from other pages (via localStorage)
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === "selectedTicket") {
        const ticketData = e.newValue;
        if (ticketData) {
          try {
            const ticket: Ticket = JSON.parse(ticketData);
            console.log(`🎫 [CHAT] Selected ticket from storage: ${ticket.id}, conversation: ${ticket.conversation_id}`);
            setCurrentTicket(ticket);
            setConnectionStatus("connected");
            // Load conversation messages for selected ticket
            if (ticket.conversation_id) {
              console.log(`🔄 [CHAT] Loading messages for NEW ticket conversation: ${ticket.conversation_id}`);
              loadConversationMessages(ticket.conversation_id);
              startPolling(ticket.conversation_id);
            }
          } catch (err) {
            console.error("Error parsing selected ticket:", err);
          }
        }
      }
    };

    window.addEventListener("storage", handleStorageChange);

    // Cleanup on unmount
    return () => {
      window.removeEventListener("storage", handleStorageChange);
      stopPolling();
    };
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    // Ensure we have a valid ticket
    let ticketId = currentTicket?.id;

    if (!ticketId || !isValidTicketId(ticketId)) {
      // Try to fetch a valid ticket
      const ticket = await fetchLatestTicket();
      ticketId = ticket?.id;

      if (!ticketId || !isValidTicketId(ticketId)) {
        // Still no valid ticket - show error message
        const errorMessage: Message = {
          id: Date.now().toString(),
          role: "assistant",
          content: "I'm unable to connect to a ticket. Please select a ticket from the Tickets page first, or refresh to try again.",
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, errorMessage]);
        return;
      }
    }

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/v1/agent/respond", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ticket_id: ticketId,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: data.response,
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } else if (response.status === 404) {
        // Ticket not found - try to reconnect
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: "The selected ticket was not found. Let me try to connect to another ticket...",
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, errorMessage]);

        // Attempt to reconnect
        const ticket = await fetchLatestTicket();
        if (ticket) {
          const retryMessage: Message = {
            id: (Date.now() + 2).toString(),
            role: "assistant",
            content: `Reconnected to ticket ${ticket.id.slice(0, 8)}... Please resend your message.`,
            timestamp: new Date(),
          };
          setMessages((prev) => [...prev, retryMessage]);
        }
      } else if (response.status === 422) {
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: "Thank you for your message! I'm processing your request.",
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } else {
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: "I received your message. Let me look into that for you.",
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, assistantMessage]);
      }
    } catch (error) {
      console.error("Error:", error);
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "I'm having trouble connecting to the server. Please try again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Format timestamp for display (client-side only)
  const formatTime = (date: Date) => {
    if (!isClient) return "";
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="flex h-full flex-col bg-gradient-to-br from-[#F8F9F8] via-[#DBE2DC] to-[#F8F9F8]">
      {/* Header */}
      <div className="flex items-center justify-between border-b-2 border-[#DBE2DC] bg-white/80 backdrop-blur-xl p-4 shadow-md">
        <div>
          <h1 className="text-lg font-bold text-[#335765]">Customer Support Chat</h1>
          <div className="text-sm text-[#74A8A4]">
            AI-powered 24/7 assistance
            {currentTicket && isValidTicketId(currentTicket.id) ? (
              <span className="ml-2 text-xs text-[#556b7a]">
                • Ticket: {currentTicket.id.slice(0, 8)}...
              </span>
            ) : (
              <span className="ml-2 text-xs text-orange-500">
                • {connectionStatus === "connecting" ? "Connecting..." : "No ticket selected"}
              </span>
            )}
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Badge
            variant="outline"
            className={
              connectionStatus === "connected"
                ? "bg-green-50 text-green-700 border-green-200 font-semibold"
                : connectionStatus === "connecting"
                ? "bg-yellow-50 text-yellow-700 border-yellow-200 font-semibold"
                : "bg-red-50 text-red-700 border-red-200 font-semibold"
            }
          >
            {connectionStatus === "connected" ? "✓ Online" : connectionStatus === "connecting" ? "⋯ Connecting..." : "✕ Offline"}
          </Badge>
          <Badge variant="secondary" className="bg-gradient-to-r from-[#74A8A4] to-[#B6D9E0] text-white border-0 font-semibold">
            <Sparkles className="w-3 h-3 mr-1" />
            Gemini
          </Badge>
        </div>
      </div>

      {/* Messages */}
      <ScrollArea className="flex-1 p-4" ref={scrollRef}>
        <div className="space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex items-start gap-3 ${
                message.role === "user" ? "flex-row-reverse" : ""
              }`}
            >
              <Avatar className="h-10 w-10 shadow-lg">
                <div className={`flex h-full w-full items-center justify-center text-xs font-bold ${
                  message.role === "user" 
                    ? "bg-gradient-to-br from-[#335765] to-[#74A8A4] text-white" 
                    : "bg-gradient-to-br from-[#74A8A4] to-[#B6D9E0] text-white"
                }`}>
                  {message.role === "user" ? "U" : "AI"}
                </div>
              </Avatar>
              <Card
                className={`max-w-[70%] p-4 shadow-lg transition-all ${
                  message.role === "user"
                    ? "bg-gradient-to-br from-[#335765] to-[#74A8A4] text-white border-0"
                    : "bg-white/90 backdrop-blur-xl text-[#335765] border-2 border-[#DBE2DC]"
                }`}
              >
                <div className="text-sm leading-relaxed">{message.content}</div>
                {isClient && (
                  <div className={`mt-2 text-xs ${
                    message.role === "user" ? "text-[#B6D9E0]" : "text-[#74A8A4]"
                  }`}>
                    {formatTime(message.timestamp)}
                  </div>
                )}
              </Card>
            </div>
          ))}
          {isLoading && (
            <div className="flex items-start gap-3">
              <Avatar className="h-10 w-10 shadow-lg">
                <div className="flex h-full w-full items-center justify-center text-xs font-bold bg-gradient-to-br from-[#74A8A4] to-[#B6D9E0] text-white">
                  AI
                </div>
              </Avatar>
              <Card className="max-w-[70%] p-4 bg-white/90 backdrop-blur-xl border-2 border-[#DBE2DC] shadow-lg">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 animate-bounce rounded-full bg-[#74A8A4]" />
                  <div className="h-2 w-2 animate-bounce rounded-full bg-[#74A8A4] [animation-delay:0.2s]" />
                  <div className="h-2 w-2 animate-bounce rounded-full bg-[#74A8A4] [animation-delay:0.4s]" />
                </div>
                <div className="mt-2 text-xs text-[#74A8A4] italic">
                  Typing...
                </div>
              </Card>
            </div>
          )}
        </div>
      </ScrollArea>

      {/* Input */}
      <div className="border-t-2 border-[#DBE2DC] bg-white/80 backdrop-blur-xl p-4 shadow-inner">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={connectionStatus === "connected" ? "Type your message..." : "Connecting to ticket..."}
            className="flex-1 rounded-xl border-2 border-[#DBE2DC] bg-white px-4 py-3 text-sm text-[#335765] placeholder:text-[#9fb5b8] focus:outline-none focus:border-[#74A8A4] focus:ring-2 focus:ring-[#74A8A4]/20 transition-all"
            disabled={isLoading || connectionStatus !== "connected"}
          />
          <Button 
            type="submit" 
            disabled={isLoading || !input.trim() || connectionStatus !== "connected"}
            className="bg-gradient-to-r from-[#335765] to-[#74A8A4] hover:from-[#2a4752] hover:to-[#5d8f8b] text-white shadow-lg hover:shadow-xl transition-all px-6"
          >
            <Send className="w-4 h-4" />
          </Button>
        </form>
      </div>
    </div>
  );
}
