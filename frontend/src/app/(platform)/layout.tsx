"use client";

import { motion, AnimatePresence } from "framer-motion";
import {
  Brain,
  LayoutDashboard,
  FileText,
  Bot,
  Network,
  Wrench,
  Shield,
  BarChart3,
  Settings,
  Search,
  ChevronLeft,
  ChevronRight,
  Bell,
  LogOut,
  User,
  Menu,
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

/* ═══════════════════════════════════════════════════════════
   Navigation Items
   ═══════════════════════════════════════════════════════════ */

const navItems = [
  { href: "/dashboard", icon: LayoutDashboard, label: "Dashboard", badge: null },
  { href: "/documents", icon: FileText, label: "Documents", badge: "1.2K" },
  { href: "/chat", icon: Bot, label: "AI Chat", badge: null },
  { href: "/knowledge-graph", icon: Network, label: "Knowledge Graph", badge: null },
  { href: "/maintenance", icon: Wrench, label: "Maintenance", badge: "3" },
  { href: "/compliance", icon: Shield, label: "Compliance", badge: null },
  { href: "/analytics", icon: BarChart3, label: "Analytics", badge: null },
];

const bottomNavItems = [
  { href: "/settings", icon: Settings, label: "Settings" },
];

/* ═══════════════════════════════════════════════════════════
   Platform Layout
   ═══════════════════════════════════════════════════════════ */

export default function PlatformLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  const sidebarWidth = collapsed ? 72 : 280;

  return (
    <div className="flex h-screen overflow-hidden bg-[var(--background)]">
      {/* ─── Mesh Gradient ─────────────────────────────── */}
      <div className="mesh-gradient" />

      {/* ─── Mobile Overlay ────────────────────────────── */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/60 z-40 md:hidden"
            onClick={() => setMobileOpen(false)}
          />
        )}
      </AnimatePresence>

      {/* ─── Sidebar ───────────────────────────────────── */}
      <motion.aside
        animate={{ width: sidebarWidth }}
        transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] as const }}
        className={`
          fixed md:relative z-50 h-full flex flex-col
          border-r border-[var(--border)] bg-[var(--card)]/80 backdrop-blur-xl
          ${mobileOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"}
          transition-transform md:transition-none
        `}
        style={{ width: sidebarWidth }}
      >
        {/* Logo */}
        <div className="flex items-center gap-3 px-5 py-5 border-b border-[var(--border)]">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center shadow-lg shadow-indigo-500/20 shrink-0">
            <Brain className="w-5 h-5 text-white" />
          </div>
          {!collapsed && (
            <motion.span
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-lg font-semibold tracking-tight whitespace-nowrap"
            >
              Indus<span className="gradient-text">Mind</span>
            </motion.span>
          )}
        </div>

        {/* Nav Items */}
        <nav className="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setMobileOpen(false)}
                className={`
                  group flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200
                  ${isActive
                    ? "bg-indigo-500/10 text-indigo-400 border border-indigo-500/20"
                    : "text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:bg-[var(--muted)]"
                  }
                `}
              >
                <item.icon className={`w-5 h-5 shrink-0 ${isActive ? "text-indigo-400" : "text-[var(--muted-foreground)] group-hover:text-[var(--foreground)]"}`} />
                {!collapsed && (
                  <>
                    <span className="flex-1 whitespace-nowrap">{item.label}</span>
                    {item.badge && (
                      <span className={`text-xs px-2 py-0.5 rounded-full ${isActive ? "bg-indigo-500/20 text-indigo-300" : "bg-[var(--muted)] text-[var(--muted-foreground)]"}`}>
                        {item.badge}
                      </span>
                    )}
                  </>
                )}
              </Link>
            );
          })}
        </nav>

        {/* Bottom */}
        <div className="border-t border-[var(--border)] py-3 px-3 space-y-1">
          {bottomNavItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`
                  flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all
                  ${isActive
                    ? "bg-indigo-500/10 text-indigo-400"
                    : "text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:bg-[var(--muted)]"
                  }
                `}
              >
                <item.icon className="w-5 h-5 shrink-0" />
                {!collapsed && <span>{item.label}</span>}
              </Link>
            );
          })}

          {/* User */}
          <div className="flex items-center gap-3 px-3 py-2.5 rounded-lg">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center text-white text-xs font-bold shrink-0">
              DU
            </div>
            {!collapsed && (
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">Demo User</p>
                <p className="text-xs text-[var(--muted-foreground)] truncate">admin</p>
              </div>
            )}
          </div>
        </div>

        {/* Collapse Toggle */}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="absolute -right-3 top-20 w-6 h-6 rounded-full bg-[var(--card)] border border-[var(--border)] flex items-center justify-center text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors hidden md:flex z-10"
        >
          {collapsed ? <ChevronRight className="w-3.5 h-3.5" /> : <ChevronLeft className="w-3.5 h-3.5" />}
        </button>
      </motion.aside>

      {/* ─── Main Content ──────────────────────────────── */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="flex items-center justify-between px-6 py-3.5 border-b border-[var(--border)] bg-[var(--card)]/40 backdrop-blur-md shrink-0">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setMobileOpen(true)}
              className="md:hidden p-2 rounded-lg hover:bg-[var(--muted)] text-[var(--muted-foreground)]"
            >
              <Menu className="w-5 h-5" />
            </button>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--muted-foreground)]" />
              <input
                type="text"
                placeholder="Search documents, equipment, knowledge..."
                className="w-64 md:w-96 pl-10 pr-4 py-2 rounded-lg bg-[var(--muted)] border border-[var(--border)] text-sm text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-1 focus:ring-indigo-500/50 focus:border-indigo-500/30 transition-all"
              />
              <kbd className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-[var(--muted-foreground)] bg-[var(--background)] px-1.5 py-0.5 rounded border border-[var(--border)] hidden md:inline">
                ⌘K
              </kbd>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="hidden md:inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-medium border border-emerald-500/20">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              Demo Mode
            </span>
            <button className="relative p-2 rounded-lg hover:bg-[var(--muted)] text-[var(--muted-foreground)] transition-colors">
              <Bell className="w-5 h-5" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-indigo-500" />
            </button>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto">
          <motion.div
            key={pathname}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, ease: "easeOut" }}
            className="p-6"
          >
            {children}
          </motion.div>
        </main>
      </div>
    </div>
  );
}
