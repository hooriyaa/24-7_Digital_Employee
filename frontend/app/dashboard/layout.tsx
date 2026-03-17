"use client";

import "../globals.css";
import { Sidebar } from "@/components/sidebar";
import { useState } from "react";
import { Menu, X } from "lucide-react";

export default function DashboardLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Mobile Overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar - Responsive */}
      <aside
        className={`
          fixed lg:static top-0 left-0 z-50 h-full w-64 
          transform transition-transform duration-300 ease-in-out
          ${sidebarOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}
        `}
      >
        <Sidebar onClose={() => setSidebarOpen(false)} />
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto flex flex-col">
        {/* Mobile Header */}
        <header className="lg:hidden bg-white border-b border-[#DBE2DC] p-4 flex items-center justify-between sticky top-0 z-30">
          <button
            onClick={() => setSidebarOpen(true)}
            className="p-2 rounded-lg hover:bg-[#DBE2DC]/50 transition-all"
            aria-label="Open menu"
          >
            <Menu className="w-6 h-6 text-[#335765]" />
          </button>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-[#335765] to-[#74A8A4] rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">FTE</span>
            </div>
            <span className="font-semibold text-[#335765]">Dashboard</span>
          </div>
          <div className="w-10" /> {/* Spacer for centering */}
        </header>

        {/* Page Content */}
        <div className="flex-1 overflow-auto">
          {children}
        </div>
      </main>
    </div>
  );
}
