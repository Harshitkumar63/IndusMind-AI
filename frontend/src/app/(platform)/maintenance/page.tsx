"use client";

import { motion } from "framer-motion";
import {
  Wrench,
  AlertTriangle,
  Timer,
  DollarSign,
  Target,
} from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

/* ═══════════════════════════════════════════════════════════
   Demo Data
   ═══════════════════════════════════════════════════════════ */

const kpiCards = [
  { label: "Total Work Orders", value: "156", change: "+12 this month", icon: Wrench, color: "from-indigo-500 to-violet-500" },
  { label: "Overdue", value: "3", change: "Urgent attention", icon: AlertTriangle, color: "from-red-500 to-rose-500" },
  { label: "Avg Downtime", value: "6.2h", change: "-1.5h vs last month", icon: Timer, color: "from-amber-500 to-orange-500" },
  { label: "Total Cost (YTD)", value: "$245K", change: "+8% vs budget", icon: DollarSign, color: "from-emerald-500 to-teal-500" },
];

const equipmentHealth = [
  { name: "P-101", health: 78.5, risk: "medium", predictions: "Seal replacement in 60-90 days", component: "Mechanical Seal" },
  { name: "B-401", health: 65.0, risk: "high", predictions: "Safety valve inspection needed", component: "Safety Valve" },
  { name: "C-201", health: 71.2, risk: "medium", predictions: "Valve plate inspection overdue", component: "Valve Plate" },
  { name: "E-301", health: 82.0, risk: "low", predictions: "Monitor pressure drop trend", component: "Tube Bundle" },
  { name: "T-801", health: 88.5, risk: "low", predictions: "On track, next service Sep 2025", component: "Bearings" },
];

const maintenanceTrendData = [
  { month: "Jan", preventive: 12, corrective: 5, predictive: 3, breakdown: 1 },
  { month: "Feb", preventive: 15, corrective: 3, predictive: 4, breakdown: 0 },
  { month: "Mar", preventive: 10, corrective: 6, predictive: 2, breakdown: 2 },
  { month: "Apr", preventive: 14, corrective: 4, predictive: 5, breakdown: 1 },
  { month: "May", preventive: 11, corrective: 7, predictive: 3, breakdown: 1 },
  { month: "Jun", preventive: 13, corrective: 4, predictive: 6, breakdown: 2 },
];

const recommendations = [
  { priority: "urgent", text: "Boiler B-401 safety valve inspection — highest failure probability (55%)", equipment: "B-401" },
  { priority: "high", text: "Schedule P-101 mechanical seal replacement during next planned shutdown", equipment: "P-101" },
  { priority: "high", text: "Compressor C-201 valve plate inspection is overdue by 5 days", equipment: "C-201" },
  { priority: "medium", text: "Review spare parts inventory for critical equipment seals and bearings", equipment: "All" },
  { priority: "low", text: "Consider upgrading to API 682 seal plan for pumps P-101 through P-104", equipment: "P-101–P-104" },
];

const riskColor: Record<string, string> = { low: "#22c55e", medium: "#eab308", high: "#ef4444" };
const priorityBadge: Record<string, string> = { urgent: "badge-danger", high: "badge-warning", medium: "badge-info", low: "badge-muted" };

interface TooltipPayloadItem {
  name: string;
  value: number | string;
  color: string;
}

interface CustomTooltipProps {
  active?: boolean;
  payload?: TooltipPayloadItem[];
  label?: string;
}

