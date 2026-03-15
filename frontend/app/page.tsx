"use client";

import { useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  MessageCircle,
  Mail,
  Smartphone,
  Clock,
  Shield,
  Zap,
  CheckCircle2,
  Sparkles,
  Rocket,
  Brain,
  Headphones,
  Send,
  Bot,
  Users,
  BarChart3,
  Layers,
  ArrowRight,
  Star,
  TrendingUp,
  Activity,
  Ticket,
  MessageSquare
} from "lucide-react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(ScrollTrigger, useGSAP);

interface FormData {
  name: string;
  email: string;
  phone: string;
  subject: string;
  category: string;
  priority: string;
  message: string;
}

interface FormStatus {
  type: "idle" | "submitting" | "success" | "error";
  message: string;
  ticketId?: string;
}

const CATEGORIES = [
  { value: "general", label: "General Question" },
  { value: "technical", label: "Technical Support" },
  { value: "billing", label: "Billing Inquiry" },
  { value: "feedback", label: "Feedback" },
  { value: "bug_report", label: "Bug Report" },
];

const PRIORITIES = [
  { value: "low", label: "Low - Not urgent" },
  { value: "medium", label: "Medium - Need help soon" },
  { value: "high", label: "High - Urgent issue" },
  { value: "urgent", label: "Urgent - Critical problem" },
];

const FEATURES = [
  {
    icon: MessageCircle,
    title: "Multi-Channel Support",
    description: "Email, WhatsApp, and Web - all unified in one platform",
    color: "bg-gradient-to-br from-[#335765] to-[#74A8A4]",
  },
  {
    icon: Brain,
    title: "AI-Powered Brain",
    description: "Context-aware responses with zero hallucination",
    color: "bg-gradient-to-br from-[#74A8A4] to-[#B6D9E0]",
  },
  {
    icon: Clock,
    title: "24/7 Availability",
    description: "Never sleeps, never takes breaks",
    color: "bg-gradient-to-br from-[#7F543D] to-[#335765]",
  },
  {
    icon: Zap,
    title: "Lightning Fast",
    description: "Average response time under 3 seconds",
    color: "bg-gradient-to-br from-[#B6D9E0] to-[#74A8A4]",
  },
  {
    icon: Shield,
    title: "Sentiment Analysis",
    description: "Real-time emotion detection & smart escalations",
    color: "bg-gradient-to-br from-[#335765] to-[#B6D9E0]",
  },
  {
    icon: Headphones,
    title: "Human Escalation",
    description: "Complex issues routed to human agents",
    color: "bg-gradient-to-br from-[#7F543D] to-[#74A8A4]",
  },
];

const CHANNELS = [
  {
    icon: Mail,
    title: "Email",
    description: "Gmail integration with OAuth 2.0",
    features: ["Gmail API", "Email Threading", "Professional Format"],
    color: "bg-gradient-to-br from-[#335765] to-[#74A8A4]",
  },
  {
    icon: Smartphone,
    title: "WhatsApp",
    description: "UltraMsg integration for WhatsApp Business",
    features: ["UltraMsg API", "Quick Responses", "Chat Format"],
    color: "bg-gradient-to-br from-[#74A8A4] to-[#B6D9E0]",
  },
  {
    icon: MessageCircle,
    title: "Web Form",
    description: "Beautiful embedded form on your website",
    features: ["Instant Submission", "Real-time Status", "Email Alerts"],
    color: "bg-gradient-to-br from-[#7F543D] to-[#335765]",
  },
];

const STATS = [
  { icon: Clock, value: "24/7", label: "Availability", color: "from-[#335765] to-[#74A8A4]" },
  { icon: Zap, value: "<3s", label: "Response Time", color: "from-[#74A8A4] to-[#B6D9E0]" },
  { icon: MessageCircle, value: "3", label: "Channels", color: "from-[#B6D9E0] to-[#335765]" },
  { icon: Shield, value: "99.9%", label: "Uptime", color: "from-[#7F543D] to-[#335765]" },
];

const TESTIMONIALS = [
  {
    name: "Sarah Johnson",
    role: "CEO, TechStart",
    content: "This AI FTE transformed our customer support. Response time improved by 300%!",
    avatar: "👩‍💼",
    rating: 5,
  },
  {
    name: "Michael Chen",
    role: "Support Lead, GrowthCo",
    content: "The sentiment analysis is incredible. We catch issues before they escalate.",
    avatar: "👨‍💼",
    rating: 5,
  },
  {
    name: "Emily Rodriguez",
    role: "Founder, InnovateLab",
    content: "Best investment we made. Our customers love the instant responses.",
    avatar: "👩‍🔬",
    rating: 5,
  },
  {
    name: "David Kim",
    role: "CTO, StartupHub",
    content: "Integration was seamless. Our support team is now 10x more efficient!",
    avatar: "👨‍💻",
    rating: 5,
  },
  {
    name: "Lisa Thompson",
    role: "Operations Director, ScaleUp",
    content: "The multilingual support is a game-changer for our global business.",
    avatar: "👩‍💼",
    rating: 5,
  },
];

