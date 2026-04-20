import { useRef, useEffect, useState } from "react";
import { MessageSquare, Send, Bot } from "lucide-react";
import { Typography } from "../atoms/Typography";
import { ChatMessage } from "../molecules/ChatMessage";

interface Message {
  role: "user" | "assistant" | "system";
  content: string;
}

interface MissionControlProps {
  messages: Message[];
  isThinking: boolean;
  onSendMessage: (msg: string) => void;
}

export const MissionControl = ({
  messages,
  isThinking,
  onSendMessage,
}: MissionControlProps) => {
  const [input, setInput] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSubmit = () => {
    if (!input.trim()) return;
    onSendMessage(input);
    setInput("");
  };

  return (
    <div className="w-[450px] flex flex-col border-l border-white/5 bg-neutral-900/40 relative">
      <header className="p-8 border-b border-white/10 flex items-center justify-between bg-black/20 backdrop-blur-md">
        <div>
          <div className="flex items-center gap-3">
            <MessageSquare className="w-5 h-5 text-violet-400" />
            <Typography variant="h2" weight="black" className="text-white">
              Mission Control
            </Typography>
          </div>
          <Typography variant="caption" className="text-neutral-500 mt-1">
            Direct Neural Overlink
          </Typography>
        </div>
        <div className="flex gap-2 bg-black/40 p-2 rounded-full px-4 border border-white/10">
          <div className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.8)] animate-pulse"></div>
          <div className="w-2 h-2 rounded-full bg-blue-500/30"></div>
          <div className="w-2 h-2 rounded-full bg-violet-500/30"></div>
        </div>
      </header>

      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-8 flex flex-col gap-8 custom-scrollbar scroll-smooth neural-stream"
      >
        {messages.map((msg, i) => (
          <ChatMessage key={i} {...msg} />
        ))}

        {isThinking && (
          <div className="flex flex-col items-start opacity-70 animate-pulse">
            <div className="flex items-center gap-2 mb-3">
              <Bot className="w-4 h-4 text-violet-400" />
              <Typography
                variant="caption"
                className="font-semibold text-violet-400"
              >
                Core_Thought_Streaming...
              </Typography>
            </div>
            <div className="bg-white/5 border border-white/10 p-6 rounded-3xl rounded-tl-none w-48 h-16 shadow-inner" />
          </div>
        )}
      </div>

      <footer className="p-8 bg-gradient-to-t from-black/40 to-transparent">
        <div className="relative group">
          <textarea
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSubmit();
              }
            }}
            placeholder="Type a command or mission objective..."
            className="w-full bg-neutral-800/50 border-2 border-white/5 rounded-3xl px-6 py-5 text-sm outline-none focus:border-violet-500/40 focus:bg-neutral-800/80 transition-all min-h-[140px] resize-none pr-16 text-neutral-100 placeholder:text-neutral-600 font-medium shadow-2xl"
          />
          <button
            onClick={handleSubmit}
            disabled={!input.trim()}
            className="absolute bottom-5 right-5 p-3.5 bg-violet-600 text-white rounded-2xl hover:bg-violet-500 transition-all disabled:opacity-20 shadow-2xl active:scale-90"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
        <div className="mt-5 flex justify-between items-center px-2">
          <Typography
            variant="caption"
            className="text-[9px] text-neutral-600 font-black"
          >
            STRIKE_MODE: ENABLED
          </Typography>
          <Typography
            variant="code"
            className="text-[9px] text-neutral-700 font-bold"
          >
            RSA_VERIFIED // 4096_BIT
          </Typography>
        </div>
      </footer>
    </div>
  );
};
