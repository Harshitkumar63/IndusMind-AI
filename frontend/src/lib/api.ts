import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor for auth
api.interceptors.request.use((config) => {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      if (typeof window !== "undefined") {
        localStorage.removeItem("token");
      }
    }
    return Promise.reject(error);
  }
);

// ─── API Functions ────────────────────────────────────────

export const analyticsApi = {
  getDashboard: () => api.get("/analytics/dashboard"),
  getIncidentTrends: () => api.get("/analytics/incidents"),
  getEquipmentHealth: () => api.get("/analytics/equipment-health"),
  getComplianceTrend: () => api.get("/analytics/compliance-trend"),
  getMaintenanceTrend: () => api.get("/analytics/maintenance-trend"),
  getDocumentGrowth: () => api.get("/analytics/document-growth"),
  getDocumentCategories: () => api.get("/analytics/document-categories"),
};

export const documentsApi = {
  list: (params?: Record<string, string>) => api.get("/documents", { params }),
  get: (id: string) => api.get(`/documents/${id}`),
  upload: (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return api.post("/documents/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  delete: (id: string) => api.delete(`/documents/${id}`),
  getChunks: (id: string) => api.get(`/documents/${id}/chunks`),
  getStatus: (id: string) => api.get(`/documents/${id}/status`),
};

export const chatApi = {
  listConversations: () => api.get("/chat/conversations"),
  createConversation: (data: { title?: string }) => api.post("/chat/conversations", data),
  getConversation: (id: string) => api.get(`/chat/conversations/${id}`),
  sendMessage: (conversationId: string, content: string) =>
    api.post(`/chat/conversations/${conversationId}/messages`, { content }),
  deleteConversation: (id: string) => api.delete(`/chat/conversations/${id}`),
};

export const knowledgeGraphApi = {
  getGraph: () => api.get("/knowledge-graph"),
  getNodes: (type?: string) => api.get("/knowledge-graph/nodes", { params: { node_type: type } }),
  getNode: (id: string) => api.get(`/knowledge-graph/nodes/${id}`),
  search: (q: string) => api.get("/knowledge-graph/search", { params: { q } }),
  getStats: () => api.get("/knowledge-graph/stats"),
};

export const equipmentApi = {
  list: (params?: Record<string, string>) => api.get("/equipment", { params }),
  get: (id: string) => api.get(`/equipment/${id}`),
  getHealth: (id: string) => api.get(`/equipment/${id}/health`),
};

export const maintenanceApi = {
  list: (params?: Record<string, string>) => api.get("/maintenance", { params }),
  getIntelligence: () => api.get("/maintenance/intelligence"),
  getPredictions: () => api.get("/maintenance/predictions"),
  getOverdue: () => api.get("/maintenance/overdue"),
};

export const complianceApi = {
  list: (params?: Record<string, string>) => api.get("/compliance", { params }),
  getScore: () => api.get("/compliance/score"),
  getViolations: () => api.get("/compliance/violations"),
  getAuditSummary: () => api.get("/compliance/audit-summary"),
};

export const searchApi = {
  search: (q: string, type?: string) => api.get("/search", { params: { q, type } }),
  semantic: (q: string, topK?: number) => api.get("/search/semantic", { params: { q, top_k: topK } }),
  getFilters: () => api.get("/search/filters"),
};
