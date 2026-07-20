"use client";

import { motion } from "framer-motion";
import { Settings, User, Bell, Shield, Database, Key, Palette, Globe } from "lucide-react";

const settingSections = [
  {
    title: "Profile",
    icon: User,
    description: "Manage your account details and preferences",
    settings: [
      { label: "Full Name", value: "Demo User", type: "text" },
      { label: "Email", value: "demo@indusmind.ai", type: "text" },
      { label: "Department", value: "Engineering", type: "text" },
      { label: "Role", value: "Admin", type: "badge" },
    ],
  },
  {
    title: "Notifications",
    icon: Bell,
    description: "Configure alert and notification preferences",
    settings: [
      { label: "Maintenance Alerts", value: true, type: "toggle" },
      { label: "Compliance Violations", value: true, type: "toggle" },
      { label: "Document Processing", value: false, type: "toggle" },
      { label: "AI Insights", value: true, type: "toggle" },
    ],
  },
  {
    title: "AI Configuration",
    icon: Key,
    description: "Configure AI model and API settings",
    settings: [
      { label: "LLM Model", value: "GPT-4o", type: "text" },
      { label: "Embedding Model", value: "all-MiniLM-L6-v2", type: "text" },
      { label: "Top-K Results", value: "10", type: "text" },
      { label: "Demo Mode", value: true, type: "toggle" },
    ],
  },
  {
    title: "Data & Storage",
    icon: Database,
    description: "Manage database connections and storage",
    settings: [
      { label: "PostgreSQL", value: "Connected", type: "status" },
      { label: "ChromaDB", value: "Connected", type: "status" },
      { label: "Neo4j", value: "Demo Mode", type: "status" },
      { label: "Redis", value: "Connected", type: "status" },
    ],
  },
];

export default function SettingsPage() {
  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold">Settings</h1>
        <p className="text-[var(--muted-foreground)] text-sm mt-1">Platform configuration and preferences</p>
      </div>

      {settingSections.map((section, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.05 }}
          className="glass-card p-6"
        >
          <div className="flex items-center gap-3 mb-1">
            <section.icon className="w-5 h-5 text-indigo-400" />
            <h3 className="text-base font-semibold">{section.title}</h3>
          </div>
          <p className="text-xs text-[var(--muted-foreground)] mb-5 ml-8">{section.description}</p>

          <div className="space-y-4 ml-8">
            {section.settings.map((setting, j) => (
              <div key={j} className="flex items-center justify-between py-2 border-b border-[var(--border)] last:border-0">
                <span className="text-sm text-[var(--muted-foreground)]">{setting.label}</span>
                {setting.type === "text" && (
                  <span className="text-sm font-medium">{String(setting.value)}</span>
                )}
                {setting.type === "badge" && (
                  <span className="badge badge-primary">{String(setting.value)}</span>
                )}
                {setting.type === "toggle" && (
                  <button className={`w-10 h-5.5 rounded-full transition-colors relative ${setting.value ? "bg-indigo-600" : "bg-[var(--muted)]"}`}>
                    <span className={`absolute top-0.5 w-4.5 h-4.5 rounded-full bg-white transition-transform ${setting.value ? "left-5" : "left-0.5"}`} />
                  </button>
                )}
                {setting.type === "status" && (
                  <span className={`badge ${String(setting.value).includes("Connected") ? "badge-success" : "badge-warning"}`}>
                    {String(setting.value)}
                  </span>
                )}
              </div>
            ))}
          </div>
        </motion.div>
      ))}
    </div>
  );
}
