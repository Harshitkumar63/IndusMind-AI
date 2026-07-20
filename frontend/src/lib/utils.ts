import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatFileSize(bytes: number): string {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + " " + sizes[i];
}

export function formatDate(date: string | Date): string {
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(new Date(date));
}

export function formatRelativeTime(date: string | Date): string {
  const now = new Date();
  const past = new Date(date);
  const diffMs = now.getTime() - past.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffMins < 1) return "just now";
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return formatDate(date);
}

export function truncate(str: string, length: number): string {
  if (str.length <= length) return str;
  return str.slice(0, length) + "…";
}

export function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    running: "badge-success",
    ready: "badge-success",
    completed: "badge-success",
    compliant: "badge-success",
    processing: "badge-info",
    in_progress: "badge-info",
    investigating: "badge-info",
    scheduled: "badge-info",
    pending: "badge-warning",
    maintenance: "badge-warning",
    partially: "badge-warning",
    overdue: "badge-danger",
    failed: "badge-danger",
    non_compliant: "badge-danger",
    critical: "badge-danger",
    stopped: "badge-muted",
    open: "badge-primary",
  };
  return colors[status] || "badge-muted";
}

export function getSeverityColor(severity: string): string {
  const colors: Record<string, string> = {
    critical: "text-[var(--critical)]",
    major: "text-[var(--major)]",
    minor: "text-[var(--minor)]",
    observation: "text-[var(--observation)]",
    urgent: "text-[var(--critical)]",
    high: "text-[var(--major)]",
    medium: "text-[var(--minor)]",
    low: "text-[var(--muted-foreground)]",
  };
  return colors[severity] || "text-[var(--muted-foreground)]";
}
