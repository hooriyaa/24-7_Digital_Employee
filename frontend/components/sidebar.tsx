"use client";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import {
  LayoutDashboard,
  Ticket,
  BookOpen,
  Users,
  Sparkles,
  ArrowLeft
} from "lucide-react";

interface NavItem {
  title: string;
  href: string;
  icon: React.ReactNode;
  badge?: string;
}

const navItems: NavItem[] = [
  {
    title: "Dashboard",
    href: "/dashboard",
    icon: <LayoutDashboard className="w-5 h-5" />,
  },
  {
    title: "Tickets",
    href: "/dashboard/tickets",
    icon: <Ticket className="w-5 h-5" />,
    badge: "Live",
  },
  {
    title: "Knowledge Base",
    href: "/dashboard/knowledge",
    icon: <BookOpen className="w-5 h-5" />,
  },
  {
    title: "Customers",
    href: "/dashboard/customers",
    icon: <Users className="w-5 h-5" />,
  },
];

interface SidebarProps {
  className?: string;
}

export function Sidebar({ className }: SidebarProps) {
  return (
    <div className={cn("flex h-full flex-col border-r border-[#DBE2DC] bg-gradient-to-b from-[#335765] to-[#2a4752]", className)}>
      {/* Back Button */}
      <div className="p-4 border-b border-[#74A8A4]/30">
        <Button
          onClick={() => window.location.href = '/'}
          variant="ghost"
          className="w-full justify-start gap-2 text-[#B6D9E0] hover:text-white hover:bg-[#74A8A4]/20 transition-all"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Home
        </Button>
      </div>

      {/* Logo */}
      <div className="flex h-16 items-center border-b border-[#74A8A4]/30 px-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-[#74A8A4] to-[#B6D9E0] rounded-xl flex items-center justify-center shadow-lg">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <p className="text-sm font-bold text-white">Customer Success</p>
            <p className="text-xs text-[#B6D9E0]/80">Digital FTE</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <ScrollArea className="flex-1 px-3 py-6">
        <div className="space-y-2">
          {navItems.map((item) => (
            <Button
              key={item.href}
              variant="ghost"
              className="w-full justify-start gap-3 text-[#B6D9E0]/90 hover:text-white hover:bg-[#74A8A4]/20 transition-all group"
              asChild
            >
              <a href={item.href}>
                <span className="group-hover:scale-110 transition-transform">{item.icon}</span>
                {item.title}
                {item.badge && (
                  <Badge variant="secondary" className="ml-auto text-xs bg-gradient-to-r from-[#74A8A4] to-[#B6D9E0] text-white font-semibold border-0">
                    {item.badge}
                  </Badge>
                )}
              </a>
            </Button>
          ))}
        </div>
      </ScrollArea>

      {/* Footer */}
      <div className="border-t border-[#74A8A4]/30 p-4">
        <Button variant="ghost" className="w-full justify-start text-xs text-[#B6D9E0]/80 hover:text-white hover:bg-[#74A8A4]/20 transition-all" asChild>
          <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer">
            <BookOpen className="w-4 h-4 mr-2" />
            API Documentation
          </a>
        </Button>
      </div>
    </div>
  );
}
