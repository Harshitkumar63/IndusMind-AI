"use client";

import { motion } from "framer-motion";
import {
  Brain,
  FileSearch,
  Network,
  Shield,
  Wrench,
  BarChart3,
  ArrowRight,
  Sparkles,
  Zap,
  Database,
  ChevronRight,
  Bot,
  Search,
  Upload,
} from "lucide-react";
import Link from "next/link";

/* ═══════════════════════════════════════════════════════════
   Animation Variants
   ═══════════════════════════════════════════════════════════ */

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.1, duration: 0.6, ease: [0.22, 1, 0.36, 1] as const },
  }),
};

const stagger = {
  visible: { transition: { staggerChildren: 0.08 } },
};

/* ═══════════════════════════════════════════════════════════
   Feature Cards Data
   ═══════════════════════════════════════════════════════════ */

const features = [
  {
    icon: Brain,
    title: "AI-Powered RAG",
    description:
      "Ask questions in natural language. Get precise answers with source citations from your entire document corpus.",
    gradient: "from-indigo-500 to-violet-500",
  },
  {
    icon: Network,
    title: "Knowledge Graph",
    description:
      "Automatically map relationships between equipment, processes, people, and regulations into an interactive graph.",
    gradient: "from-violet-500 to-purple-500",
  },
  {
    icon: Wrench,
    title: "Maintenance Intelligence",
    description:
      "Predict equipment failures, track maintenance schedules, and generate root cause analysis from historical data.",
    gradient: "from-cyan-500 to-blue-500",
  },
  {
    icon: Shield,
    title: "Compliance Analysis",
    description:
      "Compare operations against OSHA, ISO, and API standards. Detect gaps, score compliance, and generate audit summaries.",
    gradient: "from-emerald-500 to-teal-500",
  },
  {
    icon: FileSearch,
    title: "Document Intelligence",
    description:
      "OCR, extract, chunk, and embed thousands of PDFs, manuals, SOPs, and inspection reports automatically.",
    gradient: "from-amber-500 to-orange-500",
  },
  {
    icon: BarChart3,
    title: "Analytics Dashboard",
    description:
      "Real-time insights on incident trends, equipment health, compliance scores, and maintenance forecasts.",
    gradient: "from-rose-500 to-pink-500",
  },
];

const stats = [
  { value: "1,200+", label: "Documents Processed" },
  { value: "342", label: "Equipment Tracked" },
  { value: "81.6%", label: "Compliance Score" },
  { value: "2,840", label: "Knowledge Nodes" },
];

const targetUsers = [
  "Plant Engineers",
  "Maintenance Engineers",
  "Safety Officers",
  "Quality Engineers",
  "Project Managers",
  "Factory Managers",
  "Operations Teams",
  "Auditors",
];

/* ═══════════════════════════════════════════════════════════
   Landing Page Component
   ═══════════════════════════════════════════════════════════ */

