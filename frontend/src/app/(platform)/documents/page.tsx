"use client";

import { motion } from "framer-motion";
import {
  Upload,
  FileText,
  FileSpreadsheet,
  Image as ImageIcon,
  File,
  Search,
  Filter,
  Grid3X3,
  List,
  Trash2,
  Eye,
  Tag,
  Clock,
  CheckCircle2,
  Loader2,
  AlertCircle,
  X,
} from "lucide-react";
import { useState, useCallback } from "react";
import { formatFileSize, formatRelativeTime, getStatusColor } from "@/lib/utils";

/* ═══════════════════════════════════════════════════════════
   Demo Data
   ═══════════════════════════════════════════════════════════ */

const DEMO_DOCS = [
  { id: "1", title: "Centrifugal Pump P-101 Maintenance Manual", filename: "P-101_Manual.pdf", type: "pdf", size: 4523000, category: "manual", tags: ["pump", "P-101", "maintenance"], status: "ready", progress: 100, chunks: 47, uploaded: "2025-06-15T09:30:00Z" },
  { id: "2", title: "Safety SOP — Hot Work Permit Procedure", filename: "SOP_Hot_Work.pdf", type: "pdf", size: 1892000, category: "sop", tags: ["safety", "hot-work"], status: "ready", progress: 100, chunks: 23, uploaded: "2025-06-14T14:20:00Z" },
  { id: "3", title: "Annual Boiler Inspection Report 2025", filename: "Boiler_Inspection.pdf", type: "pdf", size: 8734000, category: "inspection", tags: ["boiler", "inspection"], status: "ready", progress: 100, chunks: 62, uploaded: "2025-06-10T11:00:00Z" },
  { id: "4", title: "OSHA Process Safety Management Guidelines", filename: "OSHA_PSM.pdf", type: "pdf", size: 12456000, category: "regulation", tags: ["osha", "psm", "compliance"], status: "ready", progress: 100, chunks: 89, uploaded: "2025-06-08T08:45:00Z" },
  { id: "5", title: "Vibration Analysis Report — Compressor C-201", filename: "Vibration_C201.xlsx", type: "xlsx", size: 2134000, category: "report", tags: ["vibration", "C-201"], status: "ready", progress: 100, chunks: 18, uploaded: "2025-06-12T16:30:00Z" },
  { id: "6", title: "Heat Exchanger E-301 Failure Investigation", filename: "HX_E301_Report.pdf", type: "pdf", size: 5678000, category: "report", tags: ["heat-exchanger", "failure"], status: "ready", progress: 100, chunks: 34, uploaded: "2025-06-11T10:15:00Z" },
  { id: "7", title: "ISO 45001 OHS Management System Manual", filename: "ISO_45001_Manual.pdf", type: "pdf", size: 6789000, category: "regulation", tags: ["iso", "ohs", "safety"], status: "processing", progress: 65, chunks: 0, uploaded: "2025-06-15T11:00:00Z" },
  { id: "8", title: "Quarterly Maintenance Log — Q2 2025", filename: "Maintenance_Q2_2025.xlsx", type: "xlsx", size: 3456000, category: "maintenance", tags: ["maintenance", "quarterly"], status: "ready", progress: 100, chunks: 28, uploaded: "2025-06-13T08:00:00Z" },
];

const CATEGORIES = ["all", "manual", "sop", "inspection", "regulation", "report", "maintenance", "audit"];

function getFileIcon(type: string) {
  switch (type) {
    case "pdf": return <FileText className="w-5 h-5 text-red-400" />;
    case "xlsx": case "csv": return <FileSpreadsheet className="w-5 h-5 text-emerald-400" />;
    case "image": return <ImageIcon className="w-5 h-5 text-blue-400" />;
    default: return <File className="w-5 h-5 text-[var(--muted-foreground)]" />;
  }
}

function getStatusIcon(status: string) {
  switch (status) {
    case "ready": return <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />;
    case "processing": return <Loader2 className="w-3.5 h-3.5 text-blue-400 animate-spin" />;
    case "failed": return <AlertCircle className="w-3.5 h-3.5 text-red-400" />;
    default: return <Clock className="w-3.5 h-3.5 text-[var(--muted-foreground)]" />;
  }
}

/* ═══════════════════════════════════════════════════════════
   Documents Page
   ═══════════════════════════════════════════════════════════ */

