import { Bot, User } from "lucide-react";
import { IconWrapper } from "../atoms/IconWrapper";
import { Typography } from "../atoms/Typography";

interface ChatMessageProps {
  role: "user" | "assistant" | "system";
  content: string;
}

export const ChatMessage = ({ role, content }: ChatMessageProps) => {
  const isAssistant = role === "assistant";

  return (
    <div
      className={`flex flex-col ${!isAssistant ? "items-end" : "items-start"} animate-in fade-in slide-in-from-bottom-2 duration-500`}
    >
      <div className="flex items-center gap-2 mb-2">
        {isAssistant ? (
          <>
            <IconWrapper icon={Bot} size="xs" color="text-violet-400" />
            <Typography variant="caption" className="text-neutral-400">
              Immutable_Assistant
            </Typography>
          </>
        ) : (
          <>
            <Typography variant="caption" className="text-neutral-400">
              Operator_Prime
            </Typography>
            <IconWrapper icon={User} size="xs" color="text-emerald-400" />
          </>
        )}
      </div>
      <div
        className={`max-w-[90%] p-4 rounded-2xl text-[11px] leading-relaxed shadow-lg border ${
          !isAssistant
            ? "bg-violet-600 text-white font-medium rounded-tr-none border-violet-500/50"
            : "bg-white/5 border-white/10 text-neutral-300 rounded-tl-none backdrop-blur-sm"
        }`}
      >
        {content}
      </div>
    </div>
  );
};
