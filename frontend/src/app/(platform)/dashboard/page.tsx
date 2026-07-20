"use client";

import { motion } from "framer-motion";
import {
  FileText,
  Cpu,
  AlertTriangle,
  Shield,
  Wrench,
  Users,
  Brain,
  MessageSquare,
  TrendingUp,
  TrendingDown,
  ArrowUpRight,
  Clock,
} from "lucide-react";
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { formatFileSize, formatRelativeTime } from "@/lib/utils";

/* ═══════════════════════════════════════════════════════════
   Dashboard Data
   ═══════════════════════════════════════════════════════════ */

const summaryCards = [
  { label: "Total Documents", value: "1,247", change: "+23", trend: "up", icon: FileText, color: "from-indigo-500 to-violet-500" },
  { label: "Equipment", value: "342", change: "+5", trend: "up", icon: Cpu, color: "from-cyan-500 to-blue-500" },
  { label: "Incidents", value: "89", change: "-12", trend: "down", icon: AlertTriangle, color: "from-amber-500 to-orange-500" },
  { label: "Compliance Score", value: "81.6%", change: "+2.1%", trend: "up", icon: Shield, color: "from-emerald-500 to-teal-500" },
  { label: "Maintenance Due", value: "12", change: "+3", trend: "up", icon: Wrench, color: "from-rose-500 to-pink-500" },
  { label: "AI Queries Today", value: "156", change: "+34", trend: "up", icon: MessageSquare, color: "from-violet-500 to-purple-500" },
];

const incidentData = [
  { month: "Jan", critical: 1, major: 3, minor: 8 },
  { month: "Feb", critical: 0, major: 2, minor: 6 },
  { month: "Mar", critical: 1, major: 4, minor: 9 },
  { month: "Apr", critical: 0, major: 1, minor: 5 },
  { month: "May", critical: 2, major: 3, minor: 7 },
  { month: "Jun", critical: 0, major: 2, minor: 4 },
];

const equipmentHealthData = [
  { name: "P-101", health: 78.5 },
  { name: "B-401", health: 65.0 },
  { name: "C-201", health: 71.2 },
  { name: "E-301", health: 82.0 },
  { name: "T-801", health: 88.5 },
  { name: "V-501", health: 92.0 },
  { name: "M-601", health: 95.0 },
  { name: "TV-701", health: 85.0 },
];

const complianceTrendData = [
  { month: "Jan", score: 76 },
  { month: "Feb", score: 78.5 },
  { month: "Mar", score: 80 },
  { month: "Apr", score: 79 },
  { month: "May", score: 82 },
  { month: "Jun", score: 81.6 },
];

const documentCategoryData = [
  { name: "Manuals", value: 312, color: "#6366f1" },
  { name: "SOPs", value: 245, color: "#8b5cf6" },
  { name: "Inspections", value: 198, color: "#a78bfa" },
  { name: "Maintenance", value: 178, color: "#06b6d4" },
  { name: "Regulations", value: 142, color: "#818cf8" },
  { name: "Audits", value: 98, color: "#7c3aed" },
];

const recentUploads = [
  { title: "P-101 Maintenance Manual", type: "pdf", size: 4523000, time: "2025-06-15T09:30:00Z", category: "Manual" },
  { title: "Hot Work Permit SOP", type: "pdf", size: 1892000, time: "2025-06-14T14:20:00Z", category: "SOP" },
  { title: "Boiler Inspection Report 2025", type: "pdf", size: 8734000, time: "2025-06-10T11:00:00Z", category: "Inspection" },
  { title: "OSHA PSM Guidelines", type: "pdf", size: 12456000, time: "2025-06-08T08:45:00Z", category: "Regulation" },
  { title: "Vibration Analysis C-201", type: "xlsx", size: 2134000, time: "2025-06-12T16:30:00Z", category: "Report" },
];

/* ═══════════════════════════════════════════════════════════
   Custom Tooltip
   ═══════════════════════════════════════════════════════════ */

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload) return null;
  return (
    <div className="glass-card px-4 py-3 !bg-[var(--card)] border border-[var(--border)]">
      <p className="text-xs text-[var(--muted-foreground)] mb-1.5">{label}</p>
      {payload.map((entry: any, i: number) => (
        <p key={i} className="text-sm font-medium" style={{ color: entry.color }}>
          {entry.name}: {typeof entry.value === 'number' && entry.value % 1 !== 0 ? entry.value.toFixed(1) : entry.value}
        </p>
      ))}
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════
   Animation Variants
   ═══════════════════════════════════════════════════════════ */

const cardVariant = {
  hidden: { opacity: 0, y: 20 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.05, duration: 0.4, ease: [0.22, 1, 0.36, 1] as const },
  }),
};

/* ═══════════════════════════════════════════════════════════
   Dashboard Page
   ═══════════════════════════════════════════════════════════ */

