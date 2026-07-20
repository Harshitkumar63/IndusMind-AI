"use client";

import { motion } from "framer-motion";
import { BarChart3 } from "lucide-react";
import {
  AreaChart, Area, BarChart, Bar, LineChart, Line,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell,
} from "recharts";

const incidentData = [
  { month: "Jan", critical: 1, major: 3, minor: 8, observation: 12 },
  { month: "Feb", critical: 0, major: 2, minor: 6, observation: 15 },
  { month: "Mar", critical: 1, major: 4, minor: 9, observation: 11 },
  { month: "Apr", critical: 0, major: 1, minor: 5, observation: 14 },
  { month: "May", critical: 2, major: 3, minor: 7, observation: 10 },
  { month: "Jun", critical: 0, major: 2, minor: 4, observation: 13 },
];

const failureData = [
  { name: "Bearing Failure", count: 23 },
  { name: "Seal Leak", count: 18 },
  { name: "Vibration High", count: 15 },
  { name: "Corrosion", count: 12 },
  { name: "Valve Stuck", count: 9 },
  { name: "Electrical Fault", count: 7 },
  { name: "Overheating", count: 5 },
];

const monthlyCostData = [
  { month: "Jan", cost: 32000 }, { month: "Feb", cost: 28000 }, { month: "Mar", cost: 45000 },
  { month: "Apr", cost: 38000 }, { month: "May", cost: 52000 }, { month: "Jun", cost: 50000 },
];

const documentGrowth = [
  { month: "Jan", value: 892 }, { month: "Feb", value: 945 }, { month: "Mar", value: 1023 },
  { month: "Apr", value: 1089 }, { month: "May", value: 1178 }, { month: "Jun", value: 1247 },
];

const knowledgeCoverage = [
  { area: "Equipment", coverage: 92 }, { area: "SOPs", coverage: 85 },
  { area: "Maintenance", coverage: 78 }, { area: "Safety", coverage: 88 },
  { area: "Compliance", coverage: 72 }, { area: "Inspection", coverage: 81 },
];

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload) return null;
  return (
    <div className="glass-card px-4 py-3 !bg-[var(--card)] border border-[var(--border)]">
      <p className="text-xs text-[var(--muted-foreground)] mb-1">{label}</p>
      {payload.map((e: any, i: number) => (
        <p key={i} className="text-sm font-medium" style={{ color: e.color }}>
          {e.name}: {typeof e.value === "number" && e.value > 1000 ? `$${(e.value / 1000).toFixed(0)}K` : e.value}
        </p>
      ))}
    </div>
  );
}

export default function AnalyticsPage() {
  return (
    <div className="space-y-6 max-w-[1600px] mx-auto">
      <div>
        <h1 className="text-2xl font-bold">Analytics</h1>
        <p className="text-[var(--muted-foreground)] text-sm mt-1">Comprehensive operational analytics and trend analysis</p>
      </div>

      <div className="grid lg:grid-cols-2 gap-5">
        {/* Incident Heatmap */}
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-6">
          <h3 className="text-base font-semibold mb-1">Incident Severity Distribution</h3>
          <p className="text-xs text-[var(--muted-foreground)] mb-5">Monthly breakdown by severity level</p>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={incidentData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="month" stroke="var(--muted-foreground)" fontSize={12} />
              <YAxis stroke="var(--muted-foreground)" fontSize={12} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="observation" stackId="a" fill="#6366f1" name="Observation" />
              <Bar dataKey="minor" stackId="a" fill="#eab308" name="Minor" />
              <Bar dataKey="major" stackId="a" fill="#f97316" name="Major" />
              <Bar dataKey="critical" stackId="a" fill="#ef4444" name="Critical" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Common Failures */}
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="glass-card p-6">
          <h3 className="text-base font-semibold mb-1">Most Common Failures</h3>
          <p className="text-xs text-[var(--muted-foreground)] mb-5">Top failure modes across all equipment</p>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={failureData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" horizontal={false} />
              <XAxis type="number" stroke="var(--muted-foreground)" fontSize={12} />
              <YAxis type="category" dataKey="name" stroke="var(--muted-foreground)" fontSize={11} width={100} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="count" name="Occurrences" radius={[0, 6, 6, 0]}>
                {failureData.map((_, i) => (
                  <Cell key={i} fill={`hsl(${240 + i * 15}, 70%, ${55 + i * 3}%)`} fillOpacity={0.8} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Monthly Maintenance Cost */}
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="glass-card p-6">
          <h3 className="text-base font-semibold mb-1">Monthly Maintenance Cost</h3>
          <p className="text-xs text-[var(--muted-foreground)] mb-5">Total maintenance expenditure trend</p>
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={monthlyCostData}>
              <defs>
                <linearGradient id="costGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="month" stroke="var(--muted-foreground)" fontSize={12} />
              <YAxis stroke="var(--muted-foreground)" fontSize={12} tickFormatter={(v) => `$${v / 1000}K`} />
              <Tooltip content={<CustomTooltip />} />
              <Area type="monotone" dataKey="cost" stroke="#6366f1" fill="url(#costGrad)" strokeWidth={2.5} name="Cost" />
            </AreaChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Document Growth */}
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="glass-card p-6">
          <h3 className="text-base font-semibold mb-1">Document Growth</h3>
          <p className="text-xs text-[var(--muted-foreground)] mb-5">Cumulative document count over time</p>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={documentGrowth}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="month" stroke="var(--muted-foreground)" fontSize={12} />
              <YAxis stroke="var(--muted-foreground)" fontSize={12} />
              <Tooltip content={<CustomTooltip />} />
              <Line type="monotone" dataKey="value" stroke="#22c55e" strokeWidth={2.5} dot={{ fill: "#22c55e", r: 4 }} name="Documents" />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Knowledge Coverage */}
      <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="glass-card p-6">
        <h3 className="text-base font-semibold mb-1">Knowledge Coverage</h3>
        <p className="text-xs text-[var(--muted-foreground)] mb-5">How well your document corpus covers each operational area</p>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {knowledgeCoverage.map((area, i) => (
            <div key={i} className="text-center p-4 rounded-xl bg-[var(--muted)]/50">
              <div className="relative w-16 h-16 mx-auto mb-3">
                <svg className="w-16 h-16 -rotate-90" viewBox="0 0 36 36">
                  <path d="M18 2.0845a15.9155 15.9155 0 1 1 0 31.831 15.9155 15.9155 0 0 1 0-31.831" fill="none" stroke="var(--border)" strokeWidth="3" />
                  <motion.path
                    d="M18 2.0845a15.9155 15.9155 0 1 1 0 31.831 15.9155 15.9155 0 0 1 0-31.831"
                    fill="none"
                    stroke={area.coverage >= 85 ? "#22c55e" : area.coverage >= 70 ? "#eab308" : "#ef4444"}
                    strokeWidth="3"
                    strokeLinecap="round"
                    initial={{ strokeDasharray: "0 100" }}
                    animate={{ strokeDasharray: `${area.coverage} ${100 - area.coverage}` }}
                    transition={{ delay: 0.5 + i * 0.1, duration: 1, ease: "easeOut" }}
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-sm font-bold">{area.coverage}%</span>
                </div>
              </div>
              <p className="text-xs font-medium">{area.area}</p>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
