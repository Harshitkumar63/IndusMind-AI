import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "IndusMind AI — Industrial Knowledge Intelligence Platform",
  description:
    "The AI Brain for Industrial Operations. Transform thousands of technical documents into structured, actionable intelligence with AI-powered knowledge graphs, maintenance predictions, and compliance analysis.",
  keywords: [
    "Industrial AI",
    "Knowledge Graph",
    "Maintenance Intelligence",
    "Compliance",
    "Document Intelligence",
    "RAG",
    "Enterprise AI",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased dark`}
    >
      <body className="min-h-full flex flex-col bg-[var(--background)] text-[var(--foreground)]">
        <div className="mesh-gradient" />
        {children}
      </body>
    </html>
  );
}
