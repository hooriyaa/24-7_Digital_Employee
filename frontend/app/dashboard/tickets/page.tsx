"use client";

import { TicketsTable } from "@/components/tickets-table";
import { NewTicketForm } from "@/components/new-ticket-form";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Plus, Ticket, Sparkles } from "lucide-react";

export default function TicketsPage() {
  const [showForm, setShowForm] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleSuccess = () => {
    setShowForm(false);
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="p-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <div className="w-12 h-12 bg-gradient-to-br from-[#335765] to-[#74A8A4] rounded-xl flex items-center justify-center shadow-lg">
              <Ticket className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-[#335765] to-[#74A8A4] bg-clip-text text-transparent">
                Tickets
              </h1>
              <p className="text-sm text-[#556b7a]">Manage and track customer support requests</p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge className="bg-gradient-to-r from-[#74A8A4] to-[#B6D9E0] text-white border-0 px-4 py-2 shadow-md">
            <Sparkles className="w-4 h-4 mr-2" />
            AI Processing
          </Badge>
          {!showForm && (
            <Button
              onClick={() => setShowForm(true)}
              className="gap-2 bg-gradient-to-r from-[#335765] to-[#74A8A4] hover:from-[#2a4752] hover:to-[#5d8f8b] text-white shadow-lg hover:shadow-xl transition-all"
            >
              <Plus className="h-4 w-4" />
              New Ticket
            </Button>
          )}
        </div>
      </div>

      {/* Form */}
      {showForm && (
        <div className="mb-8">
          <NewTicketForm
            onSuccess={handleSuccess}
            onCancel={() => setShowForm(false)}
          />
        </div>
      )}

      {/* Tickets Table */}
      <TicketsTable key={refreshKey} />
    </div>
  );
}
