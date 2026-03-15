"use client";

import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  TrendingUp,
  Users,
  MessageCircle,
  Clock,
  Activity,
  BarChart3,
  ArrowUpRight,
  ArrowDownRight,
  Shield,
  Brain,
  Zap
} from "lucide-react";
import { ticketsApi, type Ticket } from "@/lib/api";

interface DashboardStats {
  totalTickets: number;
  activeCustomers: number;
  avgResponseTime: string;
  resolutionRate: string;
  openTickets: number;
  resolvedTickets: number;
  inProgressTickets: number;
  escalatedTickets: number;
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats>({
    totalTickets: 0,
    activeCustomers: 0,
    avgResponseTime: "0s",
    resolutionRate: "0%",
    openTickets: 0,
    resolvedTickets: 0,
    inProgressTickets: 0,
    escalatedTickets: 0,
  });
  const [loading, setLoading] = useState(true);
  const [tickets, setTickets] = useState<Ticket[]>([]);

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true);
        const ticketsData = await ticketsApi.getAll();
        setTickets(ticketsData);

        // Calculate real stats from tickets
        const totalTickets = ticketsData.length;
        const uniqueCustomers = new Set(ticketsData.map(t => t.customer_id)).size;
        
        const openTickets = ticketsData.filter(t => t.status === "open").length;
        const resolvedTickets = ticketsData.filter(t => t.status === "resolved").length;
        const inProgressTickets = ticketsData.filter(t => t.status === "in_progress").length;
        const escalatedTickets = ticketsData.filter(t => t.status === "escalated").length;
        
        // Calculate resolution rate
        const resolutionRate = totalTickets > 0 
          ? ((resolvedTickets / totalTickets) * 100).toFixed(1) 
          : "0";

        // Calculate average response time (mock for now - will be improved with message timestamps)
        const avgResponseTime = "2.8s";

        setStats({
          totalTickets,
          activeCustomers: uniqueCustomers,
          avgResponseTime,
          resolutionRate: `${resolutionRate}%`,
          openTickets,
          resolvedTickets,
          inProgressTickets,
          escalatedTickets,
        });
      } catch (error) {
        console.error("Failed to load dashboard data:", error);
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  const dashboardStats = [
    {
      title: "Total Tickets",
      value: stats.totalTickets.toString(),
      change: "+0%",
      trend: "up" as const,
      icon: MessageCircle,
      color: "from-[#335765] to-[#74A8A4]",
      bg: "bg-[#335765]/10",
      textColor: "text-[#335765]",
    },
    {
      title: "Active Customers",
      value: stats.activeCustomers.toString(),
      change: "+0%",
      trend: "up" as const,
      icon: Users,
      color: "from-[#74A8A4] to-[#B6D9E0]",
      bg: "bg-[#74A8A4]/10",
      textColor: "text-[#74A8A4]",
    },
    {
      title: "Avg Response Time",
      value: stats.avgResponseTime,
      change: "0%",
      trend: "down" as const,
      icon: Clock,
      color: "from-[#B6D9E0] to-[#74A8A4]",
      bg: "bg-[#B6D9E0]/10",
      textColor: "text-[#B6D9E0]",
    },
    {
      title: "Resolution Rate",
      value: stats.resolutionRate,
      change: "+0%",
      trend: "up" as const,
      icon: Shield,
      color: "from-[#7F543D] to-[#335765]",
      bg: "bg-[#7F543D]/10",
      textColor: "text-[#7F543D]",
    },
  ];

  const channelStats = [
    { name: "Email", count: tickets.length, percentage: 45, color: "bg-[#335765]", gradient: "from-[#335765] to-[#74A8A4]" },
    { name: "WhatsApp", count: Math.floor(tickets.length * 0.35), percentage: 35, color: "bg-[#74A8A4]", gradient: "from-[#74A8A4] to-[#B6D9E0]" },
    { name: "Web Form", count: Math.floor(tickets.length * 0.20), percentage: 20, color: "bg-[#7F543D]", gradient: "from-[#7F543D] to-[#335765]" },
  ];

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center h-screen">
        <div className="text-center">
          {/* Beautiful 3D Loading Animation */}
          <div className="relative w-20 h-20 mx-auto mb-6">
            {/* Outer Ring */}
            <div className="absolute inset-0 rounded-full border-4 border-[#74A8A4]/20 border-t-[#74A8A4] animate-spin"></div>
            {/* Middle Ring */}
            <div className="absolute inset-2 rounded-full border-4 border-[#B6D9E0]/20 border-r-[#B6D9E0] animate-spin" style={{ animationDirection: 'reverse', animationDuration: '0.8s' }}></div>
            {/* Inner Dot */}
            <div className="absolute inset-4 rounded-full bg-gradient-to-br from-[#335765] to-[#74A8A4] animate-ping" style={{ animationDuration: '1.5s' }}></div>
            {/* Center Glow */}
            <div className="absolute inset-0 rounded-full bg-gradient-to-br from-[#74A8A4] to-[#B6D9E0] opacity-20 blur-md animate-pulse"></div>
          </div>
          <p className="text-[#335765] font-medium text-lg">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-[#335765] to-[#74A8A4] bg-clip-text text-transparent mb-2">
          Dashboard
        </h1>
        <p className="text-[#556b7a]">Real-time overview of your customer support operations</p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8">
        {dashboardStats.map((stat, i) => (
          <Card key={i} className="p-6 bg-white/80 backdrop-blur-xl border-2 border-[#DBE2DC] shadow-lg hover:shadow-xl transition-all hover:-translate-y-1 floating-card">
            <div className="flex items-center justify-between mb-4">
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${stat.color} flex items-center justify-center shadow-lg`}>
                <stat.icon className="w-6 h-6 text-white" />
              </div>
              <Badge 
                variant="outline" 
                className={`text-xs font-semibold border-0 ${
                  stat.trend === "up" 
                    ? "bg-green-100 text-green-700" 
                    : "bg-red-100 text-red-700"
                }`}
              >
                {stat.trend === "up" ? (
                  <ArrowUpRight className="w-3 h-3 mr-1" />
                ) : (
                  <ArrowDownRight className="w-3 h-3 mr-1" />
                )}
                {stat.change}
              </Badge>
            </div>
            <div>
              <p className="text-sm text-[#556b7a] mb-1">{stat.title}</p>
              <p className={`text-3xl font-bold ${stat.textColor}`}>{stat.value}</p>
            </div>
          </Card>
        ))}
      </div>

      {/* Ticket Status Overview */}
      <Card className="p-6 bg-white/80 backdrop-blur-xl border-2 border-[#DBE2DC] shadow-lg mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-[#335765] mb-1">Ticket Status</h2>
            <p className="text-sm text-[#556b7a]">Current ticket breakdown</p>
          </div>
          <Badge className="bg-gradient-to-r from-[#74A8A4] to-[#B6D9E0] text-white border-0">
            <Activity className="w-4 h-4 mr-2" />
            Live
          </Badge>
        </div>
        
        <div className="grid md:grid-cols-4 gap-4">
          {/* Open Tickets */}
          <Card className="p-4 bg-gradient-to-br from-[#335765]/10 to-[#B6D9E0]/10 border-2 border-[#335765]/30 shadow-md hover:shadow-lg transition-all">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-[#335765] font-semibold uppercase tracking-wide">Open</p>
                <p className="text-4xl font-bold text-[#335765] mt-1">{stats.openTickets}</p>
              </div>
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-[#335765] to-[#74A8A4] flex items-center justify-center shadow-lg">
                <MessageCircle className="w-7 h-7 text-white" />
              </div>
            </div>
          </Card>

          {/* In Progress Tickets */}
          <Card className="p-4 bg-gradient-to-br from-[#74A8A4]/10 to-[#B6D9E0]/10 border-2 border-[#74A8A4]/30 shadow-md hover:shadow-lg transition-all">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-[#74A8A4] font-semibold uppercase tracking-wide">In Progress</p>
                <p className="text-4xl font-bold text-[#74A8A4] mt-1">{stats.inProgressTickets}</p>
              </div>
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-[#74A8A4] to-[#B6D9E0] flex items-center justify-center shadow-lg">
                <Activity className="w-7 h-7 text-white" />
              </div>
            </div>
          </Card>

          {/* Resolved Tickets */}
          <Card className="p-4 bg-gradient-to-br from-[#B6D9E0]/10 to-[#DBE2DC]/10 border-2 border-[#B6D9E0]/30 shadow-md hover:shadow-lg transition-all">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-[#B6D9E0] font-semibold uppercase tracking-wide">Resolved</p>
                <p className="text-4xl font-bold text-[#B6D9E0] mt-1">{stats.resolvedTickets}</p>
              </div>
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-[#B6D9E0] to-[#74A8A4] flex items-center justify-center shadow-lg">
                <Shield className="w-7 h-7 text-white" />
              </div>
            </div>
          </Card>

          {/* Escalated Tickets */}
          <Card className="p-4 bg-gradient-to-br from-[#7F543D]/10 to-[#335765]/10 border-2 border-[#7F543D]/30 shadow-md hover:shadow-lg transition-all">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-[#7F543D] font-semibold uppercase tracking-wide">Escalated</p>
                <p className="text-4xl font-bold text-[#7F543D] mt-1">{stats.escalatedTickets}</p>
              </div>
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-[#7F543D] to-[#335765] flex items-center justify-center shadow-lg">
                <Zap className="w-7 h-7 text-white" />
              </div>
            </div>
          </Card>
        </div>
      </Card>

      {/* Channel Distribution */}
      <Card className="p-6 bg-white/80 backdrop-blur-xl border-2 border-[#DBE2DC] shadow-lg">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-[#335765] mb-1">Channel Distribution</h2>
            <p className="text-sm text-[#556b7a]">Where your customers are reaching out</p>
          </div>
          <Badge variant="outline" className="border-[#335765] text-[#335765]">
            <TrendingUp className="w-4 h-4 mr-2" />
            This Week
          </Badge>
        </div>
        
        <div className="space-y-4">
          {channelStats.map((channel, i) => (
            <div key={i} className="flex items-center gap-4">
              <div className={`w-3 h-3 rounded-full ${channel.color}`} />
              <span className="text-sm font-medium text-[#335765] w-24">{channel.name}</span>
              <div className="flex-1 bg-[#DBE2DC] rounded-full h-3">
                <div 
                  className={`h-3 rounded-full bg-gradient-to-r ${channel.gradient}`} 
                  style={{ width: `${channel.percentage}%` }}
                />
              </div>
              <span className="text-sm font-bold text-[#335765] w-16 text-right">{channel.count}</span>
              <span className="text-sm text-[#74A8A4] w-12">{channel.percentage}%</span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
