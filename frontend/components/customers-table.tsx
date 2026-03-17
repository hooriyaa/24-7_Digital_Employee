"use client";

import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { customersApi, Customer } from "@/lib/api";
import { RefreshCw, Mail, Phone, Search, X, User, Calendar } from "lucide-react";

export function CustomersTable() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null);

  const fetchCustomers = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await customersApi.getAll();
      setCustomers(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch customers");
      console.error("Error fetching customers:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  const getInitials = (name: string) => {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);
  };

  // Filter customers based on search query
  const filteredCustomers = customers.filter((customer) => {
    const query = searchQuery.toLowerCase();
    return (
      customer.name.toLowerCase().includes(query) ||
      customer.email.toLowerCase().includes(query) ||
      customer.phone?.toLowerCase().includes(query) ||
      customer.custom_metadata?.plan?.toLowerCase().includes(query)
    );
  });

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="space-y-3">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-xl sm:text-2xl font-semibold text-slate-900 dark:text-slate-100">Customers</h2>
            <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400">
              {filteredCustomers.length} of {customers.length} customers
            </p>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={fetchCustomers}
            disabled={loading}
            className="gap-2 w-full sm:w-auto"
          >
            <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} />
            <span className="hidden sm:inline">Refresh Data</span>
            <span className="sm:hidden">Refresh</span>
          </Button>
        </div>

        {/* Search Bar */}
        <div className="relative">
          <div className="absolute left-3 top-1/2 -translate-y-1/2 z-10">
            <Search className="h-4 w-4 text-slate-500" strokeWidth={2.5} />
          </div>
          <Input
            type="text"
            placeholder="Search customers by name, email, phone, or plan..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 pr-10 border-2 border-slate-200 focus:border-slate-400 bg-white/80 backdrop-blur-xl"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery("")}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-700 text-2xl font-bold leading-none cursor-pointer z-10"
              type="button"
            >
              ×
            </button>
          )}
        </div>
      </div>

      {/* Error State */}
      {error && (
        <Card className="p-4 bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-800">
          <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
          <p className="text-xs text-red-500 dark:text-red-500 mt-1">
            Make sure the backend is running on http://localhost:8000
          </p>
        </Card>
      )}

      {/* Loading State */}
      {loading && (
        <div className="space-y-3">
          {[...Array(5)].map((_, i) => (
            <Card key={i} className="h-20 animate-pulse bg-slate-100 dark:bg-slate-800" />
          ))}
        </div>
      )}

      {/* Customers List */}
      {!loading && !error && (
        <ScrollArea className="h-[500px] sm:h-[600px] cursor-default">
          <div className="space-y-2">
            {filteredCustomers.map((customer) => (
              <Card
                key={customer.id}
                onClick={() => setSelectedCustomer(customer)}
                className="p-3 sm:p-4 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-all cursor-pointer hover:shadow-lg"
              >
                <div className="flex flex-col sm:flex-row items-start gap-3 sm:gap-4">
                  <Avatar className="h-10 w-10 sm:h-12 sm:w-12 bg-slate-200 dark:bg-slate-700 flex-shrink-0 cursor-pointer">
                    <div className="flex h-full w-full items-center justify-center text-sm font-semibold text-slate-600 dark:text-slate-300">
                      {getInitials(customer.name)}
                    </div>
                  </Avatar>
                  <div className="flex-1 min-w-0 w-full cursor-pointer">
                    <h3 className="font-medium text-slate-900 dark:text-slate-100 text-sm sm:text-base truncate">
                      {customer.name}
                    </h3>
                    <div className="flex flex-col sm:flex-row items-start gap-2 sm:gap-4 mt-1">
                      <div className="flex items-center gap-1 text-xs sm:text-sm text-slate-500 dark:text-slate-400 w-full cursor-pointer">
                        <Mail className="h-3 w-3 flex-shrink-0" />
                        <span className="truncate">{customer.email}</span>
                      </div>
                      {customer.phone && (
                        <div className="flex items-center gap-1 text-xs sm:text-sm text-slate-500 dark:text-slate-400 cursor-pointer">
                          <Phone className="h-3 w-3 flex-shrink-0" />
                          <span className="truncate">{customer.phone}</span>
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-2 w-full sm:w-auto justify-between sm:justify-end cursor-pointer">
                    <Badge variant="secondary" className="text-xs flex-shrink-0 cursor-pointer">
                      {customer.custom_metadata?.plan || "Basic"}
                    </Badge>
                    <p className="text-xs text-slate-500 dark:text-slate-400 whitespace-nowrap cursor-pointer">
                      {formatDate(customer.created_at)}
                    </p>
                  </div>
                </div>
              </Card>
            ))}
            {filteredCustomers.length === 0 && customers.length > 0 ? (
              <Card className="p-6 sm:p-8 text-center">
                <div className="w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-slate-400 to-slate-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Search className="w-8 h-8 sm:w-10 sm:h-10 text-white" />
                </div>
                <p className="text-base sm:text-lg font-semibold text-slate-700 mb-2">No customers found</p>
                <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400">
                  Try a different search term or clear the search box.
                </p>
              </Card>
            ) : filteredCustomers.length === 0 ? (
              <Card className="p-6 sm:p-8 text-center">
                <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400">
                  No customers found. Run the seed script to populate data.
                </p>
              </Card>
            ) : null}
          </div>
        </ScrollArea>
      )}

      {/* Customer Details Modal */}
      {selectedCustomer && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fade-in">
          <Card className="max-w-md w-full bg-white/95 backdrop-blur-xl border-2 border-slate-200 shadow-2xl animate-scale-in max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              {/* Header */}
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-slate-900">Customer Details</h2>
                <button
                  onClick={() => setSelectedCustomer(null)}
                  className="p-2 hover:bg-slate-100 rounded-lg transition-all"
                  aria-label="Close"
                >
                  <X className="w-5 h-5 text-slate-500" />
                </button>
              </div>

              {/* Avatar and Name */}
              <div className="flex flex-col items-center mb-6">
                <Avatar className="w-20 h-20 bg-gradient-to-br from-slate-400 to-slate-600 mb-3">
                  <div className="flex h-full w-full items-center justify-center text-2xl font-bold text-white">
                    {getInitials(selectedCustomer.name)}
                  </div>
                </Avatar>
                <h3 className="text-xl font-bold text-slate-900">{selectedCustomer.name}</h3>
                <Badge variant="secondary" className="mt-2">
                  {selectedCustomer.custom_metadata?.plan || "Basic"}
                </Badge>
              </div>

              {/* Details */}
              <div className="space-y-4">
                {/* Email */}
                <div className="flex items-start gap-3 p-3 bg-slate-50 rounded-lg">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-blue-600 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Mail className="w-5 h-5 text-white" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs text-slate-500 font-medium">Email Address</p>
                    <p className="text-sm font-semibold text-slate-900 truncate">{selectedCustomer.email}</p>
                  </div>
                </div>

                {/* Phone */}
                {selectedCustomer.phone && (
                  <div className="flex items-start gap-3 p-3 bg-slate-50 rounded-lg">
                    <div className="w-10 h-10 bg-gradient-to-br from-green-400 to-green-600 rounded-lg flex items-center justify-center flex-shrink-0">
                      <Phone className="w-5 h-5 text-white" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs text-slate-500 font-medium">Phone Number</p>
                      <p className="text-sm font-semibold text-slate-900">{selectedCustomer.phone}</p>
                    </div>
                  </div>
                )}

                {/* Customer Since */}
                <div className="flex items-start gap-3 p-3 bg-slate-50 rounded-lg">
                  <div className="w-10 h-10 bg-gradient-to-br from-purple-400 to-purple-600 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Calendar className="w-5 h-5 text-white" />
                  </div>
                  <div className="flex-1">
                    <p className="text-xs text-slate-500 font-medium">Customer Since</p>
                    <p className="text-sm font-semibold text-slate-900">{formatDate(selectedCustomer.created_at)}</p>
                  </div>
                </div>

                {/* Customer ID */}
                <div className="flex items-start gap-3 p-3 bg-slate-50 rounded-lg">
                  <div className="w-10 h-10 bg-gradient-to-br from-slate-400 to-slate-600 rounded-lg flex items-center justify-center flex-shrink-0">
                    <User className="w-5 h-5 text-white" />
                  </div>
                  <div className="flex-1">
                    <p className="text-xs text-slate-500 font-medium">Customer ID</p>
                    <p className="text-xs font-mono text-slate-900 break-all">{selectedCustomer.id}</p>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-2 mt-6 pt-6 border-t border-slate-200">
                <Button
                  onClick={() => {
                    window.location.href = `mailto:${selectedCustomer.email}`;
                  }}
                  className="flex-1 bg-gradient-to-r from-[#335765] to-[#74A8A4] hover:from-[#2a4752] hover:to-[#5d8f8b] text-white shadow-md hover:shadow-lg transition-all cursor-pointer"
                >
                  <Mail className="w-4 h-4 mr-2" />
                  Email
                </Button>
                {selectedCustomer.phone && (
                  <Button
                    onClick={() => {
                      window.location.href = `tel:${selectedCustomer.phone}`;
                    }}
                    className="flex-1 bg-gradient-to-r from-[#74A8A4] to-[#B6D9E0] hover:from-[#5d8f8b] hover:to-[#a3c4d4] text-white shadow-md hover:shadow-lg transition-all cursor-pointer"
                  >
                    <Phone className="w-4 h-4 mr-2" />
                    Call
                  </Button>
                )}
              </div>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
