"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";

interface FormData {
  name: string;
  email: string;
  subject: string;
  message: string;
}

interface FormStatus {
  type: "idle" | "submitting" | "success" | "error";
  message: string;
}

export default function ContactPage() {
  const [formData, setFormData] = useState<FormData>({
    name: "",
    email: "",
    subject: "",
    message: "",
  });

  const [status, setStatus] = useState<FormStatus>({
    type: "idle",
    message: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus({ type: "submitting", message: "Submitting your message..." });

    try {
      // Create a ticket from the web form submission
      const response = await fetch("http://localhost:8000/api/v1/tickets", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          customer_id: "00000000-0000-0000-0000-000000000000", // Will be created or linked
          subject: formData.subject || "Web Form Inquiry",
          status: "open",
          priority: "normal",
          category: "web_form",
        }),
      });

      if (response.ok) {
        setStatus({
          type: "success",
          message: "Thank you! Your message has been submitted successfully. We'll get back to you soon.",
        });
        setFormData({ name: "", email: "", subject: "", message: "" });
      } else {
        throw new Error("Failed to submit form");
      }
    } catch (error) {
      setStatus({
        type: "error",
        message: "Sorry, there was an error submitting your message. Please try again later.",
      });
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <div className="border-b bg-white dark:bg-slate-800">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100">
                Contact Us
              </h1>
              <p className="text-slate-500 dark:text-slate-400 mt-1">
                We're here to help. Send us a message and we'll respond as soon as possible.
              </p>
            </div>
            <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
              24/7 Support
            </Badge>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-2xl mx-auto">
          {/* Status Messages */}
          {status.type === "success" && (
            <Card className="p-6 mb-6 bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-800">
              <div className="flex items-start gap-3">
                <div className="text-2xl">✅</div>
                <div>
                  <h3 className="font-semibold text-green-800 dark:text-green-400">
                    Message Sent!
                  </h3>
                  <p className="text-green-700 dark:text-green-500 mt-1">
                    {status.message}
                  </p>
                </div>
              </div>
            </Card>
          )}

          {status.type === "error" && (
            <Card className="p-6 mb-6 bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-800">
              <div className="flex items-start gap-3">
                <div className="text-2xl">❌</div>
                <div>
                  <h3 className="font-semibold text-red-800 dark:text-red-400">
                    Submission Error
                  </h3>
                  <p className="text-red-700 dark:text-red-500 mt-1">
                    {status.message}
                  </p>
                </div>
              </div>
            </Card>
          )}

          {/* Contact Form */}
          <Card className="p-8 shadow-lg">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Name */}
              <div className="space-y-2">
                <Label htmlFor="name" className="text-slate-700 dark:text-slate-300">
                  Your Name
                </Label>
                <Input
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="John Doe"
                  required
                  className="bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700"
                />
              </div>

              {/* Email */}
              <div className="space-y-2">
                <Label htmlFor="email" className="text-slate-700 dark:text-slate-300">
                  Email Address
                </Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="john@example.com"
                  required
                  className="bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700"
                />
              </div>

              {/* Subject */}
              <div className="space-y-2">
                <Label htmlFor="subject" className="text-slate-700 dark:text-slate-300">
                  Subject
                </Label>
                <Input
                  id="subject"
                  name="subject"
                  value={formData.subject}
                  onChange={handleChange}
                  placeholder="How can we help?"
                  className="bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700"
                />
              </div>

              {/* Message */}
              <div className="space-y-2">
                <Label htmlFor="message" className="text-slate-700 dark:text-slate-300">
                  Message
                </Label>
                <Textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  placeholder="Tell us more about your inquiry..."
                  required
                  rows={6}
                  className="bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 resize-none"
                />
              </div>

              {/* Submit Button */}
              <Button
                type="submit"
                disabled={status.type === "submitting"}
                className="w-full bg-slate-900 hover:bg-slate-800 text-white dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-slate-200"
              >
                {status.type === "submitting" ? (
                  <span className="flex items-center gap-2">
                    <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    Submitting...
                  </span>
                ) : (
                  "Send Message"
                )}
              </Button>
            </form>
          </Card>

          {/* Additional Info */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card className="p-4 text-center">
              <div className="text-2xl mb-2">🚀</div>
              <h3 className="font-semibold text-slate-900 dark:text-slate-100">
                Fast Response
              </h3>
              <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                Average response time: 5 minutes
              </p>
            </Card>
            <Card className="p-4 text-center">
              <div className="text-2xl mb-2">🔒</div>
              <h3 className="font-semibold text-slate-900 dark:text-slate-100">
                Secure
              </h3>
              <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                Your data is protected
              </p>
            </Card>
            <Card className="p-4 text-center">
              <div className="text-2xl mb-2">💬</div>
              <h3 className="font-semibold text-slate-900 dark:text-slate-100">
                24/7 Support
              </h3>
              <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                Always here to help
              </p>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
