"use client";

import { motion, AnimatePresence } from "framer-motion";
import {
  Send,
  Bot,
  User,
  FileText,
  Copy,
  Download,
  ThumbsUp,
  ThumbsDown,
  Plus,
  MessageSquare,
  Trash2,
  Sparkles,
  ChevronRight,
  ExternalLink,
  RotateCcw,
} from "lucide-react";
import { useState, useRef, useEffect } from "react";

/* ═══════════════════════════════════════════════════════════
   Types
   ═══════════════════════════════════════════════════════════ */

interface Citation {
  document_title: string;
  chunk_content: string;
  relevance_score: number;
}

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  citations?: Citation[];
  confidence_score?: number;
  suggested_questions?: string[];
  created_at: string;
}

interface Conversation {
  id: string;
  title: string;
  message_count: number;
  last_message_at: string;
}

/* ═══════════════════════════════════════════════════════════
   Demo Data
   ═══════════════════════════════════════════════════════════ */

const DEMO_CONVERSATIONS: Conversation[] = [
  { id: "1", title: "Pump P-101 Maintenance Query", message_count: 4, last_message_at: "2025-06-15T10:30:00Z" },
  { id: "2", title: "OSHA Compliance Check", message_count: 6, last_message_at: "2025-06-14T15:45:00Z" },
  { id: "3", title: "Boiler Inspection Findings", message_count: 3, last_message_at: "2025-06-13T09:20:00Z" },
];

const AI_RESPONSE = `Based on the analysis of your uploaded documents, here is what I found:

## Key Findings

1. **Pump P-101** has a documented maintenance schedule requiring quarterly vibration analysis and annual overhaul per the manufacturer's manual (Section 4.2).

2. The last recorded maintenance was performed on **March 15, 2025**, which means the next quarterly check is due by **June 15, 2025**.

3. According to the vibration analysis report from April 2025, bearing vibration levels were at **4.2 mm/s RMS**, which is within the acceptable range (< 7.1 mm/s) per ISO 10816-3.

## Recommendations

- Schedule the quarterly vibration check before the deadline
- Monitor bearing temperature trends — a 3°C increase was noted in the last reading
- Review the seal flush system as mentioned in Maintenance Advisory MA-2025-012`;

const AI_CITATIONS: Citation[] = [
  { document_title: "Centrifugal Pump P-101 Maintenance Manual", chunk_content: "Section 4.2: Quarterly maintenance shall include vibration analysis, bearing temperature measurement, and seal inspection...", relevance_score: 0.95 },
  { document_title: "Vibration Analysis Report — April 2025", chunk_content: "Bearing vibration measured at 4.2 mm/s RMS on the drive-end bearing. Value is within ISO 10816-3 Zone B limits...", relevance_score: 0.88 },
  { document_title: "Maintenance Advisory MA-2025-012", chunk_content: "Recommend review of seal flush system Plan 11 configuration for pumps P-101 through P-104...", relevance_score: 0.82 },
];

const SUGGESTED_QUESTIONS = [
  "What is the recommended bearing replacement interval for P-101?",
  "Show me all maintenance records for P-101 in the last 12 months",
  "What are the ISO 10816-3 vibration severity limits?",
  "Are there any pending work orders for pump P-101?",
];

/* ═══════════════════════════════════════════════════════════
   Chat Page
   ═══════════════════════════════════════════════════════════ */

