"use client";

import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ticketsApi } from "@/lib/api";
import type { Ticket } from "@/lib/api";
import { RefreshCw, Trash2, Ticket as TicketIcon } from "lucide-react";

const statusColors: Record<string, string> = {
  open: "bg-blue-50 text-blue-700 border-blue-200",
  in_progress: "bg-yellow-50 text-yellow-700 border-yellow-200",
  waiting_customer: "bg-orange-50 text-orange-700 border-orange-200",
  resolved: "bg-green-50 text-green-700 border-green-200",
  escalated: "bg-red-50 text-red-700 border-red-200",
  closed: "bg-gray-50 text-gray-700 border-gray-200",
};

const priorityColors: Record<string, string> = {
  low: "bg-brand-sand text-brand-deep",
  normal: "bg-brand-sky/30 text-brand-deep",
  high: "bg-orange-100 text-orange-600",
  urgent: "bg-red-100 text-red-600",
};

/**
 * Get sentiment emoji based on sentiment score.
 * @param score Sentiment score from -1.0 to 1.0
 * @returns Emoji representing the sentiment
 */
function getSentimentEmoji(score: number | null): string {
  if (score === null || score === undefined) return "😐";
  if (score >= 0.7) return "😊";      // Very positive
  if (score >= 0.3) return "🙂";      // Positive
  if (score >= -0.3) return "😐";     // Neutral
  if (score >= -0.7) return "😟";     // Negative
  return "😠";                         // Very negative/Angry
}

/**
 * Get sentiment label and color based on score.
 * @param score Sentiment score from -1.0 to 1.0
 * @returns Object with label and color class
 */
function getSentimentInfo(score: number | null): { label: string; color: string } {
  if (score === null || score === undefined) {
    return { label: "Neutral", color: "text-muted-foreground" };
  }
  if (score >= 0.7) {
    return { label: "Very Positive", color: "text-green-600" };
  }
  if (score >= 0.3) {
    return { label: "Positive", color: "text-green-600" };
  }
  if (score >= -0.3) {
    return { label: "Neutral", color: "text-muted-foreground" };
  }
  if (score >= -0.7) {
    return { label: "Negative", color: "text-orange-600" };
  }
  return { label: "Very Negative", color: "text-red-600" };
}

export function TicketsTable() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const fetchTickets = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await ticketsApi.getAll();
      setTickets(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch tickets");
      console.error("Error fetching tickets:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (e: React.MouseEvent, ticketId: string) => {
    e.stopPropagation(); // Prevent ticket selection
    
    if (!confirm("Are you sure you want to delete this ticket? This will also delete all messages.")) {
      return;
    }

    try {
      setDeletingId(ticketId);
      await ticketsApi.delete(ticketId);
      // Remove from local state
      setTickets(prev => prev.filter(t => t.id !== ticketId));
    } catch (err) {
      console.error("Error deleting ticket:", err);
      alert("Failed to delete ticket. Please try again.");
    } finally {
      setDeletingId(null);
    }
  };

  useEffect(() => {
    fetchTickets();
  }, []);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-[#335765]">All Tickets</h2>
          <p className="text-sm text-[#556b7a]">
            {tickets.length} tickets from database
          </p>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={fetchTickets}
          disabled={loading}
          className="gap-2 border-2 border-[#335765] text-[#335765] hover:bg-[#335765] hover:text-white transition-all"
        >
          <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} />
          Refresh Data
        </Button>
      </div>

      {/* Error State */}
      {error && (
        <Card className="p-4 bg-red-50 border-2 border-red-200 shadow-md">
          <p className="text-sm text-red-600 font-medium">{error}</p>
          <p className="text-xs text-red-500 mt-1">
            Make sure the backend is running on http://localhost:8000
          </p>
        </Card>
      )}

      {/* Loading State */}
      {loading && (
        <div className="space-y-3">
          {[...Array(5)].map((_, i) => (
            <Card key={i} className="h-16 animate-pulse bg-gradient-to-r from-[#DBE2DC] to-[#B6D9E0]/50 rounded-xl" />
          ))}
        </div>
      )}

      {/* Tickets List */}
      {!loading && !error && (
        <ScrollArea className="h-[600px]">
          <div className="space-y-2">
            {tickets.map((ticket) => {
              const sentimentEmoji = getSentimentEmoji(ticket.sentiment_score);
              const sentimentInfo = getSentimentInfo(ticket.sentiment_score);

              // Handle ticket selection - broadcast to chat via localStorage
              const handleTicketSelect = () => {
                localStorage.setItem("selectedTicket", JSON.stringify(ticket));
                // Dispatch storage event manually for same-tab communication
                window.dispatchEvent(new Event("storage"));
              };

              return (
                <Card
                  key={ticket.id}
                  onClick={handleTicketSelect}
                  className="p-5 hover:bg-gradient-to-r hover:from-[#F8F9F8] hover:to-[#DBE2DC]/50 transition-all cursor-pointer border-2 border-[#DBE2DC] bg-white/80 backdrop-blur-xl shadow-md hover:shadow-xl floating-card"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-2">
                        <Badge
                          variant="outline"
                          className={statusColors[ticket.status] || statusColors.open}
                        >
                          {ticket.status.replace("_", " ")}
                        </Badge>
                        <Badge
                          variant="secondary"
                          className={priorityColors[ticket.priority] || priorityColors.normal}
                        >
                          {ticket.priority}
                        </Badge>
                        {/* Sentiment Indicator Emoji */}
                        <span
                          className="text-lg"
                          title={`${sentimentInfo.label} (${ticket.sentiment_score?.toFixed(2) ?? 'N/A'})`}
                        >
                          {sentimentEmoji}
                        </span>
                      </div>
                      {/* Show subject or message preview */}
                      <h3 className="font-semibold text-[#335765] truncate">
                        {ticket.subject || ticket.latest_message || "No content"}
                      </h3>
                      <p className="text-sm text-[#74A8A4] mt-1">
                        Created: {formatDate(ticket.created_at)}
                      </p>
                    </div>
                    <div className="text-right flex flex-col items-end gap-2">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => handleDelete(e, ticket.id)}
                        disabled={deletingId === ticket.id}
                        className="text-red-600 hover:text-red-700 hover:bg-red-50 transition-all"
                      >
                        {deletingId === ticket.id ? (
                          <RefreshCw className="h-4 w-4 animate-spin" />
                        ) : (
                          <Trash2 className="h-4 w-4" />
                        )}
                      </Button>
                      <p className="text-xs text-[#74A8A4]">
                        ID: {ticket.id.slice(0, 8)}...
                      </p>
                      {ticket.sentiment_score !== null && (
                        <p className={`text-xs font-medium ${sentimentInfo.color}`}>
                          {sentimentInfo.label} ({ticket.sentiment_score.toFixed(2)})
                        </p>
                      )}
                    </div>
                  </div>
                </Card>
              );
            })}
            {tickets.length === 0 && (
              <Card className="p-12 text-center border-2 border-[#DBE2DC] bg-white/80 backdrop-blur-xl shadow-md">
                <div className="w-20 h-20 bg-gradient-to-br from-[#335765] to-[#74A8A4] rounded-full flex items-center justify-center mx-auto mb-4">
                  <TicketIcon className="w-10 h-10 text-white" />
                </div>
                <p className="text-lg font-semibold text-[#335765] mb-2">No tickets found</p>
                <p className="text-[#556b7a]">
                  Run the seed script to populate data.
                </p>
              </Card>
            )}
          </div>
        </ScrollArea>
      )}
    </div>
  );
}
