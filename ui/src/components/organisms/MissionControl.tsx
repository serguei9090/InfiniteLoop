import { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Activity } from "lucide-react";

interface MissionControlProps {
  messages: Array<{ role: "user" | "assistant" | "system"; content: string }>;
  isThinking: boolean;
  onSendMessage: (msg: string) => void;
}

export function MissionControl({ messages, isThinking, onSendMessage }: MissionControlProps) {
  const [input, setInput] = useState("");
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isThinking]);

  const handleSend = () => {
    if (!input.trim()) return;
    onSendMessage(input);
    setInput("");
  };

  return (
    <div className="flex-1 flex flex-col glass-panel overflow-hidden border-slate-200">
      <div className="bg-slate-50 border-b border-slate-200 p-3 flex items-center justify-between z-10">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-xs font-bold text-slate-700 tracking-wider uppercase">Mission Control</span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-4 custom-scrollbar bg-white">
        {messages.map((msg, i) => (
          <div key={i} className={`flex gap-3 ${msg.role === "user" ? "flex-row-reverse" : ""}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
              msg.role === "user" ? "bg-accent text-white" : "bg-slate-100 text-slate-600 border border-slate-200"
            }`}>
              {msg.role === "user" ? <User size={14} /> : <Bot size={14} />}
            </div>
            <div className={`max-w-[85%] rounded-2xl p-3 text-sm ${
              msg.role === "user"
                ? "bg-accent text-white rounded-tr-none"
                : "bg-slate-50 text-slate-700 border border-slate-100 rounded-tl-none shadow-sm"
            }`}>
              {msg.content}
            </div>
          </div>
        ))}
        {isThinking && (
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-slate-100 border border-slate-200 text-accent flex items-center justify-center shrink-0">
              <Activity size={14} className="animate-spin" />
            </div>
            <div className="bg-slate-50 border border-slate-100 rounded-2xl rounded-tl-none p-3 text-sm text-slate-500 flex items-center gap-2">
              <span className="flex gap-1">
                <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
              </span>
            </div>
          </div>
        )}
        <div ref={endOfMessagesRef} />
      </div>

      <div className="p-3 bg-white border-t border-slate-100">
        <div className="relative flex items-center">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Enter command (e.g., RUN: test_task)"
            className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-4 pr-12 py-3 text-sm outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-all text-slate-700"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isThinking}
            className="absolute right-2 p-1.5 bg-accent hover:bg-accent-dark text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}
