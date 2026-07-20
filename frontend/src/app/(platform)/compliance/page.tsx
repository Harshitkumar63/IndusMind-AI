"use client";

import { motion } from "framer-motion";
import {
  Shield,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  Clock,
  FileWarning,
  ChevronRight,
  BarChart3,
  Target,
  Sparkles,
} from "lucide-react";
import { PieChart, Pie, Cell, ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts";

/* ═══════════════════════════════════════════════════════════
   Demo Data
   ═══════════════════════════════════════════════════════════ */

const scoreData = [
  { name: "Compliant", value: 18, color: "#22c55e" },
  { name: "Partial", value: 4, color: "#eab308" },
  { name: "Non-Compliant", value: 2, color: "#ef4444" },
];

const standardScores = [
  { standard: "API 510", score: 95, status: "compliant", icon: "🏗️" },
  { standard: "ISO 45001", score: 88, status: "compliant", icon: "🛡️" },
  { standard: "OSHA PSM", score: 85, status: "compliant", icon: "⚠️" },
  { standard: "ISO 14001", score: 55, status: "non_compliant", icon: "🌿" },
];

const violations = [
  { id: "v-001", regulation: "OSHA 29 CFR 1910.119(j)", description: "Overdue inspection for high-pressure piping in Unit-1", severity: "major", daysOpen: 25, assignedTo: "Rajesh Kumar" },
  { id: "v-002", regulation: "ISO 14001:2015 Sec 8.1", description: "Missing air emission monitoring data for Q1 2025", severity: "major", daysOpen: 14, assignedTo: "Priya Sharma" },
  { id: "v-003", regulation: "ISO 14001:2015 Sec 8.1", description: "Hazardous waste storage exceeding 90-day limit", severity: "critical", daysOpen: 5, assignedTo: "Amit Patel" },
];

const complianceTrend = [
  { month: "Jan", score: 76 }, { month: "Feb", score: 78.5 }, { month: "Mar", score: 80 },
  { month: "Apr", score: 79 }, { month: "May", score: 82 }, { month: "Jun", score: 81.6 },
];

const auditSummary = {
  summary: "The plant's overall compliance posture is MODERATE (81.6%). While API and ISO 45001 standards show strong compliance, ISO 14001 environmental compliance is a critical gap requiring immediate attention.",
  critical_violations: [
    "Hazardous waste storage exceeding 90-day regulatory limit — immediate action required",
    "Missing continuous emission monitoring data — regulatory reporting at risk",
  ],
  recommendations: [
    "URGENT: Address hazardous waste storage violation within 48 hours",
    "Install continuous emission monitoring systems in Q3 2025",
    "Accelerate mechanical integrity piping inspection program",
    "Implement digital compliance tracking to replace manual spreadsheets",
  ],
};

const sevColor: Record<string, string> = { critical: "badge-danger", major: "badge-warning", minor: "badge-info" };

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload) return null;
  return (
    <div className="glass-card px-4 py-3 !bg-[var(--card)] border border-[var(--border)]">
      <p className="text-xs text-[var(--muted-foreground)] mb-1">{label}</p>
      {payload.map((e: any, i: number) => (
        <p key={i} className="text-sm font-medium" style={{ color: e.color }}>{e.name}: {e.value}</p>
      ))}
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════
   Compliance Page
   ═══════════════════════════════════════════════════════════ */

export default function CompliancePage() {
  return (
    <div className="space-y-6 max-w-[1600px] mx-auto">
      <div>
        <h1 className="text-2xl font-bold">Compliance Intelligence</h1>
        <p className="text-[var(--muted-foreground)] text-sm mt-1">AI-powered compliance scoring, gap analysis, and violation tracking</p>
      </div>

      <div className="grid lg:grid-cols-3 gap-5">
        {/* Overall Score Gauge */}
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-6 text-center">
          <h3 className="text-base font-semibold mb-4">Overall Compliance Score</h3>
          <div className="relative w-40 h-40 mx-auto mb-4">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={scoreData} cx="50%" cy="50%" innerRadius={50} outerRadius={70} paddingAngle={3} dataKey="value" startAngle={90} endAngle={-270}>
                  {scoreData.map((entry, i) => <Cell key={i} fill={entry.color} stroke="transparent" />)}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-3xl font-bold gradient-text">81.6%</span>
              <span className="text-[10px] text-[var(--muted-foreground)] uppercase tracking-wider">Score</span>
            </div>
          </div>
          <div className="flex justify-center gap-4 text-xs">
            {scoreData.map((s, i) => (
              <div key={i} className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full" style={{ background: s.color }} />
                <span className="text-[var(--muted-foreground)]">{s.name} ({s.value})</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Standards Scores */}
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="glass-card p-6">
          <h3 className="text-base font-semibold mb-4">Compliance by Standard</h3>
          <div className="space-y-4">
            {standardScores.map((s, i) => (
              <div key={i}>
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-sm font-medium">{s.icon} {s.standard}</span>
                  <span className={`text-sm font-bold ${s.score >= 80 ? "text-emerald-400" : s.score >= 60 ? "text-amber-400" : "text-red-400"}`}>{s.score}%</span>
                </div>
                <div className="w-full h-2 rounded-full bg-[var(--muted)] overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${s.score}%` }}
                    transition={{ delay: 0.3 + i * 0.1, duration: 0.8, ease: "easeOut" }}
                    className="h-full rounded-full"
                    style={{ background: s.score >= 80 ? "#22c55e" : s.score >= 60 ? "#eab308" : "#ef4444" }}
                  />
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Compliance Trend */}
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="glass-card p-6">
          <h3 className="text-base font-semibold mb-4">Score Trend</h3>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={complianceTrend}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="month" stroke="var(--muted-foreground)" fontSize={12} />
              <YAxis domain={[60, 100]} stroke="var(--muted-foreground)" fontSize={12} />
              <Tooltip content={<CustomTooltip />} />
              <Line type="monotone" dataKey="score" stroke="#6366f1" strokeWidth={2.5} dot={{ fill: "#6366f1", r: 4 }} name="Score" />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Active Violations */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="glass-card p-6">
        <div className="flex items-center gap-2 mb-5">
          <AlertTriangle className="w-5 h-5 text-red-400" />
          <h3 className="text-base font-semibold">Active Violations</h3>
          <span className="badge badge-danger ml-2">{violations.length}</span>
        </div>
        <div className="space-y-3">
          {violations.map((v, i) => (
            <div key={i} className="flex items-start gap-4 p-4 rounded-lg bg-[var(--muted)]/50 border border-[var(--border)] hover:border-red-500/20 transition-colors">
              <span className={`badge ${sevColor[v.severity]} shrink-0 capitalize`}>{v.severity}</span>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium">{v.description}</p>
                <p className="text-xs text-[var(--muted-foreground)] mt-1">{v.regulation}</p>
              </div>
              <div className="text-right shrink-0">
                <p className="text-sm font-medium text-red-400">{v.daysOpen} days</p>
                <p className="text-xs text-[var(--muted-foreground)]">{v.assignedTo}</p>
              </div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* AI Audit Summary */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="glass-card p-6">
        <div className="flex items-center gap-2 mb-5">
          <Sparkles className="w-5 h-5 text-indigo-400" />
          <h3 className="text-base font-semibold">AI Audit Summary</h3>
        </div>
        <p className="text-sm text-[var(--muted-foreground)] mb-5 leading-relaxed">{auditSummary.summary}</p>

        <div className="grid md:grid-cols-2 gap-5">
          <div>
            <h4 className="text-sm font-semibold text-red-400 mb-3 flex items-center gap-1.5">
              <XCircle className="w-4 h-4" /> Critical Violations
            </h4>
            <ul className="space-y-2">
              {auditSummary.critical_violations.map((v, i) => (
                <li key={i} className="text-sm text-[var(--muted-foreground)] pl-4 border-l-2 border-red-500/30">{v}</li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="text-sm font-semibold text-indigo-400 mb-3 flex items-center gap-1.5">
              <Target className="w-4 h-4" /> AI Recommendations
            </h4>
            <ul className="space-y-2">
              {auditSummary.recommendations.map((r, i) => (
                <li key={i} className="text-sm text-[var(--muted-foreground)] pl-4 border-l-2 border-indigo-500/30">{r}</li>
              ))}
            </ul>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