function CustomTooltip({ active, payload, label }: CustomTooltipProps) {
  if (!active || !payload) return null;
  return (
    <div className="glass-card px-4 py-3 !bg-[var(--card)] border border-[var(--border)]">
      <p className="text-xs text-[var(--muted-foreground)] mb-1">{label}</p>
      {payload.map((entry: TooltipPayloadItem, i: number) => (
        <p key={i} className="text-sm font-medium" style={{ color: entry.color }}>{entry.name}: {entry.value}</p>
      ))}
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════
   Maintenance Page
   ═══════════════════════════════════════════════════════════ */

export default function MaintenancePage() {
  return (
    <div className="space-y-6 max-w-[1600px] mx-auto">
      <div>
        <h1 className="text-2xl font-bold">Maintenance Intelligence</h1>
        <p className="text-[var(--muted-foreground)] text-sm mt-1">AI-powered maintenance insights, failure predictions, and recommendations</p>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {kpiCards.map((card, i) => (
          <motion.div key={i} initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }} className="glass-card p-5">
            <div className={`w-9 h-9 rounded-lg bg-gradient-to-br ${card.color} flex items-center justify-center mb-3`}>
              <card.icon className="w-4.5 h-4.5 text-white" />
            </div>
            <p className="text-2xl font-bold">{card.value}</p>
            <p className="text-xs text-[var(--muted-foreground)] mt-1">{card.label}</p>
            <p className="text-[10px] text-[var(--muted-foreground)] mt-0.5">{card.change}</p>
          </motion.div>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-5">
        {/* Equipment Health Table */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="glass-card p-6">
          <h3 className="text-base font-semibold mb-1">Equipment Health & Predictions</h3>
          <p className="text-xs text-[var(--muted-foreground)] mb-5">AI-generated failure risk assessment</p>
          <div className="space-y-3">
            {equipmentHealth.map((eq, i) => (
              <div key={i} className="flex items-center gap-4 p-3 rounded-lg bg-[var(--muted)]/50 hover:bg-[var(--muted)] transition-colors">
                <div className="w-12 text-center">
                  <div className="text-lg font-bold" style={{ color: riskColor[eq.risk] }}>{eq.health}%</div>
                  <div className="text-[9px] uppercase tracking-wider" style={{ color: riskColor[eq.risk] }}>{eq.risk}</div>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium">{eq.name} — <span className="text-[var(--muted-foreground)]">{eq.component}</span></p>
                  <p className="text-xs text-[var(--muted-foreground)] truncate">{eq.predictions}</p>
                </div>
                <div className="w-24 h-2 rounded-full bg-[var(--background)] overflow-hidden shrink-0">
                  <div className="h-full rounded-full" style={{ width: `${eq.health}%`, background: riskColor[eq.risk] }} />
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Maintenance Trend */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="glass-card p-6">
          <h3 className="text-base font-semibold mb-1">Maintenance Activity Trend</h3>
          <p className="text-xs text-[var(--muted-foreground)] mb-5">Work orders by maintenance type</p>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={maintenanceTrendData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="month" stroke="var(--muted-foreground)" fontSize={12} />
              <YAxis stroke="var(--muted-foreground)" fontSize={12} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="preventive" stackId="a" fill="#6366f1" name="Preventive" radius={[0, 0, 0, 0]} />
              <Bar dataKey="corrective" stackId="a" fill="#f59e0b" name="Corrective" />
              <Bar dataKey="predictive" stackId="a" fill="#06b6d4" name="Predictive" />
              <Bar dataKey="breakdown" stackId="a" fill="#ef4444" name="Breakdown" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* AI Recommendations */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="glass-card p-6">
        <div className="flex items-center gap-2 mb-5">
          <Target className="w-5 h-5 text-indigo-400" />
          <h3 className="text-base font-semibold">AI Recommendations</h3>
        </div>
        <div className="space-y-3">
          {recommendations.map((rec, i) => (
            <div key={i} className="flex items-start gap-3 p-3 rounded-lg bg-[var(--muted)]/50 hover:bg-[var(--muted)] transition-colors">
              <span className={`badge ${priorityBadge[rec.priority]} shrink-0 mt-0.5 capitalize`}>{rec.priority}</span>
              <div className="flex-1 min-w-0">
                <p className="text-sm">{rec.text}</p>
                <p className="text-xs text-[var(--muted-foreground)] mt-0.5">Equipment: {rec.equipment}</p>
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
