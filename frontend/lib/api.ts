/**
 * API services for data fetching.
 */
import api from './api-client';

export interface Ticket {
  id: string;
  customer_id: string;
  conversation_id: string | null;
  status: string;
  priority: string;
  category: string | null;
  subject: string | null;  // Keep for backward compatibility but will be null
  sentiment_score: number | null;
  confidence_score: number | null;
  assigned_to: string | null;
  created_at: string;
  resolved_at: string | null;
  customer?: {
    name: string;
    email: string;
  };
  // New field for message preview
  latest_message?: string;
}

export interface CreateTicketData {
  customer_name: string;
  customer_email: string;
  customer_phone?: string;
  subject: string;
  message?: string;
  channel?: string;
  priority?: string;
}

export interface Customer {
  id: string;
  email: string;
  phone: string | null;
  name: string;
  custom_metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface KnowledgeBaseArticle {
  id: string;
  title: string;
  content: string;
  source: string;
  url: string | null;
  category: string | null;
  tags: string[];
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface HealthStatus {
  status: string;
  timestamp: string;
  version: string;
  environment: string;
  database?: string;
  database_latency_ms?: number;
}

// Tickets API
export const ticketsApi = {
  getAll: async (): Promise<Ticket[]> => {
    const response = await api.get<Ticket[]>('/tickets');
    return response.data;
  },

  getById: async (id: string): Promise<Ticket> => {
    const response = await api.get<Ticket>(`/tickets/${id}`);
    return response.data;
  },

  create: async (data: CreateTicketData): Promise<Ticket> => {
    const response = await api.post<Ticket>('/tickets', data);
    return response.data;
  },

  update: async (id: string, data: Partial<Ticket>): Promise<Ticket> => {
    const response = await api.put<Ticket>(`/tickets/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/tickets/${id}`);
  },
};

// Customers API
export const customersApi = {
  getAll: async (): Promise<Customer[]> => {
    const response = await api.get<Customer[]>('/customers');
    return response.data;
  },
  
  getById: async (id: string): Promise<Customer> => {
    const response = await api.get<Customer>(`/customers/${id}`);
    return response.data;
  },
};

// Knowledge Base API
export const knowledgeBaseApi = {
  getAll: async (): Promise<KnowledgeBaseArticle[]> => {
    const response = await api.get<KnowledgeBaseArticle[]>('/knowledge-base');
    return response.data;
  },
};

// Health API
export const healthApi = {
  check: async (): Promise<HealthStatus> => {
    const response = await api.get<HealthStatus>('/health');
    return response.data;
  },
};
