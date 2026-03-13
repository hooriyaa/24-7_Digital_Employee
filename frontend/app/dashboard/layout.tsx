import type { Metadata } from "next";
import "../globals.css";
import { Sidebar } from "@/components/sidebar";

export const metadata: Metadata = {
  title: "Dashboard - Customer Success FTE",
  description: "24/7 AI-powered customer support dashboard",
};

export default function DashboardLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 flex-shrink-0 shadow-2xl">
        <Sidebar />
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        {children}
      </main>
    </div>
  );
}