export default function DashboardPage() {
  return (
    <div className="space-y-6 max-w-[1600px] mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <p className="text-[var(--muted-foreground)] text-sm mt-1">
          Real-time overview of your industrial intelligence platform
        </p>
      </div>

      {/* ─── Summary Cards ────────────────────────────── */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {summaryCards.map((card, i) => (
          <motion.div
            key={i}
            custom={i}
            initial="hidden"
            animate="visible"
            variants={cardVariant}
            className="glass-card p-5 group"
          >
            <div className="flex items-center justify-between mb-3">
              <div className={`w-9 h-9 rounded-lg bg-gradient-to-br ${card.color} flex items-center justify-center shadow-lg`}>
                <card.icon className="w-4.5 h-4.5 text-white" />
              </div>
              <span className={`flex items-center gap-0.5 text-xs font-medium ${card.trend === "up" ? (card.label.includes("Incident") || card.label.includes("Maintenance") ? "text-amber-400" : "text-emerald-400") : "text-emerald-400"}`}>
                {card.trend === "up" ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                {card.change}
              </span>
            </div>
            <p className="text-2xl font-bold">{card.value}</p>
            <p className="text-xs text-[var(--muted-foreground)] mt-1">{card.label}</p>
          </motion.div>
        ))}
      </div>

      {/* ─── Charts Row 1 ─────────────────────────────── */}
      <div className="grid lg:grid-cols-2 gap-5">
        {/* Incident Trends */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="glass-card p-6"
        >
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-base font-semibold">Incident Trends</h3>
              <p className="text-xs text-[var(--muted-foreground)] mt-0.5">Monthly incident distribution by severity</p>
            </div>
            <span className="badge badge-warning">89 Total</span>
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <AreaChart data={incidentData}>
              <defs>
                <linearGradient id="criticalGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="majorGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f97316" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#f97316" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="minorGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#eab308" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#eab308" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="month" stroke="var(--muted-foreground)" fontSize={12} />
              <YAxis stroke="var(--muted-foreground)" fontSize={12} />
              <Tooltip content={<CustomTooltip />} />
              <Area type="monotone" dataKey="minor" stackId="1" stroke="#eab308" fill="url(#minorGrad)" name="Minor" />
              <Area type="monotone" dataKey="major" stackId="1" stroke="#f97316" fill="url(#majorGrad)" name="Major" />
              <Area type="monotone" dataKey="critical" stackId="1" stroke="#ef4444" fill="url(#criticalGrad)" name="Critical" />
            </AreaChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Equipment Health */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.5 }}
          className="glass-card p-6"
        >
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-base font-semibold">Equipment Health</h3>
              <p className="text-xs text-[var(--muted-foreground)] mt-0.5">Health score by equipment (0–100)</p>
            </div>
            <span className="badge badge-info">8 Assets</span>
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={equipmentHealthData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" horizontal={false} />
              <XAxis type="number" domain={[0, 100]} stroke="var(--muted-foreground)" fontSize={12} />
              <YAxis type="category" dataKey="name" stroke="var(--muted-foreground)" fontSize={11} width={55} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="health" name="Health Score" radius={[0, 6, 6, 0]}>
                {equipmentHealthData.map((entry, i) => (
                  <Cell key={i} fill={entry.health >= 85 ? "#22c55e" : entry.health >= 70 ? "#eab308" : "#ef4444"} fillOpacity={0.8} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* ─── Charts Row 2 ─────────────────────────────── */}
      <div className="grid lg:grid-cols-3 gap-5">
        {/* Compliance Trend */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.5 }}
          className="glass-card p-6"
        >
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-base font-semibold">Compliance Trend</h3>
              <p className="text-xs text-[var(--muted-foreground)] mt-0.5">Overall compliance score</p>
            </div>
            <span className="badge badge-success">81.6%</span>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={complianceTrendData}>
              <defs>
                <linearGradient id="complianceGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="month" stroke="var(--muted-foreground)" fontSize={12} />
              <YAxis domain={[60, 100]} stroke="var(--muted-foreground)" fontSize={12} />
              <Tooltip content={<CustomTooltip />} />
              <Line type="monotone" dataKey="score" stroke="#6366f1" strokeWidth={2.5} dot={{ fill: "#6366f1", strokeWidth: 0, r: 4 }} name="Score" />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Document Categories */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.5 }}
          className="glass-card p-6"
        >
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-base font-semibold">Document Categories</h3>
              <p className="text-xs text-[var(--muted-foreground)] mt-0.5">Distribution by type</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={documentCategoryData}
                cx="50%"
                cy="50%"
                innerRadius={55}
                outerRadius={85}
                paddingAngle={3}
                dataKey="value"
              >
                {documentCategoryData.map((entry, i) => (
                  <Cell key={i} fill={entry.color} stroke="transparent" />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
          <div className="flex flex-wrap gap-x-4 gap-y-1 mt-2 justify-center">
            {documentCategoryData.map((item, i) => (
              <div key={i} className="flex items-center gap-1.5 text-xs text-[var(--muted-foreground)]">
                <span className="w-2 h-2 rounded-full" style={{ background: item.color }} />
                {item.name}
              </div>
            ))}
          </div>
        </motion.div>

        {/* Recent Uploads */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7, duration: 0.5 }}
          className="glass-card p-6"
        >
          <div className="flex items-center justify-between mb-5">
            <div>
              <h3 className="text-base font-semibold">Recent Uploads</h3>
              <p className="text-xs text-[var(--muted-foreground)] mt-0.5">Latest documents added</p>
            </div>
            <a href="/documents" className="text-xs text-indigo-400 hover:text-indigo-300 flex items-center gap-1">
              View All <ArrowUpRight className="w-3 h-3" />
            </a>
          </div>
          <div className="space-y-3">
            {recentUploads.map((doc, i) => (
              <div key={i} className="flex items-center gap-3 group cursor-pointer">
                <div className="w-9 h-9 rounded-lg bg-indigo-500/10 border border-indigo-500/10 flex items-center justify-center shrink-0">
                  <FileText className="w-4 h-4 text-indigo-400" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate group-hover:text-indigo-300 transition-colors">
                    {doc.title}
                  </p>
                  <div className="flex items-center gap-2 text-xs text-[var(--muted-foreground)]">
                    <span>{doc.category}</span>
                    <span>•</span>
                    <span>{formatFileSize(doc.size)}</span>
                  </div>
                </div>
                <div className="flex items-center gap-1 text-xs text-[var(--muted-foreground)] shrink-0">
                  <Clock className="w-3 h-3" />
                  {formatRelativeTime(doc.time)}
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
