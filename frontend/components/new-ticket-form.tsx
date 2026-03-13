"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { ticketsApi } from "@/lib/api";
import { Loader2, Send, X, Users, Ticket } from "lucide-react";

interface NewTicketFormProps {
  onSuccess?: () => void;
  onCancel?: () => void;
}

interface FormData {
  customer_name: string;
  customer_email: string;
  customer_phone: string;
  subject: string;
  message: string;
  channel: string;
  priority: string;
}

const initialFormData: FormData = {
  customer_name: "",
  customer_email: "",
  customer_phone: "",
  subject: "",
  message: "",
  channel: "web",
  priority: "normal",
};

export function NewTicketForm({ onSuccess, onCancel }: NewTicketFormProps) {
  const router = useRouter();
  const [formData, setFormData] = useState<FormData>(initialFormData);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSelectChange = (name: string, value: string) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Validate required fields
      if (!formData.customer_name || !formData.customer_email || !formData.subject || !formData.message) {
        setError("Please fill in all required fields (name, email, subject, message)");
        setLoading(false);
        return;
      }

      // Submit ticket - subject and message are correctly mapped here
      console.log("🎫 [FORM] Creating ticket with payload:", {
        customer_name: formData.customer_name,
        customer_email: formData.customer_email,
        subject: formData.subject,
        message: formData.message,
        channel: formData.channel,
        priority: formData.priority,
      });

      const createdTicket = await ticketsApi.create({
        customer_name: formData.customer_name,
        customer_email: formData.customer_email,
        customer_phone: formData.customer_phone || undefined,
        subject: formData.subject,      // ✅ Subject mapped correctly
        message: formData.message,      // ✅ Message mapped correctly
        channel: formData.channel,
        priority: formData.priority,
      });

      console.log("✅ [FORM] Ticket created:", createdTicket);

      // Reset form
      setFormData(initialFormData);

      // Store selected ticket for chat interface
      localStorage.setItem("selectedTicket", JSON.stringify(createdTicket));
      console.log("💾 [FORM] Stored ticket in localStorage");
      console.log("💾 [FORM] Ticket ID:", createdTicket.id);
      console.log("💾 [FORM] Conversation ID:", createdTicket.conversation_id);

      // Wait for AI to start processing
      console.log("⏳ [FORM] Waiting 1.5 seconds for AI to start processing...");
      await new Promise(resolve => setTimeout(resolve, 1500));

      // Redirect to chat page to see AI response
      console.log("🔄 [FORM] Redirecting to chat page (/)");
      router.push("/");

      // Notify parent component (if still mounted)
      if (onSuccess) {
        onSuccess();
      }
    } catch (err) {
      console.error("Error creating ticket:", err);
      setError(
        err instanceof Error
          ? err.message
          : "Failed to create ticket. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="p-8 border-2 border-[#DBE2DC] bg-white/90 backdrop-blur-xl shadow-xl">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-2xl font-bold bg-gradient-to-r from-[#335765] to-[#74A8A4] bg-clip-text text-transparent">
            Create New Ticket
          </h2>
          <p className="text-sm text-[#556b7a] mt-1">
            Fill in the details below
          </p>
        </div>
        {onCancel && (
          <Button
            variant="ghost"
            size="sm"
            onClick={onCancel}
            className="text-[#74A8A4] hover:text-[#335765] transition-colors"
          >
            <X className="h-4 w-4" />
          </Button>
        )}
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Customer Information */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 pb-2 border-b-2 border-[#DBE2DC]">
            <Users className="w-5 h-5 text-[#74A8A4]" />
            <h3 className="text-lg font-bold text-[#335765]">
              Customer Information
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="customer_name" className="text-[#335765] font-semibold mb-2">
                Name <span className="text-red-500">*</span>
              </Label>
              <Input
                id="customer_name"
                name="customer_name"
                value={formData.customer_name}
                onChange={handleChange}
                placeholder="John Doe"
                required
                className="border-2 border-[#DBE2DC] focus:border-[#74A8A4] focus:ring-2 focus:ring-[#74A8A4]/20 transition-all"
              />
            </div>

            <div>
              <Label htmlFor="customer_email" className="text-[#335765] font-semibold mb-2">
                Email <span className="text-red-500">*</span>
              </Label>
              <Input
                id="customer_email"
                name="customer_email"
                type="email"
                value={formData.customer_email}
                onChange={handleChange}
                placeholder="john@example.com"
                required
                className="border-2 border-[#DBE2DC] focus:border-[#74A8A4] focus:ring-2 focus:ring-[#74A8A4]/20 transition-all"
              />
            </div>
          </div>

          <div>
            <Label htmlFor="customer_phone" className="text-[#335765] font-semibold mb-2">Phone</Label>
            <Input
              id="customer_phone"
              name="customer_phone"
              value={formData.customer_phone}
              onChange={handleChange}
              placeholder="+1-234-567-8900"
              className="border-2 border-[#DBE2DC] focus:border-[#74A8A4] focus:ring-2 focus:ring-[#74A8A4]/20 transition-all"
            />
          </div>
        </div>

        {/* Ticket Details */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 pb-2 border-b-2 border-[#DBE2DC]">
            <Ticket className="w-5 h-5 text-[#74A8A4]" />
            <h3 className="text-lg font-bold text-[#335765]">
              Ticket Details
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="priority" className="text-[#335765] font-semibold mb-2">Priority</Label>
              <Select
                value={formData.priority}
                onValueChange={(value) => handleSelectChange("priority", value)}
              >
                <SelectTrigger className="border-2 border-[#DBE2DC] focus:border-[#74A8A4] focus:ring-2 focus:ring-[#74A8A4]/20 transition-all">
                  <SelectValue placeholder="Select priority" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="low">Low</SelectItem>
                  <SelectItem value="normal">Normal</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                  <SelectItem value="urgent">Urgent</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="channel" className="text-[#335765] font-semibold mb-2">Channel</Label>
              <Select
                value={formData.channel}
                onValueChange={(value) => handleSelectChange("channel", value)}
              >
                <SelectTrigger className="border-2 border-[#DBE2DC] focus:border-[#74A8A4] focus:ring-2 focus:ring-[#74A8A4]/20 transition-all">
                  <SelectValue placeholder="Select channel" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="web">Web</SelectItem>
                  <SelectItem value="email">Email</SelectItem>
                  <SelectItem value="whatsapp">WhatsApp</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div>
            <Label htmlFor="subject" className="text-[#335765] font-semibold mb-2">
              Subject <span className="text-red-500">*</span>
            </Label>
            <Input
              id="subject"
              name="subject"
              value={formData.subject}
              onChange={handleChange}
              placeholder="Brief summary of the issue..."
              required
              className="border-2 border-[#DBE2DC] focus:border-[#74A8A4] focus:ring-2 focus:ring-[#74A8A4]/20 transition-all"
            />
          </div>

          <div>
            <Label htmlFor="message" className="text-[#335765] font-semibold mb-2">
              Message <span className="text-red-500">*</span>
            </Label>
            <Textarea
              id="message"
              name="message"
              value={formData.message}
              onChange={handleChange}
              placeholder="Describe the customer's issue or request..."
              rows={5}
              required
              className="border-2 border-[#DBE2DC] focus:border-[#74A8A4] focus:ring-2 focus:ring-[#74A8A4]/20 transition-all resize-none"
            />
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="p-4 bg-red-50 border-2 border-red-200 rounded-lg">
            <p className="text-sm text-red-600 font-medium">{error}</p>
          </div>
        )}

        {/* Submit Button */}
        <div className="flex gap-3 pt-4">
          <Button
            type="submit"
            disabled={loading}
            className="flex-1 gap-2 bg-gradient-to-r from-[#335765] to-[#74A8A4] hover:from-[#2a4752] hover:to-[#5d8f8b] text-white shadow-lg hover:shadow-xl transition-all py-6"
          >
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Creating Ticket...
              </>
            ) : (
              <>
                <Send className="h-4 w-4" />
                Create Ticket
              </>
            )}
          </Button>

          {onCancel && (
            <Button
              type="button"
              variant="outline"
              onClick={onCancel}
              disabled={loading}
              className="border-2 border-[#335765] text-[#335765] hover:bg-[#335765] hover:text-white transition-all px-8"
            >
              Cancel
            </Button>
          )}
        </div>
      </form>
    </Card>
  );
}