export default function LandingPage() {
  return (
    <div className="relative min-h-screen overflow-hidden">
      {/* ─── Ambient Glow Effects ───────────────────────── */}
      <div className="pointer-events-none fixed inset-0 z-0">
        <div className="absolute top-[-20%] left-[10%] w-[600px] h-[600px] rounded-full bg-indigo-600/[0.07] blur-[120px] animate-glow-pulse" />
        <div className="absolute top-[20%] right-[5%] w-[500px] h-[500px] rounded-full bg-violet-600/[0.05] blur-[100px] animate-glow-pulse" style={{ animationDelay: "1s" }} />
        <div className="absolute bottom-[-10%] left-[30%] w-[700px] h-[700px] rounded-full bg-cyan-600/[0.04] blur-[140px] animate-glow-pulse" style={{ animationDelay: "2s" }} />
      </div>

      {/* ─── Navigation ─────────────────────────────────── */}
      <motion.nav
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="relative z-20 flex items-center justify-between px-6 md:px-12 py-5 border-b border-[var(--border)]"
      >
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <Brain className="w-5 h-5 text-white" />
          </div>
          <span className="text-lg font-semibold tracking-tight">
            Indus<span className="gradient-text">Mind</span> AI
          </span>
        </div>
        <div className="hidden md:flex items-center gap-8 text-sm text-[var(--muted-foreground)]">
          <a href="#features" className="hover:text-[var(--foreground)] transition-colors">Features</a>
          <a href="#platform" className="hover:text-[var(--foreground)] transition-colors">Platform</a>
          <a href="#users" className="hover:text-[var(--foreground)] transition-colors">For Teams</a>
        </div>
        <Link
          href="/dashboard"
          className="flex items-center gap-2 px-5 py-2.5 rounded-full bg-gradient-to-r from-indigo-600 to-violet-600 text-white text-sm font-medium hover:from-indigo-500 hover:to-violet-500 transition-all shadow-lg shadow-indigo-500/20 hover:shadow-indigo-500/30"
        >
          Launch Platform
          <ArrowRight className="w-4 h-4" />
        </Link>
      </motion.nav>

      {/* ─── Hero Section ───────────────────────────────── */}
      <section className="relative z-10 flex flex-col items-center justify-center px-6 pt-20 pb-16 md:pt-32 md:pb-24 text-center max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-indigo-500/20 bg-indigo-500/[0.06] text-indigo-400 text-sm mb-8"
        >
          <Sparkles className="w-3.5 h-3.5" />
          Enterprise AI Platform for Industrial Operations
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.1 }}
          className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight leading-[1.1] max-w-4xl"
        >
          The <span className="gradient-text">AI Brain</span> for
          <br />
          Industrial Operations
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2 }}
          className="mt-6 text-lg md:text-xl text-[var(--muted-foreground)] max-w-2xl leading-relaxed"
        >
          Transform thousands of PDFs, SOPs, inspection reports, and maintenance logs
          into structured, searchable intelligence. Ask questions. Get answers with citations.
          Predict failures. Ensure compliance.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.3 }}
          className="flex flex-wrap items-center justify-center gap-4 mt-10"
        >
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 px-7 py-3.5 rounded-full bg-gradient-to-r from-indigo-600 to-violet-600 text-white font-medium text-base hover:from-indigo-500 hover:to-violet-500 transition-all shadow-xl shadow-indigo-500/25 hover:shadow-indigo-500/40 hover:scale-[1.02]"
          >
            <Zap className="w-4.5 h-4.5" />
            Get Started
          </Link>
          <Link
            href="/chat"
            className="inline-flex items-center gap-2 px-7 py-3.5 rounded-full border border-[var(--border)] bg-[var(--card)] text-[var(--foreground)] font-medium text-base hover:border-indigo-500/30 hover:bg-[var(--muted)] transition-all"
          >
            <Bot className="w-4.5 h-4.5" />
            Try AI Chat
            <ChevronRight className="w-4 h-4 text-[var(--muted-foreground)]" />
          </Link>
        </motion.div>

        {/* ─── Stats Bar ──────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.5 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-12 mt-16 md:mt-20 py-6 px-8 rounded-2xl border border-[var(--border)] bg-[var(--card)]/40 backdrop-blur-sm w-full max-w-3xl"
        >
          {stats.map((stat, i) => (
            <div key={i} className="text-center">
              <div className="text-2xl md:text-3xl font-bold gradient-text">{stat.value}</div>
              <div className="text-xs md:text-sm text-[var(--muted-foreground)] mt-1">{stat.label}</div>
            </div>
          ))}
        </motion.div>
      </section>

      {/* ─── How It Works ───────────────────────────────── */}
      <section id="platform" className="relative z-10 px-6 py-16 md:py-24 max-w-6xl mx-auto">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={stagger}
          className="text-center mb-16"
        >
          <motion.h2 variants={fadeUp} custom={0} className="text-3xl md:text-4xl font-bold">
            How <span className="gradient-text">IndusMind</span> Works
          </motion.h2>
          <motion.p variants={fadeUp} custom={1} className="mt-4 text-[var(--muted-foreground)] max-w-xl mx-auto">
            Three simple steps to unlock intelligence from your industrial documents
          </motion.p>
        </motion.div>

        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-50px" }}
          variants={stagger}
          className="grid md:grid-cols-3 gap-6"
        >
          {[
            { step: "01", icon: Upload, title: "Upload Documents", desc: "Drag & drop PDFs, manuals, SOPs, inspection reports. Our OCR and AI pipeline processes everything automatically." },
            { step: "02", icon: Database, title: "AI Understands", desc: "Text extraction, semantic chunking, embeddings, knowledge graph extraction — all happening in the background." },
            { step: "03", icon: Search, title: "Ask & Act", desc: "Query your knowledge base naturally. Get cited answers, maintenance insights, compliance scores, and action items." },
          ].map((item, i) => (
            <motion.div
              key={i}
              variants={fadeUp}
              custom={i}
              className="glass-card p-8 relative group"
            >
              <div className="absolute top-6 right-6 text-5xl font-black text-[var(--border)] group-hover:text-indigo-500/20 transition-colors">
                {item.step}
              </div>
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500/20 to-violet-500/20 flex items-center justify-center mb-5 border border-indigo-500/10">
                <item.icon className="w-6 h-6 text-indigo-400" />
              </div>
              <h3 className="text-xl font-semibold mb-3">{item.title}</h3>
              <p className="text-[var(--muted-foreground)] text-sm leading-relaxed">{item.desc}</p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* ─── Features Grid ──────────────────────────────── */}
      <section id="features" className="relative z-10 px-6 py-16 md:py-24 max-w-6xl mx-auto">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={stagger}
          className="text-center mb-16"
        >
          <motion.h2 variants={fadeUp} custom={0} className="text-3xl md:text-4xl font-bold">
            Enterprise-Grade <span className="gradient-text">AI Features</span>
          </motion.h2>
          <motion.p variants={fadeUp} custom={1} className="mt-4 text-[var(--muted-foreground)] max-w-xl mx-auto">
            Everything your industrial operations team needs in one intelligent platform
          </motion.p>
        </motion.div>

        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-50px" }}
          variants={stagger}
          className="grid md:grid-cols-2 lg:grid-cols-3 gap-5"
        >
          {features.map((feature, i) => (
            <motion.div
              key={i}
              variants={fadeUp}
              custom={i}
              className="glass-card p-7 group cursor-pointer"
            >
              <div className={`w-11 h-11 rounded-xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-5 shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                <feature.icon className="w-5.5 h-5.5 text-white" />
              </div>
              <h3 className="text-lg font-semibold mb-2 group-hover:text-indigo-300 transition-colors">
                {feature.title}
              </h3>
              <p className="text-sm text-[var(--muted-foreground)] leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* ─── Target Users ───────────────────────────────── */}
      <section id="users" className="relative z-10 px-6 py-16 md:py-24 max-w-4xl mx-auto text-center">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={stagger}
        >
          <motion.h2 variants={fadeUp} custom={0} className="text-3xl md:text-4xl font-bold">
            Built for <span className="gradient-text">Industrial Teams</span>
          </motion.h2>
          <motion.p variants={fadeUp} custom={1} className="mt-4 text-[var(--muted-foreground)] max-w-lg mx-auto mb-10">
            From plant floor to boardroom — empowering every role in industrial operations
          </motion.p>

          <motion.div variants={fadeUp} custom={2} className="flex flex-wrap items-center justify-center gap-3">
            {targetUsers.map((user, i) => (
              <span
                key={i}
                className="px-5 py-2.5 rounded-full border border-[var(--border)] bg-[var(--card)] text-sm text-[var(--muted-foreground)] hover:border-indigo-500/30 hover:text-indigo-300 transition-all cursor-default"
              >
                {user}
              </span>
            ))}
          </motion.div>
        </motion.div>
      </section>

      {/* ─── CTA Section ────────────────────────────────── */}
      <section className="relative z-10 px-6 py-16 md:py-24 max-w-4xl mx-auto text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7 }}
          className="glass-card p-10 md:p-14 relative overflow-hidden"
        >
          <div className="absolute inset-0 bg-gradient-to-br from-indigo-600/10 via-transparent to-violet-600/10" />
          <div className="relative">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Ready to Transform Your Operations?
            </h2>
            <p className="text-[var(--muted-foreground)] mb-8 max-w-lg mx-auto">
              Start extracting intelligence from your industrial documents today.
              No complex setup required.
            </p>
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-2 px-8 py-4 rounded-full bg-gradient-to-r from-indigo-600 to-violet-600 text-white font-medium text-lg hover:from-indigo-500 hover:to-violet-500 transition-all shadow-xl shadow-indigo-500/25 hover:shadow-indigo-500/40 hover:scale-[1.02]"
            >
              Launch IndusMind AI
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </motion.div>
      </section>

      {/* ─── Footer ─────────────────────────────────────── */}
      <footer className="relative z-10 border-t border-[var(--border)] px-6 py-8 text-center text-sm text-[var(--muted-foreground)]">
        <div className="flex items-center justify-center gap-2 mb-2">
          <Brain className="w-4 h-4 text-indigo-400" />
          <span className="font-medium text-[var(--foreground)]">IndusMind AI</span>
        </div>
        <p>Industrial Knowledge Intelligence Platform • Built for AI Hackathon 2025</p>
      </footer>
    </div>
  );
}
