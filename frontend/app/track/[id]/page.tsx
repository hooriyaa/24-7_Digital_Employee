"use client";

import { useState, useEffect, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
  ArrowLeft,
  Send,
  User,
  Bot,
  Clock,
  CheckCircle2,
  AlertCircle,
  Loader2,
  Sparkles,
  MessageSquare,
  Ticket
} from "lucide-react";
import { gsap } from "gsap";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(useGSAP);

interface Message {
  id: string;
  content: string;
  sender_type: string;
  role: string;
  channel: string;
  created_at: string;
}

interface TicketData {
  ticket_id: string;
  subject: string;
  status: string;
  priority: string;
  created_at: string;
  messages: Message[];
  message_count: number;
}

export default function TrackPage() {
  const params = useParams();
  const router = useRouter();
  const ticketId = params.id as string;
  
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState("");
  const [ticketData, setTicketData] = useState<TicketData | null>(null);
  const [newMessage, setNewMessage] = useState("");
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [ticketData?.messages]);

  // Fetch ticket data
  useEffect(() => {
    if (ticketId) {
      fetchTicket();
    }
  }, [ticketId]);

  const fetchTicket = async (isRefresh = false) => {
    if (isRefresh) {
      setRefreshing(true);
    } else {
      setLoading(true);
    }
    setError("");
    
    try {
      const response = await fetch(`http://localhost:8000/api/v1/tickets/status?ticket_id=${ticketId}`);
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ticket not found");
      }

      const data = await response.json();
      
      // Update ticket data - use backend data as source of truth
      setTicketData(prev => {
        if (!prev) return data;
        
        // Get optimistic messages that haven't been confirmed by backend yet
        const optimisticMessages = prev.messages.filter(m => m.id.startsWith("temp-"));
        
        // Remove optimistic messages that are now in backend data
        // Match by content (since backend generates new ID)
        const confirmedOptimisticContents = new Set(
          optimisticMessages
            .filter(optMsg => 
              data.messages.some(dataMsg => dataMsg.content === optMsg.content)
            )
            .map(optMsg => optMsg.content)
        );
        
        // Keep only optimistic messages that haven't been confirmed
        const remainingOptimisticMessages = optimisticMessages.filter(
          optMsg => !confirmedOptimisticContents.has(optMsg.content)
        );
        
        // Combine backend messages with remaining optimistic messages
        const allMessages = [...data.messages, ...remainingOptimisticMessages];
        
        // Sort by timestamp
        allMessages.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
        
        return {
          ...data,
          messages: allMessages,
          message_count: allMessages.length
        };
      });
    } catch (err: any) {
      setError(err.message || "Failed to fetch ticket");
    } finally {
      if (isRefresh) {
        setRefreshing(false);
      } else {
        setLoading(false);
      }
    }
  };

  const handleSendMessage = async (e?: React.FormEvent) => {
    if (e) e.preventDefault(); // Prevent page reload
    
    if (!newMessage.trim() || !ticketData) return;

    setSending(true);
    
    // Optimistically add user message to UI immediately
    const tempMessage = {
      id: "temp-" + Date.now(),
      content: newMessage,
      sender_type: "customer",
      role: "user",
      channel: "web",
      created_at: new Date().toISOString(),
    };
    
    // Update UI immediately with user message
    setTicketData(prev => prev ? {
      ...prev,
      messages: [...prev.messages, tempMessage],
      message_count: prev.message_count + 1
    } : null);
    
    const messageToSend = newMessage;
    setNewMessage("");
    
    try {
      const response = await fetch(`http://localhost:8000/api/v1/tickets/${ticketData.ticket_id}/messages`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          content: messageToSend,
          sender_type: "customer",
          channel: "web",
          role: "user",
        }),
      });

      if (response.ok) {
        // Refresh to get AI response after a short delay
        setTimeout(() => fetchTicket(true), 800);
      } else {
        throw new Error("Failed to send message");
      }
    } catch (err: any) {
      setError(err.message || "Failed to send message");
      // Revert optimistic update on error
      setTicketData(prev => prev ? {
        ...prev,
        messages: prev.messages.filter(m => !m.id.startsWith("temp-")),
        message_count: prev.message_count - 1
      } : null);
    } finally {
      setSending(false);
    }
  };

  // GSAP animations
  useGSAP(() => {
    gsap.from(".track-header", {
      opacity: 0,
      y: 30,
      duration: 0.8,
      ease: "power3.out",
    });

    gsap.from(".messages-container", {
      opacity: 0,
      y: 50,
      duration: 0.8,
      delay: 0.2,
      ease: "power3.out",
    });

    gsap.from(".message-input", {
      opacity: 0,
      y: 30,
      duration: 0.6,
      delay: 0.4,
      ease: "power3.out",
    });
  });

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      open: "bg-[#B6D9E0]/30 text-[#335765] border-[#335765]/30",
      active: "bg-[#74A8A4]/30 text-[#335765] border-[#335765]/30",
      resolved: "bg-[#74A8A4]/30 text-[#335765] border-[#335765]/30",
      escalated: "bg-[#E74C3C]/30 text-[#335765] border-[#335765]/30",
    };
    return colors[status.toLowerCase()] || "bg-[#95A5A6]/30";
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-[#F8F9F8] via-[#DBE2DC] to-[#F8F9F8] flex items-center justify-center p-4">
        <div className="text-center">
          {/* Beautiful 3D Loading Animation */}
          <div className="relative w-16 h-16 sm:w-20 sm:h-20 mx-auto mb-4 sm:mb-6">
            {/* Outer Ring */}
            <div className="absolute inset-0 rounded-full border-4 border-[#74A8A4]/20 border-t-[#74A8A4] animate-spin"></div>
            {/* Middle Ring */}
            <div className="absolute inset-2 rounded-full border-4 border-[#B6D9E0]/20 border-r-[#B6D9E0] animate-spin" style={{ animationDirection: 'reverse', animationDuration: '0.8s' }}></div>
            {/* Inner Dot */}
            <div className="absolute inset-4 rounded-full bg-gradient-to-br from-[#335765] to-[#74A8A4] animate-ping" style={{ animationDuration: '1.5s' }}></div>
            {/* Center Glow */}
            <div className="absolute inset-0 rounded-full bg-gradient-to-br from-[#74A8A4] to-[#B6D9E0] opacity-20 blur-md animate-pulse"></div>
          </div>
          <p className="text-[#335765] font-semibold text-sm sm:text-lg">Loading ticket...</p>
        </div>
      </div>
    );
  }

  if (error || !ticketData) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-[#F8F9F8] via-[#DBE2DC] to-[#F8F9F8] flex items-center justify-center p-4">
        <Card className="max-w-md sm:max-w-lg w-full p-6 sm:p-8 md:p-10 bg-white/95 backdrop-blur-xl border-2 border-[#DBE2DC] shadow-2xl text-center animate-scale-in">
          {/* Animated Error Icon */}
          <div className="relative mb-4 sm:mb-6">
            {/* Outer Glow */}
            <div className="absolute inset-0 rounded-full bg-[#E74C3C] opacity-20 blur-xl animate-pulse"></div>
            {/* Main Icon Container */}
            <div className="relative w-16 h-16 sm:w-20 sm:h-20 md:w-24 md:h-24 mx-auto bg-gradient-to-br from-[#E74C3C] via-[#E74C3C]/80 to-[#E74C3C]/60 rounded-full flex items-center justify-center shadow-lg transform hover:scale-110 transition-transform duration-300">
              <AlertCircle className="w-8 h-8 sm:w-10 sm:h-10 md:w-12 md:h-12 text-white" />
            </div>
            {/* Orbiting Dot */}
            <div className="absolute inset-0 animate-spin" style={{ animationDuration: '3s' }}>
              <div className="absolute top-0 left-1/2 w-2 h-2 sm:w-3 sm:h-3 bg-[#E74C3C] rounded-full transform -translate-x-1/2 -translate-y-1 shadow-lg"></div>
            </div>
          </div>

          {/* Title */}
          <h2 className="text-xl sm:text-2xl md:text-3xl font-bold bg-gradient-to-r from-[#E74C3C] to-[#E74C3C]/60 bg-clip-text text-transparent mb-2 sm:mb-3">
            Ticket Not Found
          </h2>

          {/* Description */}
          <p className="text-[#556b7a] text-sm sm:text-base md:text-lg mb-6 sm:mb-8 leading-relaxed">
            {error || "We couldn't find a ticket with that ID. Please check the tracking ID and try again."}
          </p>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-2 sm:gap-3 justify-center">
            <Button
              onClick={() => router.push("/")}
              className="bg-gradient-to-r from-[#335765] to-[#74A8A4] text-white shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 px-4 sm:px-6 md:px-8 py-4 sm:py-5 md:py-6 text-sm sm:text-base font-semibold"
            >
              Go to Home
            </Button>
            <Button
              onClick={() => router.push("/check-status")}
              variant="outline"
              className="border-2 border-[#335765] text-[#335765] hover:bg-[#335765] hover:text-white transition-all duration-300 hover:-translate-y-1 px-4 sm:px-6 md:px-8 py-4 sm:py-5 md:py-6 text-sm sm:text-base font-semibold"
            >
              Check Another Ticket
            </Button>
          </div>

          {/* Help Text */}
          <div className="mt-4 sm:mt-6 pt-4 sm:pt-6 border-t border-[#DBE2DC]">
            <p className="text-xs sm:text-sm text-[#74A8A4] font-medium">
              Need help?{" "}
              <a href="/contact" className="text-[#335765] hover:text-[#74A8A4] underline font-semibold">
                Contact Support
              </a>
            </p>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#F8F9F8] via-[#DBE2DC] to-[#F8F9F8]">
      {/* Navigation */}
      <nav className="border-b border-[#DBE2DC]/50 bg-white/95 backdrop-blur-xl sticky top-0 z-50 shadow-md">
        <div className="container mx-auto px-3 md:px-4 py-2 md:py-3">
          <div className="flex items-center justify-between gap-2">
            <div className="flex items-center gap-2 flex-1 min-w-0">
              <Button
                onClick={() => router.push("/check-status?ticket=" + ticketId)}
                variant="outline"
                className="border-2 border-[#335765] text-[#335765] hover:bg-[#335765] hover:text-white transition-all cursor-pointer flex-shrink-0 h-9 md:h-10 px-2 md:px-3"
                disabled={refreshing}
              >
                {refreshing ? (
                  <Loader2 className="w-3 h-3 md:w-4 md:h-4 animate-spin" />
                ) : (
                  <ArrowLeft className="w-3 h-3 md:w-4 md:h-4" />
                )}
                <span className="hidden sm:inline ml-1 md:ml-2 text-xs md:text-sm">Back</span>
              </Button>
              <div className="w-8 h-8 md:w-10 md:h-10 bg-gradient-to-br from-[#335765] via-[#74A8A4] to-[#B6D9E0] rounded-lg md:rounded-xl flex items-center justify-center shadow-md flex-shrink-0">
                <MessageSquare className="w-4 h-4 md:w-5 md:h-5 md:h-6 text-white" />
              </div>
              <div className="flex-1 min-w-0">
                <h1 className="text-sm md:text-lg font-bold bg-gradient-to-r from-[#335765] to-[#74A8A4] bg-clip-text text-transparent truncate">
                  Ticket Conversation
                </h1>
                <p className="text-[10px] md:text-xs text-[#556b7a] font-medium hidden sm:block">Track & Chat</p>
              </div>
            </div>
            <div className="flex items-center gap-1 md:gap-2 flex-shrink-0">
              {refreshing && (
                <Badge className="bg-[#74A8A4]/30 text-[#335765] border-[#335765]/30 hidden sm:flex">
                  <Loader2 className="w-3 h-3 mr-1 md:mr-2 animate-spin" />
                  <span className="text-xs">Updating...</span>
                </Badge>
              )}
              <Badge className={`${getStatusColor(ticketData.status)} border px-2 md:px-3 py-1 rounded-full font-semibold text-xs md:text-sm`}>
                <span className="hidden xs:inline">{ticketData.status.replace("_", " ")}</span>
                <span className="xs:hidden">{ticketData.status}</span>
              </Badge>
            </div>
          </div>
        </div>
      </nav>

      {/* Main content */}
      <div className="container mx-auto px-3 md:px-4 py-4 md:py-8 max-w-4xl">
        {/* Header */}
        <Card className="track-header mb-4 md:mb-6 bg-white/90 backdrop-blur-xl border-2 border-[#DBE2DC] shadow-2xl">
          <div className="p-4 md:p-6">
            <div className="flex flex-col sm:flex-row items-start justify-between gap-3 mb-3 md:mb-4">
              <div className="flex-1 min-w-0">
                <h2 className="text-lg sm:text-xl md:text-2xl font-bold text-[#335765] mb-1 md:mb-2 truncate">
                  {ticketData.subject}
                </h2>
                <p className="text-xs sm:text-sm text-[#556b7a] break-all">
                  Ticket ID: <span className="font-mono text-[#74A8A4] font-bold">{ticketId}</span>
                </p>
              </div>
              <div className="flex items-center gap-2 flex-shrink-0">
                <Badge className={`${getStatusColor(ticketData.priority)} border px-2 md:px-3 py-1 rounded-full font-semibold text-xs md:text-sm`}>
                  {ticketData.priority}
                </Badge>
              </div>
            </div>
            <div className="flex flex-wrap items-center gap-2 md:gap-4 text-xs sm:text-sm text-[#556b7a]">
              <div className="flex items-center gap-1 md:gap-2">
                <Clock className="w-3 h-3 md:w-4 md:h-4 text-[#74A8A4]" />
                <span className="truncate">Created: {new Date(ticketData.created_at).toLocaleDateString()}</span>
              </div>
              <div className="flex items-center gap-1 md:gap-2">
                <MessageSquare className="w-3 h-3 md:w-4 md:h-4 text-[#74A8A4]" />
                <span>{ticketData.message_count} messages</span>
              </div>
            </div>
          </div>
        </Card>

        {/* Messages */}
        <Card className="messages-container mb-4 md:mb-6 bg-white/90 backdrop-blur-xl border-2 border-[#DBE2DC] shadow-2xl">
          <div className="p-3 md:p-6">
            <div className="space-y-3 md:space-y-4 max-h-[400px] sm:max-h-[500px] overflow-y-auto">
              {ticketData.messages.map((msg, index) => (
                <div
                  key={msg.id}
                  className={`flex gap-2 md:gap-3 ${
                    msg.sender_type === "customer" ? "flex-row-reverse" : ""
                  }`}
                >
                  <div
                    className={`w-8 h-8 md:w-10 md:h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                      msg.sender_type === "customer"
                        ? "bg-gradient-to-br from-[#74A8A4] to-[#335765]"
                        : "bg-gradient-to-br from-[#335765] to-[#74A8A4]"
                    }`}
                  >
                    {msg.sender_type === "customer" ? (
                      <User className="w-4 h-4 md:w-5 md:h-5 text-white" />
                    ) : (
                      <Bot className="w-4 h-4 md:w-5 md:h-5 text-white" />
                    )}
                  </div>
                  <div
                    className={`max-w-[75%] sm:max-w-[70%] ${
                      msg.sender_type === "customer" ? "text-right" : "text-left"
                    }`}
                  >
                    <div
                      className={`p-2 md:p-4 rounded-xl md:rounded-2xl ${
                        msg.sender_type === "customer"
                          ? "bg-gradient-to-br from-[#74A8A4] to-[#335765] text-white"
                          : "bg-gradient-to-br from-[#B6D9E0] to-[#DBE2DC] text-[#335765]"
                      }`}
                    >
                      <p className="text-xs sm:text-sm leading-relaxed break-words">{msg.content}</p>
                    </div>
                    <p className="text-[10px] sm:text-xs text-[#556b7a] mt-1">
                      {new Date(msg.created_at).toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </p>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          </div>
        </Card>

        {/* Message Input */}
        <Card className="message-input bg-white/90 backdrop-blur-xl border-2 border-[#DBE2DC] shadow-2xl">
          <div className="p-3 md:p-4">
            <form onSubmit={handleSendMessage} className="flex gap-2 md:gap-3">
              <Input
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
                placeholder="Type your message..."
                className="flex-1 bg-white border-2 border-[#DBE2DC] text-[#335765] placeholder:text-[#9fb5b8] focus:border-[#74A8A4] focus:ring-2 focus:ring-[#74A8A4]/20 h-10 md:h-12 rounded-xl text-sm md:text-base"
                disabled={sending}
              />
              <Button
                type="submit"
                disabled={sending || !newMessage.trim()}
                className="bg-gradient-to-r from-[#335765] via-[#74A8A4] to-[#7F543D] hover:from-[#2a4752] hover:via-[#5d8f8b] hover:to-[#6b4632] text-white font-bold shadow-lg hover:shadow-xl transition-all h-10 md:h-12 px-3 md:px-6 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer flex-shrink-0"
              >
                {sending ? (
                  <Loader2 className="w-4 h-4 md:w-5 md:h-5 animate-spin" />
                ) : (
                  <>
                    <Send className="w-4 h-4 md:w-5 md:h-5 mr-1 md:mr-2" />
                    <span className="hidden sm:inline">Send</span>
                  </>
                )}
              </Button>
            </form>
            <p className="text-[10px] sm:text-xs text-[#556b7a] mt-2 text-center">
              Our AI assistant typically responds within 5 minutes
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
}
