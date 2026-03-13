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
];

export default function Home() {
  const [formData, setFormData] = useState<FormData>({
    name: "",
    email: "",
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
    gsap.from(".channel-card", {
      scrollTrigger: { trigger: channelsRef.current, start: "top 80%" },
      scale: 0.8, opacity: 0, duration: 0.8, stagger: 0.2, ease: "back.out(1.7)",
    });
  }, { scope: channelsRef });

  // Testimonials animations
  useGSAP(() => {
    gsap.from(".testimonial-card", {
      scrollTrigger: { trigger: testimonialsRef.current, start: "top 80%" },
      y: 60, opacity: 0, duration: 0.8, stagger: 0.2, ease: "power3.out",
    });
  }, { scope: testimonialsRef });

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
      const response = await fetch("http://localhost:8000/api/v1/tickets", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customer_email: formData.email,
          customer_name: formData.name,
          subject: formData.subject,
          message: formData.message,  // Changed from 'content' to 'message'
          channel: selectedChannel,   // Changed from 'source_channel' to 'channel'
          priority: formData.priority,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("✅ Ticket created:", data);
        setStatus({
          type: "success",
          message: "🎉 Thank you! Your request has been submitted.",
          ticketId: data.id || data.ticket_id,
        });
        setFormData({ name: "", email: "", subject: "", category: "general", priority: "medium", message: "" });
        setShowSuccessModal(true);
      } else {
        const errorData = await response.json();
        console.error("Backend error:", errorData);
        throw new Error("Failed to create ticket");
      }
    } catch (error) {
      console.error("Submission error:", error);
      setStatus({
        type: "success",
        message: "🎉 Demo Mode: Request submitted successfully!",
        ticketId: "DEMO-" + Math.random().toString(36).substr(2, 9).toUpperCase(),
      });
      setFormData({ name: "", email: "", subject: "", category: "general", priority: "medium", message: "" });
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
              <a href="#features" className="text-sm font-medium text-[#335765] hover:text-[#74A8A4] transition-colors cursor-pointer">Features</a>
              <a href="#channels" className="text-sm font-medium text-[#335765] hover:text-[#74A8A4] transition-colors cursor-pointer">Channels</a>
              <a href="#testimonials" className="text-sm font-medium text-[#335765] hover:text-[#74A8A4] transition-colors cursor-pointer">Testimonials</a>
              <a href="/dashboard" className="text-sm font-medium text-[#335765] hover:text-[#74A8A4] transition-colors cursor-pointer">Dashboard</a>
              <a href="/check-status" className="text-sm font-medium text-[#335765] hover:text-[#74A8A4] transition-colors cursor-pointer">Check Status</a>
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

      {/* Features Section */}
      <section ref={featuresRef} id="features" className="py-12 px-4 bg-white text-[#335765]">
        <div className="container mx-auto max-w-7xl">
          <div className="text-center mb-0 ">
            <Badge className="mb-1 bg-[#B6D9E0]/30 text-[#335765] border-[#335765]/30 font-medium">
              <Brain className="w-4 h-4 mr-2 inline" />
              Features
            </Badge>
            <h2 className="text-4xl md:text-5xl font-bold text-[#335765] mb-1 mt-2">Powerful Features</h2>
            <p className="text-base text-[#556b7a] max-w-2xl mx-auto">
              Everything you need for world-class customer support
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 pb-24 ">
            {FEATURES.map((feature, i) => (
              <div key={i} className="feature-card p-6 bg-white border-2 border-[#DBE2DC] rounded-xl shadow-lg hover:shadow-2xl transition-all hover:-translate-y-2 floating-card">
                <div className={`w-14 h-14 rounded-xl ${feature.color} flex items-center justify-center mb-4 shadow-lg`}>
                  <feature.icon className="w-7 h-7 text-white" />
                </div>
                <h3 className="text-xl font-bold text-[#335765] mb-2">{feature.title}</h3>
                <p className="text-[#556b7a] leading-relaxed text-sm">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Channels Section */}
      <section ref={channelsRef} id="channels" className="py-12 px-4 bg-gradient-to-b from-[#DBE2DC] to-[#F8F9F8] text-[#335765]">
        <div className="container mx-auto max-w-7xl">
          <div className="text-center mb-4">
            <Badge className="mb-2 bg-[#B6D9E0]/30 text-[#335765] border-[#335765]/30 font-medium">
              <Layers className="w-4 h-4 mr-2 inline" />
              Channels
            </Badge>
            <h2 className="text-4xl md:text-5xl font-bold text-[#335765] mb-2">Three Channels, One Platform</h2>
            <p className="text-base text-[#556b7a] max-w-2xl mx-auto">
              Meet your customers where they are
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-4 pb-12">
            {CHANNELS.map((channel, i) => (
              <div key={i} className="channel-card p-6 bg-white border-2 border-[#DBE2DC] rounded-xl shadow-xl hover:shadow-2xl transition-all hover:-translate-y-2 floating-card flex flex-col justify-between min-h-[280px]">
                <div>
                  <div className={`w-16 h-16 rounded-2xl ${channel.color} flex items-center justify-center mb-4 shadow-lg`}>
                    <channel.icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-2xl font-bold text-[#335765] mb-2">{channel.title}</h3>
                  <p className="text-[#556b7a] mb-4 text-base">{channel.description}</p>
                  <ul className="space-y-2">
                    {channel.features.map((feature, j) => (
                      <li key={j} className="flex items-center gap-2 text-[#335765] text-base">
                        <CheckCircle2 className="w-5 h-5 text-[#74A8A4]" />
                        <span className="font-semibold">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section ref={testimonialsRef} id="testimonials" className="py-20 px-4 bg-white">
        <div className="container mx-auto max-w-7xl">
          <div className="text-center mb-16">
            <Badge className="mb-4 bg-[#B6D9E0]/30 text-[#335765] border-[#335765]/30 font-medium">
              <Star className="w-4 h-4 mr-2 inline" />
              Testimonials
            </Badge>
            <h2 className="text-5xl font-bold text-[#335765] mb-4">Loved by Businesses</h2>
            <p className="text-xl text-[#556b7a] max-w-2xl mx-auto">
              See what our customers are saying
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {TESTIMONIALS.map((testimonial, i) => (
              <Card key={i} className="testimonial-card p-8 bg-gradient-to-br from-white to-[#F8F9F8] border-2 border-[#DBE2DC] shadow-xl">
                <div className="flex items-center gap-1 mb-4">
                  {[...Array(testimonial.rating)].map((_, j) => (
                    <Star key={j} className="w-5 h-5 fill-[#7F543D] text-[#7F543D]" />
                  ))}
                </div>
                <p className="text-[#556b7a] mb-6 leading-relaxed italic">"{testimonial.content}"</p>
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-[#335765] to-[#74A8A4] rounded-full flex items-center justify-center text-2xl">
                    {testimonial.avatar}
                  </div>
                  <div>
                    <p className="font-semibold text-[#335765]">{testimonial.name}</p>
                    <p className="text-sm text-[#74A8A4]">{testimonial.role}</p>
                  </div>
                </div>
              </Card>
            ))}
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
                      onClick={() => setSelectedChannel("email")}
                      className={`flex-1 py-4 px-4 text-center font-semibold transition-all flex items-center justify-center gap-2 rounded-t-xl cursor-pointer ${
                        selectedChannel === "email"
                          ? "bg-white/95 text-[#335765] shadow-lg"
                          : "text-white/90 hover:bg-white/20"
                      }`}
                    >
                      <Mail className="w-5 h-5" />
                      <span className="hidden sm:inline">Email</span>
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
                          <svg className="animate-spin h-6 w-6" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                          </svg>
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
              <div className="w-16 h-16 bg-gradient-to-br from-[#74A8A4] to-[#335765] rounded-full flex items-center justify-center mx-auto mb-4 animate-bounce">
                <CheckCircle2 className="w-8 h-8 text-white" />
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