export default function ChatPage() {
  const [conversations] = useState<Conversation[]>(DEMO_CONVERSATIONS);
  const [activeConversation, setActiveConversation] = useState<string>("1");
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [showCitations, setShowCitations] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isTyping) return;
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input.trim(),
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsTyping(true);

    // Simulate AI typing delay
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: AI_RESPONSE,
        citations: AI_CITATIONS,
        confidence_score: 0.92,
        suggested_questions: SUGGESTED_QUESTIONS,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, aiMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex h-[calc(100vh-120px)] gap-0 -m-6">
      {/* ─── Conversation Sidebar ─────────────────────── */}
      <div className="w-72 border-r border-[var(--border)] bg-[var(--card)]/40 flex flex-col shrink-0 hidden lg:flex">
        <div className="p-4 border-b border-[var(--border)]">
          <button className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg bg-gradient-to-r from-indigo-600 to-violet-600 text-white text-sm font-medium hover:from-indigo-500 hover:to-violet-500 transition-all">
            <Plus className="w-4 h-4" />
            New Conversation
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-3 space-y-1">
          {conversations.map((conv) => (
            <button
              key={conv.id}
              onClick={() => setActiveConversation(conv.id)}
              className={`w-full text-left px-3 py-3 rounded-lg transition-all group ${
                activeConversation === conv.id
                  ? "bg-indigo-500/10 border border-indigo-500/20"
                  : "hover:bg-[var(--muted)]"
              }`}
            >
              <div className="flex items-center gap-2 mb-1">
                <MessageSquare className={`w-3.5 h-3.5 shrink-0 ${activeConversation === conv.id ? "text-indigo-400" : "text-[var(--muted-foreground)]"}`} />
                <span className="text-sm font-medium truncate">{conv.title}</span>
              </div>
              <p className="text-xs text-[var(--muted-foreground)] pl-5.5">
                {conv.message_count} messages
              </p>
            </button>
          ))}
        </div>
      </div>

      {/* ─── Chat Area ────────────────────────────────── */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-4 md:px-8 py-6 space-y-6">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500/20 to-violet-500/20 flex items-center justify-center mb-6 border border-indigo-500/10">
                <Sparkles className="w-8 h-8 text-indigo-400" />
              </div>
              <h2 className="text-xl font-semibold mb-2">Ask IndusMind AI</h2>
              <p className="text-sm text-[var(--muted-foreground)] max-w-md mb-8">
                I can answer questions about your industrial documents, equipment, maintenance schedules, and compliance requirements.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-lg w-full">
                {SUGGESTED_QUESTIONS.map((q, i) => (
                  <button
                    key={i}
                    onClick={() => { setInput(q); inputRef.current?.focus(); }}
                    className="text-left px-4 py-3 rounded-xl border border-[var(--border)] bg-[var(--card)] text-sm text-[var(--muted-foreground)] hover:border-indigo-500/30 hover:text-[var(--foreground)] transition-all group"
                  >
                    <ChevronRight className="w-3.5 h-3.5 inline mr-2 text-indigo-500/50 group-hover:text-indigo-400" />
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          <AnimatePresence initial={false}>
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className={`flex gap-4 ${msg.role === "user" ? "justify-end" : ""}`}
              >
                {msg.role === "assistant" && (
                  <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center shrink-0 shadow-lg shadow-indigo-500/20 mt-1">
                    <Bot className="w-4.5 h-4.5 text-white" />
                  </div>
                )}
                <div className={`max-w-2xl ${msg.role === "user" ? "order-first" : ""}`}>
                  <div className={`rounded-2xl px-5 py-4 ${
                    msg.role === "user"
                      ? "bg-indigo-600 text-white rounded-br-md"
                      : "bg-[var(--card)] border border-[var(--border)] rounded-bl-md"
                  }`}>
                    <div className="text-sm leading-relaxed whitespace-pre-wrap prose prose-invert prose-sm max-w-none">
                      {msg.content.split('\n').map((line, i) => {
                        if (line.startsWith('## ')) return <h3 key={i} className="text-base font-semibold mt-4 mb-2 text-indigo-300">{line.slice(3)}</h3>;
                        if (line.startsWith('- ')) return <li key={i} className="ml-4 mb-1">{line.slice(2)}</li>;
                        if (line.match(/^\d+\.\s\*\*/)) {
                          const parts = line.match(/^(\d+\.)\s\*\*(.+?)\*\*(.*)$/);
                          if (parts) return <p key={i} className="mb-2"><span className="text-[var(--muted-foreground)]">{parts[1]}</span> <strong className="text-indigo-300">{parts[2]}</strong>{parts[3]}</p>;
                        }
                        if (line.startsWith('*Confidence')) return <p key={i} className="mt-3 text-xs text-[var(--muted-foreground)] italic">{line.replace(/\*/g, '')}</p>;
                        if (line.trim() === '') return <br key={i} />;
                        return <p key={i} className="mb-1">{line}</p>;
                      })}
                    </div>
                  </div>

                  {/* Assistant Actions */}
                  {msg.role === "assistant" && (
                    <div className="mt-3 space-y-3">
                      {/* Confidence + Actions */}
                      <div className="flex items-center gap-3 text-xs text-[var(--muted-foreground)]">
                        {msg.confidence_score && (
                          <span className="badge badge-success">
                            {Math.round(msg.confidence_score * 100)}% Confident
                          </span>
                        )}
                        <button className="flex items-center gap-1 hover:text-[var(--foreground)] transition-colors"><Copy className="w-3 h-3" /> Copy</button>
                        <button className="flex items-center gap-1 hover:text-[var(--foreground)] transition-colors"><Download className="w-3 h-3" /> Export</button>
                        <button className="flex items-center gap-1 hover:text-emerald-400 transition-colors"><ThumbsUp className="w-3 h-3" /></button>
                        <button className="flex items-center gap-1 hover:text-red-400 transition-colors"><ThumbsDown className="w-3 h-3" /></button>
                      </div>

                      {/* Citations */}
                      {msg.citations && msg.citations.length > 0 && (
                        <div>
                          <button
                            onClick={() => setShowCitations(!showCitations)}
                            className="flex items-center gap-2 text-xs text-indigo-400 hover:text-indigo-300 font-medium transition-colors"
                          >
                            <FileText className="w-3.5 h-3.5" />
                            {msg.citations.length} Sources
                            <ChevronRight className={`w-3 h-3 transition-transform ${showCitations ? "rotate-90" : ""}`} />
                          </button>
                          <AnimatePresence>
                            {showCitations && (
                              <motion.div
                                initial={{ height: 0, opacity: 0 }}
                                animate={{ height: "auto", opacity: 1 }}
                                exit={{ height: 0, opacity: 0 }}
                                className="overflow-hidden mt-2 space-y-2"
                              >
                                {msg.citations.map((citation, i) => (
                                  <div key={i} className="p-3 rounded-lg bg-[var(--muted)] border border-[var(--border)] text-xs">
                                    <div className="flex items-center justify-between mb-1.5">
                                      <span className="font-medium text-indigo-300 flex items-center gap-1.5">
                                        <FileText className="w-3 h-3" />
                                        {citation.document_title}
                                      </span>
                                      <span className="badge badge-primary text-[10px]">
                                        {Math.round(citation.relevance_score * 100)}% Match
                                      </span>
                                    </div>
                                    <p className="text-[var(--muted-foreground)] leading-relaxed">{citation.chunk_content}</p>
                                  </div>
                                ))}
                              </motion.div>
                            )}
                          </AnimatePresence>
                        </div>
                      )}

                      {/* Suggested Questions */}
                      {msg.suggested_questions && (
                        <div className="flex flex-wrap gap-2">
                          {msg.suggested_questions.map((q, i) => (
                            <button
                              key={i}
                              onClick={() => { setInput(q); inputRef.current?.focus(); }}
                              className="text-xs px-3 py-1.5 rounded-full border border-[var(--border)] bg-[var(--card)] text-[var(--muted-foreground)] hover:border-indigo-500/30 hover:text-indigo-300 transition-all"
                            >
                              {q}
                            </button>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
                {msg.role === "user" && (
                  <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center shrink-0 mt-1">
                    <User className="w-4.5 h-4.5 text-white" />
                  </div>
                )}
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Typing Indicator */}
          {isTyping && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex items-center gap-4"
            >
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center shrink-0 shadow-lg shadow-indigo-500/20">
                <Bot className="w-4.5 h-4.5 text-white" />
              </div>
              <div className="flex items-center gap-1.5 px-4 py-3 rounded-2xl bg-[var(--card)] border border-[var(--border)] rounded-bl-md">
                <span className="w-2 h-2 rounded-full bg-indigo-400 animate-bounce" style={{ animationDelay: "0ms" }} />
                <span className="w-2 h-2 rounded-full bg-indigo-400 animate-bounce" style={{ animationDelay: "150ms" }} />
                <span className="w-2 h-2 rounded-full bg-indigo-400 animate-bounce" style={{ animationDelay: "300ms" }} />
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t border-[var(--border)] p-4 bg-[var(--card)]/40 backdrop-blur-md">
          <div className="max-w-3xl mx-auto relative">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about your documents, equipment, maintenance, compliance..."
              rows={1}
              className="w-full resize-none px-5 py-3.5 pr-14 rounded-xl bg-[var(--muted)] border border-[var(--border)] text-sm text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500/30 transition-all"
              style={{ minHeight: 48, maxHeight: 160 }}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || isTyping}
              className="absolute right-3 top-1/2 -translate-y-1/2 w-9 h-9 rounded-lg bg-gradient-to-r from-indigo-600 to-violet-600 flex items-center justify-center text-white disabled:opacity-40 hover:from-indigo-500 hover:to-violet-500 transition-all"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
          <p className="text-center text-[10px] text-[var(--muted-foreground)] mt-2">
            IndusMind AI can make mistakes. Verify important information from source documents.
          </p>
        </div>
      </div>
    </div>
  );
}