export default function DocumentsPage() {
  const [docs] = useState(DEMO_DOCS);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("all");
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");
  const [isDragging, setIsDragging] = useState(false);

  const filteredDocs = docs.filter((doc) => {
    const matchesSearch = doc.title.toLowerCase().includes(search.toLowerCase()) || doc.tags.some(t => t.includes(search.toLowerCase()));
    const matchesCategory = category === "all" || doc.category === category;
    return matchesSearch && matchesCategory;
  });

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback(() => {
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    // In production: handle file upload
  }, []);

  return (
    <div className="space-y-6 max-w-[1600px] mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Documents</h1>
          <p className="text-[var(--muted-foreground)] text-sm mt-1">
            Upload and manage your industrial documents
          </p>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm text-[var(--muted-foreground)]">{filteredDocs.length} documents</span>
        </div>
      </div>

      {/* ─── Upload Zone ──────────────────────────────── */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`
          relative border-2 border-dashed rounded-xl p-8 text-center transition-all cursor-pointer
          ${isDragging
            ? "border-indigo-500 bg-indigo-500/[0.06]"
            : "border-[var(--border)] hover:border-indigo-500/30 hover:bg-[var(--card)]"
          }
        `}
      >
        <Upload className={`w-10 h-10 mx-auto mb-3 ${isDragging ? "text-indigo-400" : "text-[var(--muted-foreground)]"}`} />
        <p className="text-sm font-medium mb-1">
          {isDragging ? "Drop files here" : "Drag & drop files or click to upload"}
        </p>
        <p className="text-xs text-[var(--muted-foreground)]">
          Supports PDF, DOCX, XLSX, CSV, TXT, and Images — Max 50 MB per file
        </p>
        <input type="file" className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" multiple accept=".pdf,.docx,.xlsx,.csv,.txt,.png,.jpg,.jpeg" />
      </motion.div>

      {/* ─── Filters Bar ──────────────────────────────── */}
      <div className="flex items-center gap-4 flex-wrap">
        <div className="relative flex-1 min-w-[240px]">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--muted-foreground)]" />
          <input
            type="text"
            placeholder="Search documents..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 rounded-lg bg-[var(--muted)] border border-[var(--border)] text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500/50 transition-all"
          />
        </div>
        <div className="flex items-center gap-2 overflow-x-auto">
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => setCategory(cat)}
              className={`px-3.5 py-1.5 rounded-full text-xs font-medium capitalize whitespace-nowrap transition-all ${
                category === cat
                  ? "bg-indigo-500/15 text-indigo-400 border border-indigo-500/25"
                  : "bg-[var(--muted)] text-[var(--muted-foreground)] border border-transparent hover:border-[var(--border)]"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-1 bg-[var(--muted)] rounded-lg p-1">
          <button onClick={() => setViewMode("grid")} className={`p-1.5 rounded-md ${viewMode === "grid" ? "bg-[var(--card)] shadow-sm" : ""}`}>
            <Grid3X3 className="w-4 h-4" />
          </button>
          <button onClick={() => setViewMode("list")} className={`p-1.5 rounded-md ${viewMode === "list" ? "bg-[var(--card)] shadow-sm" : ""}`}>
            <List className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* ─── Document Grid ────────────────────────────── */}
      <div className={viewMode === "grid" ? "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4" : "space-y-3"}>
        {filteredDocs.map((doc, i) => (
          <motion.div
            key={doc.id}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.04, duration: 0.3 }}
            className={`glass-card group cursor-pointer ${viewMode === "list" ? "flex items-center gap-4 p-4" : "p-5"}`}
          >
            {viewMode === "grid" ? (
              <>
                <div className="flex items-start justify-between mb-4">
                  <div className="w-11 h-11 rounded-xl bg-[var(--muted)] flex items-center justify-center">
                    {getFileIcon(doc.type)}
                  </div>
                  <div className="flex items-center gap-1.5">
                    {getStatusIcon(doc.status)}
                    <span className={`text-xs capitalize ${doc.status === "ready" ? "text-emerald-400" : doc.status === "processing" ? "text-blue-400" : "text-red-400"}`}>
                      {doc.status}
                    </span>
                  </div>
                </div>
                <h3 className="text-sm font-semibold mb-1.5 line-clamp-2 group-hover:text-indigo-300 transition-colors leading-snug">
                  {doc.title}
                </h3>
                <p className="text-xs text-[var(--muted-foreground)] mb-3">{doc.filename}</p>
                <div className="flex flex-wrap gap-1.5 mb-4">
                  {doc.tags.slice(0, 3).map((tag, j) => (
                    <span key={j} className="px-2 py-0.5 rounded-full bg-[var(--muted)] text-[10px] text-[var(--muted-foreground)]">
                      {tag}
                    </span>
                  ))}
                </div>
                {doc.status === "processing" && (
                  <div className="mb-3">
                    <div className="w-full h-1.5 rounded-full bg-[var(--muted)] overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${doc.progress}%` }}
                        className="h-full bg-gradient-to-r from-indigo-500 to-violet-500 rounded-full"
                      />
                    </div>
                    <p className="text-[10px] text-[var(--muted-foreground)] mt-1">{doc.progress}% processed</p>
                  </div>
                )}
                <div className="flex items-center justify-between text-xs text-[var(--muted-foreground)]">
                  <span>{formatFileSize(doc.size)}</span>
                  <span>{doc.chunks > 0 ? `${doc.chunks} chunks` : ""}</span>
                </div>
                <div className="flex items-center gap-1 mt-2 text-[10px] text-[var(--muted-foreground)]">
                  <Clock className="w-3 h-3" />
                  {formatRelativeTime(doc.uploaded)}
                </div>
              </>
            ) : (
              <>
                <div className="w-10 h-10 rounded-lg bg-[var(--muted)] flex items-center justify-center shrink-0">
                  {getFileIcon(doc.type)}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-sm font-medium truncate group-hover:text-indigo-300 transition-colors">{doc.title}</h3>
                  <div className="flex items-center gap-3 text-xs text-[var(--muted-foreground)] mt-0.5">
                    <span className="capitalize">{doc.category}</span>
                    <span>{formatFileSize(doc.size)}</span>
                    <span>{doc.chunks} chunks</span>
                  </div>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  {doc.tags.slice(0, 2).map((tag, j) => (
                    <span key={j} className="px-2 py-0.5 rounded-full bg-[var(--muted)] text-[10px] text-[var(--muted-foreground)]">{tag}</span>
                  ))}
                </div>
                <div className="flex items-center gap-1.5 shrink-0">
                  {getStatusIcon(doc.status)}
                  <span className="text-xs text-[var(--muted-foreground)]">{formatRelativeTime(doc.uploaded)}</span>
                </div>
                <div className="flex items-center gap-1 shrink-0 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button className="p-1.5 rounded-md hover:bg-[var(--muted)] text-[var(--muted-foreground)]"><Eye className="w-4 h-4" /></button>
                  <button className="p-1.5 rounded-md hover:bg-red-500/10 text-[var(--muted-foreground)] hover:text-red-400"><Trash2 className="w-4 h-4" /></button>
                </div>
              </>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  );
}
