"use client";

import { TicketsTable } from "@/components/tickets-table";
import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Ticket, Sparkles } from "lucide-react";

export default function TicketsPage() {
  return (
    <div className="p-4 md:p-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6 md:mb-8">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 sm:w-12 sm:h-12 bg-gradient-to-br from-[#335765] to-[#74A8A4] rounded-xl flex items-center justify-center shadow-lg">
            <Ticket className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold bg-gradient-to-r from-[#335765] to-[#74A8A4] bg-clip-text text-transparent">
              Tickets
            </h1>
            <p className="text-xs sm:text-sm text-[#556b7a]">Manage and track customer support requests</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge className="bg-gradient-to-r from-[#74A8A4] to-[#B6D9E0] text-white border-0 px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm shadow-md">
            <Sparkles className="w-3 h-3 sm:w-4 sm:h-4 mr-1 sm:mr-2" />
            <span className="hidden xs:inline">AI Processing</span>
            <span className="xs:hidden">AI</span>
          </Badge>
        </div>
      </div>

      {/* Tickets Table */}
      <TicketsTable />
    </div>
  );
}