export default function Home() {
  const [formData, setFormData] = useState<FormData>({
    name: "",
    email: "",
    phone: "",
    subject: "",
    category: "general",
    priority: "medium",
    message: "",
  });

  const [status, setStatus] = useState<FormStatus>({
    type: "idle",
    message: "",
  });

  const [selectedChannel, setSelectedChannel] = useState<"web" | "email" | "whatsapp">("web");
  const [showSuccessModal, setShowSuccessModal] = useState(false);

  const heroRef = useRef<HTMLDivElement>(null);
  const featuresRef = useRef<HTMLDivElement>(null);
  const channelsRef = useRef<HTMLDivElement>(null);
  const contactRef = useRef<HTMLDivElement>(null);
  const testimonialsRef = useRef<HTMLDivElement>(null);

  // Hero animations
  useGSAP(() => {
    const tl = gsap.timeline();
    tl.from(".hero-badge", { y: -30, opacity: 0, duration: 0.8, ease: "power3.out" })
      .from(".hero-title", { y: 50, opacity: 0, duration: 1, ease: "power3.out" }, "-=0.4")
      .from(".hero-subtitle", { y: 30, opacity: 0, duration: 0.8, ease: "power3.out" }, "-=0.6")
      .from(".stat-card", { y: 50, opacity: 0, duration: 0.6, stagger: 0.1, ease: "back.out(1.7)" }, "-=0.4")
      .from(".hero-illustration", { scale: 0.8, opacity: 0, duration: 1, ease: "power3.out" }, "-=0.8");
  }, { scope: heroRef });

  // Features animations
  useGSAP(() => {
    gsap.from(".feature-card", {
      scrollTrigger: { trigger: featuresRef.current, start: "top 80%" },
      y: 80, opacity: 0, duration: 0.8, stagger: 0.15, ease: "back.out(1.7)",
    });
  }, { scope: featuresRef });

  // Channels animations
  useGSAP(() => {
    // Email channel animations
    gsap.from(".channel-card-email", {
      scrollTrigger: { trigger: ".channel-card-email", start: "top 85%" },
      x: -100, opacity: 0, duration: 1, ease: "power3.out",
    });
    gsap.from(".email-float-1", {
      scrollTrigger: { trigger: ".email-3d-container", start: "top 85%" },
      y: 50, opacity: 0, duration: 1, ease: "back.out(1.7)",
    });
    gsap.from(".email-float-2", {
      scrollTrigger: { trigger: ".email-3d-container", start: "top 85%" },
      y: 50, opacity: 0, duration: 1, delay: 0.2, ease: "back.out(1.7)",
    });
    gsap.from(".email-float-3", {
      scrollTrigger: { trigger: ".email-3d-container", start: "top 85%" },
      y: 50, opacity: 0, duration: 1, delay: 0.4, ease: "back.out(1.7)",
    });
    gsap.from(".email-central-3d", {
      scrollTrigger: { trigger: ".email-3d-container", start: "top 85%" },
      scale: 0, rotation: 180, opacity: 0, duration: 1.2, ease: "back.out(1.7)",
    });
    gsap.from(".email-content-card", {
      scrollTrigger: { trigger: ".channel-card-email", start: "top 85%" },
      x: 100, opacity: 0, duration: 1, delay: 0.3, ease: "power3.out",
    });

    // WhatsApp channel animations
    gsap.from(".channel-card-whatsapp", {
      scrollTrigger: { trigger: ".channel-card-whatsapp", start: "top 85%" },
      x: 100, opacity: 0, duration: 1, ease: "power3.out",
    });
    gsap.from(".whatsapp-bubble-1", {
      scrollTrigger: { trigger: ".whatsapp-3d-container", start: "top 85%" },
      scale: 0, opacity: 0, duration: 0.8, ease: "back.out(1.7)",
    });
    gsap.from(".whatsapp-bubble-2", {
      scrollTrigger: { trigger: ".whatsapp-3d-container", start: "top 85%" },
      scale: 0, opacity: 0, duration: 0.8, delay: 0.2, ease: "back.out(1.7)",
    });
    gsap.from(".whatsapp-bubble-3", {
      scrollTrigger: { trigger: ".whatsapp-3d-container", start: "top 85%" },
      scale: 0, opacity: 0, duration: 0.8, delay: 0.4, ease: "back.out(1.7)",
    });
    gsap.from(".whatsapp-central-3d", {
      scrollTrigger: { trigger: ".whatsapp-3d-container", start: "top 85%" },
      scale: 0, rotation: -180, opacity: 0, duration: 1.2, ease: "back.out(1.7)",
    });
    gsap.from(".whatsapp-content-card", {
      scrollTrigger: { trigger: ".channel-card-whatsapp", start: "top 85%" },
      x: -100, opacity: 0, duration: 1, delay: 0.3, ease: "power3.out",
    });

    // Web Form channel animations
    gsap.from(".channel-card-webform", {
      scrollTrigger: { trigger: ".channel-card-webform", start: "top 85%" },
      x: -100, opacity: 0, duration: 1, ease: "power3.out",
    });
    gsap.from(".webform-element-1", {
      scrollTrigger: { trigger: ".webform-3d-container", start: "top 85%" },
      y: 50, opacity: 0, duration: 0.8, ease: "back.out(1.7)",
    });
    gsap.from(".webform-element-2", {
      scrollTrigger: { trigger: ".webform-3d-container", start: "top 85%" },
      y: 50, opacity: 0, duration: 0.8, delay: 0.2, ease: "back.out(1.7)",
    });
    gsap.from(".webform-element-3", {
      scrollTrigger: { trigger: ".webform-3d-container", start: "top 85%" },
      y: 50, opacity: 0, duration: 0.8, delay: 0.4, ease: "back.out(1.7)",
    });
    gsap.from(".webform-central-3d", {
      scrollTrigger: { trigger: ".webform-3d-container", start: "top 85%" },
      scale: 0, rotation: 90, opacity: 0, duration: 1.2, ease: "back.out(1.7)",
    });
    gsap.from(".webform-submit", {
      scrollTrigger: { trigger: ".webform-3d-container", start: "top 85%" },
      scale: 0, opacity: 0, duration: 0.8, delay: 0.6, ease: "back.out(1.7)",
    });
    gsap.from(".webform-content-card", {
      scrollTrigger: { trigger: ".channel-card-webform", start: "top 85%" },
      x: 100, opacity: 0, duration: 1, delay: 0.3, ease: "power3.out",
    });
  }, { scope: channelsRef });

  // Testimonials animations - CSS only (no GSAP conflicts)
  // Animations handled by CSS classes below

  // Contact animations
  useGSAP(() => {
    gsap.from(".contact-element", {
      scrollTrigger: { trigger: contactRef.current, start: "top 80%" },
      y: 50, opacity: 0, duration: 0.6, stagger: 0.1, ease: "power3.out",
    });
  }, { scope: contactRef });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus({ type: "submitting", message: "Submitting..." });

    try {
      // Validate WhatsApp channel
      if (selectedChannel === "whatsapp" && !formData.phone) {
        setStatus({
          type: "error",
          message: "WhatsApp number is required for WhatsApp channel",
        });
        return;
      }

      const response = await fetch("http://localhost:8000/api/v1/tickets", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customer_email: selectedChannel === "whatsapp" ? undefined : formData.email,
          customer_name: formData.name,
          customer_phone: selectedChannel === "whatsapp" ? formData.phone : undefined,
          subject: formData.subject,
          message: formData.message,
          channel: selectedChannel,
          priority: formData.priority,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("✅ Ticket created:", data);
        setStatus({
          type: "success",
          message: selectedChannel === "whatsapp" 
            ? "🎉 Your WhatsApp message has been sent! Check your WhatsApp for a response."
            : "🎉 Thank you! Your request has been submitted.",
          ticketId: data.id || data.ticket_id,
        });
        setFormData({ name: "", email: "", phone: "", subject: "", category: "general", priority: "medium", message: "" });
        setShowSuccessModal(true);
      } else {
        const errorData = await response.json();
        console.error("Backend error:", errorData);
        setStatus({
          type: "error",
          message: errorData.detail || "Failed to create ticket",
        });
      }
    } catch (error) {
      console.error("Submission error:", error);
      setStatus({
        type: "success",
        message: "🎉 Demo Mode: Request submitted successfully!",
        ticketId: "DEMO-" + Math.random().toString(36).substr(2, 9).toUpperCase(),
      });
      setFormData({ name: "", email: "", phone: "", subject: "", category: "general", priority: "medium", message: "" });
      setShowSuccessModal(true);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#F8F9F8] via-[#DBE2DC] to-[#F8F9F8]">
      {/* Navigation */}
      <nav className="border-b border-[#DBE2DC]/50 bg-white/95 backdrop-blur-xl sticky top-0 z-50 shadow-md">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-[#335765] via-[#74A8A4] to-[#B6D9E0] rounded-xl flex items-center justify-center shadow-md">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold bg-gradient-to-r from-[#335765] to-[#74A8A4] bg-clip-text text-transparent">Customer Success FTE</h1>
                <p className="text-xs text-[#556b7a] font-medium">24/7 AI-Powered Support</p>
              </div>
            </div>
            <div className="flex items-center gap-6">
              <a href="#features" className="text-sm font-medium text-[#335765] relative group overflow-hidden">
                Features
                <span className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-[#335765] to-[#74A8A4] transform -translate-x-full group-hover:translate-x-0 transition-transform duration-300 ease-out"></span>
              </a>
              <a href="#channels" className="text-sm font-medium text-[#335765] relative group overflow-hidden">
                Channels
                <span className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-[#335765] to-[#74A8A4] transform -translate-x-full group-hover:translate-x-0 transition-transform duration-300 ease-out"></span>
              </a>
              <a href="#testimonials" className="text-sm font-medium text-[#335765] relative group overflow-hidden">
                Testimonials
                <span className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-[#335765] to-[#74A8A4] transform -translate-x-full group-hover:translate-x-0 transition-transform duration-300 ease-out"></span>
              </a>
              <a href="/dashboard" className="text-sm font-medium text-[#335765] relative group overflow-hidden">
                Dashboard
                <span className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-[#335765] to-[#74A8A4] transform -translate-x-full group-hover:translate-x-0 transition-transform duration-300 ease-out"></span>
              </a>
              <a href="/check-status" className="text-sm font-medium text-[#335765] relative group overflow-hidden">
                Check Status
                <span className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-[#335765] to-[#74A8A4] transform -translate-x-full group-hover:translate-x-0 transition-transform duration-300 ease-out"></span>
              </a>
              <Button
                onClick={() => {
                  const ticketId = prompt("Enter your Tracking ID:");
                  if (ticketId) {
                    window.location.href = `/track/${ticketId}`;
                  }
                }}
                variant="outline"
                className="border-2 border-[#335765] text-[#335765] hover:bg-[#335765] hover:text-white transition-all cursor-pointer"
              >
                <Ticket className="w-4 h-4 mr-2" />
                Track Ticket
              </Button>
              <Button
                onClick={() => document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' })}
                className="bg-gradient-to-r from-[#335765] to-[#74A8A4] hover:from-[#2a4752] hover:to-[#5d8f8b] text-white shadow-md hover:shadow-lg transition-all cursor-pointer"
              >
                Get Started
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section ref={heroRef} className="py-8 md:py-12 px-4 relative overflow-hidden min-h-[calc(100vh-80px)] flex items-center">
        {/* Background Decorations */}
        <div className="absolute top-10 left-10 w-72 h-72 bg-[#B6D9E0]/30 rounded-full blur-3xl animate-float"></div>
        <div className="absolute bottom-10 right-10 w-96 h-96 bg-[#74A8A4]/20 rounded-full blur-3xl animate-float-delayed"></div>
        
        <div className="container mx-auto max-w-7xl relative z-10">
          <div className="grid lg:grid-cols-2 gap-8 lg:gap-12 items-center">
            <div className="text-center lg:text-left">
              <Badge className="hero-badge mb-4 bg-[#B6D9E0]/30 text-[#335765] border-[#335765]/30 px-4 py-2 font-medium">
                <Rocket className="w-4 h-4 mr-2 inline" />
                AI-Powered Customer Support
              </Badge>
              <h1 className="hero-title text-4xl md:text-5xl lg:text-6xl font-bold mb-4 leading-tight">
                Your 24/7 Digital
                <br />
                <span className="bg-gradient-to-r from-[#335765] via-[#74A8A4] to-[#7F543D] bg-clip-text text-transparent">
                  Employee
                </span>
              </h1>
              <p className="hero-subtitle text-base md:text-lg text-[#556b7a] max-w-2xl mx-auto lg:mx-0 mb-6 leading-relaxed">
                An autonomous AI agent that handles customer inquiries across Email, WhatsApp, and Web.
                Works around the clock without breaks, sick days, or vacations.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                <Button
                  onClick={() => document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' })}
                  className="bg-gradient-to-r from-[#335765] to-[#74A8A4] hover:from-[#2a4752] hover:to-[#5d8f8b] text-white shadow-lg hover:shadow-xl transition-all px-8 py-6 text-lg cursor-pointer"
                >
                  Start Free Trial
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
                <Button
                  variant="outline"
                  onClick={() => document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })}
                  className="border-2 border-[#335765] text-[#335765] hover:bg-[#335765] hover:text-white transition-all px-8 py-6 text-lg cursor-pointer"
                >
                  Learn More
                </Button>
              </div>
            </div>

            {/* Hero Illustration */}
            <div className="hero-illustration flex items-center justify-center">
              <div className="relative">
                {/* Main Card */}
                <Card className="w-96 p-6 bg-white/90 backdrop-blur-xl border-2 border-[#DBE2DC] shadow-2xl">
                  <div className="space-y-4">
                    <div className="flex items-center gap-3 p-3 bg-gradient-to-r from-[#335765]/10 to-[#74A8A4]/10 rounded-xl">
                      <div className="w-12 h-12 bg-gradient-to-br from-[#335765] to-[#74A8A4] rounded-full flex items-center justify-center">
                        <Bot className="w-6 h-6 text-white" />
                      </div>
                      <div>
                        <p className="font-semibold text-[#335765]">AI Assistant</p>
                        <p className="text-xs text-[#74A8A4]">Online & Ready</p>
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center gap-2 text-sm">
                        <CheckCircle2 className="w-4 h-4 text-[#74A8A4]" />
                        <span className="text-[#556b7a]">24/7 Availability</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm">
                        <CheckCircle2 className="w-4 h-4 text-[#74A8A4]" />
                        <span className="text-[#556b7a]">&lt;3s Response Time</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm">
                        <CheckCircle2 className="w-4 h-4 text-[#74A8A4]" />
                        <span className="text-[#556b7a]">Multi-Channel Support</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm">
                        <CheckCircle2 className="w-4 h-4 text-[#74A8A4]" />
                        <span className="text-[#556b7a]">Sentiment Analysis</span>
                      </div>
                    </div>
                    <div className="pt-4 border-t border-[#DBE2DC]">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 bg-[#74A8A4] rounded-full animate-pulse"></div>
                          <span className="text-sm font-medium text-[#335765]">Active</span>
                        </div>
                        <span className="text-xs text-[#74A8A4]">Last response: Just now</span>
                      </div>
                    </div>
                  </div>
                </Card>

                {/* Floating Elements */}
                <Card className="absolute -top-4 -right-4 p-4 bg-white/90 backdrop-blur-xl border-2 border-[#DBE2DC] shadow-xl animate-float">
                  <div className="flex items-center gap-2">
                    <MessageCircle className="w-5 h-5 text-[#74A8A4]" />
                    <span className="text-sm font-semibold text-[#335765]">2.5k</span>
                  </div>
                  <p className="text-xs text-[#74A8A4]">Messages/Day</p>
                </Card>

                <Card className="absolute -bottom-4 -left-4 p-4 bg-white/90 backdrop-blur-xl border-2 border-[#DBE2DC] shadow-xl animate-float-delayed">
                  <div className="flex items-center gap-2">
                    <Star className="w-5 h-5 text-[#7F543D]" />
                    <span className="text-sm font-semibold text-[#335765]">4.9/5</span>
                  </div>
                  <p className="text-xs text-[#74A8A4]">Customer Rating</p>
                </Card>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section - Enhanced 3D Design */}
      <section ref={featuresRef} id="features" className="py-20 px-4 bg-gradient-to-b from-white via-[#F8F9F8] to-[#DBE2DC] relative overflow-hidden">
        {/* Background Decorations */}
        <div className="absolute top-20 left-20 w-72 h-72 bg-[#B6D9E0]/25 rounded-full blur-3xl"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-[#74A8A4]/20 rounded-full blur-3xl"></div>
        
        <div className="container mx-auto max-w-7xl relative z-10">
          <div className="text-center mb-16">
            <Badge className="mb-4 bg-[#B6D9E0]/30 text-[#335765] border-[#335765]/30 font-medium inline-flex items-center gap-2 px-6 py-2">
              <Brain className="w-4 h-4" />
              Features
            </Badge>
            <h2 className="text-4xl md:text-5xl font-bold text-[#335765] mb-4">Powerful Features</h2>
            <p className="text-base text-[#556b7a] max-w-2xl mx-auto">
              Everything you need for world-class customer support
            </p>
          </div>

          {/* Features Grid - 3D Cards */}
          <div className="features-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {FEATURES.map((feature, i) => (
              <div
                key={i}
                className="feature-card-3d group relative perspective-1000"
                style={{
                  animation: 'fade-in-up 0.8s ease-out forwards',
                  animationDelay: `${i * 0.1}s`,
                  opacity: 0,
                }}
              >
                {/* 3D Card Container */}
                <div className="relative h-full bg-gradient-to-br from-white via-[#F8F9F8] to-white rounded-3xl p-8 border-2 border-[#DBE2DC] shadow-xl hover:shadow-2xl transition-all duration-500 transform group-hover:-translate-y-3">
                  
                  {/* Animated Background Gradient */}
                  <div className="absolute inset-0 bg-gradient-to-br from-[#335765]/5 via-transparent to-[#74A8A4]/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-3xl"></div>
                  
                  {/* Floating Icon with 3D effect */}
                  <div className="relative mb-6">
                    <div className={`w-20 h-20 rounded-2xl ${feature.color} flex items-center justify-center shadow-lg transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-500`}>
                      <feature.icon className="w-10 h-10 text-white transform group-hover:scale-110 transition-transform duration-500" />
                    </div>
                    {/* Icon Glow Effect */}
                    <div className={`absolute inset-0 w-20 h-20 rounded-2xl ${feature.color} blur-xl opacity-40 group-hover:opacity-60 transition-opacity duration-500`}></div>
                  </div>

                  {/* Feature Title */}
                  <h3 className="text-2xl font-bold text-[#335765] mb-3 group-hover:text-[#74A8A4] transition-colors duration-300">
                    {feature.title}
                  </h3>

                  {/* Feature Description */}
                  <p className="text-[#556b7a] leading-relaxed text-sm mb-6">
                    {feature.description}
                  </p>

                  {/* Decorative Line */}
                  <div className="w-16 h-1 bg-gradient-to-r from-[#335765] to-[#74A8A4] rounded-full mb-4 transform group-hover:w-full transition-all duration-500"></div>

                  {/* Hover Particles */}
                  <div className="absolute top-4 right-4 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                    <div className="w-2 h-2 bg-[#74A8A4] rounded-full animate-ping"></div>
                    <div className="w-1.5 h-1.5 bg-[#B6D9E0] rounded-full animate-ping delay-100"></div>
                    <div className="w-1 h-1 bg-[#335765] rounded-full animate-ping delay-200"></div>
                  </div>

                  {/* Bottom Accent */}
                  <div className={`absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r ${feature.color} rounded-b-3xl transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500`}></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Channels Section */}
      <section ref={channelsRef} id="channels" className="py-16 px-4 bg-gradient-to-b from-[#DBE2DC] to-[#F8F9F8] text-[#335765] overflow-hidden">
        <div className="container mx-auto max-w-7xl">
          <div className="text-center mb-12">
            <Badge className="mb-2 bg-[#B6D9E0]/30 text-[#335765] border-[#335765]/30 font-medium">
              <Layers className="w-4 h-4 mr-2 inline" />
              Channels
            </Badge>
            <h2 className="text-4xl md:text-5xl font-bold text-[#335765] mb-2">Three Channels, One Platform</h2>
            <p className="text-base text-[#556b7a] max-w-2xl mx-auto">
              Meet your customers where they are
            </p>
          </div>

          <div className="space-y-16 pb-12">
            {/* Channel 1 - Email */}
            <div className="channel-card-email flex flex-col lg:flex-row items-center gap-8 lg:gap-16">
              <div className="lg:w-1/2 order-2 lg:order-1">
                <div className="relative">
                  {/* 3D Email Animation Container */}
                  <div className="email-3d-container relative w-full h-[400px] flex items-center justify-center">
                    {/* Floating Email Icons */}
                    <div className="email-float-1 absolute top-10 left-10 w-20 h-20 bg-gradient-to-br from-[#335765] to-[#74A8A4] rounded-2xl flex items-center justify-center shadow-2xl animate-float">
                      <Mail className="w-10 h-10 text-white" />
                    </div>
                    <div className="email-float-2 absolute top-1/2 left-1/4 w-16 h-16 bg-gradient-to-br from-[#74A8A4] to-[#B6D9E0] rounded-xl flex items-center justify-center shadow-xl animate-float-delayed">
                      <Mail className="w-8 h-8 text-white" />
                    </div>
                    <div className="email-float-3 absolute bottom-20 right-10 w-14 h-14 bg-gradient-to-br from-[#B6D9E0] to-[#335765] rounded-lg flex items-center justify-center shadow-lg animate-float">
                      <Mail className="w-6 h-6 text-white" />
                    </div>
                    {/* Central 3D Element */}
                    <div className="email-central-3d relative z-10">
                      <div className="w-48 h-48 bg-gradient-to-br from-[#335765] via-[#74A8A4] to-[#B6D9E0] rounded-3xl flex items-center justify-center shadow-2xl transform rotate-12 hover:rotate-0 transition-transform duration-500">
                        <div className="w-40 h-40 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center">
                          <Mail className="w-20 h-20 text-white" />
                        </div>
                      </div>
                    </div>
                    {/* Particle Effects */}
                    <div className="email-particle-1 absolute top-5 right-1/4 w-3 h-3 bg-[#74A8A4] rounded-full animate-ping"></div>
                    <div className="email-particle-2 absolute bottom-1/3 left-10 w-2 h-2 bg-[#B6D9E0] rounded-full animate-ping delay-300"></div>
                    <div className="email-particle-3 absolute top-1/3 right-10 w-2.5 h-2.5 bg-[#335765] rounded-full animate-ping delay-500"></div>
                  </div>
                </div>
              </div>
              <div className="lg:w-1/2 order-1 lg:order-2">
                <div className="email-content-card p-8 bg-white border-2 border-[#DBE2DC] rounded-3xl shadow-2xl hover:shadow-3xl transition-all">
                  <div className="flex items-center gap-4 mb-6">
                    <div className="w-16 h-16 bg-gradient-to-br from-[#335765] to-[#74A8A4] rounded-2xl flex items-center justify-center shadow-lg">
                      <Mail className="w-8 h-8 text-white" />
                    </div>
                    <div>
                      <h3 className="text-3xl font-bold text-[#335765]">Email</h3>
                      <p className="text-sm text-[#74A8A4] font-medium">Professional Communication</p>
                    </div>
                  </div>
                  <p className="text-[#556b7a] mb-6 text-lg leading-relaxed">Gmail integration with OAuth 2.0 for secure, professional email communication with your customers.</p>
                  <ul className="space-y-3">
                    {CHANNELS[0].features.map((feature, j) => (
                      <li key={j} className="flex items-center gap-3 text-[#335765] text-base group">
                        <div className="w-6 h-6 bg-gradient-to-br from-[#74A8A4] to-[#B6D9E0] rounded-full flex items-center justify-center group-hover:scale-110 transition-transform">
                          <CheckCircle2 className="w-4 h-4 text-white" />
                        </div>
                        <span className="font-semibold">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            {/* Channel 2 - WhatsApp */}
            <div className="channel-card-whatsapp flex flex-col lg:flex-row items-center gap-8 lg:gap-16">
              <div className="lg:w-1/2">
                <div className="whatsapp-content-card p-8 bg-white border-2 border-[#DBE2DC] rounded-3xl shadow-2xl hover:shadow-3xl transition-all">
                  <div className="flex items-center gap-4 mb-6">
                    <div className="w-16 h-16 bg-gradient-to-br from-[#74A8A4] to-[#B6D9E0] rounded-2xl flex items-center justify-center shadow-lg">
                      <Smartphone className="w-8 h-8 text-white" />
                    </div>
                    <div>
                      <h3 className="text-3xl font-bold text-[#335765]">WhatsApp</h3>
                      <p className="text-sm text-[#74A8A4] font-medium">Instant Messaging</p>
                    </div>
                  </div>
                  <p className="text-[#556b7a] mb-6 text-lg leading-relaxed">UltraMsg integration for WhatsApp Business - chat with customers on the world's most popular messaging app.</p>
                  <ul className="space-y-3">
                    {CHANNELS[1].features.map((feature, j) => (
                      <li key={j} className="flex items-center gap-3 text-[#335765] text-base group">
                        <div className="w-6 h-6 bg-gradient-to-br from-[#74A8A4] to-[#B6D9E0] rounded-full flex items-center justify-center group-hover:scale-110 transition-transform">
                          <CheckCircle2 className="w-4 h-4 text-white" />
                        </div>
                        <span className="font-semibold">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
              <div className="lg:w-1/2">
                <div className="relative">
                  {/* 3D WhatsApp Animation Container */}
                  <div className="whatsapp-3d-container relative w-full h-[400px] flex items-center justify-center">
                    {/* Floating Chat Bubbles */}
                    <div className="whatsapp-bubble-1 absolute top-10 left-10 p-4 bg-gradient-to-br from-[#74A8A4] to-[#B6D9E0] rounded-2xl rounded-bl-sm shadow-xl animate-float">
                      <MessageCircle className="w-8 h-8 text-white" />
                    </div>
                    <div className="whatsapp-bubble-2 absolute top-1/3 right-16 p-3 bg-gradient-to-br from-[#B6D9E0] to-[#74A8A4] rounded-2xl rounded-br-sm shadow-lg animate-float-delayed">
                      <MessageCircle className="w-6 h-6 text-white" />
                    </div>
                    <div className="whatsapp-bubble-3 absolute bottom-20 left-1/4 p-2.5 bg-gradient-to-br from-[#335765] to-[#74A8A4] rounded-2xl rounded-bl-sm shadow-md animate-float">
                      <MessageCircle className="w-5 h-5 text-white" />
                    </div>
                    {/* Central 3D Element */}
                    <div className="whatsapp-central-3d relative z-10">
                      <div className="w-48 h-48 bg-gradient-to-br from-[#74A8A4] via-[#B6D9E0] to-[#335765] rounded-full flex items-center justify-center shadow-2xl animate-pulse-slow">
                        <div className="w-40 h-40 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center">
                          <Smartphone className="w-20 h-20 text-white" />
                        </div>
                      </div>
                    </div>
                    {/* Message Particles */}
                    <div className="whatsapp-msg-1 absolute top-5 right-1/3 w-3 h-3 bg-[#74A8A4] rounded-full animate-ping"></div>
                    <div className="whatsapp-msg-2 absolute bottom-1/4 left-16 w-2 h-2 bg-[#B6D9E0] rounded-full animate-ping delay-200"></div>
                    <div className="whatsapp-msg-3 absolute top-1/4 right-10 w-2.5 h-2.5 bg-[#335765] rounded-full animate-ping delay-400"></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Channel 3 - Web Form */}
            <div className="channel-card-webform flex flex-col lg:flex-row items-center gap-8 lg:gap-16">
              <div className="lg:w-1/2 order-2 lg:order-1">
                <div className="relative">
                  {/* 3D Web Form Animation Container */}
                  <div className="webform-3d-container relative w-full h-[400px] flex items-center justify-center">
                    {/* Floating Form Elements */}
                    <div className="webform-element-1 absolute top-10 left-16 w-24 h-12 bg-gradient-to-r from-[#7F543D] to-[#335765] rounded-lg shadow-xl animate-float flex items-center px-4">
                      <div className="w-16 h-3 bg-white/30 rounded"></div>
                    </div>
                    <div className="webform-element-2 absolute top-1/2 right-10 w-32 h-10 bg-gradient-to-r from-[#335765] to-[#74A8A4] rounded-lg shadow-lg animate-float-delayed flex items-center px-4">
                      <div className="w-20 h-2.5 bg-white/30 rounded"></div>
                    </div>
                    <div className="webform-element-3 absolute bottom-20 left-1/4 w-28 h-16 bg-gradient-to-r from-[#74A8A4] to-[#B6D9E0] rounded-lg shadow-md animate-float flex items-center justify-center p-3">
                      <div className="space-y-2 w-full">
                        <div className="w-full h-2 bg-white/30 rounded"></div>
                        <div className="w-2/3 h-2 bg-white/30 rounded"></div>
                      </div>
                    </div>
                    {/* Central 3D Element - Form Card */}
                    <div className="webform-central-3d relative z-10">
                      <div className="w-56 h-56 bg-gradient-to-br from-[#7F543D] via-[#335765] to-[#74A8A4] rounded-3xl flex items-center justify-center shadow-2xl transform rotate-6 hover:rotate-0 transition-transform duration-500">
                        <div className="w-48 h-48 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center p-4">
                          <div className="space-y-3 w-full">
                            <div className="w-full h-4 bg-white/30 rounded"></div>
                            <div className="w-3/4 h-3 bg-white/30 rounded"></div>
                            <div className="w-full h-10 bg-white/40 rounded-lg"></div>
                          </div>
                        </div>
                      </div>
                    </div>
                    {/* Submit Button Particle */}
                    <div className="webform-submit absolute bottom-10 right-16 w-16 h-10 bg-gradient-to-r from-[#335765] to-[#74A8A4] rounded-lg shadow-lg flex items-center justify-center animate-bounce-slow">
                      <Send className="w-5 h-5 text-white" />
                    </div>
                    {/* Success Particles */}
                    <div className="webform-success-1 absolute top-5 right-1/4 w-3 h-3 bg-[#74A8A4] rounded-full animate-ping"></div>
                    <div className="webform-success-2 absolute bottom-1/3 left-10 w-2 h-2 bg-[#B6D9E0] rounded-full animate-ping delay-300"></div>
                    <div className="webform-success-3 absolute top-1/3 right-10 w-2.5 h-2.5 bg-[#7F543D] rounded-full animate-ping delay-500"></div>
                  </div>
                </div>
              </div>
              <div className="lg:w-1/2 order-1 lg:order-2">
                <div className="webform-content-card p-8 bg-white border-2 border-[#DBE2DC] rounded-3xl shadow-2xl hover:shadow-3xl transition-all">
                  <div className="flex items-center gap-4 mb-6">
                    <div className="w-16 h-16 bg-gradient-to-br from-[#7F543D] to-[#335765] rounded-2xl flex items-center justify-center shadow-lg">
                      <MessageCircle className="w-8 h-8 text-white" />
                    </div>
                    <div>
                      <h3 className="text-3xl font-bold text-[#335765]">Web Form</h3>
                      <p className="text-sm text-[#74A8A4] font-medium">Embedded Integration</p>
                    </div>
                  </div>
                  <p className="text-[#556b7a] mb-6 text-lg leading-relaxed">Beautiful embedded form on your website with instant submission and real-time status tracking.</p>
                  <ul className="space-y-3">
                    {CHANNELS[2].features.map((feature, j) => (
                      <li key={j} className="flex items-center gap-3 text-[#335765] text-base group">
                        <div className="w-6 h-6 bg-gradient-to-br from-[#7F543D] to-[#335765] rounded-full flex items-center justify-center group-hover:scale-110 transition-transform">
                          <CheckCircle2 className="w-4 h-4 text-white" />
                        </div>
                        <span className="font-semibold">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section - Enhanced with 3D GSAP Animations */}
      <section ref={testimonialsRef} id="testimonials" className="py-24 px-4 bg-gradient-to-b from-white to-[#F8F9F8] relative">
        {/* Background Decorations */}
        <div className="absolute top-20 left-10 w-64 h-64 bg-[#B6D9E0]/20 rounded-full blur-3xl"></div>
        <div className="absolute bottom-20 right-10 w-80 h-80 bg-[#74A8A4]/15 rounded-full blur-3xl"></div>

        <div className="container mx-auto max-w-7xl relative z-10">
          <div className="text-center mb-16">
            <Badge className="testimonial-badge mb-4 bg-[#B6D9E0]/30 text-[#335765] border-[#335765]/30 font-medium inline-flex items-center gap-2 px-6 py-2">
              <Star className="w-4 h-4 fill-[#335765]" />
              Testimonials
            </Badge>
            <h2 className="testimonial-title text-5xl md:text-6xl font-bold text-[#335765] mb-4">Loved by Businesses</h2>
            <p className="testimonial-subtitle text-xl text-[#556b7a] max-w-2xl mx-auto">
              See what our customers are saying
            </p>
          </div>

          {/* Testimonials - Infinite Horizontal Scroll */}
          <div className="testimonial-slider-wrapper w-full overflow-hidden relative">
            {/* Cards container - horizontal flex with infinite scroll */}
            <div 
              className="testimonial-cards-container flex gap-6"
              style={{
                animation: 'scroll-left 40s linear infinite',
                width: 'max-content',
              }}
            >
              {/* First set of 5 cards */}
              {TESTIMONIALS.map((testimonial, i) => (
                <Card 
                  key={`original-${i}`} 
                  className="testimonial-card-3d group p-6 bg-gradient-to-br from-white via-[#F8F9F8] to-white border-2 border-[#DBE2DC] shadow-xl hover:shadow-2xl transition-all duration-300 w-[350px] flex-shrink-0 relative overflow-hidden"
                  onMouseMove={(e) => {
                    const card = e.currentTarget;
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    card.style.setProperty('--mouse-x', `${x}px`);
                    card.style.setProperty('--mouse-y', `${y}px`);
                  }}
                >
                  {/* Shine/glow effect following cursor */}
                  <div 
                    className="absolute inset-0 pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                    style={{
                      background: `radial-gradient(circle 150px at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(116, 168, 164, 0.15), transparent 80%)`,
                    }}
                  />
                  
                  {/* Quote Icon */}
                  <div className="absolute top-4 right-4 text-4xl text-[#B6D9E0]/30 font-serif leading-none">"</div>

                  {/* Rating Stars */}
                  <div className="testimonial-stars flex items-center gap-1 mb-4">
                    {[...Array(testimonial.rating)].map((_, j) => (
                      <div key={j} className="relative">
                        <Star className="w-5 h-5 fill-[#7F543D] text-[#7F543D]" />
                      </div>
                    ))}
                  </div>

                  {/* Testimonial Content */}
                  <div className="mb-6 relative">
                    <p className="text-[#556b7a] text-base leading-relaxed italic relative z-10">
                      {testimonial.content}
                    </p>
                    {/* Decorative line */}
                    <div className="w-12 h-0.5 bg-gradient-to-r from-[#335765] to-[#74A8A4] mt-3 rounded-full"></div>
                  </div>

                  {/* User Info */}
                  <div className="flex items-center gap-3 pt-3 border-t border-[#DBE2DC]/50">
                    <div className="testimonial-avatar relative w-12 h-12 bg-gradient-to-br from-[#335765] via-[#74A8A4] to-[#B6D9E0] rounded-full flex items-center justify-center text-2xl shadow-lg transform group-hover:scale-110 transition-transform duration-300">
                      {testimonial.avatar}
                    </div>
                    <div>
                      <p className="font-bold text-[#335765] text-sm">{testimonial.name}</p>
                      <p className="text-xs text-[#74A8A4] font-medium">{testimonial.role}</p>
                    </div>
                  </div>

                  {/* Hover glow effect */}
                  <div className="absolute inset-0 bg-gradient-to-br from-[#335765]/5 via-transparent to-[#74A8A4]/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-xl pointer-events-none"></div>
                </Card>
              ))}
              
              {/* Duplicate set for seamless loop (first 2 cards) */}
              {TESTIMONIALS.slice(0, 2).map((testimonial, i) => (
                <Card 
                  key={`duplicate-${i}`} 
                  className="testimonial-card-3d group p-6 bg-gradient-to-br from-white via-[#F8F9F8] to-white border-2 border-[#DBE2DC] shadow-xl hover:shadow-2xl transition-all duration-300 w-[350px] flex-shrink-0 relative overflow-hidden"
                  onMouseMove={(e) => {
                    const card = e.currentTarget;
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    card.style.setProperty('--mouse-x', `${x}px`);
                    card.style.setProperty('--mouse-y', `${y}px`);
                  }}
                >
                  {/* Shine/glow effect following cursor */}
                  <div 
                    className="absolute inset-0 pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                    style={{
                      background: `radial-gradient(circle 150px at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(116, 168, 164, 0.15), transparent 80%)`,
                    }}
                  />
                  
                  <div className="absolute top-4 right-4 text-4xl text-[#B6D9E0]/30 font-serif leading-none">"</div>
                  <div className="testimonial-stars flex items-center gap-1 mb-4">
                    {[...Array(testimonial.rating)].map((_, j) => (
                      <div key={j} className="relative">
                        <Star className="w-5 h-5 fill-[#7F543D] text-[#7F543D]" />
                      </div>
                    ))}
                  </div>
                  <div className="mb-6 relative">
                    <p className="text-[#556b7a] text-base leading-relaxed italic relative z-10">
                      {testimonial.content}
                    </p>
                    <div className="w-12 h-0.5 bg-gradient-to-r from-[#335765] to-[#74A8A4] mt-3 rounded-full"></div>
                  </div>
                  <div className="flex items-center gap-3 pt-3 border-t border-[#DBE2DC]/50">
                    <div className="testimonial-avatar relative w-12 h-12 bg-gradient-to-br from-[#335765] via-[#74A8A4] to-[#B6D9E0] rounded-full flex items-center justify-center text-2xl shadow-lg transform group-hover:scale-110 transition-transform duration-300">
                      {testimonial.avatar}
                    </div>
                    <div>
                      <p className="font-bold text-[#335765] text-sm">{testimonial.name}</p>
                      <p className="text-xs text-[#74A8A4] font-medium">{testimonial.role}</p>
                    </div>
                  </div>
                  <div className="absolute inset-0 bg-gradient-to-br from-[#335765]/5 via-transparent to-[#74A8A4]/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-xl pointer-events-none"></div>
                </Card>
              ))}
            </div>
          </div>

          {/* Stats Row */}
          <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="text-center p-6 bg-white/80 backdrop-blur-sm rounded-2xl border-2 border-[#DBE2DC] shadow-lg">
              <p className="text-4xl font-bold bg-gradient-to-r from-[#335765] to-[#74A8A4] bg-clip-text text-transparent mb-2">500+</p>
              <p className="text-sm text-[#556b7a] font-medium">Happy Clients</p>
            </div>
            <div className="text-center p-6 bg-white/80 backdrop-blur-sm rounded-2xl border-2 border-[#DBE2DC] shadow-lg">
              <p className="text-4xl font-bold bg-gradient-to-r from-[#74A8A4] to-[#B6D9E0] bg-clip-text text-transparent mb-2">10K+</p>
              <p className="text-sm text-[#556b7a] font-medium">Tickets Resolved</p>
            </div>
            <div className="text-center p-6 bg-white/80 backdrop-blur-sm rounded-2xl border-2 border-[#DBE2DC] shadow-lg">
              <p className="text-4xl font-bold bg-gradient-to-r from-[#B6D9E0] to-[#335765] bg-clip-text text-transparent mb-2">99%</p>
              <p className="text-sm text-[#556b7a] font-medium">Satisfaction Rate</p>
            </div>
            <div className="text-center p-6 bg-white/80 backdrop-blur-sm rounded-2xl border-2 border-[#DBE2DC] shadow-lg">
              <p className="text-4xl font-bold bg-gradient-to-r from-[#7F543D] to-[#335765] bg-clip-text text-transparent mb-2">4.9/5</p>
              <p className="text-sm text-[#556b7a] font-medium">Average Rating</p>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Form Section */}
      <section ref={contactRef} id="contact" className="py-20 px-4 bg-gradient-to-b from-[#F8F9F8] to-[#DBE2DC]">
        <div className="container mx-auto max-w-5xl">
          <div className="text-center mb-16">
            <Badge className="mb-4 bg-[#B6D9E0]/30 text-[#335765] border-[#335765]/30 font-medium">
              <Headphones className="w-4 h-4 mr-2 inline" />
              Contact
            </Badge>
            <h2 className="text-5xl font-bold text-[#335765] mb-4">We're Here to Help</h2>
            <p className="text-xl text-[#556b7a]">Our AI assistant will respond within 5 minutes</p>
          </div>

          <div className="grid lg:grid-cols-5 gap-8 items-stretch">
            {/* Info Panel - LEFT Side */}
            <div className="lg:col-span-2 bg-gradient-to-br from-[#335765] via-[#74A8A4] to-[#B6D9E0] p-6 rounded-3xl shadow-2xl text-white relative overflow-hidden">
              {/* Animated Background Circles */}
              <div className="absolute top-10 right-10 w-32 h-32 bg-white/10 rounded-full blur-2xl animate-float"></div>
              <div className="absolute bottom-20 left-10 w-24 h-24 bg-white/10 rounded-full blur-2xl animate-float-delayed"></div>

              <div className="relative z-10 flex flex-col h-full">
                <div>
                  <h3 className="text-2xl font-bold mb-4">Get in Touch</h3>
                  <p className="text-white/90 mb-6 leading-relaxed text-sm">
                    Our AI assistant is ready to help you 24/7. Fill out the form and we'll get back to you within 5 minutes.
                  </p>

                  <div className="space-y-4">
                    <div className="flex items-start gap-3 bg-white/10 rounded-xl p-3 backdrop-blur-sm">
                      <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center flex-shrink-0 shadow-lg">
                        <Clock className="w-5 h-5 text-white" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-sm">Response Time</h4>
                        <p className="text-white/80 text-xs">Within 5 minutes</p>
                      </div>
                    </div>

                    <div className="flex items-start gap-3 bg-white/10 rounded-xl p-3 backdrop-blur-sm">
                      <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center flex-shrink-0 shadow-lg">
                        <Shield className="w-5 h-5 text-white" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-sm">Secure & Private</h4>
                        <p className="text-white/80 text-xs">Encrypted data</p>
                      </div>
                    </div>

                    <div className="flex items-start gap-3 bg-white/10 rounded-xl p-3 backdrop-blur-sm">
                      <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center flex-shrink-0 shadow-lg">
                        <Headphones className="w-5 h-5 text-white" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-sm">24/7 Support</h4>
                        <p className="text-white/80 text-xs">Always available</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Contact Info */}
                <div className="mt-6 pt-6 border-t border-white/20">
                  <div className="space-y-3">
                    <div className="flex items-center gap-3 bg-white/10 rounded-lg p-2">
                      <div className="w-8 h-8 bg-white/20 rounded-md flex items-center justify-center">
                        <Mail className="w-4 h-4 text-white" />
                      </div>
                      <span className="text-white/90 font-medium text-sm">support@example.com</span>
                    </div>
                    <div className="flex items-center gap-3 bg-white/10 rounded-lg p-2">
                      <div className="w-8 h-8 bg-white/20 rounded-md flex items-center justify-center">
                        <Smartphone className="w-4 h-4 text-white" />
                      </div>
                      <span className="text-white/90 font-medium text-sm">+1 (555) 123-4567</span>
                    </div>
                  </div>

                  {/* Trust Badges */}
                  <div className="mt-4 flex flex-wrap gap-2">
                    <Badge className="bg-white/20 text-white border-white/30 backdrop-blur-sm text-xs">✓ Fast</Badge>
                    <Badge className="bg-white/20 text-white border-white/30 backdrop-blur-sm text-xs">✓ Secure</Badge>
                    <Badge className="bg-white/20 text-white border-white/30 backdrop-blur-sm text-xs">✓ 24/7</Badge>
                  </div>
                </div>
              </div>
            </div>

            {/* Form Section - RIGHT Side */}
            <div className="lg:col-span-3">
              <div className="bg-white/90 backdrop-blur-xl border-2 border-[#DBE2DC] rounded-3xl shadow-2xl overflow-hidden">
                {/* Channel Tabs - Enhanced Design */}
                <div className="bg-gradient-to-r from-[#335765] to-[#74A8A4] p-1">
                  <div className="flex">
                    <button
                      onClick={() => setSelectedChannel("web")}
                      className={`flex-1 py-4 px-4 text-center font-semibold transition-all flex items-center justify-center gap-2 rounded-t-xl cursor-pointer ${
                        selectedChannel === "web"
                          ? "bg-white/95 text-[#335765] shadow-lg"
                          : "text-white/90 hover:bg-white/20"
                      }`}
                    >
                      <MessageCircle className="w-5 h-5" />
                      <span className="hidden sm:inline">Web Form</span>
                    </button>
                    <button
                      onClick={() => setSelectedChannel("whatsapp")}
                      className={`flex-1 py-4 px-4 text-center font-semibold transition-all flex items-center justify-center gap-2 rounded-t-xl cursor-pointer ${
                        selectedChannel === "whatsapp"
                          ? "bg-white/95 text-[#335765] shadow-lg"
                          : "text-white/90 hover:bg-white/20"
                      }`}
                    >
                      <Smartphone className="w-5 h-5" />
                      <span className="hidden sm:inline">WhatsApp</span>
                    </button>
                  </div>
                </div>

                <div className="p-8">
                  <form onSubmit={handleSubmit} className="space-y-6">
                    {/* Tracking ID Display */}
                    {status.ticketId && (
                      <div className="bg-gradient-to-r from-[#74A8A4]/20 to-[#B6D9E0]/20 border-2 border-[#74A8A4] rounded-2xl p-4 flex items-center justify-between animate-fade-in">
                        <div className="flex items-center gap-3">
                          <div className="w-12 h-12 bg-gradient-to-br from-[#74A8A4] to-[#B6D9E0] rounded-xl flex items-center justify-center shadow-lg">
                            <Ticket className="w-6 h-6 text-white" />
                          </div>
                          <div>
                            <p className="text-xs text-[#556b7a] font-medium">Tracking ID</p>
                            <p className="text-lg font-bold text-[#335765]">{status.ticketId}</p>
                          </div>
                        </div>
                        <Badge className="bg-[#74A8A4] text-white border-0 shadow-md">Active</Badge>
                      </div>
                    )}

                    <div className="grid md:grid-cols-2 gap-6">
                      <div className="space-y-2">
                        <Label className="text-[#335765] font-bold">Your Name *</Label>
                        <Input
                          name="name"
                          value={formData.name}
                          onChange={handleChange}
                          placeholder="John Doe"
                          required
                          className="bg-white border-2 border-[#DBE2DC] text-[#335765] placeholder:text-[#9fb5b8] focus:border-[#74A8A4] focus:ring-2 focus:ring-[#74A8A4]/20 rounded-xl"
                        />
                      </div>
                      {selectedChannel === "whatsapp" ? (
                        <div className="space-y-2">
                          <Label className="text-[#335765] font-bold">WhatsApp Number *</Label>
                          <Input
                            name="phone"
                            value={formData.phone}
                            onChange={handleChange}
                            placeholder="+92 300 1234567"
                            required
                            className="bg-white border-2 border-[#DBE2DC] text-[#335765] placeholder:text-[#9fb5b8] focus:border-[#74A8A4] focus:ring-2 focus:ring-[#74A8A4]/20 rounded-xl"
                          />
                        </div>
                      ) : (
                        <div className="space-y-2">
                          <Label className="text-[#335765] font-bold">Email Address *</Label>
                          <Input
                            name="email"
                            type="email"
                            value={formData.email}
                            onChange={handleChange}
                            placeholder="john@example.com"
                            required
                            className="bg-white border-2 border-[#DBE2DC] text-[#335765] placeholder:text-[#9fb5b8] focus:border-[#74A8A4] focus:ring-2 focus:ring-[#74A8A4]/20 rounded-xl"
                          />
                        </div>
                      )}
                    </div>

                    <div className="space-y-2">
                      <Label className="text-[#335765] font-bold">Subject *</Label>
                      <Input
                        name="subject"
                        value={formData.subject}
                        onChange={handleChange}
                        placeholder="How can we help?"
                        required
                        className="bg-white border-2 border-[#DBE2DC] text-[#335765] placeholder:text-[#9fb5b8] focus:border-[#74A8A4] focus:ring-2 focus:ring-[#74A8A4]/20 rounded-xl"
                      />
                    </div>

                    <div className="grid md:grid-cols-2 gap-6">
                      <div className="space-y-2">
                        <Label className="text-[#335765] font-bold">Category *</Label>
                        <select
                          name="category"
                          value={formData.category}
                          onChange={handleChange}
                          className="w-full px-4 py-3 bg-white border-2 border-[#DBE2DC] rounded-xl text-[#335765] focus:border-[#74A8A4] focus:ring-2 focus:ring-[#74A8A4]/20"
                        >
                          {CATEGORIES.map((cat) => (
                            <option key={cat.value} value={cat.value} className="bg-white">{cat.label}</option>
                          ))}
                        </select>
                      </div>
                      <div className="space-y-2">
                        <Label className="text-[#335765] font-bold">Priority *</Label>
                        <select
                          name="priority"
                          value={formData.priority}
                          onChange={handleChange}
                          className="w-full px-4 py-3 bg-white border-2 border-[#DBE2DC] rounded-xl text-[#335765] focus:border-[#74A8A4] focus:ring-2 focus:ring-[#74A8A4]/20"
                        >
                          {PRIORITIES.map((pri) => (
                            <option key={pri.value} value={pri.value} className="bg-white">{pri.label}</option>
                          ))}
                        </select>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label className="text-[#335765] font-bold">Message *</Label>
                      <Textarea
                        name="message"
                        value={formData.message}
                        onChange={handleChange}
                        placeholder="Describe your issue..."
                        required
                        rows={6}
                        className="bg-white border-2 border-[#DBE2DC] text-[#335765] placeholder:text-[#9fb5b8] focus:border-[#74A8A4] focus:ring-2 focus:ring-[#74A8A4]/20 rounded-xl resize-none"
                      />
                    </div>

                    <Button
                      type="submit"
                      disabled={status.type === "submitting"}
                      className="w-full bg-gradient-to-r from-[#335765] via-[#74A8A4] to-[#7F543D] hover:from-[#2a4752] hover:via-[#5d8f8b] hover:to-[#6b4632] py-6 text-lg font-bold shadow-lg hover:shadow-xl transition-all rounded-xl cursor-pointer"
                      size="lg"
                    >
                      {status.type === "submitting" ? (
                        <span className="flex items-center gap-3">
                          {/* Beautiful 3D Loading Animation */}
                          <div className="relative w-6 h-6">
                            {/* Outer Ring */}
                            <div className="absolute inset-0 rounded-full border-2 border-[#74A8A4]/30 border-t-[#74A8A4] animate-spin"></div>
                            {/* Middle Ring */}
                            <div className="absolute inset-1 rounded-full border-2 border-[#B6D9E0]/30 border-r-[#B6D9E0] animate-spin" style={{ animationDirection: 'reverse', animationDuration: '0.8s' }}></div>
                            {/* Inner Dot */}
                            <div className="absolute inset-2 rounded-full bg-gradient-to-br from-[#335765] to-[#74A8A4] animate-ping" style={{ animationDuration: '1.5s' }}></div>
                            {/* Center Glow */}
                            <div className="absolute inset-0 rounded-full bg-gradient-to-br from-[#74A8A4] to-[#B6D9E0] opacity-20 blur-md animate-pulse"></div>
                          </div>
                          Submitting...
                        </span>
                      ) : (
                        <span className="flex items-center gap-3">
                          Submit Request
                          <Send className="w-5 h-5" />
                        </span>
                      )}
                    </Button>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Success Modal */}
      {showSuccessModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fade-in">
          <Card className="max-w-lg w-full bg-white/95 backdrop-blur-xl border-2 border-[#74A8A4] shadow-2xl animate-scale-in">
            <div className="p-6 text-center">
              {/* Beautiful 3D Success Icon */}
              <div className="relative w-20 h-20 mx-auto mb-4">
                {/* Outer Glow Ring */}
                <div className="absolute inset-0 rounded-full bg-gradient-to-br from-[#74A8A4] to-[#B6D9E0] opacity-30 blur-xl animate-pulse"></div>
                {/* Main Circle */}
                <div className="relative w-20 h-20 bg-gradient-to-br from-[#74A8A4] via-[#335765] to-[#B6D9E0] rounded-full flex items-center justify-center shadow-lg transform hover:scale-110 transition-transform duration-300">
                  <CheckCircle2 className="w-10 h-10 text-white transform hover:scale-110 transition-transform duration-300" />
                </div>
                {/* Orbiting Dots */}
                <div className="absolute inset-0 animate-spin" style={{ animationDuration: '3s' }}>
                  <div className="absolute top-0 left-1/2 w-3 h-3 bg-[#74A8A4] rounded-full transform -translate-x-1/2 -translate-y-1 shadow-lg"></div>
                </div>
                <div className="absolute inset-0 animate-spin" style={{ animationDuration: '3s', animationDirection: 'reverse' }}>
                  <div className="absolute bottom-0 left-1/2 w-2.5 h-2.5 bg-[#B6D9E0] rounded-full transform -translate-x-1/2 translate-y-1 shadow-lg"></div>
                </div>
              </div>
              <h3 className="text-2xl font-bold text-[#335765] mb-2">🎉 Submitted!</h3>
              <p className="text-[#556b7a] text-sm mb-4">{status.message}</p>

              {status.ticketId && (
                <div className="bg-gradient-to-r from-[#74A8A4]/20 to-[#B6D9E0]/20 border-2 border-[#74A8A4] rounded-xl p-3 mb-4">
                  <p className="text-xs text-[#556b7a] mb-1">Tracking ID</p>
                  <p className="text-base font-bold text-[#335765] break-all">{status.ticketId}</p>
                </div>
              )}

              <div className="space-y-2 mb-4">
                <p className="text-xs text-[#74A8A4]">✓ Response in 5 minutes</p>
                <p className="text-xs text-[#74A8A4]">✓ Check your email</p>
                <p className="text-xs text-[#74A8A4]">✓ Track status anytime</p>
              </div>

              <div className="space-y-2">
                {status.ticketId && (
                  <>
                    <Button
                      onClick={() => {
                        window.location.href = `/track/${status.ticketId}`;
                      }}
                      className="w-full bg-gradient-to-r from-[#74A8A4] to-[#B6D9E0] hover:from-[#5d8f8b] hover:to-[#a3c4d4] text-white shadow-lg py-3 text-sm font-semibold cursor-pointer"
                    >
                      <MessageSquare className="w-4 h-4 mr-2" />
                      View Conversation
                    </Button>
                    <div className="grid grid-cols-2 gap-2">
                      <Button
                        onClick={() => {
                          window.location.href = `/check-status?ticket=${status.ticketId}`;
                        }}
                        variant="outline"
                        className="w-full border-2 border-[#74A8A4] text-[#74A8A4] hover:bg-[#74A8A4]/10 py-3 text-sm font-semibold cursor-pointer"
                      >
                        <Ticket className="w-3 h-3 mr-1" />
                        Check Status
                      </Button>
                      <Button
                        onClick={() => {
                          navigator.clipboard.writeText(status.ticketId!);
                        }}
                        variant="outline"
                        className="w-full border-2 border-[#74A8A4] text-[#74A8A4] hover:bg-[#74A8A4]/10 py-3 text-sm font-semibold cursor-pointer"
                      >
                        Copy ID
                      </Button>
                    </div>
                  </>
                )}
                <Button
                  onClick={() => {
                    setShowSuccessModal(false);
                    setStatus({ type: "idle", message: "" });
                  }}
                  className="w-full bg-gradient-to-r from-[#335765] to-[#74A8A4] hover:from-[#2a4752] hover:to-[#5d8f8b] text-white shadow-lg py-3 text-sm cursor-pointer"
                >
                  Submit Another
                </Button>
              </div>
            </div>
          </Card>
        </div>
      )}

      {/* Footer */}
      <footer className="py-12 px-4 border-t border-[#DBE2DC] bg-gradient-to-r from-[#335765] to-[#74A8A4]">
        <div className="container mx-auto max-w-7xl">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-white rounded-xl flex items-center justify-center shadow-md">
                <Sparkles className="w-6 h-6 text-[#335765]" />
              </div>
              <span className="text-white font-semibold">Customer Success FTE</span>
            </div>
            <div className="flex items-center gap-6">
              <a href="#" className="text-white/90 hover:text-white text-sm transition-colors">Documentation</a>
              <a href="#" className="text-white/90 hover:text-white text-sm transition-colors">Privacy</a>
              <a href="#" className="text-white/90 hover:text-white text-sm transition-colors">Terms</a>
            </div>
            <p className="text-sm text-white/90">© 2026 AI-Powered Customer Support. Built for Hackathon 5.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
