"use client";

import { useState, useEffect, useRef } from "react";
import { useSearchParams } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import {
  Ticket,
  Search,
  Mail,
  Clock,
  CheckCircle2,
  AlertCircle,
  Loader2,
  ArrowLeft,
  MessageSquare,
  User,
  Calendar,
  Bot,
  Sparkles,
  MessageCircle,
  Shield,
  Zap,
  Brain
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

interface TicketStatus {
  ticket_id: string;
  subject: string;
  status: string;
  priority: string;
  created_at: string;
  updated_at: string | null;
  resolved_at: string | null;
  customer_name: string;
  customer_email: string;
  messages: Message[];
  message_count: number;
}

export default function CheckStatusPage() {
  const searchParams = useSearchParams();
  const [searchType, setSearchType] = useState<"ticket" | "email">("ticket");
  const [ticketId, setTicketId] = useState("");
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [ticketData, setTicketData] = useState<TicketStatus | null>(null);
  const [expandedMessage, setExpandedMessage] = useState<string | null>(null);

  const featuresRef = useRef<HTMLDivElement>(null);

  // Auto-search if ticket ID is in URL
  useEffect(() => {
    const ticketParam = searchParams.get("ticket");
    if (ticketParam) {
      setTicketId(ticketParam);
      setTimeout(() => {
        handleSearch();
      }, 500);
    }
  }, [searchParams]);

  // Status badge colors - matching website theme
  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      open: "bg-[#B6D9E0]/30 text-[#335765] border-[#335765]/30",
      active: "bg-[#74A8A4]/30 text-[#335765] border-[#335765]/30",
      pending: "bg-[#F4D03F]/30 text-[#335765] border-[#335765]/30",
      waiting_customer: "bg-[#E67E22]/30 text-[#335765] border-[#335765]/30",
      resolved: "bg-[#74A8A4]/30 text-[#335765] border-[#335765]/30",
      escalated: "bg-[#E74C3C]/30 text-[#335765] border-[#335765]/30",
      closed: "bg-[#95A5A6]/30 text-[#335765] border-[#335765]/30",
    };
    return colors[status.toLowerCase()] || "bg-[#95A5A6]/30 text-[#335765] border-[#335765]/30";
  };

  // Priority badge colors
  const getPriorityColor = (priority: string) => {
    const colors: Record<string, string> = {
      urgent: "bg-[#E74C3C]/30 text-[#335765] border-[#335765]/30",
      high: "bg-[#E67E22]/30 text-[#335765] border-[#335765]/30",
      normal: "bg-[#3498DB]/30 text-[#335765] border-[#335765]/30",
      low: "bg-[#95A5A6]/30 text-[#335765] border-[#335765]/30",
    };
    return colors[priority.toLowerCase()] || "bg-[#95A5A6]/30 text-[#335765] border-[#335765]/30";
  };

  // Format date
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  // Search for ticket
  const handleSearch = async () => {
    setLoading(true);
    setError("");
    setTicketData(null);

    try {
      const params = new URLSearchParams();
      if (searchType === "ticket" && ticketId) {
        params.append("ticket_id", ticketId);
      } else if (searchType === "email" && email) {
        params.append("email", email);
      } else {
        setError("Please enter a ticket ID or email address");
        setLoading(false);
        return;
      }

      const response = await fetch(`http://localhost:8000/api/v1/tickets/status?${params.toString()}`);
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ticket not found");
      }

      const data = await response.json();
      setTicketData(data);
      
      // Animate results
      gsap.fromTo(
        ".result-card",
        { opacity: 0, y: 50 },
        { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }
      );
    } catch (err: any) {
      setError(err.message || "Failed to fetch ticket status");
    } finally {
      setLoading(false);
    }
  };

  // GSAP animations
  useGSAP(() => {
    // Hero section animations
    gsap.from(".hero-badge", {
      opacity: 0,
      y: 30,
      duration: 0.8,
      ease: "power3.out",
    });

    gsap.from(".hero-title", {
      opacity: 0,
      y: 50,
      duration: 0.8,
      delay: 0.2,
      ease: "power3.out",
    });

    gsap.from(".hero-subtitle", {
      opacity: 0,
      y: 40,
      duration: 0.8,
      delay: 0.4,
      ease: "power3.out",
    });

    // Search card entrance
    gsap.fromTo(
      ".search-card",
      { opacity: 0, y: 100, rotateX: -10 },
      { opacity: 1, y: 0, rotateX: 0, duration: 1, ease: "power4.out" }
    );

    // Input fields stagger
    gsap.fromTo(
      ".input-field",
      { opacity: 0, x: -30 },
      { opacity: 1, x: 0, duration: 0.5, stagger: 0.2, delay: 0.5 }
    );

    // Search button pulse
    gsap.to(".search-btn", {
      scale: 1.02,
      duration: 2,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut",
    });

    // Floating elements
    gsap.to(".floating-orb-1", {
      x: "random(-30, 30)",
      y: "random(-30, 30)",
      duration: "random(4, 6)",
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut",
    });

    gsap.to(".floating-orb-2", {
      x: "random(-30, 30)",
      y: "random(-30, 30)",
      duration: "random(5, 7)",
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut",
    });
  });

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#F8F9F8] via-[#DBE2DC] to-[#F8F9F8]">
      {/* Animated background orbs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="floating-orb-1 absolute top-20 left-10 w-64 h-64 bg-[#B6D9E0]/30 rounded-full blur-3xl" />
        <div className="floating-orb-2 absolute bottom-20 right-10 w-80 h-80 bg-[#74A8A4]/20 rounded-full blur-3xl" />
      </div>

      {/* Navigation */}
      <nav className="border-b border-[#DBE2DC]/50 bg-white/95 backdrop-blur-xl sticky top-0 z-50 shadow-md">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-[#335765] via-[#74A8A4] to-[#B6D9E0] rounded-xl flex items-center justify-center shadow-md">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold bg-gradient-to-r from-[#335765] to-[#74A8A4] bg-clip-text text-transparent">
                  Check Status
                </h1>
                <p className="text-xs text-[#556b7a] font-medium">Track Your Ticket</p>
              </div>
            </div>
            <Button
              onClick={() => window.location.href = "/"}
              variant="outline"
              className="border-2 border-[#335765] text-[#335765] hover:bg-[#335765] hover:text-white transition-all cursor-pointer"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Home
            </Button>
          </div>
        </div>
      </nav>

      {/* Main content */}
      <div className="relative z-10 container mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <Badge className="hero-badge mb-4 bg-[#B6D9E0]/30 text-[#335765] border-[#335765]/30 font-medium px-4 py-2">
            <Ticket className="w-4 h-4 mr-2 inline" />
            Track Your Request
          </Badge>
          <h1 className="hero-title text-4xl md:text-5xl font-bold text-[#335765] mb-4">
            Check Your Ticket Status
          </h1>
          <p className="hero-subtitle text-lg text-[#556b7a] max-w-xl mx-auto">
            Track your support request in real-time. Enter your ticket ID or email to see updates.
          </p>
        </div>

        {/* Search Card */}
        <Card className="search-card max-w-2xl mx-auto bg-white/90 backdrop-blur-xl border-2 border-[#DBE2DC] shadow-2xl">
          <div className="p-8">
            {/* Search Type Toggle */}
            <div className="flex gap-4 mb-6">
              <button
                onClick={() => setSearchType("ticket")}
                className={`flex-1 py-3 px-4 rounded-xl font-semibold transition-all duration-300 cursor-pointer ${
                  searchType === "ticket"
                    ? "bg-gradient-to-r from-[#335765] to-[#74A8A4] text-white shadow-lg"
                    : "bg-[#F8F9F8] text-[#556b7a] hover:bg-[#DBE2DC]"
                }`}
              >
                <Ticket className="w-4 h-4 inline mr-2" />
                Search by Ticket ID
              </button>
              <button
                onClick={() => setSearchType("email")}
                className={`flex-1 py-3 px-4 rounded-xl font-semibold transition-all duration-300 cursor-pointer ${
                  searchType === "email"
                    ? "bg-gradient-to-r from-[#335765] to-[#74A8A4] text-white shadow-lg"
                    : "bg-[#F8F9F8] text-[#556b7a] hover:bg-[#DBE2DC]"
                }`}
              >
                <Mail className="w-4 h-4 inline mr-2" />
                Search by Email
              </button>
            </div>

            {/* Input Fields */}
            {searchType === "ticket" ? (
              <div className="space-y-4">
                <div className="input-field">
                  <Label className="text-[#335765] font-bold mb-2 block">
                    <Ticket className="w-4 h-4 inline mr-2" />
                    Ticket ID
                  </Label>
                  <Input
                    value={ticketId}
                    onChange={(e) => setTicketId(e.target.value)}
                    placeholder="e.g., TKT-12345 or full ID"
                    className="bg-white border-2 border-[#DBE2DC] text-[#335765] placeholder:text-[#9fb5b8] focus:border-[#74A8A4] focus:ring-2 focus:ring-[#74A8A4]/20 h-12 rounded-xl"
                    onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                  />
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="input-field">
                  <Label className="text-[#335765] font-bold mb-2 block">
                    <Mail className="w-4 h-4 inline mr-2" />
                    Email Address
                  </Label>
                  <Input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="your@email.com"
                    className="bg-white border-2 border-[#DBE2DC] text-[#335765] placeholder:text-[#9fb5b8] focus:border-[#74A8A4] focus:ring-2 focus:ring-[#74A8A4]/20 h-12 rounded-xl"
                    onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                  />
                </div>
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="mt-4 p-4 rounded-xl bg-[#E74C3C]/10 border border-[#E74C3C]/30 flex items-center gap-3">
                <AlertCircle className="w-5 h-5 text-[#E74C3C]" />
                <span className="text-[#E74C3C]">{error}</span>
              </div>
            )}

            {/* Search Button */}
            <Button
              onClick={handleSearch}
              disabled={loading}
              className="search-btn w-full mt-6 h-12 bg-gradient-to-r from-[#335765] via-[#74A8A4] to-[#7F543D] hover:from-[#2a4752] hover:via-[#5d8f8b] hover:to-[#6b4632] text-white font-bold shadow-lg hover:shadow-xl transition-all rounded-xl disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                  Searching...
                </>
              ) : (
                <>
                  <Search className="w-5 h-5 mr-2" />
                  Check Status
                </>
              )}
            </Button>
          </div>
        </Card>

        {/* Results */}
        {ticketData && (
          <div className="result-card max-w-4xl mx-auto mt-8 space-y-6">
            {/* Ticket Info Card */}
            <Card className="bg-white/90 backdrop-blur-xl border-2 border-[#DBE2DC] shadow-2xl">
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-2xl font-bold text-[#335765] mb-2">
                      {ticketData.subject}
                    </h3>
                    <p className="text-[#556b7a] text-sm">
                      Ticket ID: <span className="font-mono text-[#74A8A4] font-bold">{ticketData.ticket_id.slice(0, 8)}...</span>
                    </p>
                  </div>
                  <div className="flex gap-2">
                    <Badge className={`${getStatusColor(ticketData.status)} border px-3 py-1 rounded-full font-semibold`}>
                      {ticketData.status.replace("_", " ")}
                    </Badge>
                    <Badge className={`${getPriorityColor(ticketData.priority)} border px-3 py-1 rounded-full font-semibold`}>
                      {ticketData.priority}
                    </Badge>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 pt-4 border-t border-[#DBE2DC]">
                  <div className="flex items-center gap-2 text-[#556b7a]">
                    <User className="w-4 h-4 text-[#74A8A4]" />
                    <span className="text-sm">{ticketData.customer_name}</span>
                  </div>
                  <div className="flex items-center gap-2 text-[#556b7a]">
                    <Mail className="w-4 h-4 text-[#74A8A4]" />
                    <span className="text-sm">{ticketData.customer_email}</span>
                  </div>
                  <div className="flex items-center gap-2 text-[#556b7a]">
                    <Calendar className="w-4 h-4 text-[#74A8A4]" />
                    <span className="text-sm">Created: {formatDate(ticketData.created_at)}</span>
                  </div>
                  {ticketData.resolved_at && (
                    <div className="flex items-center gap-2 text-[#556b7a]">
                      <CheckCircle2 className="w-4 h-4 text-[#74A8A4]" />
                      <span className="text-sm">Resolved: {formatDate(ticketData.resolved_at)}</span>
                    </div>
                  )}
                </div>

                {/* View Conversation Button */}
                <div className="mt-6">
                  <Button
                    onClick={() => window.location.href = `/track/${ticketData.ticket_id}`}
                    className="w-full bg-gradient-to-r from-[#335765] via-[#74A8A4] to-[#7F543D] hover:from-[#2a4752] hover:via-[#5d8f8b] hover:to-[#6b4632] text-white font-bold shadow-lg hover:shadow-xl transition-all py-4 rounded-xl cursor-pointer"
                  >
                    <MessageSquare className="w-5 h-5 mr-2" />
                    View Full Conversation & Chat
                  </Button>
                </div>
              </div>
            </Card>

            {/* Messages Timeline */}
            <Card className="bg-white/90 backdrop-blur-xl border-2 border-[#DBE2DC] shadow-2xl">
              <div className="p-6">
                <h3 className="text-xl font-bold text-[#335765] mb-4 flex items-center gap-2">
                  <MessageSquare className="w-5 h-5 text-[#74A8A4]" />
                  Conversation ({ticketData.message_count})
                </h3>
                <div className="space-y-4">
                  {ticketData.messages.map((msg, idx) => (
                    <div
                      key={msg.id}
                      className={`p-4 rounded-xl border-2 transition-all duration-300 ${
                        msg.sender_type === "customer"
                          ? "bg-gradient-to-br from-[#B6D9E0]/20 to-[#74A8A4]/20 border-[#74A8A4]/30 ml-8"
                          : "bg-gradient-to-br from-[#74A8A4]/20 to-[#335765]/20 border-[#335765]/30 mr-8"
                      }`}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <div
                            className={`w-8 h-8 rounded-full flex items-center justify-center ${
                              msg.sender_type === "customer"
                                ? "bg-[#74A8A4]/30"
                                : "bg-[#335765]/30"
                            }`}
                          >
                            {msg.sender_type === "customer" ? (
                              <User className="w-4 h-4 text-[#335765]" />
                            ) : (
                              <Bot className="w-4 h-4 text-[#335765]" />
                            )}
                          </div>
                          <span className="text-sm font-bold text-[#335765]">
                            {msg.sender_type === "customer" ? "You" : "AI Assistant"}
                          </span>
                        </div>
                        <span className="text-xs text-[#556b7a]">
                          {formatDate(msg.created_at)}
                        </span>
                      </div>
                      <p className="text-[#335765] text-sm leading-relaxed">
                        {msg.content}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </Card>
          </div>
        )}

        {/* Features Section */}
        <div ref={featuresRef} className="mt-16 grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <Card className="p-6 bg-white/90 backdrop-blur-xl border-2 border-[#DBE2DC] shadow-xl hover:shadow-2xl transition-all hover:-translate-y-2">
            <div className="w-12 h-12 bg-gradient-to-br from-[#335765] to-[#74A8A4] rounded-xl flex items-center justify-center mb-4 shadow-lg">
              <Clock className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-lg font-bold text-[#335765] mb-2">Real-time Updates</h3>
            <p className="text-[#556b7a] text-sm">Get instant updates on your ticket status</p>
          </Card>

          <Card className="p-6 bg-white/90 backdrop-blur-xl border-2 border-[#DBE2DC] shadow-xl hover:shadow-2xl transition-all hover:-translate-y-2">
            <div className="w-12 h-12 bg-gradient-to-br from-[#74A8A4] to-[#B6D9E0] rounded-xl flex items-center justify-center mb-4 shadow-lg">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-lg font-bold text-[#335765] mb-2">Secure Access</h3>
            <p className="text-[#556b7a] text-sm">Only you can view your tickets via email</p>
          </Card>

          <Card className="p-6 bg-white/90 backdrop-blur-xl border-2 border-[#DBE2DC] shadow-xl hover:shadow-2xl transition-all hover:-translate-y-2">
            <div className="w-12 h-12 bg-gradient-to-br from-[#7F543D] to-[#335765] rounded-xl flex items-center justify-center mb-4 shadow-lg">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-lg font-bold text-[#335765] mb-2">AI-Powered</h3>
            <p className="text-[#556b7a] text-sm">Smart responses from our AI assistant</p>
          </Card>
        </div>
      </div>
    </div>
  );
}
